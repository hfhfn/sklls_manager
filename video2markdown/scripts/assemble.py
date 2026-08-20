#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""assemble：把 transcript + ocr + describe + frames 按时间线交错，输出 Markdown。

三种深度：
  light     — 逐字稿 + 画面注释（OCR+VLM），轻量
  standard  — 默认：元信息 + 时间轴/画面注释 + 逐字稿 + 幻灯片/代码快照
  deep      — standard + 自动摘要 + 关键要点(按场景) + 完整素材附录

原则：脚本只忠实呈现已提取内容 + 极轻的自动摘要；不做编造，
精炼/润色留给后续整理者（可用 Claude 据本稿再优化）。
"""
import argparse
import json
from pathlib import Path

from common import ProgressLog, read_jsonl, fmt_ts, load_config


def load_all(inter):
    return {
        "meta": json.loads((Path(inter) / "meta.json").read_text(encoding="utf-8"))
        if (Path(inter) / "meta.json").exists() else {},
        "transcript": read_jsonl(Path(inter) / "transcript.jsonl"),
        "frames": read_jsonl(Path(inter) / "frames.jsonl"),
        "ocr": read_jsonl(Path(inter) / "ocr.jsonl"),
        "describe": read_jsonl(Path(inter) / "describe.jsonl"),
    }


def _merged_events(data):
    """把 语音段 / 关键帧(OCR+VLM) 揉成一条带时间的事件序列。"""
    ev = []
    for r in data["transcript"]:
        ev.append({"t": r["t0"], "kind": "speech", "text": r["text"], "end": r["t1"]})
    ocr_by_t = {r["t"]: r["ocr_text"] for r in data["ocr"]}
    cap_by_t = {r["t"]: r["caption"] for r in data["describe"]}
    prov_by_t = {r["t"]: r.get("provider", "") for r in data["describe"]}
    for f in data["frames"]:
        t = f["t"]
        ev.append({"t": t, "kind": "frame", "text": None,
                   "ocr": ocr_by_t.get(t, ""), "cap": cap_by_t.get(t, ""),
                   "prov": prov_by_t.get(t, ""), "path": f["path"]})
    ev.sort(key=lambda x: (x["t"], 0 if x["kind"] == "frame" else 1))
    return ev


def _abstract(data, bucket_s=60):
    """极轻自动摘要：每 ~60s 取首个语音段首句。供整理者精炼。"""
    seen = set()
    lines = []
    for r in data["transcript"]:
        b = int(r["t0"] // bucket_s)
        if b in seen:
            continue
        seen.add(b)
        s = r["text"].strip("。 ")
        if s:
            lines.append(f"{fmt_ts(r['t0'])} " + (s if len(s) <= 80 else s[:79] + "…"))
    return lines


def _slides_snapshot(data, big_thresh=80):
    """OCR 文本较长的帧 → 幻灯片/代码快照。"""
    ocr_by_t = {r["t"]: r["ocr_text"] for r in data["ocr"]}
    snaps = [(t, txt) for t, txt in sorted(ocr_by_t.items()) if len(txt) >= big_thresh]
    return snaps


def _key_points(data):
    """deep 用：每场景的 VLM 描述浓缩为要点(非编造，来自画面理解)。"""
    return [r["caption"] for r in data["describe"] if r.get("caption")]


def render(data, depth, engine, extra_meta):
    L = []
    A = L.append
    m = data["meta"]
    dur = m.get("duration")
    A("---")
    A(f"title: \"{m.get('title', '')}\"")
    A(f"source: \"{m.get('source', '')}\"")
    if dur:
        A(f"duration_sec: {int(dur)}")
    A(f"engine: {engine}")
    A("generated_by: video2markdown")
    A("---")
    A("")
    A(f"# {m.get('title', '未命名视频')}")
    A("")

    if depth in ("standard", "deep"):
        A("## 摘要")
        if depth == "deep":
            for line in _abstract(data):
                A(f"- {line}")
        else:
            A("> （轻量摘要：由完整逐字稿提炼，见下文。可再精炼。）")
        A("")

    A("## 时间轴 · 画面与讲解")
    A("")
    events = _merged_events(data)
    ocr_by_t = {r["t"]: r["ocr_text"] for r in data["ocr"]}
    cap_by_t = {r["t"]: r["caption"] for r in data["describe"]}
    prov_by_t = {r["t"]: r.get("provider", "") for r in data["describe"]}
    speech_buf = []   # 待收拢的语音段文本
    speech_t0 = None

    def flush_speech(until_t):
        nonlocal speech_buf, speech_t0
        if not speech_buf:
            return
        ts = f"**{fmt_ts(speech_t0)}–{fmt_ts(until_t)}**" if until_t >= speech_t0 \
            else f"**{fmt_ts(speech_t0)}**"
        A(f"- {ts} 讲解：{' '.join(speech_buf)}")
        speech_buf, speech_t0 = [], None

    for ev in events:
        if ev["kind"] == "speech":
            if speech_t0 is None:
                speech_t0 = ev["t"]
            speech_buf.append(ev["text"])
        else:  # frame
            flush_speech(ev["t"])
            ocp = ocr_by_t.get(ev["t"], "")
            cp = cap_by_t.get(ev["t"], "")
            prov = prov_by_t.get(ev["t"], "")
            line = f"- 🖼 **{fmt_ts(ev['t'])}**"
            detail = []
            if cp and "无额外视觉信息" not in cp:
                detail.append(f"*描述*：{cp}" + (f" _(via {prov})_" if prov else ""))
            if ocp:
                ocp_flat = ocp.strip().replace("\n", " ／ ")
                detail.append(f"*屏内文字*：{ocp_flat}")
            A(line + ("：" if detail else ""))
            for d in detail:
                A(f"  - {d}")
    flush_speech(events[-1]["t"] if events else 0.0)
    A("")
    A("## 逐字稿（完整，带时间戳）")
    A("")
    for r in data["transcript"]:
        A(f"- **{fmt_ts(r['t0'])}–{fmt_ts(r['t1'])}** {r['text']}")
    A("")

    if depth in ("standard", "deep"):
        snaps = _slides_snapshot(data)
        A("## 幻灯片 / 代码快照（OCR 抓取的整页文字）")
        A("")
        if snaps:
            for t, txt in snaps:
                A(f"### {fmt_ts(t)}")
                A("")
                A(f"```text")
                A(txt)
                A("```")
                A("")
        else:
            A("_（无长文本帧）_")
        A("")

    if depth == "deep":
        kp = _key_points(data)
        A("## 关键要点（按场景，来自画面理解）")
        A("")
        if kp:
            for c in kp:
                A(f"- {c}")
        else:
            A("_（无）_")
        A("")
        A("## 附录：采样关键帧清单")
        A("")
        for f in sorted(data["frames"], key=lambda x: x["t"]):
            A(f"- {fmt_ts(f['t'])}：`{f['path']}`")

    return "\n".join(L)


def assemble(inter_dir, cfg, progress, out_md=None, extra_meta=None):
    inter = Path(inter_dir)
    data = load_all(inter)
    depth = cfg.get("depth", "standard")
    engine = cfg.get("engine", "sensevoice")
    md = render(data, depth, engine, extra_meta or {})
    out = out_md or (inter.parent / f"{data['meta'].get('title') or 'video'}.md")
    out = Path(out)
    out.write_text(md, encoding="utf-8")
    progress.log(f"[asr→md] 写出 {out}（depth={depth}）")
    return str(Path(out).resolve())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--inter", required=True)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    cfg = load_config()
    plog = ProgressLog(a.inter)
    print(assemble(a.inter, cfg, plog, a.out))