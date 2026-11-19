#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""douyin_download.py — 抖音在线视频下载（浏览器 CDN 直链法，无需登录/cookies）。

yt-dlp 直连 www.douyin.com 常被 cookie 签名拦截（"Fresh cookies needed"）。本脚本改用
Playwright 驱动本机 Edge/Chrome 打开视频页，从 performance 资源里抓 douyinvod.com 的
音视频直链，再 urllib 直连下载两轨、ffmpeg 合并成本地 mp4。全程不走代理（抖音国内 CDN）。

用法:
    python douyin_download.py <url|短链|id> [outdir] [--force]

输出: <outdir>/<modal_id>.mp4（共用一个签名直链抓取，幂等：已存在且音视频齐全则复用，除非 --force）。
退出码:
    0  成功（最后一行打印成品 mp4 的绝对路径）
    1  下载失败 / 无法判定（UNKNOWN，可能是登录墙或临时故障）
    2  确认是图文帖（NO_VIDEO <uid>，可安全转 note_ocr）
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

from common import harden_stdio

# 抖音国内 CDN 直连，绝不上代理
for _k in ("HTTPS_PROXY", "HTTP_PROXY", "ALL_PROXY",
           "https_proxy", "http_proxy", "all_proxy", "NO_PROXY", "no_proxy"):
    os.environ.pop(_k, None)

# GBK 控制台下 print 路径/标题时遇到编不出的字符会抛异常，整条下载中断
harden_stdio()
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Edg/151.0.0.0")

# 兜底：performance 资源里抓不到 douyinvod（页面被登录墙挡住、player 没真正拉流）时，
# 改用进程内在页面同源 fetch aweme/detail API 拿真实 play_addr / video_id 与标题。
# 同源 fetch 会带上当前浏览器上下文的 cookies/signature，绕开 yt-dlp 那个"fresh cookies"签名校验。
# 返回 {video, audio, title, no_video, ok}：ok=False 表示请求失败、无法判定（≠ 图文帖）。
API_JS = r"""
async () => {
  const uid = '__AWEME__';
  const u = 'https://www.douyin.com/aweme/v1/web/aweme/detail/'
      + '?device_platform=webapp&aid=6383&channel=channel_pc_web'
      + '&aweme_id=' + uid + '&request_source=6';
  try {
    const r = await fetch(u, {headers: {'referer': 'https://www.douyin.com/'}});
    const j = await r.json();
    const d = j.aweme_detail || j || {};
    const images = (d.images && d.images.length) || (d.image_post_info ? 1 : 0);
    let video = '';
    const v = d.video || {};
    const play = (v.play_addr && v.play_addr.url_list) || [];
    const bits = (v.bit_rate || []).filter(b => b && b.play_addr);
    const bk = bits.length ? (bits[0].play_addr.url_list || []) : [];
    video = play[0] || bk[0] || '';
    const vid = v.vid || v.video_id || v.uri || '';
    if (!video && vid) {
      video = 'https://www.douyin.com/aweme/v1/play/?video_id=' + vid;
    }
    // ok 只在真的拿到字段时才算成功；aweme_detail 为空 = 没查到，不能据此判图文帖
    const ok = !!(d.aweme_id || d.desc || d.video || d.images || d.image_post_info);
    return {video: video, audio: '', title: (d.desc || '').trim(),
            no_video: images > 0, ok: ok};
  } catch (e) {
    return {video: '', audio: '', title: '', no_video: false, ok: false};
  }
}
"""


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
    """打开视频页抓 douyinvod 直链 + 页面标题。

    返回 (video_url, audio_url, title, status)，status 三态：
      'video'   确认是视频（audio 可能为空：单轨视频或没抓到音频轨）
      'note'    确认是图文帖（API 的 images 字段非空）
      'unknown' 既没抓到轨、API 也没给出结论 —— **不是**图文帖，调用方必须按失败处理
    """
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
            v = res["video"]
            a = res["audio"]
            title = res["title"]

            # 音频轨缺失（或两轨都没抓到）时走 API：play_addr 是「视频+人声已混轨」的 mp4，
            # 拿它当单一来源比「只有视频轨的无声 mp4」可靠。
            if not a:
                try:
                    api = pg.evaluate(API_JS.replace("__AWEME__", modal_id))
                    if api.get("no_video"):
                        return "", "", api.get("title") or title, "note"
                    if api.get("video"):
                        # API 的 play_addr 已含音轨，直接当整片来源，audio 留空
                        return api["video"], "", api.get("title") or title, "video"
                    if not api.get("ok"):
                        # 请求失败/字段为空：没查到 ≠ 图文帖
                        return "", "", title, "unknown" if not v else "video"
                except Exception:
                    pass

            if v:
                return v, a, title, "video"
            return "", "", title, "unknown"
        finally:
            b.close()


def http_get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://www.douyin.com/"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def _has_audio(path):
    """ffprobe 判断 mp4 是否含音频流。ffprobe 缺失/出错时返回 None（未知）。"""
    try:
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "a",
             "-show_entries", "stream=codec_type", "-of", "csv=p=0", str(path)],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
        if r.returncode != 0:
            return None
        return bool((r.stdout or "").strip())
    except Exception:
        return None


def ffmpeg_merge(vpath, apath, out_mp4):
    """合并两轨。返回 (out_mp4 或 None, has_audio)。"""
    cmd = ["ffmpeg", "-y"]
    if vpath.exists():
        cmd += ["-i", str(vpath)]
    if apath.exists():
        cmd += ["-i", str(apath)]
    if len(cmd) < 3:
        return None, False
    cmd += ["-c", "copy", "-movflags", "+faststart", str(out_mp4)]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    if r.returncode == 0 and out_mp4.exists():
        return out_mp4, apath.exists() or bool(_has_audio(out_mp4))
    # 退化：视频轨可直接当成品（但很可能没有音轨，交给调用方告警）
    if vpath.exists() and vpath.stat().st_size:
        shutil.copy2(vpath, out_mp4)
        return out_mp4, bool(_has_audio(out_mp4))
    return None, False


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
        # 复用前先验一下音轨：历史上曾产出过无声 mp4，直接复用会让 ASR 在深处报错
        if _has_audio(out) is not False:
            print(out.resolve())
            return 0
        print(f"[warn] 已有 mp4 无音频轨，重新下载: {out}", file=sys.stderr)

    # unknown 多为登录墙/临时故障，重试一次再放弃（不要一次就判死）
    v = a = title = ""
    status = "unknown"
    for attempt in (1, 2):
        v, a, title, status = grab_cdn(uid)
        if status != "unknown":
            break
        if attempt == 1:
            print("[retry] 未抓到视频轨且 API 无结论，重试一次 ...", file=sys.stderr)

    if status == "note":
        print(f"NO_VIDEO {uid}")  # 确认是图文帖，无视频轨
        return 2
    if status == "unknown" or (not v and not a):
        # 关键：这里**不能**报 NO_VIDEO —— 没查到不等于图文帖，否则下游会拿真视频去抓图并失败
        print(f"UNKNOWN {uid}")
        return 1

    tmp = outdir / ".douyin_tmp"
    tmp.mkdir(parents=True, exist_ok=True)
    vp = tmp / "v.mp4"
    ap = tmp / "a.m4a"
    has_audio = False
    try:
        if v:
            vp.write_bytes(http_get(v))
        if a:
            ap.write_bytes(http_get(a))
        out, has_audio = ffmpeg_merge(vp, ap, out)
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
    if not has_audio:
        print(f"[warn] 成品无音频轨（ASR 会失败）：{out}", file=sys.stderr)
    # 写标题旁车 (.meta.json)，供 video2md.py 注入真实标题（避免 md 用数字 ID 当标题）
    try:
        (out.with_suffix(".meta.json")).write_text(
            json.dumps({"uid": uid, "title": title, "source": s,
                        "has_audio": has_audio},
                       ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass
    print(out.resolve())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
