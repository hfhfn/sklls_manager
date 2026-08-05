#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""批量转录：ffmpeg 提取音频 → FunASR SenseVoiceSmall 语音识别 → 原始转录 txt

支持断点续传：已存在 .txt 的视频自动跳过
中间文件放在 .notes_intermediates/ 下，镜像原目录结构
"""

import os
import re
import subprocess
import sys
import traceback
from datetime import datetime
from pathlib import Path

# ⚠ 可移植副本（course-transcribe 技能自带）。复用到新课程时，把下面这行 ROOT 改成新课程根目录的绝对路径。
ROOT = r"C:\Users\hfhfn\Desktop\其他\mksz955-MCP+A2A 从0到1构建类Manus多Agent全栈应用资源"
VIDEO_ROOT = os.path.join(ROOT, "videos")
INTER = os.path.join(ROOT, ".notes_intermediates")
FAILED_LOG = os.path.join(ROOT, ".transcribe_failed.log")
PROGRESS_LOG = os.path.join(ROOT, ".transcribe_progress.log")


def log(msg):
    """同时输出到 stdout 和进度日志"""
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(PROGRESS_LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def log_failure(video_path, error):
    with open(FAILED_LOG, "a", encoding="utf-8") as f:
        f.write(f"{video_path}\n  {error}\n\n")


def collect_videos():
    """收集所有章节下的 MP4 文件，按章节名、课时号排序"""
    videos = []
    source_root = VIDEO_ROOT if os.path.isdir(VIDEO_ROOT) else ROOT
    all_items = sorted(os.listdir(source_root), key=chapter_sort_key)
    for ch in all_items:
        chdir = os.path.join(source_root, ch)
        if not os.path.isdir(chdir):
            continue
        if not ch.startswith("第"):
            continue
        mp4_files = sorted((f for f in os.listdir(chdir) if f.endswith(".mp4")), key=lesson_sort_key)
        for f in mp4_files:
            videos.append((chdir, ch, f))
    return videos


def chapter_sort_key(name):
    match = re.match(r"第(\d+)章", name)
    return (int(match.group(1)) if match else 10_000, name)


def lesson_sort_key(name):
    match = re.match(r"(\d+)-(\d+)", name)
    return (
        int(match.group(1)) if match else 10_000,
        int(match.group(2)) if match else 10_000,
        name,
    )


def extract_audio(video_path, wav_path):
    """ffmpeg 提取 16kHz 单声道 WAV"""
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", video_path,
            "-vn",                      # 丢弃视频流
            "-acodec", "pcm_s16le",     # PCM 16-bit
            "-ar", "16000",             # 16kHz 采样率
            "-ac", "1",                 # 单声道
            wav_path,
        ],
        check=True,
        capture_output=True,
        timeout=300,                    # 5 分钟超时
    )


def transcribe(wav_path, txt_path, model):
    """FunASR SenseVoiceSmall 语音识别"""
    from funasr.utils.postprocess_utils import rich_transcription_postprocess

    res = model.generate(
        input=wav_path,
        cache={},
        language="zh",
        use_itn=True,                  # 逆文本正则化（数字/日期等）
        batch_size_s=60,               # 60 秒动态批处理
        merge_vad=True,                # 合并 VAD 片段
    )
    text = rich_transcription_postprocess(res[0]["text"])
    Path(txt_path).write_text(text, encoding="utf-8")


def main():
    # 初始化进度日志
    with open(PROGRESS_LOG, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*60}\n开始于 {datetime.now().isoformat()}\n")

    # 收集视频
    videos = collect_videos()
    log(f"找到 {len(videos)} 个 MP4 视频")

    # 批量统计
    total = len(videos)
    skipped = 0
    done = 0
    failed = 0

    # 加载 FunASR 模型（全局复用）
    log("加载 FunASR SenseVoiceSmall + fsmn-vad 模型...")
    from funasr import AutoModel
    model = AutoModel(
        model="iic/SenseVoiceSmall",
        vad_model="fsmn-vad",
        vad_kwargs={"max_single_segment_time": 30000},
        device="cuda:0",
        disable_update=True,
    )
    log("模型加载完成，开始转录...")

    for idx, (chdir, ch, fname) in enumerate(videos, 1):
        stem = Path(fname).stem
        wav_path = os.path.join(INTER, ch, stem + ".wav")
        txt_path = os.path.join(INTER, ch, stem + ".txt")

        # 断点续传：跳过已完成
        if os.path.exists(txt_path) and os.path.getsize(txt_path) > 10:
            log(f"[{idx}/{total}] 跳过（已转录）: {stem}")
            skipped += 1
            continue

        os.makedirs(os.path.dirname(txt_path), exist_ok=True)
        video_full = os.path.join(chdir, fname)

        try:
            # 提取音频
            if not os.path.exists(wav_path):
                extract_audio(video_full, wav_path)

            # 语音识别
            transcribe(wav_path, txt_path, model)

            # 转录后删除 wav 节约空间
            if os.path.exists(wav_path):
                os.remove(wav_path)

            done += 1
            log(f"[{idx}/{total}] 完成: {stem}")

        except Exception as e:
            failed += 1
            err_msg = traceback.format_exc()
            log(f"[{idx}/{total}] 失败: {stem} — {e}")
            log_failure(video_full, err_msg)
            # 清理损坏文件
            for p in [wav_path, txt_path]:
                if os.path.exists(p):
                    os.remove(p)

    # 汇总
    log(f"\n{'='*40}")
    log(f"转录完成！")
    log(f"  总数: {total}")
    log(f"  跳过（已有）: {skipped}")
    log(f"  新完成: {done}")
    log(f"  失败: {failed}")
    if failed:
        log(f"  失败清单见: {FAILED_LOG}")
    log(f"结束于 {datetime.now().isoformat()}")


if __name__ == "__main__":
    main()
