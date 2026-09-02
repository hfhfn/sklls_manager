#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Terminology review final step: regenerate the final adjusted transcript.

After ASR (FunASR) + review (Whisper + alignment), this applies the
*confirmed* term repairs from the project term dictionary and renders the
final clean transcript. Raw ASR output is never overwritten.

Repair rule (deterministic & auditable):
  - only aliases typed `spoken_variant` and status approved/published qualify;
  - a repair fires only when the alias text literally occurs in the sentence
    AND the canonical form is not already present (avoid double-replacement);
  - longest aliases first to honour longer spellings over shorter substrings.

Outputs (in <run_dir>):
  funasr.reviewed.json   # copy of raw with repaired sentence text + audit log
  funasr.reviewed.txt    # turns-style clean final transcript
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path

from transcript_core import write_json


REPAIR_TYPE = "spoken_variant"
AUDIT_KEY = "review"


def build_repair_map(terms_path: str | Path) -> dict[str, str]:
    """Return {alias_text: canonical} for approved spoken_variant aliases."""
    data = json.loads(Path(terms_path).read_text(encoding="utf-8"))
    mapping: dict[str, str] = {}
    for item in data.get("terms", []):
        canonical = str(item.get("canonical", "")).strip()
        if not canonical or item.get("status") not in {"approved", "published"}:
            continue
        for alias in item.get("aliases", []):
            if not isinstance(alias, dict):
                continue
            if alias.get("type") != REPAIR_TYPE:
                continue
            if alias.get("status") not in {"approved", "published"}:
                continue
            text = str(alias.get("text", "")).strip()
            if text:
                mapping[text] = canonical
    return mapping


def make_reviewed(run_json: str | Path, terms_path: str | Path, reviewed_json: str | Path) -> dict:
    data = json.loads(Path(run_json).read_text(encoding="utf-8"))
    mapping = build_repair_map(terms_path)
    # longest first so e.g. "BG 杠三" is handled before a shorter overlapping alias
    ordered = sorted(mapping.items(), key=lambda kv: (len(kv[0]), kv[0]), reverse=True)
    repairs: list[dict] = []
    sentences = data.get("sentences", [])
    for sentence in sentences:
        text = str(sentence.get("text", ""))
        original = text
        for alias, canonical in ordered:
            if alias in text and canonical not in text:
                text = text.replace(alias, canonical)
        if text != original:
            sentence["text"] = text
            repairs.append({"sentence_id": sentence.get("id"),
                            "raw": original, "reviewed": text})
    data.setdefault("config", {})[AUDIT_KEY] = {
        "source": str(Path(run_json).resolve()),
        "script": "make_reviewed.py",
        "rule": "replace approved spoken_variant alias with canonical when canonical absent",
        "terms_file": str(Path(terms_path).resolve()),
        "repair_count": len(repairs),
        "applied": repairs,
    }
    write_json(reviewed_json, data)
    return {"repair_count": len(repairs), "by_alias": dict(Counter(r["raw"] for r in repairs))}


def render_turns(reviewed_json: str | Path, out_txt: str | Path, *extra: str) -> None:
    cmd = [sys.executable, str(Path(__file__).resolve().parent / "postprocess.py"),
           "--json", str(reviewed_json), "--out", str(out_txt), *extra]
    subprocess.run(cmd, check=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("run_dir", help="directory containing funasr.raw.json")
    ap.add_argument("--terms",
                    default=str(Path(__file__).resolve().parent.parent / "config" / "terms" / "technical-interview.json"))
    ap.add_argument("--no-render", action="store_true", help="skip turns .txt rendering")
    args = ap.parse_args()

    run_dir = Path(args.run_dir)
    terms_path = args.terms if os.path.isabs(args.terms) else run_dir.parent.parent / args.terms
    run_json = run_dir / "funasr.raw.json"
    if not run_json.exists():
        ap.error(f"not found: {run_json}")
    reviewed_json = run_dir / "funasr.reviewed.json"
    report = make_reviewed(run_json, terms_path, reviewed_json)
    if not args.no_render:
        render_turns(reviewed_json, run_dir / "funasr.reviewed.txt")
    print(f"[reviewed] repairs={report['repair_count']} -> {reviewed_json}")
    for alias, n in report["by_alias"].items():
        print(f"    {alias!r} -> {n}x")


if __name__ == "__main__":
    main()