#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""refine：把"原始提取材料"（语音转写/OCR/画面描述）送 LLM（优先 agnes）整合成最终 MD。

价值：
- 两个 OCR（本地+云端）输出重复/矛盾 → 由 LLM 去重合并、选优；
- 语音转写错别字/口头禅/重复 → 由 LLM 修正润色（可配合本地+云端双 ASR 一起喂给它对比择优）；
- 幻灯片要点、代码块 → 归纳成条理结构；
- 不编造：提示词强约束。

效率：≤ max_chars 一段一次调用；超长按时段分块多次调用再拼接。全部失败回退原始组装。

输入：inter_dir 下 transcript.jsonl / ocr.jsonl / describe.jsonl / frames.jsonl / meta.json。
输出：整理后的 Markdown 字符串（video2md.py 决定写盘/回退）。
"""
import json
import time
from pathlib import Path

from common import ProgressLog, read_jsonl, fmt_ts

SYS = (
    "你是资深的视频学习笔记编辑。你的任务是把视频的原始提取材料"
    "（自动语音转写/屏幕OCR/画面理解）整理成高质量 Markdown 学习笔记。"
    "铁律：只整理、去重、修正错别字与术语，绝不编造原文没有的内容。"
)

USER_TMPL = """以下是某视频的【原始提取材料】。请整理成一份结构清晰的 Markdown 学习笔记。

【材料】
{raw}

【整理要求】
1. 标题/引言：用视频标题，写 2-3 句摘要。
2. 时间轴·画面与讲解：保留 mm:ss 时间戳，按时间组织；同一时间段内的语音+画面要点合并陈述。
3. 修正错别字与术语（结合上下文；例如 "大同学"→"大模型"、"变程工具"→"编程工具"）。
4. OCR 去重：同一页幻灯片在本地/云端 OCR 里重复或矛盾的条目，合并保留更准的；条目化为要点列表。
5. 代码/命令：用 ```text 或对应语言代码块保留。
6. 画面描述里有推理痕迹/废话的，只保留有效结论；若为"（无额外视觉信息）"则删掉该条。
7. 不编造：没有的信息不要补充；拿不准的术语保留原文。
8. 只输出 Markdown 正文，不要用 ``` 包住整篇。"""


def build_raw(inter_dir):
    """把中间产物拼成紧凑的纯文本材料。返回 str。"""
    inter = Path(inter_dir)
    meta = json.loads((inter / "meta.json").read_text(encoding="utf-8")) \
        if (inter / "meta.json").exists() else {}
    transcript = read_jsonl(inter / "transcript.jsonl")
    ocr = read_jsonl(inter / "ocr.jsonl")
    describe = read_jsonl(inter / "describe.jsonl")
    ocr_by_t = {r["t"]: r["ocr_text"] for r in ocr}
    cap_by_t = {r["t"]: r["caption"] for r in describe}
    lines = []
    lines.append(f"视频标题：{meta.get('title', '')}")
    lines.append(f"时长：{meta.get('duration', '')} 秒\n")

    # 画面按时间穿插语音（复用 assemble 的合并思路，但更紧凑）
    events = []
    for r in transcript:
        events.append((r["t0"], "speech", r["text"]))
    for t in sorted(set(list(ocr_by_t) + list(cap_by_t))):
        events.append((t, "frame", ""))
    events.sort(key=lambda x: (x[0], 0 if x[1] == "frame" else 1))

    cur = []
    for t, kind, text in events:
        if kind == "speech":
            cur.append(text)
        else:
            if cur:
                lines.append(f"[{fmt_ts(t)}] 讲解：{' '.join(cur)}")
                cur = []
            seg = [f"[{fmt_ts(t)}] 画面："]
            oc = ocr_by_t.get(t, "")
            cp = cap_by_t.get(t, "")
            if cp:
                seg.append(f"  描述：{cp}")
            if oc:
                seg.append(f"  屏内文字：{oc.replace(chr(10), ' ／ ')}")
            lines.append("\n".join(seg))
    if cur:
        lines.append(f"[末段] 讲解：{' '.join(cur)}")

    # 说明：语音全文已全部并入上方"讲解"行（帧间合并），不再重复附完整逐字稿，
    # 既省 token 又避免精修时重复生成标题/摘要。
    return "\n".join(lines)


def chunk_raw(raw, max_chars=24000):
    """把超长材料切成 ≤max_chars 的块，尽量在时间标记行([mm:ss])处切。"""
    if len(raw) <= max_chars:
        return [raw]
    blocks, cur, cur_len = [], [], 0
    for ln in raw.splitlines():
        if cur_len + len(ln) + 1 > max_chars and cur and ln.startswith("["):
            blocks.append("\n".join(cur))
            cur, cur_len = [], 0
        cur.append(ln)
        cur_len += len(ln) + 1
    if cur:
        blocks.append("\n".join(cur))
    return blocks


def call_refine(raw, cfg, progress, is_first=True):
    """送 LLM 整理。providers 按 refine.providers 顺序试，含模型内回退。返回整理后文本。"""
    from openai import OpenAI
    rcfg = cfg.get("refine", {}) or {}
    order = rcfg.get("providers", ["agnes", "zhipu"])
    providers = cfg.get("providers", {}) or {}
    if is_first:
        user = USER_TMPL.format(raw=raw)
    else:
        user = ("继续整理同一视频的后续分块。**不要重写标题/摘要/引言**，"
                "直接从你负责的时间段开始输出正文（时间轴·画面与讲解），保持 Markdown 结构。\n\n"
                "以下为本块的【原始材料】：\n" + raw + "\n\n"
                "仍遵守：修正错别字、OCR去重合并、保留 mm:ss、不编造、只输出正文。")
    last = None
    for name in order:
        p = providers.get(name) or {}
        if not p.get("enabled", True) or not p.get("api_key"):
            continue
        models = [p.get("model", "")] + [m for m in p.get("models", [])
                                         if m != p.get("model")]
        cli = OpenAI(base_url=p["base_url"], api_key=p["api_key"],
                     timeout=300, max_retries=0)
        for model in models:
            try:
                r = cli.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": SYS},
                        {"role": "user", "content": user},
                    ],
                    max_tokens=6000, temperature=0.3,
                )
                out = (r.choices[0].message.content or "").strip()
                if out:
                    progress.log(f"[refine] 完成（{name}/{model}）")
                    return out
                last = f"{name}/{model}: empty"
            except Exception as e:
                last = f"{name}/{model}: {str(e)[:90]}"
        time.sleep(1)
    raise RuntimeError(f"refine 所有 provider 失败: {last}")


def refine(inter_dir, cfg, progress):
    """返回整理后 Markdown 字符串；失败抛异常由上层回退。"""
    rcfg = cfg.get("refine", {}) or {}
    raw = build_raw(inter_dir)
    max_chars = int(rcfg.get("max_chars", 24000))
    blocks = chunk_raw(raw, max_chars)
    progress.log(f"[refine] 材料 {len(raw)} 字 → {len(blocks)} 块，送 LLM 整理 ...")
    if len(blocks) == 1:
        return call_refine(blocks[0], cfg, progress)
    parts = []
    for i, b in enumerate(blocks, 1):
        progress.log(f"[refine] 块 {i}/{len(blocks)} ...")
        parts.append(call_refine(b, cfg, progress, is_first=(i == 1)))
    return "\n\n---\n\n".join(parts)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--inter", required=True)
    a = ap.parse_args()
    from common import load_config
    cfg = load_config()
    plog = ProgressLog(a.inter)
    md = refine(a.inter, cfg, plog)
    Path(a.inter).parent.mkdir(parents=True, exist_ok=True)
    out = Path(a.inter).parent / f"{Path(a.inter).name}.refined.md"
    out.write_text(md, encoding="utf-8")
    print(f"→ {out}")
    print(md[:1200])