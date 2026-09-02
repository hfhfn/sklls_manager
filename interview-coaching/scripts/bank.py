#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
bank.py — pull the relevant depth questions for a session.

The coaching question bank is accumulated across projects; each question
carries `triggers` (tokens like "评测","成本","降级","MCP","召回"). This
script filters the bank to the questions whose triggers match the session's
ambiguous terms / requested gaps / used tech stack, so the gap-prep only
drills what this candidate actually needs.

Usage:
  python bank.py --bank config/depth-questions.json \
    --context "评测,成本,降级,Milvus" [--gap "评测体系"] [--all] --out X.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def matches(question: dict, context_tokens: list[str], gap_tokens: list[str]) -> bool:
    trig = [t.strip().lower() for t in (question.get("triggers") or [])]
    if not trig:
        return True  # untriggered questions are always safe to include
    ctx = [t.strip().lower() for t in context_tokens]
    ga = [t.strip().lower() for t in gap_tokens]
    return any(t in ctx or t in ga for t in trig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bank", required=True)
    ap.add_argument("--context", default="")
    ap.add_argument("--gap", default="")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    bank = load(args.bank)
    ctx = [t for t in args.context.replace("，", ",").split(",") if t]
    gap = [t for t in args.gap.replace("，", ",").split(",") if t]

    groups = []
    total = 0
    for grp in bank.get("groups", []):
        qs = grp.get("questions", [])
        if args.all:
            keep = qs
        else:
            keep = [q for q in qs if matches(q, ctx, gap)]
        if not keep:
            continue
        groups.append({**grp, "questions": keep})
        total += len(keep)

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump({
            "schema_version": bank.get("schema_version"),
            "bank_version": bank.get("version"),
            "context": [*ctx, *gap],
            "groups": groups,
        }, f, ensure_ascii=False, indent=2)
    print(f"[bank] {total} questions in {len(groups)} groups -> {args.out}")


if __name__ == "__main__":
    main()