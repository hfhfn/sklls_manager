#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Suggest terminology candidates from an existing alignment report.

This command is deliberately read-only with respect to all dictionaries and raw transcripts.
"""
from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path

from transcript_core import load_terms, normalize_text, read_json, sha256_file, write_json

LATIN = re.compile(r"(?<![A-Za-z0-9])(?:[A-Z][A-Za-z0-9]*(?:[-_][A-Za-z0-9]+)*|[A-Z]{2,})(?![A-Za-z0-9])")
MIXED = re.compile(r"[A-Za-z]{2,}[一-鿿]+|[一-鿿]+[A-Za-z]{2,}")
STOP = {"the", "this", "that", "with", "from", "have", "就", "然后", "我们", "你们"}


def candidate_forms(text: str) -> list[str]:
    values = LATIN.findall(text) + MIXED.findall(text)
    return [value for value in values if normalize_text(value) not in STOP and len(normalize_text(value)) >= 2]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--alignment-json", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--terms-file", action="append", default=[])
    parser.add_argument("--min-occurrences", type=int, default=2)
    args = parser.parse_args()

    alignment_path = Path(args.alignment_json)
    document = read_json(alignment_path)
    known = []
    for path in args.terms_file:
        known.extend(load_terms(path)[0])
    known_forms = {normalize_text(term["canonical"]) for term in known}
    for term in known:
        known_forms.update(normalize_text(alias if isinstance(alias, str) else alias["text"]) for alias in term.get("aliases", []))

    observations = defaultdict(list)
    for pair in document.get("pairs", []):
        if pair.get("status") == "unmatched":
            continue
        fun_text = pair.get("funasr", {}).get("text", "")
        whi_text = pair.get("whisper", {}).get("text", "")
        for engine, text in (("funasr", fun_text), ("whisper", whi_text)):
            for value in candidate_forms(text):
                if normalize_text(value) not in known_forms:
                    observations[normalize_text(value)].append({
                        "observed": value, "engine": engine,
                        "funasr_ids": pair.get("funasr_ids", []),
                        "whisper_ids": pair.get("whisper_ids", []),
                        "interval_ms": pair.get("interval_ms"),
                        "text_similarity": pair.get("text_similarity"),
                    })

    candidates = []
    for key, occurrences in sorted(observations.items()):
        unique_windows = {(tuple(item.get("funasr_ids", [])), tuple(item.get("whisper_ids", []))) for item in occurrences}
        engines = {item["engine"] for item in occurrences}
        if len(unique_windows) < args.min_occurrences and len(engines) < 2:
            continue
        candidates.append({
            "candidate_id": f"term-candidate-{len(candidates) + 1:05d}",
            "observed_variants": sorted({item["observed"] for item in occurrences}),
            "canonical_candidate": None,
            "occurrence_count": len(unique_windows),
            "engines": sorted(engines),
            "occurrences": occurrences,
            "reason_codes": ["cross_engine_or_repeated_observation", "latin_or_mixed_shape"],
            "risk_flags": ["canonical_requires_human_confirmation"],
            "status": "proposed",
            "target_scope": None,
        })

    payload = {
        "schema_version": "term-suggestions-v1",
        "source": {"alignment": str(alignment_path), "alignment_sha256": sha256_file(alignment_path)},
        "rules": {"min_occurrences": args.min_occurrences, "known_terms": args.terms_file},
        "candidates": candidates,
    }
    write_json(args.out, payload)
    print(f"wrote {args.out} | {len(candidates)} proposed candidates | dictionaries unchanged")


if __name__ == "__main__":
    main()
