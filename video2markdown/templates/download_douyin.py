#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""download_douyin.py — 供无命令行 agent（DSH/浏览器沙箱）落盘到用户工作区的一键下载脚本。

用途：在无法执行命令的 agent 会话里，把 yt-dlp 下载抖音/B站/YouTube 视频到本地 mp4，
再交给 video2md.py 转录。agent 只需把它写进用户工作区；用户在本机双击配套的
run_transcribe.bat（或直接 `python download_douyin.py <URL> <outdir> [cookies.txt]`）即可。

用法：
    python download_douyin.py <URL> <OUT_DIR> [COOKIES_FILE]
    URL       视频链接（抖音 v.douyin.com / 单条 / B站 / YouTube 均可）
    OUT_DIR   视频落地目录（建议工作区下的 video/）
    COOKIES   可选 cookies.txt（由浏览器扩展导出；抖音/B站能显著提高成功率）

策略（按优先级降序）：
    1) cookies.txt 明文文件（若存在于参数路径）——最可靠
    2) 各浏览器 cookiefrombrowser（firefox/chrome/edge/brave/opera）
    3) 无 cookie 直连
   任一路径成功即返回 0，最后一行打印产物绝对路径。
编码：全 ASCII + CRLF，避免 cmd 按 GBK 解析乱码；无中文输出。

注意：Windows 上 Chrome/Edge 的 cookie 用 DPAPI 加密，cookiefrombrowser 常常读不到
有效值（yt-dlp 报 "Fresh cookies needed"）。优先让用户提供 cookies.txt。
"""
import sys
import glob
import pathlib


def main():
    if len(sys.argv) < 2:
        print("usage: download_douyin.py URL OUT_DIR [COOKIES_FILE]")
        return 2
    url = sys.argv[1]
    out_dir = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "video")
    cookies_file = sys.argv[3] if len(sys.argv) > 3 else None
    out_dir.mkdir(parents=True, exist_ok=True)
    # 清空旧的半成品，避免误判下载成功
    for f in out_dir.iterdir():
        if f.is_file():
            f.unlink()

    try:
        import yt_dlp  # noqa
    except ImportError:
        print("YTDLP_MISSING: run: pip install -U yt-dlp")
        return 2

    base = {
        "format": "bv*+ba/b",
        "merge_output_format": "mp4",
        "outtmpl": str(out_dir / "%(id)s.%(ext)s"),
        "noplaylist": True,
        "no_warnings": True,
        "quiet": True,
    }

    last = None
    # 候选序列：cookie 文件优先，其次各浏览器，最后无 cookie
    planned = [("no-cookie", dict(base))]
    if cookies_file and pathlib.Path(cookies_file).exists():
        planned.insert(0, ("cookie-file", {**base, "cookiefile": cookies_file}))
    for b in ["firefox", "chrome", "edge", "brave", "opera"]:
        planned.append(("browser:" + b, {**base, "cookiefrombrowser": (b,)}))

    for label, opts in planned:
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
            got = glob.glob(str(out_dir / "*"))
            if got:
                print("OK_SOURCE " + label)
                print(got[0])
                return 0
        except Exception as e:  # noqa: BLE001
            last = e

    print("DOWNLOAD_FAILED: " + repr(last))
    return 1


if __name__ == "__main__":
    sys.exit(main())