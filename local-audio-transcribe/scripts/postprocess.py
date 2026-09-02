#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Render traceable FunASR turns; raw sentence JSON is never modified."""
import argparse
import json
from pathlib import Path

from transcript_core import extract_segments, read_json, write_json
from turns import render_turns, segment_turns


def parse_map(value: str) -> dict[str, str]:
    result = {}
    for pair in value.split(",") if value else []:
        if ":" in pair:
            key, label = pair.split(":", 1)
            result[key.strip()] = label.strip()
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", default="output/funasr.json")
    parser.add_argument("--out", default="output/funasr.clean.txt")
    parser.add_argument("--out-json", default=None)
    parser.add_argument("--gap-ms", type=int, default=900)
    parser.add_argument("--max-turn-ms", type=int, default=30_000)
    parser.add_argument("--max-chars", type=int, default=180)
    parser.add_argument("--speaker-map", default="", help="explicit model_spk:label pairs")
    parser.add_argument("--keep-fillers", action="store_true")
    args = parser.parse_args()

    source = read_json(args.json)
    sentences = extract_segments(source, engine_hint="funasr")
    turns = segment_turns(sentences, gap_ms=args.gap_ms, max_turn_ms=args.max_turn_ms, max_chars=args.max_chars)
    speaker_map = parse_map(args.speaker_map)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(render_turns(turns, speaker_map=speaker_map, keep_fillers=args.keep_fillers), encoding="utf-8")
    if args.out_json:
        write_json(args.out_json, {"schema_version": "transcript-turns-v1", "source": args.json, "config": vars(args), "turns": turns})
    print(f"wrote {args.out} | {len(turns)} turns | raw preserved")


if __name__ == "__main__":
    main()
