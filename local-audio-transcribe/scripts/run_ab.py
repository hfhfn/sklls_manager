#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Run an offline, reproducible FunASR/Whisper comparison in an isolated directory."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("audio", nargs="?", help="required with --run-models; used for manifest hashing")
    parser.add_argument("--funasr-json", default=None, help="existing FunASR JSON for offline-only evaluation")
    parser.add_argument("--whisper-json", default=None, help="existing Whisper JSON for offline-only evaluation")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--ref", default=None)
    parser.add_argument("--terms-file", default=None)
    parser.add_argument("--cache-dir", default=None)
    parser.add_argument("--run-models", action="store_true")
    args = parser.parse_args()
    if args.run_models and not args.audio:
        parser.error("audio is required with --run-models")
    if not args.run_models and not (args.funasr_json and args.whisper_json):
        parser.error("provide --funasr-json and --whisper-json for offline evaluation")
    root = Path(__file__).resolve().parent
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    commands = []
    if args.run_models:
        commands = [
            [sys.executable, str(root / "run_funasr.py"), args.audio, "--out-dir", str(out), "--out-label", "funasr", "--spk-num", "2", "--offline"],
            [sys.executable, str(root / "run_whisper.py"), args.audio, "--out-dir", str(out), "--out-label", "whisper", "--offline"],
        ]
        if args.terms_file:
            commands[0] += ["--hotwords-file", args.terms_file]
            commands[1] += ["--hotwords-file", args.terms_file]
        if args.cache_dir:
            commands[0] += ["--cache-dir", args.cache_dir]
    if args.run_models:
        for command in commands:
            subprocess.run(command, check=True)
    funasr = out / "funasr.raw.json"
    whisper = out / "whisper.raw.json"
    if not args.run_models:
        funasr = Path(args.funasr_json)
        whisper = Path(args.whisper_json)
    subprocess.run([sys.executable, str(root / "postprocess.py"), "--json", str(funasr), "--out", str(out / "funasr.turns.txt"), "--out-json", str(out / "funasr.turns.json")], check=True)
    subprocess.run([sys.executable, str(root / "align_transcripts.py"), "--funasr-json", str(funasr), "--whisper-json", str(whisper), "--terms-file", args.terms_file or "", "--out-json", str(out / "alignment.json"), "--out-md", str(out / "alignment.md")], check=True)
    if args.ref:
        for label, hyp_path in (("funasr", funasr), ("whisper", whisper)):
            subprocess.run([sys.executable, str(root / "score_transcript.py"), "--ref", args.ref, "--hyp-json", str(hyp_path), "--terms-file", args.terms_file or "", "--out-json", str(out / f"{label}.score.json"), "--engine-label", label], check=True)
    manifest = {
        "audio": str(Path(args.audio).resolve()) if args.audio else None,
        "audio_sha256": hashlib.sha256(Path(args.audio).read_bytes()).hexdigest() if args.audio else None,
        "existing_inputs": {"funasr": str(funasr), "whisper": str(whisper)},
        "commands": commands, "created_at": time.time(), "run_models": args.run_models,
    }
    (out / "run.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
