#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Resolve, lint and explicitly approve terminology candidates into a project dictionary."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from transcript_core import load_terms, load_term_layers, normalize_text, read_json, sha256_file, utc_now, write_json


def resolve(args):
    terms, snapshot = load_term_layers(global_files=args.global_file, project_files=args.project_file,
                                       session_file=args.session_file, explicit_terms=args.hotword,
                                       strict=not args.allow_conflicts)
    result = {"terms": terms, "snapshot": snapshot}
    if args.out:
        write_json(args.out, result)
    print(json.dumps({"terms": len(terms), "resolved_sha256": snapshot["resolved_sha256"], "conflicts": snapshot["conflicts"]}, ensure_ascii=False, indent=2))


def lint(args):
    terms, _ = load_terms(args.terms_file)
    warnings = []
    forms = {}
    for term in terms:
        if len(normalize_text(term["canonical"])) < 2:
            warnings.append({"term": term["canonical"], "warning": "term_too_short"})
        for alias in term.get("aliases", []):
            key = normalize_text(alias if isinstance(alias, str) else alias["text"])
            if key in forms and forms[key] != term["canonical"]:
                warnings.append({"alias": alias["text"], "warning": "alias_collision", "terms": [forms[key], term["canonical"]]})
            forms[key] = term["canonical"]
    print(json.dumps({"terms": len(terms), "warnings": warnings}, ensure_ascii=False, indent=2))


def approve(args):
    suggestions = read_json(args.suggestions)
    candidate = next((item for item in suggestions.get("candidates", []) if item["candidate_id"] == args.candidate_id), None)
    if candidate is None:
        raise SystemExit(f"candidate not found: {args.candidate_id}")
    if not args.canonical:
        raise SystemExit("--canonical is required; observed ASR text must not silently become canonical")
    target = Path(args.target_file)
    if target.exists():
        dictionary = read_json(target)
    else:
        dictionary = {"schema_version": "terms-v2", "dictionary_id": target.stem, "version": 0, "scope": args.scope, "terms": []}
    before = sha256_file(target) if target.exists() else None
    term = {"term_id": f"{args.scope}.{normalize_text(args.canonical)}", "canonical": args.canonical,
            "aliases": [{"text": value, "status": "approved", "type": "reviewed_observation"} for value in args.alias],
            "category": args.category, "priority": 50 if args.scope == "project" else 10,
            "enabled": True, "status": "approved", "source": {"candidate_id": args.candidate_id}}
    dictionary["terms"] = [item for item in dictionary.get("terms", []) if normalize_text(item.get("canonical", "")) != normalize_text(args.canonical)] + [term]
    dictionary["version"] = int(dictionary.get("version", 0)) + 1
    dictionary["parent_hash"] = before
    dictionary["updated_at"] = utc_now()
    write_json(target, dictionary)
    history = Path(args.history)
    history.parent.mkdir(parents=True, exist_ok=True)
    with history.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"event":"approve","candidate_id":args.candidate_id,"scope":args.scope,"canonical":args.canonical,"aliases":args.alias,"source_suggestions_sha256":sha256_file(args.suggestions),"previous_dictionary_sha256":before,"created_at":utc_now()}, ensure_ascii=False) + "\n")
    print(f"approved {args.candidate_id} -> {args.scope}: {args.canonical}; suggestions and raw files unchanged")


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("resolve")
    p.add_argument("--global-file", action="append", default=[]); p.add_argument("--project-file", action="append", default=[])
    p.add_argument("--session-file"); p.add_argument("--hotword", action="append", default=[]); p.add_argument("--allow-conflicts", action="store_true"); p.add_argument("--out")
    p.set_defaults(func=resolve)
    p = sub.add_parser("lint"); p.add_argument("--terms-file", required=True); p.set_defaults(func=lint)
    p = sub.add_parser("approve"); p.add_argument("--suggestions", required=True); p.add_argument("--candidate-id", required=True); p.add_argument("--canonical", required=True); p.add_argument("--alias", action="append", default=[]); p.add_argument("--scope", choices=["project", "session", "global"], required=True); p.add_argument("--target-file", required=True); p.add_argument("--history", required=True); p.add_argument("--category", default="technical"); p.set_defaults(func=approve)
    args = parser.parse_args(); args.func(args)


if __name__ == "__main__":
    main()
