#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""video2markdown 共享工具：配置加载 / 日志 / 路径 / 时间格式化 / JSONL 读写。"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
CONFIG_DEFAULT = {
    "providers": {},
    "failover": {"randomize": True, "retries": 2, "min_delay_s": 2,
                 "consecutive_fail_to_sleep": 3},
    "describe_prompt": "",
    "engine": "sensevoice",
    "faster_whisper": {"size": "large-v3", "device": "auto", "compute_type": "float16"},
    "scene_threshold": 0.35,
    "max_keyframes": 120,
    "fallback_interval_s": 10,
    "ocr_conf_threshold": 0.45,
    "vlm": True,
    "max_vlm_frames": 60,
    "depth": "standard",
    "output_dir": None,          # 若设置，最终 md 输出到该目录（可选，否则视频旁）
    "keep_intermediate": False,  # 完成后是否保留 .vid_* 中间产物（默认清理）
}

# 用户配置位置：~/.video2md/config.json （Key 只存本地）
def user_config_path():
    return Path.home() / ".video2md" / "config.json"


def load_config():
    """合并默认值与用户配置(若有)。返回 dict。"""
    cfg = json.loads(json.dumps(CONFIG_DEFAULT))  # deep copy
    p = user_config_path()
    if p.exists():
        try:
            user = json.loads(p.read_text(encoding="utf-8"))
            cfg.update(user)
            # 深合并 providers
            if "providers" in user:
                cfg["providers"] = {**cfg["providers"], **user["providers"]}
            if "failover" in user:
                cfg["failover"] = {**cfg["failover"], **user["failover"]}
            if "faster_whisper" in user:
                cfg["faster_whisper"] = {**cfg["faster_whisper"], **user["faster_whisper"]}
        except Exception as e:
            print(f"[warning] 配置读取失败({p})，使用内置默认: {e}", file=sys.stderr)
    return cfg


def get_intermediate_dir(video_path):
    """中间产物目录：与视频同名的 .vid_<basename>/，镜像在视频所在目录。"""
    p = Path(video_path)
    d = p.parent / (".vid_" + p.stem)
    d.mkdir(parents=True, exist_ok=True)
    return d


class ProgressLog:
    """带时间戳的进度日志，写进中间目录 .progress.log。"""

    def __init__(self, log_dir, name="video2md"):
        self.path = Path(log_dir) / ".progress.log"
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, msg):
        line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
        print(line, flush=True)
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(line + "\n")


def fmt_ts(seconds):
    """秒 → mm:ss 或 hh:mm:ss。"""
    s = int(round(seconds))
    h, rem = divmod(s, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def read_jsonl(path):
    if not Path(path).exists():
        return []
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return out


def write_jsonl(path, rows):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def ffmpeg_bin():
    """优先用 conda 自带 ffmpeg，否则 PATH。"""
    for cand in (Path(sys.prefix).parent / "Library" / "bin" / "ffmpeg.exe",
                 Path(sys.prefix) / "Library" / "bin" / "ffmpeg.exe"):
        if cand.exists():
            return str(cand)
    return "ffmpeg"