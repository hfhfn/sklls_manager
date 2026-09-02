#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
extract.py — deterministic signals from a reviewed transcript for analysis.

Pulls three things the LLM then interprets contextually:
  1. metrics   — number+unit claims (%, 分钟, ms, "top N", ratios) with the
                 sentence they appeared in as evidence.
  2. tech_stack — how often each dictionary *canonical* term occurs (a proxy
                 for which parts of the stack the candidate actively used),
                 plus a count of unrepaired spoken_variant aliases (speech
                 the dict knows but ASR heard phonetically) — those are the
                 "ambiguous speech" the gap-prep must nail down.
  3. ambiguous — alignment pairs flagged needs_review / candidate whose two
                 engines disagree (funasr vs whisper), i.e. the phonetic
                 guesses a follow-up interview should confirm.

Output is conservative, heuristic evidence — never a judgment itself.
Usage:
  python extract.py --reviewed X --alignment Y --terms A.json --terms B.json --out X.json
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


# --- metric regexes (conservative, value/unit pairs) -------------------------
_METRIC_PATTERNS = [
    (re.compile(r"(\d+(?:\.\d+)?)\s*%"), "percent"),
    (re.compile(r"(\d+(?:\.\d+)?)\s*ms"), "ms"),
    (re.compile(r"(\d+(?:\.\d+)?)\s*毫秒"), "毫秒"),
    (re.compile(r"(\d+(?:\.\d+)?)\s*秒"), "秒"),
    (re.compile(r"(?:平均响应时间|解决时间|响应时间)[是为在]*\s*(\d+(?:\.\d+)?)"), "时间"),
    (re.compile(r"(\d+(?:\.\d+)?)\s*(?:分钟|钟|分)\s*内"), "分钟"),
    (re.compile(r"(?:召回率|准确率|命中率|成功率|相似度)[是为在]*\s*(\d+(?:\.\d+)?)\s*%"), "率"),
    (re.compile(r"top\s*(\d+)", re.I), "top_n"),
    (re.compile(r"(\d+(?:\.\d+)?)\s*倍"), "倍"),
]

_PCT_CLAIM = re.compile(r"(?:召回率|准确率|命中率|成功率|相似度|精确率|答题率)[是为在到约]*\s*(\d+(?:\.\d+)?)\s*%")

# --- spoken (Chinese-numeral) metric handling --------------------------------
_CN_DIGITS = {"零": 0, "一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5,
              "六": 6, "七": 7, "八": 8, "九": 9}
_CN_TENS = {"十": 10, "百": 100}
_PCT_SPOKEN = re.compile(r"(百分之|有)?([零一二两三四五六七八九十]+)")
_CN_DECIMAL = re.compile(r"([零一二两三四五六七八九十]+)点([零一二两三四五六七八九十]+)?")
_MIN_SPOKEN = re.compile(r"(?:分钟|钟|分)[内在是]*")
_RATE_SPOKEN = re.compile(r"(?:召回率|准确率|命中率|成功率|相似度|平均响应时间|解决时间)[是在到约]*[第之]?([零一二两三四五六七八九十]+)(?:以上|左右|内)?")
_PCT_BARE = re.compile(r"百分之([零一二两三四五六七八九十]+)")


def _cn_to_int(s: str) -> float:
    """Convert a Chinese number string (0..999) to int; returns -1 on garbage."""
    if not s:
        return -1
    total, cur = 0, 0
    for ch in s:
        if ch in _CN_DIGITS:
            cur += _CN_DIGITS[ch]
        elif ch in _CN_TENS:
            unit = _CN_TENS[ch]
            if cur == 0 and total == 0:
                cur = 1  # "十二" -> 十 counts as 1 unit
            total += cur * unit
            cur = 0
        else:
            return -1
    total += cur
    return total if total > 0 else -1


def extract_spoken_metrics(sentences):
    """Fix up the common FunASR habit of writing spoken numbers in characters."""
    out = []
    for s in sentences:
        text = s.get("text", "") or ""
        sid = str(s.get("id", ""))
        # 百分之八十 / 相似度九十以上
        for m in _RATE_SPOKEN.finditer(text):
            n = _cn_to_int(m.group(1))
            if n > 0:
                out.append({"sentence": sid, "value": str(n), "unit": "percent_spoken",
                            "raw": m.group(0)})
        for m in _PCT_BARE.finditer(text):
            n = _cn_to_int(m.group(1))
            if n > 0 and not any(x.get("raw") == m.group(0) and x.get("sentence") == sid
                                 for x in out):
                out.append({"sentence": sid, "value": str(n), "unit": "percent_spoken",
                            "raw": m.group(0)})
        # 三点二分钟  / 十余分钟
        for m in _CN_DECIMAL.finditer(text):
            frac_pos = text.find(m.group(0))
            tail = text[m.end(): m.end() + 6]
            if _MIN_SPOKEN.search(tail):
                int_part = _cn_to_int(m.group(1))
                if int_part >= 0:
                    frac = _cn_to_int(m.group(2)) if m.group(2) else 0
                    val = int_part + frac / 10 ** len(m.group(2) or "0")
                    out.append({"sentence": sid, "value": str(val), "unit": "分钟_spoken",
                                "raw": m.group(0)})
                _ = m  # keep `m` referenced
    return out


def extract_metrics(sentences, ctx_texts):
    """Return {pattern_key: [objs]} with per-match value+unit+sentence id."""
    found = defaultdict(list)
    for s in sentences:
        text = s.get("text", "") or ""
        sid = str(s.get("id", ""))
        for regex, key in _METRIC_PATTERNS:
            for m in regex.finditer(text):
                found[key].append({
                    "sentence": sid, "value": m.group(1),
                    "unit": key, "raw": m.group(0),
                })
    # also collect explicit 命中/准确/召回 claims with percentages
    claims = []
    for s in sentences:
        text = s.get("text", "") or ""
        for m in _PCT_CLAIM.finditer(text):
            claims.append(m.group(0))
    return found, claims


def extract_tech_stack(sentences, terms_files):
    """Count canonical occurrences + unrepaired spoken_variant alias hits."""
    canon_count = Counter()
    canon_sents = defaultdict(list)
    alias_count = Counter()
    alias_eg = defaultdict(set)

    for tf in terms_files:
        data = json.loads(Path(tf).read_text(encoding="utf-8"))
        for item in data.get("terms", []):
            canon = str(item.get("canonical", "") or "").strip()
            if not canon:
                continue
            for s in sentences:
                text = s.get("text", "") or ""
                sid = str(s.get("id", ""))
                n = text.count(canon)
                if n:
                    canon_count[canon] += n
                    if len(canon_sents[canon]) < 6:
                        canon_sents[canon].append(sid)
            for alias in item.get("aliases", []):
                if not isinstance(alias, dict) or alias.get("type") != "spoken_variant":
                    continue
                a = str(alias.get("text", "") or "").strip()
                if not a or len(a) < 3:
                    continue
                for s in sentences:
                    text = s.get("text", "") or ""
                    if a in text:
                        sid = str(s.get("id", ""))
                        alias_count[alias["text"]] += 1
                        alias_eg[alias["text"]].add(sid)
    return {
        "canonical": [
            {"term": t, "occurrences": n, "sentence_ids": canon_sents[t]}
            for t, n in canon_count.most_common()
        ],
        "unrepaired_spoken_variants": [
            {"spoken": a, "occurrences": n, "sentence_ids": sorted(sids)}
            for a, n in alias_count.most_common()
            for sids in [sorted(alias_eg[a])]
        ],
    }


def extract_ambiguous(alignment):
    """Alignment needs_review/candidate pairs where engines disagree."""
    out = []
    for p in alignment.get("pairs", []):
        if p.get("status") not in ("needs_review", "candidate"):
            continue
        fa = (p.get("funasr") or {}).get("text", "") or ""
        wh = (p.get("whisper") or {}).get("text", "") or ""
        if not fa and not wh:
            continue
        sim = p.get("text_similarity", 1.0)
        out.append({
            "status": p.get("status"),
            "text_similarity": round(sim, 3),
            "funasr": fa, "whisper": wh,
            "interval_ms": p.get("interval_ms"),
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reviewed", required=True)
    ap.add_argument("--alignment", required=True)
    ap.add_argument("--terms", action="append", default=[])
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    rv = json.loads(Path(args.reviewed).read_text(encoding="utf-8"))
    sentences = rv.get("sentences", [])
    aln = json.loads(Path(args.alignment).read_text(encoding="utf-8"))

    metrics, claims = extract_metrics(sentences, None)
    for sm in extract_spoken_metrics(sentences):
        unit = sm["unit"]
        metrics[unit] = metrics.get(unit, []) + [sm]
    stack = extract_tech_stack(sentences, args.terms)
    ambiguous = extract_ambiguous(aln)

    payload = {
        "schema_version": "coach-extract-2026-09",
        "metrics": {k: v[:60] for k, v in metrics.items()},
        "percentage_claims": claims[:40],
        "tech_stack": stack,
        "ambiguous": ambiguous[:80],
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"[extract] metrics={sum(len(v) for v in metrics.values())} "
          f"tech_terms={len(stack['canonical'])} ambiguous={len(payload['ambiguous'])} "
          f"-> {args.out}")


if __name__ == "__main__":
    main()