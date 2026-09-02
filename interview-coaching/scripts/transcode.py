#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
transcode.py — normalise an audio file for ASR engines.

faster-whisper (and sometimes FunASR pipelines) assume 16 kHz mono PCM.
Non-16k / multi-channel inputs can make Whisper fail with
`RuntimeError: No position encodings are defined for positions >= 448`
and make channel-split interviews ambiguous. This helper probes the
container and re-encodes only when needed, so downstream ASR is always
fed a 16 kHz mono WAV regardless of the source m4a/mp3/ogg/aac.

Usage:
  python transcode.py <audio> [--out <wav>] [--force]
Exit 0 and prints the final path. Output keeps the same base name in
--out's directory when --out given, else next to the input as <base>_16k.wav.
Idempotent: a file already 16k mono is passed through unchanged.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def probe(audio: str | Path) -> dict:
    """Return {codec, sample_rate, channels} via ffprobe JSON."""
    cmd = ["ffprobe", "-v", "error", "-show_entries",
           "stream=codec_name,sample_rate,channels", "-of", "json", str(audio)]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        raise SystemExit(f"transcode: cannot probe {audio}: {e!r}") from e
    data = json.loads(out.stdout or "{}")
    streams = data.get("streams", [])
    if not streams:
        raise SystemExit(f"transcode: no audio stream in {audio}")
    s = streams[0]
    return {
        "codec": s.get("codec_name"),
        "sample_rate": int(s.get("sample_rate") or 0),
        "channels": int(s.get("channels") or 0),
    }


def needs_transcode(meta: dict) -> bool:
    return meta.get("channels", 0) != 1 or meta.get("sample_rate", 0) != 16000


def transcode(audio: str | Path, out: str | Path | None = None, force: bool = False) -> Path:
    meta = probe(audio)
    if not force and not needs_transcode(meta):
        return Path(audio)
    src = Path(audio)
    dst = Path(out) if out else src.with_name(f"{src.stem}_16k.wav")
    if not dst.parent.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(src),
           "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", str(dst)]
    subprocess.run(cmd, check=True)
    return dst


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("--out", default=None, help="explicit output wav path")
    ap.add_argument("--force", action="store_true", help="re-encode even if already 16k mono")
    ap.add_argument("--probe", action="store_true", help="only print probe JSON and exit")
    args = ap.parse_args()
    if args.probe:
        print(json.dumps(probe(args.audio), ensure_ascii=False))
        return
    dst = transcode(args.audio, args.out, force=args.force)
    print(f"[transcode] 16k mono WAV ready -> {dst}")


if __name__ == "__main__":
    main()