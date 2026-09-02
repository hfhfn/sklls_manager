#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FunASR full offline pipeline: ASR + VAD + punctuation + speaker diarization.
Outputs JSON (with per-sentence spk/timestamps) and a baseline-style readable transcript.
Usage: run_funasr.py <audio_file> [--out-label LABEL] [--spk-num N] [--cache-dir DIR]
"""
import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

from transcript_core import RAW_SCHEMA_VERSION, resolve_cli_terms, merge_hotwords, sha256_file, utc_now


def fmt_ts(ms):
    s = ms / 1000.0
    m = int(s // 60)
    sec = int(s % 60)
    return f"{m:02d}:{sec:02d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio", help="input audio file (wav/m4a/mp3...)")
    ap.add_argument("--out-label", default="funasr")
    ap.add_argument("--model", default="paraformer-zh", help="paraformer-zh / iic/SenseVoiceSmall")
    ap.add_argument("--no-spk", action="store_true", help="disable speaker diarization (ASR-only)")
    ap.add_argument("--spk-num", type=int, default=None,
                    help="optionally fix the number of speakers")
    ap.add_argument("--hotwords", default="",
                    help="comma-separated hotwords to boost mixed CN/EN terms")
    ap.add_argument("--hotwords-file", default=None,
                    help="JSON term dictionary with canonical terms and aliases")
    ap.add_argument("--global-terms-file", action="append", default=[])
    ap.add_argument("--project-terms-file", action="append", default=[])
    ap.add_argument("--session-terms-file", default=None)
    ap.add_argument("--allow-cross-session-terms", action="store_true")
    ap.add_argument("--allow-term-conflicts", action="store_true")
    ap.add_argument("--cache-dir", default=None,
                    help="optional MODELSCOPE_CACHE root")
    ap.add_argument("--model-path", default=None,
                    help="local model directory; avoids logical-name resolution")
    ap.add_argument("--out-dir", default="runs/default")
    ap.add_argument("--offline", action="store_true",
                    help="fail fast instead of allowing model downloads")
    args = ap.parse_args()

    if args.no_spk and args.spk_num is not None:
        ap.error("--spk-num cannot be combined with --no-spk")
    if args.offline:
        os.environ["MODELSCOPE_OFFLINE"] = "1"
        os.environ["HF_HUB_OFFLINE"] = "1"
    if args.cache_dir:
        os.environ.setdefault("MODELSCOPE_CACHE", args.cache_dir)
    if args.model_path and not Path(args.model_path).exists():
        ap.error(f"local model path does not exist: {args.model_path}")
    audio_hash = sha256_file(args.audio)
    terms, term_meta = resolve_cli_terms(args, audio_sha256=audio_hash)
    hotwords = merge_hotwords(terms)
    # prefer GPU
    import torch
    dev = "cuda:0" if torch.cuda.is_available() else "cpu"
    print(f"[info] device = {dev}", file=sys.stderr, flush=True)

    from funasr import AutoModel
    model_kw = dict(
        model=args.model_path or args.model,
        vad_model="fsmn-vad",
        punc_model="ct-punc",
        disable_update=True,
        device=dev,
    )
    if not args.no_spk:
        model_kw["spk_model"] = "cam++"   # speaker embedding for diarization
    if args.spk_num:
        model_kw["spk_num"] = args.spk_num

    print("[info] loading FunASR pipeline ...", file=sys.stderr, flush=True)
    t0 = time.time()
    model = AutoModel(**model_kw)
    print(f"[info] model loaded in {time.time()-t0:.1f}s", file=sys.stderr, flush=True)

    t1 = time.time()
    res = model.generate(input=args.audio,
                         batch_size_s=300,   # chunked batch to bound GPU mem
                         sentence_timestamp=True,
                         hotwords=hotwords)
    print(f"[info] inference done in {time.time()-t1:.1f}s", file=sys.stderr, flush=True)

    r = res[0]
    full_text = r.get("text", "")
    sentences = []
    for seg in r.get("sentence_info", []):
        raw = seg.get("sentence") or seg.get("text") or ""
        raw = re.sub(r"<\|[^|]*\|>", "", raw).strip()   # strip SenseVoice special tokens
        sentences.append({
            "start_ms": seg.get("start"),
            "end_ms": seg.get("end"),
            "spk": seg.get("spk"),
            "text": raw,
        })

    os.makedirs(args.out_dir, exist_ok=True)
    base = args.out_label
    source = {
        "audio": str(Path(args.audio).resolve()),
        "audio_sha256": sha256_file(args.audio),
        "engine": "funasr",
        "model": args.model_path or args.model,
        "created_at": utc_now(),
        "offline": args.offline,
    }
    metadata = {
        "schema_version": RAW_SCHEMA_VERSION,
        "source": source,
        "config": {
            "device": dev, "model_args": model_kw, "hotwords": hotwords,
            "terms": term_meta, "spk_num": args.spk_num, "spk_on": not args.no_spk,
            "inference_s": round(time.time() - t1, 3),
        },
        "full_text": full_text,
        "sentences": [dict(s, id=f"funasr-{i:06d}") for i, s in enumerate(sentences, 1)],
    }
    with open(Path(args.out_dir) / f"{base}.raw.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    # Legacy-compatible readable transcript, derived from raw sentences.
    lines = []
    for s in sentences:
        spk = s["spk"]
        spk_label = f"说话人 {spk}" if spk is not None else "(no-spk)"
        lines.append(f"{spk_label} {fmt_ts(s['start_ms'])}")
        lines.append(s["text"].strip())
        lines.append("")
    with open(Path(args.out_dir) / f"{base}.transcript.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    spks = sorted({s["spk"] for s in sentences})
    print(f"[result] speakers detected: {spks}", file=sys.stderr, flush=True)
    print(f"[result] sentences: {len(sentences)}", file=sys.stderr, flush=True)
    print(f"[result] output -> {args.out_dir}/{base}.raw.json and {args.out_dir}/{base}.transcript.txt",
          file=sys.stderr, flush=True)


if __name__ == "__main__":
    main()