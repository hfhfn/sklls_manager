#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
faster-whisper ASR (industry-standard large model) comparison engine.
No diarization built in (whisper is ASR-only) - segments with timestamps.
Usage: run_whisper.py <audio> --model large-v3 --out-label whisper
"""
import argparse, json, os, sys, time
from pathlib import Path

from transcript_core import RAW_SCHEMA_VERSION, build_whisper_prompt, merge_hotwords, resolve_cli_terms, sha256_file, utc_now

# Make ctranslate2 able to load cuBLAS/cuDNN 9 shipped with torch (Windows).
def _prepend_torch_dlls():
    try:
        import torch
        tlib = os.path.join(os.path.dirname(torch.__file__), "lib")
        if os.path.isdir(tlib):
            os.environ["PATH"] = tlib + os.pathsep + os.environ.get("PATH", "")
    except Exception:
        pass


_prepend_torch_dlls()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("--model", default="large-v3", help="large-v3 / medium / small")
    ap.add_argument("--compute-type", default="int8_float16")
    ap.add_argument("--out-label", default="whisper")
    ap.add_argument("--hf-home", default=None)
    ap.add_argument("--model-path", default=None)
    ap.add_argument("--hotwords-file", default=None)
    ap.add_argument("--global-terms-file", action="append", default=[])
    ap.add_argument("--project-terms-file", action="append", default=[])
    ap.add_argument("--session-terms-file", default=None)
    ap.add_argument("--allow-cross-session-terms", action="store_true")
    ap.add_argument("--allow-term-conflicts", action="store_true")
    ap.add_argument("--initial-prompt", default="")
    ap.add_argument("--initial-prompt-file", default=None)
    ap.add_argument("--word-timestamps", action="store_true")
    ap.add_argument("--out-dir", default="runs/default")
    ap.add_argument("--offline", action="store_true")
    args = ap.parse_args()

    if args.offline:
        os.environ["HF_HUB_OFFLINE"] = "1"
    if args.model_path and not Path(args.model_path).exists():
        ap.error(f"local model path does not exist: {args.model_path}")
    audio_hash = sha256_file(args.audio)
    terms, term_meta = resolve_cli_terms(args, audio_sha256=audio_hash)
    extra_prompt = args.initial_prompt
    if args.initial_prompt_file:
        extra_prompt = Path(args.initial_prompt_file).read_text(encoding="utf-8").strip()
    prompt = build_whisper_prompt(terms, extra_prompt)
    hotword_text = ", ".join(merge_hotwords(terms))

    if args.hf_home:
        os.environ["HF_HOME"] = args.hf_home
        os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

    from faster_whisper import WhisperModel

    model_name = args.model_path or args.model
    print(f"[info] loading faster-whisper {model_name} ({args.compute_type}) ...", flush=True)
    t0 = time.time()
    try:
        model = WhisperModel(model_name, device="cuda",
                             compute_type=args.compute_type)
        dev = "cuda"
    except Exception as e:
        print(f"[warn] cuda init failed ({e!r}); falling back to cpu", flush=True)
        model = WhisperModel(args.model, device="cpu", compute_type="int8")
        dev = "cpu"
    print(f"[info] loaded in {time.time()-t0:.1f}s", flush=True)

    t1 = time.time()
    segments, info = model.transcribe(
        args.audio, language="zh", beam_size=5,
        vad_filter=True, word_timestamps=args.word_timestamps,
        condition_on_previous_text=True,
        initial_prompt=prompt or None,
        hotwords=hotword_text or None,
    )
    segs = []
    for s in segments:
        segs.append({"start": round(s.start, 3), "end": round(s.end, 3), "text": s.text.strip()})
    print(f"[info] inference in {time.time()-t1:.1f}s | lang={info.language} dur={info.duration:.1f}s", flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    payload = {
        "schema_version": RAW_SCHEMA_VERSION,
        "source": {
            "audio": str(Path(args.audio).resolve()),
            "audio_sha256": sha256_file(args.audio), "engine": "whisper",
            "model": model_name, "created_at": utc_now(), "offline": args.offline,
        },
        "config": {
            "device": dev, "compute_type": args.compute_type, "language": "zh",
            "beam_size": 5, "vad_filter": True, "word_timestamps": args.word_timestamps,
            "initial_prompt": prompt, "hotwords": hotword_text, "terms": term_meta,
            "inference_s": round(time.time() - t1, 3),
        },
        "language": info.language, "audio_duration": info.duration,
        "segments": [dict(s, id=f"whisper-{i:06d}") for i, s in enumerate(segs, 1)],
    }
    with open(Path(args.out_dir) / f"{args.out_label}.raw.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    txt = "\n\n".join(f"{s['start']:.1f}s-{s['end']:.1f}s\n{s['text']}" for s in segs)
    with open(Path(args.out_dir) / f"{args.out_label}.txt", "w", encoding="utf-8") as f:
        f.write(txt)
    print(f"[result] {len(segs)} segments -> {args.out_dir}/{args.out_label}.raw.json", flush=True)


if __name__ == "__main__":
    main()