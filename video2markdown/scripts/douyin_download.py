#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""douyin_download.py — 抖音在线视频下载（浏览器 CDN 直链法，无需登录/cookies）。

yt-dlp 直连 www.douyin.com 常被 cookie 签名拦截（"Fresh cookies needed"）。本脚本改用
Playwright 驱动本机 Edge/Chrome 打开视频页，从 performance 资源里抓 douyinvod.com 的
音视频直链，再 urllib 直连下载两轨、ffmpeg 合并成本地 mp4。全程不走代理（抖音国内 CDN）。

用法:
    python douyin_download.py <url|短链|id> [outdir] [--force]

输出: <outdir>/<modal_id>.mp4（共用一个签名直链抓取，幂等：已存在则复用，除非 --force）。
退出码:
    0  成功（最后一行打印成品 mp4 的绝对路径）
    1  下载失败
    2  图文帖/无视频（NO_VIDEO，可安全跳过）
依赖: pip install playwright（驱动已装 Edge，channel=msedge，无需下载浏览器）; ffmpeg
"""
import os
import json
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

# 抖音国内 CDN 直连，绝不上代理
for _k in ("HTTPS_PROXY", "HTTP_PROXY", "ALL_PROXY",
           "https_proxy", "http_proxy", "all_proxy", "NO_PROXY", "no_proxy"):
    os.environ.pop(_k, None)

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Edg/151.0.0.0")


def resolve_id(s):
    """短链/URL → modal_id（如 v.douyin.com/xxx → 7673474900073434414）"""
    req = urllib.request.Request(s, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            final = r.geturl()
    except urllib.error.HTTPError as e:
        final = e.geturl() or s
    for pat in (r"/video/(\d+)", r"/share/video/(\d+)", r"/note/(\d+)"):
        m = re.search(pat, final)
        if m:
            return m.group(1)
    m = re.search(r"(?:^|/)(\d{15,25})(?:/|\?|$)", s)
    return m.group(1) if m else None


def grab_cdn(modal_id):
    """打开视频页抓 douyinvod 直链 + 页面标题。返回 (video_url, audio_url, title)。
    图文帖抓到不到 video 轨时返回 ('','',title)。"""
    from playwright.sync_api import sync_playwright
    url = f"https://www.douyin.com/video/{modal_id}"
    js = r"""
    () => {
      const entries = performance.getEntriesByType('resource').map(e => e.name)
          .filter(n => n.indexOf('douyinvod.com') > -1);
      const video = entries.find(n => n.indexOf('/media-video-') > -1);
      const audio = entries.find(n => n.indexOf('/media-audio-') > -1);
      const tSel = document.querySelector('h1[data-e2e="video-desc"]')
          || document.querySelector('[data-e2e="video-desc"]')
          || document.querySelector('h1')
          || document.querySelector('title');
      let t = tSel ? tSel.textContent.trim() : '';
      t = t.replace(/[\s|\-—·,#]+抖音\s*$/, '').trim();  // 去掉「… - 抖音」尾巴
      return {video: video||'', audio: audio||'', title: t||''};
    }
    """
    with sync_playwright() as p:
        try:
            b = p.chromium.launch(channel="msedge", headless=True,
                                  args=["--no-sandbox", "--disable-blink-features=AutomationControlled"])
        except Exception:
            b = p.chromium.launch(channel="chrome", headless=True,
                                  args=["--no-sandbox", "--disable-blink-features=AutomationControlled"])
        try:
            ctx = b.new_context(user_agent=UA, viewport={"width": 1280, "height": 900}, locale="zh-CN")
            pg = ctx.new_page()
            pg.goto(url, wait_until="domcontentloaded", timeout=60000)
            try:
                pg.wait_for_function(
                    "document.querySelector('video') || document.title.includes('- 抖音')",
                    timeout=30000)
            except Exception:
                pass
            pg.wait_for_timeout(5000)
            for _ in range(4):
                pg.mouse.wheel(0, 1200)
                pg.wait_for_timeout(700)
            pg.wait_for_timeout(2000)
            res = pg.evaluate(js)
            return res["video"], res["audio"], res["title"]
        finally:
            b.close()


def http_get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://www.douyin.com/"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def ffmpeg_merge(vpath, apath, out_mp4):
    cmd = ["ffmpeg", "-y"]
    if vpath.exists():
        cmd += ["-i", str(vpath)]
    if apath.exists():
        cmd += ["-i", str(apath)]
    if len(cmd) < 3:
        return None
    cmd += ["-c", "copy", "-movflags", "+faststart", str(out_mp4)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode == 0 and out_mp4.exists():
        return out_mp4
    # 退化：视频轨可直接当成品
    if vpath.exists() and vpath.stat().st_size:
        shutil.copy2(vpath, out_mp4)
        return out_mp4
    return None


def main(argv):
    if not argv:
        print("usage: douyin_download.py <url|短链|id> [outdir] [--force]")
        return 1
    s = argv[0]
    force = "--force" in argv
    outdir = Path(argv[1]) if len(argv) > 1 and not argv[1].startswith("--") else Path(".")
    outdir.mkdir(parents=True, exist_ok=True)

    uid = resolve_id(s)
    if not uid:
        print("RESOLVE_FAIL")
        return 1
    out = outdir / f"{uid}.mp4"
    if out.exists() and not force:
        print(out.resolve())
        return 0

    v, a, title = grab_cdn(uid)
    if not v and not a:
        print(f"NO_VIDEO {uid}")  # 图文帖，无视频轨
        return 2

    tmp = outdir / ".douyin_tmp"
    tmp.mkdir(parents=True, exist_ok=True)
    vp = tmp / "v.mp4"
    ap = tmp / "a.m4a"
    try:
        if v:
            vp.write_bytes(http_get(v))
        if a:
            ap.write_bytes(http_get(a))
        out = ffmpeg_merge(vp, ap, out)
    finally:
        for p in (vp, ap):
            if p.exists():
                p.unlink()
        try:
            tmp.rmdir()
        except Exception:
            pass

    if not out:
        print("DOWNLOAD_FAIL")
        return 1
    # 写标题旁车 (.meta.json)，供 video2md.py 注入真实标题（避免 md 用数字 ID 当标题）
    try:
        (out.with_suffix(".meta.json")).write_text(
            json.dumps({"uid": uid, "title": title, "source": s},
                       ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass
    print(out.resolve())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))