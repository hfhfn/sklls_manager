#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""extract_frames.py — 用 ffmpeg 从课程视频抽取"候选关键帧"，供讲义配图。

用途：course-handout 技能里，对演示/UI/终端类课时抽帧。脚本只负责**产出候选帧**，
真正"挑哪几张有意义 + 配中文标题"交给视觉子代理(Read 图片)完成。

两种模式：
1. 场景检测(默认)：抽画面明显变化处的帧，适合幻灯片/代码/终端切换。
2. 定时采样(--interval N)：每 N 秒一帧，作为兜底或补充。

用法：
    python extract_frames.py --video "<xxx.mp4>" --out "<assets 目录>" \
        [--threshold 0.3] [--max 24] [--interval 0] [--scale 1280]

依赖：ffmpeg（本仓库走 llm_gpu 环境里配置为独显的 ffmpeg）。
输出：候选 PNG（顺序编号），并打印产出清单。
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path


def run_ffmpeg(args_list):
    return subprocess.run(
        ["ffmpeg", "-y", *args_list],
        check=True, capture_output=True, timeout=1800,
    )


def extract_scene(video, out_dir, threshold, scale, max_frames):
    """抽场景变化帧。"""
    pattern = str(out_dir / "cand_%03d.png")
    vf = f"select='gt(scene,{threshold})',scale={scale}:-1"
    run_ffmpeg(["-i", str(video), "-vf", vf, "-vsync", "vfr",
                "-frames:v", str(max_frames), pattern])
    return sorted(out_dir.glob("cand_*.png"))


def extract_interval(video, out_dir, interval, scale, max_frames):
    """每 interval 秒抽一帧。"""
    pattern = str(out_dir / "tick_%03d.png")
    vf = f"fps=1/{interval},scale={scale}:-1"
    run_ffmpeg(["-i", str(video), "-vf", vf, "-vsync", "vfr",
                "-frames:v", str(max_frames), pattern])
    return sorted(out_dir.glob("tick_*.png"))


def main():
    ap = argparse.ArgumentParser(description="ffmpeg 抽取讲义候选关键帧")
    ap.add_argument("--video", required=True)
    ap.add_argument("--out", required=True, help="候选帧输出目录")
    ap.add_argument("--threshold", type=float, default=0.3, help="场景检测阈值 0~1，越大越少")
    ap.add_argument("--max", type=int, default=24, help="最多候选帧数")
    ap.add_argument("--interval", type=float, default=0, help=">0 则改用每 N 秒采样")
    ap.add_argument("--scale", type=int, default=1280, help="缩放宽度(px)")
    args = ap.parse_args()

    video = Path(args.video)
    if not video.exists():
        raise SystemExit(f"视频不存在: {video}")
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        if args.interval and args.interval > 0:
            frames = extract_interval(video, out_dir, args.interval, args.scale, args.max)
        else:
            frames = extract_scene(video, out_dir, args.threshold, args.scale, args.max)
    except subprocess.CalledProcessError as e:
        sys.stderr.write(e.stderr.decode("utf-8", "ignore")[-2000:])
        raise SystemExit(f"ffmpeg 失败: {video}")
    except FileNotFoundError:
        raise SystemExit("未找到 ffmpeg，请先 conda activate llm_gpu 或将 ffmpeg 加入 PATH")

    result = {"video": str(video), "out": str(out_dir),
              "count": len(frames), "frames": [str(f) for f in frames]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\n候选帧 {len(frames)} 张 -> {out_dir}", file=sys.stderr)


if __name__ == "__main__":
    main()
