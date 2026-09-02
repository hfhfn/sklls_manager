#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
analyze_schema.py — bootstrap / validate the typed interview analysis.

`interview/analysis.json` is the single source of truth for a session: the
deterministic evidence (metrics, tech stack, ambiguous terms) is filled by
scripts; the semantic fields (project lines, depth evaluation, strengths,
risks, gap-prep points) are filled by the coaching LLM. This script keeps
that file schema-complete so every session is comparable.

Usage:
  python analyze_schema.py --schema defaults/analysis-schema.json --init --out X.json
  python analyze_schema.py --schema defaults/analysis-schema.json --validate X.json
Exit nonzero (and lists the missing/typed fields) when validation fails.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


_TYPE_DEFAULTS = {
    "str": "", "int": 0, "float": 0.0, "list": [], "dict": {},
}


def load_schema(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def empty_from_schema(schema: dict) -> dict:
    out = {"schema_version": schema.get("schema_version", "coach-analysis-2026-09")}
    for field, spec in schema.get("fields", {}).items():
        ftype = spec.get("type", "list")
        default = spec.get("default", _TYPE_DEFAULTS.get(ftype, ""))
        if ftype == "dict" and "fields" in spec:
            default = empty_from_schema({"fields": spec["fields"]})
        out[field] = default
    return out


def validate(data: dict, schema: dict) -> list[str]:
    problems = []
    for field, spec in schema.get("fields", {}).items():
        ftype = spec.get("type")
        required = spec.get("required", False)
        if field not in data:
            if required:
                problems.append(f"missing required field: {field}")
            continue
        val = data[field]
        ok = {
            "str": isinstance(val, str),
            "int": isinstance(val, int) and not isinstance(val, bool),
            "float": isinstance(val, (int, float)),
            "list": isinstance(val, list),
            "dict": isinstance(val, dict),
        }.get(ftype, True)
        if ftype in ("str", "list") and required and (
            (ftype == "str" and not val.strip()) or (ftype == "list" and not val)
        ):
            problems.append(f"required field is empty: {field}")
        if not ok:
            problems.append(f"field {field} should be {ftype}, got {type(val).__name__}")
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--schema", required=True)
    ap.add_argument("--init", action="store_true")
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--target", required=True)
    args = ap.parse_args()
    schema = load_schema(args.schema)

    if args.init:
        p = Path(args.target)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(empty_from_schema(schema), ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[schema] initialised -> {args.target}")
        return

    if args.validate:
        data = json.loads(Path(args.target).read_text(encoding="utf-8"))
        problems = validate(data, schema)
        if problems:
            print("[schema] FAILED:")
            for p in problems:
                print("  -", p)
            sys.exit(1)
        print(f"[schema] OK -> {args.target}")
        return

    ap.error("provide --init or --validate")


if __name__ == "__main__":
    main()