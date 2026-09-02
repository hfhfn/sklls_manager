#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Validate and apply human-approved transcript revision patches."""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

from transcript_core import read_json, sha256_file, write_json


def load_patches(path: str) -> list[dict]:
    patches = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            patches.append(json.loads(line))
    return patches


def apply_patches(source: dict, patches: list[dict], source_hash: str, *, apply: bool = False) -> tuple[dict, list[dict]]:
    result = copy.deepcopy(source)
    statuses = []
    turns = result.get("turns") or result.get("sentences") or result.get("segments") or []
    for patch in patches:
        status = {"revision_id": patch.get("revision_id"), "status": "rejected"}
        if patch.get("expected_source_sha256") and patch["expected_source_sha256"] != source_hash:
            status["reason"] = "source_hash_mismatch"
        else:
            target = next((item for item in turns if item.get("id") == patch.get("source_id")), None)
            if target is None:
                status["reason"] = "source_id_not_found"
            elif patch.get("old_text") not in target.get("text", ""):
                status["reason"] = "old_text_not_found"
            elif patch.get("status") not in {"approved", "proposed"}:
                status["reason"] = "patch_not_approved"
            elif apply:
                target["text"] = target["text"].replace(patch["old_text"], patch["new_text"], 1)
                status["status"] = "applied"
            else:
                status["status"] = "validated"
        statuses.append(status)
    return result, statuses


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--patch", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--log", required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    source = read_json(args.source)
    source_hash = sha256_file(args.source)
    result, statuses = apply_patches(source, load_patches(args.patch), source_hash, apply=args.apply)
    if args.apply and any(item["status"] == "applied" for item in statuses):
        result.setdefault("revision_metadata", {})["source_sha256"] = source_hash
        write_json(args.out, result)
    Path(args.log).parent.mkdir(parents=True, exist_ok=True)
    with Path(args.log).open("a", encoding="utf-8") as handle:
        for status in statuses:
            handle.write(json.dumps(status, ensure_ascii=False) + "\n")
    print(json.dumps({"applied": sum(s["status"] == "applied" for s in statuses), "validated": sum(s["status"] == "validated" for s in statuses), "rejected": sum(s["status"] == "rejected" for s in statuses)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
