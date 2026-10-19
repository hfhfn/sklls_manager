#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""note：把「时间轴转录稿」重组成「主题式知识笔记」。

video2md 每次产出两份：
  <标题>_原文.md   refine 精修后的**时间轴**转录稿（按时间顺序，忠实还原视频）
  <标题>.md        本脚本产出的**主题式笔记**（按概念重组，脱离视频可直读）

为什么需要两份：时间轴稿适合回溯"视频第几分钟讲了什么"，但概念被打散在多个时间点、
同一知识点会重复出现，不适合当笔记读。主题式笔记打散时间轴、按概念重排、合并重复。

长稿走 map-reduce：先分块抽取「知识要点」（只列概念/定义/数字/表格，不写散文），
再把各块要点合成一份主题笔记 —— 比逐块直出更能保持全局的主题组织。
"""
import re

import llm

SYS = ("你是资深的技术知识编辑，擅长把口语化的视频转录稿重组成结构化的知识笔记。"
       "你的铁律：只重组与合并，绝不编造转录稿里没有的内容。")

NOTE_TMPL = """以下是一份视频的【时间轴转录稿】。请把它重组为一份【主题式知识笔记】。

【转录稿】
{raw}

【重组要求】
1. **打散时间轴**：不要按 mm:ss 顺序罗列，按概念/主题重新组织章节。读者不看视频也能读懂。
2. **合并重复**：同一个知识点在转录稿里跨时间点重复出现的（例如"API 调优"在 12:50 和 13:40 各讲一次），
   合并到同一节，只保留最完整的表述，不要两处都写。
3. **保留全部硬信息**：数字、价格、延迟、阈值、代码、JSON、表格、专有名词一律保留，不得省略或概括掉。
4. **去掉转录痕迹**：删除时间戳、"讲解/画面/本页带走"等字样，以及"整理完毕""后续分块请继续提供"这类过场语。
5. **不编造**：转录稿没有的内容不要补。拿不准的术语保留原文写法。
6. **结构**：开头一句话定位（这讲的是什么、核心结论）→ 分主题章节（`##` 标题 + 必要的对比表/代码块）
   → 速查表（术语表 / 场景对照表，若材料里有）→ 核心金句。章节多少由内容决定，不硬凑、不写空话。
7. 只输出 Markdown 正文：不要用 ``` 包住整篇，不要写"以下是整理后的笔记"这类开场白。"""

MAP_TMPL = """这是同一份视频转录稿的第 {i}/{n} 块。请只做**信息抽取**，不要写散文。

【第 {i} 块】
{raw}

【要求】
- 逐条列出本块涉及的**知识点**：概念/定义、数字/参数/阈值、代码/JSON、表格、结论、案例。
- 每条尽量带足上下文，独立可读（后续的合并步骤看不到原文）。
- 不要写过渡句、不要评论、不要写"本块讲述了"。
- 用 Markdown 列表输出。"""

REDUCE_TMPL = """以下是同一份视频转录稿各分块抽取出的【知识要点】。请把它们合成一份【主题式知识笔记】。

【知识要点】
{digests}

【要求】
1. 按概念/主题组织章节，不要按抽取顺序罗列。
2. 跨块重复的知识点合并到一处，只保留最完整的表述。
3. 保留全部数字、代码、JSON、表格、专有名词，不得省略。
4. 不编造；拿不准的术语保留原文写法。
5. 结构：开头一句话定位 → 分主题章节（`##` 标题）→ 速查表（若材料里有）→ 核心金句。
6. 只输出 Markdown 正文，不要开场白。"""


def _chunk(md_text, max_chars):
    """按 `##`/`###` 标题边界切块，尽量不切碎小节。"""
    if len(md_text) <= max_chars:
        return [md_text]
    blocks, cur, cur_len = [], [], 0
    for ln in md_text.splitlines():
        is_head = re.match(r"^#{2,3}\s", ln) is not None
        if cur_len + len(ln) + 1 > max_chars and cur and is_head:
            blocks.append("\n".join(cur))
            cur, cur_len = [], 0
        cur.append(ln)
        cur_len += len(ln) + 1
    if cur:
        blocks.append("\n".join(cur))
    return blocks


def build_note(md_text, cfg, progress):
    """时间轴转录稿 → 主题式笔记。返回 Markdown 字符串；失败抛异常由上层回退。"""
    ncfg = cfg.get("note", {}) or {}
    max_chars = int(ncfg.get("max_chars", 24000))
    max_tokens = int(ncfg.get("max_tokens", 8000))

    if len(md_text) <= max_chars:
        progress.log(f"[note] 材料 {len(md_text)} 字 → 单次重组 ...")
        return llm.chat(cfg, SYS, NOTE_TMPL.format(raw=md_text),
                        progress=progress, tag="note", section="note",
                        max_tokens=max_tokens)

    blocks = _chunk(md_text, max_chars)
    progress.log(f"[note] 材料 {len(md_text)} 字 → {len(blocks)} 块，先抽取要点 ...")
    digests = []
    for i, b in enumerate(blocks, 1):
        progress.log(f"[note] 抽取 {i}/{len(blocks)} ...")
        digests.append(llm.chat(cfg, SYS,
                                MAP_TMPL.format(i=i, n=len(blocks), raw=b),
                                progress=progress, tag="note-map", section="note",
                                max_tokens=max_tokens))
    merged = "\n\n".join(digests)
    progress.log(f"[note] 要点 {len(merged)} 字 → 合成主题笔记 ...")
    return llm.chat(cfg, SYS, REDUCE_TMPL.format(digests=merged),
                    progress=progress, tag="note", section="note",
                    max_tokens=max_tokens)


if __name__ == "__main__":
    import argparse
    import tempfile
    from pathlib import Path
    from common import load_config, ProgressLog

    ap = argparse.ArgumentParser(description="时间轴转录稿 → 主题式笔记")
    ap.add_argument("--md", required=True, help="时间轴转录稿路径（如 <标题>_原文.md）")
    ap.add_argument("--out", default=None, help="输出路径（默认 <md去掉_原文>.md）")
    a = ap.parse_args()

    cfg = load_config()
    src = Path(a.md)
    out = Path(a.out) if a.out else src.with_name(
        src.stem[:-3] + ".md" if src.stem.endswith("_原文") else src.stem + "_笔记.md")
    # 日志写临时目录：不要把 .progress.log 落到用户的笔记库目录里
    plog = ProgressLog(Path(tempfile.gettempdir()) / "video2md-note", name="note")
    md = build_note(src.read_text(encoding="utf-8"), cfg, plog)
    out.write_text(md, encoding="utf-8")
    print(f"→ {out}")
