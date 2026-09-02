#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Compare an engine transcript (engine json) against a reference baseline transcript.

Extracts comparable reference/hypothesis plain-text (strip speaker labels/timestamps),
then reports text-similarity metrics + speaker count. Good for a RELATIVE comparison
between engines (which captures the reference content best).
"""
import argparse
import json
import re
import sys
from difflib import SequenceMatcher
from collections import Counter

from transcript_core import load_terms, normalize_text, term_matches, write_json


def clean_zh(s):
    s = re.sub(r"[\s]+", "", s)
    return s


def parse_baseline(path):
    """Extract plain transcription text from the baseline txt (after '文字记录:' header)."""
    lines = open(path, encoding="utf-8").read().splitlines()
    in_body = False
    parts = []
    for ln in lines:
        t = ln.strip()
        if t.startswith("文字记录"):
            in_body = True
            continue
        if not in_body:
            continue
        if not t:
            continue
        if re.match(r"^说话人\s*\d", t):      # speaker header line
            continue
        if re.match(r"^\d{1,2}:\d{2}$", t):    # bare timestamp line
            continue
        parts.append(t)
    return clean_zh("".join(parts))


def parse_engine(path):
    d = json.load(open(path, encoding="utf-8"))
    # support both FunASR ("sentences") and faster-whisper ("segments") schemas
    segs = d.get("sentences") or d.get("segments") or []
    texts, spks = [], []
    for s in segs:
        t = (s.get("text") or s.get("sentence") or "")
        t = re.sub(r"<\|[^|]*\|>", "", t).strip()
        if t:
            texts.append(t)
        if s.get("spk") is not None:
            spks.append(s["spk"])
    return {
        "text": clean_zh("".join(texts)),
        "n_sentences": len(texts),
        "spk_set": sorted(set(spks)),
        "spk_counter": Counter(spks),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", default="2026年08月18日 14点58分.txt")
    ap.add_argument("--hyp-json", required=True)
    ap.add_argument("--terms-file", default=None)
    ap.add_argument("--out-json", default=None)
    ap.add_argument("--engine-label", default=None)
    args = ap.parse_args()

    ref_txt = parse_baseline(args.ref)
    eng = parse_engine(args.hyp_json)
    hyp_txt = eng["text"]

    if not ref_txt or not hyp_txt:
        print("empty text, ref=%d hyp=%d" % (len(ref_txt), len(hyp_txt)))
        sys.exit(1)

    sm = SequenceMatcher(None, ref_txt, hyp_txt)
    ratio = sm.ratio()
    # matching blocks char coverage (as fraction of reference)
    blocks = [b for b in sm.get_matching_blocks() if b.size > 0]
    matched_ref = sum(b.size for b in blocks)
    ref_cov = matched_ref / len(ref_txt)

    # char-level WER-ish (treat ref as reference, hyp as hypothesis) via Levenshtein
    # Use difflib-based rough edit distance
    edits = _lev(ref_txt, hyp_txt)
    wer_like = edits / max(len(ref_txt), len(hyp_txt))

    terms, term_meta = load_terms(args.terms_file)
    ref_norm = normalize_text(ref_txt)
    hyp_norm = normalize_text(hyp_txt)
    term_metrics = []
    for term in terms:
        canonical = normalize_text(term["canonical"])
        ref_count = ref_norm.count(canonical)
        hyp_count = hyp_norm.count(canonical)
        alias_hits = sum(hyp_norm.count(normalize_text(alias if isinstance(alias, str) else alias["text"])) for alias in term["aliases"])
        found = min(ref_count, hyp_count + alias_hits)
        precision_den = hyp_count + alias_hits
        term_metrics.append({
            "canonical": term["canonical"], "reference_count": ref_count,
            "hypothesis_count": hyp_count, "alias_hits": alias_hits,
            "found": found, "missing": max(0, ref_count - found),
            "extra": max(0, precision_den - found),
            "precision": None if precision_den == 0 else found / precision_den,
            "recall": None if ref_count == 0 else found / ref_count,
        })
    active = [item for item in term_metrics if item["reference_count"]]
    aggregate = {
        "reference_occurrences": sum(item["reference_count"] for item in active),
        "found": sum(item["found"] for item in active),
        "recall": None if not active else sum(item["found"] for item in active) / sum(item["reference_count"] for item in active),
    }
    result = {
        "reference_chars": len(ref_txt), "hypothesis_chars": len(hyp_txt),
        "sequence_matcher": ratio, "reference_char_coverage": ref_cov,
        "edit_distance_ratio": wer_like, "speakers": eng["spk_set"],
        "speaker_counts": dict(eng["spk_counter"]), "sentences": eng["n_sentences"],
        "engine": args.engine_label, "terms": term_metrics, "term_aggregate": aggregate,
        "term_dictionary": term_meta,
    }
    if args.out_json:
        write_json(args.out_json, result)
    print("=== comparison vs baseline ===")
    print(f"reference chars    : {len(ref_txt)}")
    print(f"hypothesis chars   : {len(hyp_txt)}")
    print(f"SequenceMatcher    : {ratio:.4f}")
    print(f"ref char coverage  : {ref_cov:.4f}")
    print(f"edit-distance/len  : {wer_like:.4f}")
    print(f"speakers detected  : {eng['spk_set']} (n={len(eng['spk_set'])}; baseline=2)")
    print(f"speaker label counts: {dict(eng['spk_counter'])}")
    print(f"sentences          : {eng['n_sentences']}")
    if active:
        print(f"term recall        : {aggregate['recall']:.4f} ({aggregate['found']}/{aggregate['reference_occurrences']})")
    else:
        print("term recall        : N/A (no reference term occurrences)")


def _lev(a, b):
    # simple Levenshtein distance, O(n*m) memory-light row-based
    if len(a) < len(b):
        a, b = b, a
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j-1] + 1, prev[j-1] + (ca != cb)))
        prev = cur
    return prev[-1]


if __name__ == "__main__":
    main()