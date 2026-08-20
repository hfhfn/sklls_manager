#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""transcribe：mp4 → 16kHz 单声道 WAV → ASR 分段(带时间戳) → transcript.jsonl

默认引擎 FunASR SenseVoiceSmall（中文最优、快、省显存）。
做法：
  1. ffmpeg 抽 16kHz 单声道 wav；
  2. fsmn-vad 先切出语音段(秒)，再对每段单独跑 SenseVoice → 每段 t0/t1/text 都可靠；
  3. 写 transcript.jsonl：[{t0,t1,text}, ...]，并汇总 full_text.txt。
可选引擎 faster-whisper（英文/多语/苛求准确），分段自带时间戳。

只依赖本机已验证的 FunASR 管线（llm_gpu 环境）。
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

from common import ProgressLog, write_jsonl, ffmpeg_bin, fmt_ts

WAV_SR = 16000

# SenseVoice rich 后处理会注入情绪/事件 emoji（如 😊）——从笔记文本里清掉
_EMOJI_RE = re.compile(r"[\U0001F000-\U0001FFFF☀-➿️]")


def extract_wav(video_path, wav_path):
    subprocess.run(
        [ffmpeg_bin(), "-y", "-i", video_path,
         "-vn", "-acodec", "pcm_s16le", "-ar", str(WAV_SR), "-ac", "1",
         str(wav_path)],
        check=True, capture_output=True, timeout=600,
    )


def _load_wav_np(wav_path):
    import soundfile as sf
    import numpy as np
    data, sr = sf.read(str(wav_path), dtype="float32")
    if data.ndim > 1:
        data = data.mean(axis=1)
    return data, sr


def transcribe_sensevoice(wav_path, progress):
    """返回 [{t0,t1,text}]。fsmn-vad 分段 → 每段 SenseVoice。"""
    from funasr import AutoModel
    from funasr.utils.postprocess_utils import rich_transcription_postprocess
    import numpy as np

    user_cache = {}  # FunASR 流式缓存参数，需为 dict
    val = Path(wav_path)
    out_path = Path(val.parent) / "transcript.jsonl"
    if out_path.exists() and out_path.stat().st_size > 10:
        progress.log("[asr] 已有 transcript.jsonl，跳过转录")
        from common import read_jsonl
        return read_jsonl(out_path)

    progress.log("[asr] 加载 fsmn-vad + SenseVoiceSmall ...")
    vad = AutoModel(model="fsmn-vad", disable_update=True, device="cuda:0")
    asr = AutoModel(model="iic/SenseVoiceSmall", device="cuda:0",
                    disable_update=True)
    data, sr = _load_wav_np(wav_path)

    # 1) VAD 分段
    vad_res = vad.generate(input=data, cache=user_cache, fs=sr)
    segments = (vad_res[0].get("value", []) or []) if vad_res else []
    dur_s = len(data) / sr
    # fsmn-vad 的 value 以"毫秒"为段单位（如 [0,60010]=0-60.01s）。
    # 用全体段的最大端值一次性判定量纲，再统一归一，避免逐段误判。
    max_raw = max((seg[1] for seg in segments if seg and len(seg) >= 2), default=0)
    div = None
    if max_raw > dur_s * 2:
        if max_raw / dur_s > 5000:      # ~采样率量级 → raw samples
            div = sr
        else:                            # ~1000 量级 → 毫秒
            div = 1000.0
    segs = []
    for seg in segments:
        if not seg or len(seg) < 2:
            continue
        s, e = float(seg[0]), float(seg[1])
        if div is not None:
            s, e = s / div, e / div
        if e > s + 0.3:
            segs.append((s, e))
    if not segs:
        progress.log("[asr] VAD 无有效段，退化整段一次识别")
        segs = [(0.0, len(data) / sr)]

    progress.log(f"[asr] VAD 分段 {len(segs)} 段，开始识别 ...")
    out = []
    N = len(segs)
    for i, (s, e) in enumerate(segs):
        seg_audio = data[int(s * sr):int(e * sr)]
        if len(seg_audio) == 0:
            continue
        res = asr.generate(input=seg_audio, language="zh", use_itn=True,
                           cache=user_cache)
        text = rich_transcription_postprocess(res[0]["text"])
        text = _EMOJI_RE.sub("", text)
        # 去掉 SenseVoice 的 <|…|> 标签与说话人标记残留
        text = text.replace("<|Speech|>", "").replace("<|zh|>", "").strip()
        if text:
            out.append({"t0": round(s, 2), "t1": round(e, 2), "text": text})
        if (i + 1) % 50 == 0 or i == N - 1:
            progress.log(f"[asr] {i+1}/{N} 段")

    write_jsonl(out_path, out)
    # 汇总全文
    full = "\n".join(r["text"] for r in out)
    (val.parent / "full_text.txt").write_text(full, encoding="utf-8")
    progress.log(f"[asr] 完成，共 {len(out)} 段")
    return out


def transcribe_faster_whisper(wav_path, progress, fw):
    """{t0,t1,text} 用 faster-whisper（自带时间戳）。"""
    from faster_whisper import WhisperModel
    out_path = Path(wav_path).parent / "transcript.jsonl"
    if out_path.exists() and out_path.stat().st_size > 10:
        from common import read_jsonl
        return read_jsonl(out_path)
    progress.log(f"[asr] 加载 faster-whisper {fw.get('size')} ({fw.get('device')}) ...")
    model = WhisperModel(fw.get("size"), device=fw.get("device", "auto"),
                         compute_type=fw.get("compute_type", "float16"))
    segs, _ = model.transcribe(wav_path, vad_filter=True)
    out = [{"t0": round(s.start, 2), "t1": round(s.end, 2), "text": s.text.strip()}
           for s in segs if s.text and s.text.strip()]
    write_jsonl(out_path, out)
    (Path(wav_path).parent / "full_text.txt").write_text(
        "\n".join(r["text"] for r in out), encoding="utf-8")
    progress.log(f"[asr] 完成，共 {len(out)} 段")
    return out


def _cloud_asr_candidates(cfg, prefer=None):
    """返回 [(base_url, api_key, model)]；prefer 指定某 asr_providers key 排最前。"""
    provs = cfg.get("asr_providers", {}) or {}
    cand = []
    for name, p in provs.items():
        if not p.get("enabled", False):
            continue
        if p.get("api_key") and p.get("base_url") and p.get("model"):
            cand.append((name, p["base_url"], p["api_key"], p["model"]))
    if prefer:
        cand.sort(key=lambda c: 0 if c[0] == prefer else 1)
    return cand


def transcribe_cloud_speech(wav_path, cfg, progress, prefer=None, window_s=45):
    """云端 ASR（硅基 FunAudioLLM/SenseVoiceSmall / TeleAI/TeleSpeechASR 等）。
    按 window_s 固定分窗以保留时间戳；每窗逐 provider 故障转移。
    返回 [{t0,t1,text}]。"""
    import io
    import soundfile as sf
    out_path = Path(wav_path).parent / "transcript.jsonl"
    if out_path.exists() and out_path.stat().st_size > 10:
        from common import read_jsonl
        return read_jsonl(out_path)
    cand = _cloud_asr_candidates(cfg, prefer)
    if not cand:
        raise RuntimeError("engine=cloud* 但 asr_providers 无已启用 provider")
    data, sr = sf.read(wav_path, dtype="float32")
    if data.ndim > 1:
        data = data.mean(axis=1)
    dur = len(data) / sr
    progress.log(f"[asr] 云端识别 {len(cand)} 家 provider，{window_s}s 分窗 ...")
    out = []
    start = 0.0
    while start < dur:
        end = min(start + window_s, dur)
        seg = data[int(start * sr):int(end * sr)]
        buf = io.BytesIO()
        sf.write(buf, seg, sr, format="WAV")
        buf.seek(0)
        text = ""
        last_err = None
        for name, base_url, key, model in cand:
            try:
                from openai import OpenAI
                cli = OpenAI(base_url=base_url, api_key=key, timeout=180, max_retries=0)
                r = cli.audio.transcriptions.create(
                    model=model, file=("seg.wav", buf, "audio/wav"), language="zh")
                text = (r.text or "").strip()
                if text:
                    break
                last_err = "empty"
            except Exception as e:
                last_err = f"{name}:{type(e).__name__}:{str(e)[:80]}"
        if text:
            out.append({"t0": round(start, 2), "t1": round(end, 2), "text": text})
        else:
            progress.log(f"[asr][!] {fmt_ts(start)} 窗全部 provider 失败: {last_err}")
        start = end
    write_jsonl(out_path, out)
    (Path(wav_path).parent / "full_text.txt").write_text(
        "\n".join(r["text"] for r in out), encoding="utf-8")
    progress.log(f"[asr] 云端完成，共 {len(out)} 段（{window_s}s/窗）")
    return out


def transcribe(video_path, inter_dir, cfg, progress):
    wav = Path(inter_dir) / "audio.wav"
    if not wav.exists():
        progress.log("[asr] ffmpeg 抽取音频 ...")
        extract_wav(video_path, wav)
    engine = cfg.get("engine", "sensevoice")
    if engine == "faster-whisper":
        return transcribe_faster_whisper(str(wav), progress, cfg.get("faster_whisper", {}))
    if engine.startswith("cloud"):
        prefer = {"cloud-sensevoice": "siliconflow-sensevoice",
                  "cloud-tele": "siliconflow-tele-speech"}.get(engine)
        return transcribe_cloud_speech(str(wav), cfg, progress, prefer=prefer)
    return transcribe_sensevoice(str(wav), progress)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--inter", default=None)
    a = ap.parse_args()
    from common import load_config, get_intermediate_dir
    cfg = load_config()
    inter = a.inter or get_intermediate_dir(a.video)
    plog = ProgressLog(inter)
    rows = transcribe(a.video, inter, cfg, plog)
    print(json.dumps(rows[:3], ensure_ascii=False, indent=2))
    print(f"... 共 {len(rows)} 段 -> {Path(inter)/'transcript.jsonl'}")