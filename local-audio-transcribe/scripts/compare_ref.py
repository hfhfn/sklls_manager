#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Reference-driven cross-check: compare a manual reference transcript against
the engine (reviewed) transcript and render a human-readable divergence report.

This is the backbone of the quality feedback loop: each manual reference
exposes where the final (reviewed) output diverges — missing terms, garbled
audio segments, speaker label drift — so the term dictionary / repair aliases
can be tightened and re-measured.

Renders markdown to --out-md with:
  1. run metadata (reference date|duration, keywords, char counts, similarity)
  2. term-recall table for the reference (approved dictionary terms)
  3. reference terms missing / phonetically-garbled in the hypothesis
  4. hypothesis-only dictionary terms (candidates where the engine may be more
     correct than the reference — e.g. "Milvus" vs a human-typed "Mysql")
  5. turn-level divergence: 参考段落 vs 最佳匹配引擎句, low-similarity flagged
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

from transcript_core import load_terms, normalize_text, term_matches


def strip_ws(s: str) -> str:
    return re.sub(r"\s+", "", s)


def parse_reference(path) -> dict:
    """Return metadata (date|duration, keywords) and turn list [(speaker, text)]. """
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    header = {"raw": "", "keywords": []}
    turns: list[list[str]] = []           # list of [speaker_label, timestamp, text...]
    in_body = False
    cur = None
    for ln in lines:
        t = ln.strip()
        if t.startswith("文字记录"):
            in_body = True
            continue
        if not in_body:
            if t and not t.startswith("关键词"):
                header["raw"] = t
            elif t.startswith("关键词"):
                header["keywords"] = [k.strip() for k in t[len("关键词:"):].split("、") if k.strip()]
            continue
        m = re.match(r"^说话人\s*(\d+)\s+(\d+:\d+)\s*$", ln)
        if m:
            cur = [f"说话人 {m.group(1)}", m.group(2)]
            turns.append(cur)
            continue
        if cur and t:
            cur.append(t)
    turns = [t for t in turns if len(t) >= 3]   # drop header-only turns
    return header, turns


def hyp_sentences(hyp_json: str) -> tuple[dict, list[dict]]:
    data = json.loads(Path(hyp_json).read_text(encoding="utf-8"))
    segs = data.get("sentences") or data.get("segments") or []
    out = []
    for s in segs:
        t = re.sub(r"<\|[^|]*\|>", "", str(s.get("text") or s.get("sentence") or "")).strip()
        if not t:
            continue
        ms = s.get("start_ms", s.get("start"))
        ss = (ms or 0) / 1000 if (ms or 0) > 10000 else (ms or 0)
        out.append({"speaker": s.get("spk"), "text": t,
                    "time": f"{int(ss//60):02d}:{int(ss%60):02d}"})
    return data, out


def term_table(ref_txt: str, hyp_txt: str, terms) -> list[dict]:
    ref, hyp = normalize_text(ref_txt), normalize_text(hyp_txt)
    rows = []
    for term in terms:
        canon = normalize_text(term["canonical"])
        rc, hc = ref.count(canon), hyp.count(canon)
        aliases = [normalize_text(a if isinstance(a, str) else a["text"]) for a in term.get("aliases", [])]
        alias_hits = sum(hyp.count(a) for a in aliases)
        if rc:
            rows.append({"canonical": term["canonical"], "ref": rc, "hyp": hc,
                         "alias_hits": alias_hits, "recall": min(1.0, (hc + alias_hits) / rc)})
    return rows


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ref", required=True)
    ap.add_argument("--hyp-json", required=True)
    ap.add_argument("--terms-file", default=None)
    ap.add_argument("--out-md", required=True)
    ap.add_argument("--match-threshold", type=float, default=0.35,
                    help="similarity below which a reference turn is flagged divergent")
    args = ap.parse_args()

    header, ref_turns = parse_reference(args.ref)
    _, hyp = hyp_sentences(args.hyp_json)
    ref_txt = "".join(strip_ws(turn[-1]) for turn in ref_turns)
    hyp_txt = "".join(strip_ws(s["text"]) for s in hyp)
    sm = SequenceMatcher(None, ref_txt, hyp_txt)
    ratio = sm.ratio()
    blocks = [b for b in sm.get_matching_blocks() if b.size > 0]
    ref_cov = sum(b.size for b in blocks) / max(1, len(ref_txt))
    terms, _ = load_terms(args.terms_file) if args.terms_file else ([], {})
    tref_norm = normalize_text(ref_txt)
    trows = term_table(ref_txt, hyp_txt, terms)
    missing = [r for r in trows if r["ref"] > 0 and (r["hyp"] + r["alias_hits"]) < r["ref"] and not r["recall"] >= 1.0]
    # hypothesis-only terms (dictionary canonical in hyp but not in ref)
    hyp_only = []
    for term in terms:
        canon = normalize_text(term["canonical"])
        if hyp_txt.count(canon) and not tref_norm.count(canon):
            hyp_only.append(term["canonical"])

    # turn-level divergence
    rows = []
    for speaker, tstamp, *txt in ref_turns:
        full = "".join(txt)
        full_n = normalize_text(full)
        best = max(hyp, key=lambda s: SequenceMatcher(None, full_n, normalize_text(s["text"])).ratio())
        sim = SequenceMatcher(None, full_n, normalize_text(best["text"])).ratio()
        rows.append({"speaker": speaker, "tstamp": tstamp, "ref": full,
                     "hyp_best": best["text"] if best else "", "sim": sim,
                     "flag": sim < args.match_threshold})

    Path(args.out_md).parent.mkdir(parents=True, exist_ok=True)
    out = []
    out.append("# 参考稿互证报告\n")
    out.append(f"- 参考稿元信息：`{header['raw']}`")
    out.append(f"- 关键词：{'、'.join(header['keywords']) or '—'}")
    out.append(f"- 参考稿字数：{len(ref_txt)}　|　引擎(reviewed)字数：{len(hyp_txt)}")
    out.append(f"- 整体相似度：`{ratio:.3f}`　|　参考稿字符覆盖：`{ref_cov:.3f}`")
    out.append(f"- 参考稿轮次：{len(ref_turns)}　|　引擎句数：{len(hyp)}\n")

    out.append("## 一、参考稿术语召回（按词典 approved 术语）\n")
    if trows:
        out.append("| 术语 | 参考出现 | 引擎(reviewed) | 别名命中 | 召回 |")
        out.append("|---|---|---|---|---|")
        for r in sorted(trows, key=lambda x: x["recall"]):
            out.append(f"| {r['canonical']} | {r['ref']} | {r['hyp']} | {r['alias_hits']} | {r['recall']:.2f} |")
    else:
        out.append("（无参考术语命中样本）\n")

    out.append("\n## 二、参考稿有、引擎(reviewed,含别名)遗漏或音译错的术语\n")
    out.append("\n".join(f"- **{m['canonical']}**：参考 {m['ref']} 次 / 引擎命中 {m['hyp']} + 别名 {m['alias_hits']}" for m in missing) or "- （无）\n")

    out.append("\n## 三、引擎有、参考稿无的词典术语（可能引擎更合理 → 参考稿存疑点）\n")
    out.append("\n".join(f"- {h}" for h in hyp_only) or "- （无）\n")

    out.append(f"\n## 四、轮次差异（相似度 < {args.match_threshold:.2f} 判为「大改/缺失」）\n")
    low = [r for r in rows if r["flag"]]
    out.append(f"共 {len(rows)} 段，**{len(low)} 段**相似度低于阈值。示例前 12 段：\n")
    shown = [r for r in rows if r["flag"]][:12] or rows[:12]
    for r in shown:
        tag = "⚠大改" if r["flag"] else " ✓"
        out.append(f"- [{tag}] {r['speaker']} {r['tstamp']}（sim={r['sim']:.2f}）")
        out.append(f"  - 参考：{r['ref']}")
        out.append(f"  - 引擎：{r['hyp_best']}")
        out.append("")

    Path(args.out_md).write_text("\n".join(out), encoding="utf-8")
    print(f"wrote {args.out_md} | turns={len(rows)} low={len(low)} sim={ratio:.3f} cov={ref_cov:.3f}")


if __name__ == "__main__":
    main()