#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""ingest：把输入归一化成一份本地 mp4 —— 本地文件校验 / 在线 URL 用 yt-dlp 下载。

在线下载走 yt-dlp；外网(非内网)请求失败时自动叠加本机代理 127.0.0.1:7890。
返回规整后的本地 mp4 路径 + 元信息(title/duration/source)。
"""
import argparse
import ipaddress
import shutil
import subprocess
import sys
import urllib.parse
import uuid
from pathlib import Path

from common import ffmpeg_bin

PROXY = "http://127.0.0.1:7890"
PROXY_HOST = "127.0.0.1"
PROXY_PORT = 7890

LOCAL_EXT = {".mp4", ".mkv", ".webm", ".mov", ".avi", ".flv", ".ts", ".m4v", ".wmv"}
ONLINE_HINTS = ("://", "v.douyin.com", "b23.tv", "bilibili.com", "youtube.com",
                "youtu.be", "xiaohongshu.com", "weibo.com", "kuaishou.com", "t.co")


def is_url(s):
    return ("://" in s) or s.startswith("www.")

def is_internal_host(host):
    """内网 host -> True（直连，不走代理）。"""
    if host in ("localhost",) or host.endswith((".local", ".lan", ".internal", ".corp")):
        return True
    # 去掉端口
    host = host.split(":")[0].strip("[]")
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        return False


def probe_duration(video_path):
    """ffprobe 取时长(秒)。"""
    try:
        r = subprocess.run(
            [ffmpeg_bin().replace("ffmpeg", "ffprobe"), "-v", "error", "-show_entries",
             "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", video_path],
            capture_output=True, text=True, timeout=120,
        )
        return float(r.stdout.strip())
    except Exception:
        return None


def ingest_local(src, dst_mp4):
    src = Path(src)
    if not src.exists():
        raise FileNotFoundError(f"本地文件不存在: {src}")
    if src.suffix.lower() not in LOCAL_EXT:
        raise ValueError(f"不支持的视频格式: {src.suffix} (仅 {sorted(LOCAL_EXT)})")
    if src.suffix.lower() == ".mp4":
        # 同盘直接复用；否则复制
        if src.resolve().parent == dst_mp4.resolve().parent:
            return str(src)
    dst_mp4.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst_mp4)
    return str(dst_mp4)


def _ytdlp_proxy_args(url):
    """判断是否需走代理。YouTube 等外网在直连失败后自动叠加代理。"""
    host = urllib.parse.urlparse(url).hostname or ""
    if is_internal_host(host):
        return []  # 内网直连
    return ["--proxy", PROXY]  # 外网统一走本地代理（被墙环境）

def download_online(url, out_dir):
    """yt-dlp 下载为 mp4，返回完整路径。"""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    outtmpl = str(out_dir / "%(title).80s.%(ext)s")
    # 先试直连(其内默认走系统代理)，失败再显式指代理人
    base = [sys.executable, "-m", "yt_dlp",
            "-f", "bv*+ba/b",                # 优先最佳画质+音轨
            "-S", "res:1080,ext:mp4:m4a",    # 1080 内、优先 mp4
            "--no-playlist", "-o", outtmpl,
            "--no-warnings", "--no-mtime"]
    last_err = None
    for proxy_args in ([], ["--proxy", PROXY]):  # 直连优先(国内站快), 外网失败再走代理
        cmd = base + proxy_args + [url]
        try:
            subprocess.run(cmd, check=True, capture_output=True, timeout=900)
            # 找到产物
            files = [f for f in out_dir.iterdir() if f.is_file() and f.suffix.lower() in LOCAL_EXT]
            if files:
                return sorted(files, key=lambda p: p.stat().st_mtime)[-1]
        except subprocess.CalledProcessError as e:
            last_err = e.stderr[-400:] if e.stderr else str(e)
    raise RuntimeError(f"下载失败: {last_err}")


def to_unique_mp4(dst_dir, stem=None):
    dst_dir = Path(dst_dir)
    dst_dir.mkdir(parents=True, exist_ok=True)
    name = stem or f"video_{uuid.uuid4().hex[:8]}"
    safe = "".join(c for c in name if c.isalnum() or c in " _-()[]").strip() or "video"
    return dst_dir / f"{safe}.mp4"


def ingest(input_, work_dir, progress=None):
    """输入(路径或URL) → (本地mp4绝对路径, meta)"""
    work_dir = Path(work_dir)
    vids = work_dir / "video"
    vids.mkdir(parents=True, exist_ok=True)
    s = input_.strip()

    if is_url(s):
        if progress:
            progress.log(f"[ingest] 在线下载: {s[:60]}")
        mp4 = download_online(s, vids)
        duration = probe_duration(mp4)
        return str(mp4), {"source": s, "title": Path(mp4).stem, "duration": duration}
    else:
        if progress:
            progress.log(f"[ingest] 本地文件: {s}")
        dst = to_unique_mp4(vids, stem=Path(s).stem)
        mp4 = ingest_local(s, dst)
        duration = probe_duration(mp4)
        return mp4, {"source": s, "title": Path(s).stem, "duration": duration}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--work", default=".")
    a = ap.parse_args()
    mp4, meta = ingest(a.input, a.work)
    print(mp4)
    print(meta)