#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""note_ocr.py — 抖音图文帖（/note/<uid>）图片下载 + RapidOCR 逐张识别 → Markdown。

抖音图文帖没有视频轨，video2md 的下载器判定为 NO_VIDEO。本脚本补上「按图文转」：
- Playwright(Edge, headless) 打开 note 页，滚动触发懒加载；
- 采集 <img> 里 `aweme_images` 的签名直链（正文大图），同会话内立即下载
  （签名 URL 带短 x-expires，过期前必须落地）；
- RapidOCR(CPU) 逐张识别，组装成 `## 图片逐张识别` + `## 全文字合并` 的 Markdown；
- 图片落在 `<outdir>/.note_<uid>/`（原文配图保留），md 落 `<outdir>/<uid>.md`。

用法:
    python note_ocr.py <note_url|短链|id> [outdir]
退出码:
    0  成功（末尾打印成品 md 绝对路径 / OK -> ...）
    1  解析/失败
    2  无图片（NO_IMAGES）
依赖: pip install playwright（驱动已装 Edge，channel=msedge）; rapidocr_onnxruntime; ffmpeg 可选
"""
import os
import re
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

MAX_IMAGES = 15  # 最多下载识别前 N 张正文图


def resolve_id(s):
    """短链/URL → modal_id（兼容 /video/、/share/video/、/note/）。"""
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


def http_get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://www.douyin.com/"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def fetch_note(uid, img_dir):
    """打开 note 页，滚动触发懒加载，采集并下载正文图片。返回 (desc, [图片路径])。"""
    from playwright.sync_api import sync_playwright
    url = f"https://www.douyin.com/note/{uid}"
    out, desc = [], ""
    with sync_playwright() as p:
        try:
            b = p.chromium.launch(channel="msedge", headless=True,
                                  args=["--no-sandbox", "--disable-blink-features=AutomationControlled"])
        except Exception:
            b = p.chromium.launch(channel="chrome", headless=True,
                                  args=["--no-sandbox", "--disable-blink-features=AutomationControlled"])
        try:
            ctx = b.new_context(user_agent=UA, viewport={"width": 1280, "height": 2000}, locale="zh-CN")
            pg = ctx.new_page()
            pg.goto(url, wait_until="domcontentloaded", timeout=60000)
            pg.wait_for_timeout(3000)
            for _ in range(12):      # 滚动触发正文图片懒加载
                pg.mouse.wheel(0, 1500)
                pg.wait_for_timeout(700)
            pg.wait_for_timeout(2000)
            imgs = pg.evaluate(
                "() => Array.from(document.querySelectorAll('img')).map(im=>"
                "(im.currentSrc||im.src||'').slice(0,300)).filter(s=>"
                "s.indexOf('aweme_images') > -1 && s.indexOf('douyinpic.com') > -1)")
            desc = re.sub(r"[\s]*抖音$", "", pg.title() or "").strip()
            # 按完整 URL（去掉 x-expires）去重，保留 DOM 顺序
            seen, uniq = set(), []
            for s in imgs:
                k2 = re.sub(r"&x-expires=\d+", "", s)
                if k2 not in seen:
                    seen.add(k2)
                    uniq.append(s)
            for i, s in enumerate(uniq[:MAX_IMAGES], 1):
                ext = ".webp"
                mm = re.search(r"\.(webp|jpeg|jpg|png)(?:\?|$)", s, re.I)
                if mm:
                    ext = "." + mm.group(1).lower()
                pth = img_dir / f"{i:02d}{ext}"
                try:
                    data = http_get(s)
                    pth.write_bytes(data)
                    out.append(pth)
                    print(f"[img] {i}/{min(len(uniq), MAX_IMAGES)} {pth.name} {len(data)//1024}KB", flush=True)
                except Exception as e:
                    print(f"[img] FAIL {i}: {e}", flush=True)
            if len(uniq) > MAX_IMAGES:
                print(f"[note] 图超过 {MAX_IMAGES} 张，仅处理前 {MAX_IMAGES} 张", flush=True)
        finally:
            b.close()
    return desc, out


def main(argv):
    if not argv:
        print("usage: note_ocr.py <note_url|short|id> [outdir]")
        return 1
    outdir = Path(argv[1]) if len(argv) > 1 else Path(".")
    uid = resolve_id(argv[0])
    if not uid:
        print("RESOLVE_FAIL")
        return 1
    print(f"[note] uid={uid}", flush=True)

    img_dir = outdir / f".note_{uid}"
    img_dir.mkdir(parents=True, exist_ok=True)
    desc, paths = fetch_note(uid, img_dir)
    print(f"[note] desc: {desc[:60]!r} | 正文图 {len(paths)} 张", flush=True)
    if not paths:
        print("NO_IMAGES")
        return 2

    from rapidocr_onnxruntime import RapidOCR
    ocr = RapidOCR()
    blocks = []
    for i, p in enumerate(paths, 1):
        try:
            result, _ = ocr(str(p))
        except Exception as e:
            print(f"[ocr] 图{i} 崩溃: {e}", flush=True)
            result = None
        lines = [it[1] for it in result] if result else []
        print(f"[ocr] 图{i} 识别 {len(lines)} 行", flush=True)
        blocks.append((p.name, lines))

    title_md = (desc.replace("\n", " ").strip()) or f"抖音图文帖 {uid}"
    md = [f"# {title_md}", "",
          f"**来源**: https://www.douyin.com/note/{uid}　（图文帖，OCR 识别 {len(paths)} 张图片）",
          f"**原文配图**: 本笔记同目录 `.note_{uid}/`（图片原样保留）", ""]
    md.append("## 图片逐张识别")
    md.append("")
    for i, (name, lines) in enumerate(blocks, 1):
        md.append(f"### 图 {i}（{name}）")
        md.append("")
        if lines:
            md.extend(f"- {ln}" for ln in lines)
        else:
            md.append("（未识别到文字）")
        md.append("")
    md.append("## 全文字合并")
    md.append("")
    all_lines = []
    for _, lines in blocks:
        for ln in lines:
            if ln.strip() and (not all_lines or all_lines[-1] != ln.strip()):
                all_lines.append(ln.strip())
    md.append("\n".join(all_lines))
    md.append("")

    out_md = outdir / f"{uid}.md"
    out_md.write_text("\n".join(md), encoding="utf-8")
    print(f"OK -> {out_md}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))