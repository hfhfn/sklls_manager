#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Create time-constrained FunASR/Whisper review candidates without overwriting either transcript."""
from __future__ import annotations

import argparse
from pathlib import Path

from transcript_core import extract_segments, load_terms, read_json, term_matches, text_similarity, to_ms, write_json


def overlap(a: dict, b: dict) -> int:
    return max(0, min(a["end_ms"] or 0, b["end_ms"] or 0) - max(a["start_ms"] or 0, b["start_ms"] or 0))


def align(funasr: list[dict], whisper: list[dict], terms: list[dict], window_ms: int = 1200) -> list[dict]:
    pairs = []
    used: set[int] = set()
    for f in funasr:
        candidates = []
        for index, w in enumerate(whisper):
            if index in used:
                continue
            distance = min(abs((f["start_ms"] or 0) - (w["start_ms"] or 0)), abs((f["end_ms"] or 0) - (w["end_ms"] or 0)))
            ov = overlap(f, w)
            if ov or distance <= window_ms:
                candidates.append((index, ov, distance, text_similarity(f["text"], w["text"])))
        candidates.sort(key=lambda item: (item[3], item[1], -item[2]), reverse=True)
        if candidates:
            index, ov, distance, similarity = candidates[0]
            used.add(index)
            w = whisper[index]
            reasons = ["time_overlap" if ov else "nearby_time"]
            if similarity < 0.45:
                reasons.append("low_text_similarity")
            if term_matches(f["text"], terms) != term_matches(w["text"], terms):
                reasons.append("term_disagreement")
            pairs.append({
                "funasr_ids": [f["id"]], "whisper_ids": [w["id"]],
                "interval_ms": [min(f["start_ms"] or 0, w["start_ms"] or 0), max(f["end_ms"] or 0, w["end_ms"] or 0)],
                "overlap_ms": ov, "text_similarity": round(similarity, 4),
                "funasr": {"spk": f.get("spk"), "text": f["text"]}, "whisper": {"text": w["text"]},
                "term_hits": {"funasr": term_matches(f["text"], terms), "whisper": term_matches(w["text"], terms)},
                "status": "needs_review" if reasons != ["time_overlap"] or similarity < 0.85 else "candidate",
                "reasons": reasons,
            })
        else:
            pairs.append({"funasr_ids": [f["id"]], "whisper_ids": [], "funasr": {"spk": f.get("spk"), "text": f["text"]}, "status": "unmatched", "reasons": ["no_whisper_candidate"]})
    for index, w in enumerate(whisper):
        if index not in used:
            pairs.append({"funasr_ids": [], "whisper_ids": [w["id"]], "whisper": {"text": w["text"]}, "status": "unmatched", "reasons": ["no_funasr_candidate"]})
    return pairs


def render(pairs: list[dict]) -> str:
    lines = ["# 双引擎转录对齐候选", "", "> 本报告只用于人工审核，不自动覆盖任一引擎原文。", ""]
    for index, pair in enumerate(pairs, 1):
        lines.append(f"## {index}. {pair['status']}")
        if pair.get("interval_ms"):
            lines.append(f"时间：{pair['interval_ms'][0] / 1000:.3f}s – {pair['interval_ms'][1] / 1000:.3f}s")
        if pair.get("funasr"):
            lines.append(f"FunASR / spk {pair['funasr'].get('spk')}：{pair['funasr']['text']}")
        if pair.get("whisper"):
            lines.append(f"Whisper：{pair['whisper']['text']}")
        lines.append(f"原因：{', '.join(pair.get('reasons', []))}")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--funasr-json", required=True)
    parser.add_argument("--whisper-json", required=True)
    parser.add_argument("--terms-file", default=None)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-md", default=None)
    args = parser.parse_args()
    terms, _ = load_terms(args.terms_file)
    funasr = extract_segments(read_json(args.funasr_json), engine_hint="funasr")
    whisper = extract_segments(read_json(args.whisper_json), engine_hint="whisper")
    pairs = align(funasr, whisper, terms)
    payload = {"schema_version": "alignment-v1", "source": {"funasr": args.funasr_json, "whisper": args.whisper_json}, "pairs": pairs}
    write_json(args.out_json, payload)
    if args.out_md:
        Path(args.out_md).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out_md).write_text(render(pairs), encoding="utf-8")
    print(f"wrote {args.out_json} | {len(pairs)} candidates")


if __name__ == "__main__":
    main()
