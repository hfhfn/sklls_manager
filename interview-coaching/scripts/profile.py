#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
profile.py — fold a session analysis into a candidate's cross-session file.

The candidate profile is the accumulation that makes coaching "mature":
across projects/sessions we dedupe the tech stack the person keeps reaching
for, track ambiguous terms until they get resolved (or keep flagging them),
and compare repeated metric claims for consistency. The whole point is that
a 3rd 魏新龙-session is not analyzed as if it were a new person.

Usage:
  python profile.py --analysis <run>/interview/analysis.json \
    --profiles <skill>/profiles --project-tag record_review
Creates profiles/<候选名>.json on first use; merges on later ones.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


def load_profile(p: Path) -> dict:
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {
        "schema_version": "candidate-profile-2026-09",
        "name": Path(p).stem,
        "first_seen": None,
        "sessions": [],
        "tech_stack": {},      # term -> {"sessions": [..], "occurrences": n}
        "metric_claims": [],   # {metric, value, sessions: []}
        "ambiguous_terms": {}, # spoken -> {"possible":.., "resolved":bool, "sessions":[]}
        "recurrent_gaps": {},  # gap -> {"sessions": [], "evidence": []}
        "deep_terms": [],      # terms seen in >=2 sessions (repeated stack)
        "pattern_note": "",
    }


def fold(profile: dict, ana: dict, project_tag: str) -> None:
    cand = ana.get("candidate", {})
    sid = str(ana.get("session", {}).get("run_dir", "")).replace("\\", "/").rstrip("/")
    date = ana.get("session", {}).get("date") or ""
    sess = {"tag": project_tag, "run_dir": sid, "date": date,
            "role": ana.get("role", ""), "project_tag": project_tag}

    if profile["first_seen"] is None:
        profile["first_seen"] = {"date": date, "run_dir": sid, "project_tag": project_tag}
    if not any(s["run_dir"] == sid for s in profile["sessions"]):
        profile["sessions"].append(sess)

    # tech stack
    for t in ana.get("tech_stack_summary") or []:
        entry = profile["tech_stack"].setdefault(t, {"sessions": [], "occurrences": 0})
        if sid not in entry["sessions"]:
            entry["sessions"].append(sid)
        entry["occurrences"] += 1

    # ambiguous terms -> resolved when session's canonical stack contains "possible"
    for a in ana.get("ambiguous_terms") or []:
        spoken = a.get("spoken", "")
        if not spoken:
            continue
        ent = profile["ambiguous_terms"].setdefault(
            spoken, {"possible": a.get("possible", ""), "resolved": False, "sessions": []})
        if sid not in ent["sessions"]:
            ent["sessions"].append(sid)
        if any(a.get("possible", "") in (profile["tech_stack"].keys() or []) for _ in [0]):
            ent["resolved"] = True
        if not ent["possible"]:
            ent["possible"] = a.get("possible", "")

    # metric claims (repeated numbers across sessions -> consistency check)
    for c in (ana.get("data_claims") or []):
        key = c.get("metric", "")
        val = c.get("value", "")
        found = next((x for x in profile["metric_claims"]
                      if x["metric"] == key and x["value"] == val), None)
        if found:
            if sid not in found["sessions"]:
                found["sessions"].append(sid)
        else:
            profile["metric_claims"].append({"metric": key, "value": val, "sessions": [sid]})

    # recurrent gaps
    for g in ana.get("depth_gaps") or []:
        gap = g.get("gap", "")
        if not gap:
            continue
        ent = profile["recurrent_gaps"].setdefault(gap, {"sessions": [], "evidence": []})
        if sid not in ent["sessions"]:
            ent["sessions"].append(sid)
        if g.get("evidence") and g["evidence"] not in ent["evidence"]:
            ent["evidence"].append(g["evidence"])

    # repeated-stack detection
    repeated = sorted(
        t for t, e in profile["tech_stack"].items() if len(e["sessions"]) >= 2)
    profile["deep_terms"] = repeated
    n = len(profile["sessions"])
    if n >= 2 and repeated:
        profile["pattern_note"] = (
            f"已见 {n} 场；跨场反复出现同一技术栈（{len(repeated)} 个："
            + "、".join(repeated[:8]) + "…），需警惕套路单一、逐场追问深度增量。")
    else:
        profile["pattern_note"] = "单场/新候选人，暂无可比的跨场重复。"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--analysis", required=True)
    ap.add_argument("--profiles", required=True)
    ap.add_argument("--project-tag", default="default")
    args = ap.parse_args()

    ana = json.loads(Path(args.analysis).read_text(encoding="utf-8"))
    name = ana.get("candidate", {}).get("name", "")
    if not name:
        raise SystemExit("analysis.json lacks candidate.name")
    safe = name.replace("/", "_").replace("\\", "_").strip()
    pdir = Path(args.profiles)
    pdir.mkdir(parents=True, exist_ok=True)
    profile_path = pdir / f"{safe}.json"
    profile = load_profile(profile_path)
    fold(profile, ana, args.project_tag)
    profile_path.write_text(json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[profile] {name}: {len(profile['sessions'])}场 | "
          f"tech_stack={len(profile['tech_stack'])} | "
          f"ambiguous={len(profile['ambiguous_terms'])} | "
          f"{profile['pattern_note']}")
    if profile.get("deep_terms"):
        print(f"[profile] 跨场重复栈: {profile['deep_terms']}")


if __name__ == "__main__":
    main()