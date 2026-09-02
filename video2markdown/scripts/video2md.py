#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""video2md：视频 → 带画面的 Markdown 编排器（一键串联全流程）。

用法：
  python video2md.py <本地视频路径 | 在线分享链接/URL> [--depth standard|light|deep]
                     [--engine sensevoice|faster-whisper|cloud-sensevoice|cloud-tele]
                     [--vlm on|off] [--max-vlm-frames N] [--out xxx.md]
                     [--outdir DIR] [--work DIR] [--keep-intermediate]
  python video2md.py --urls-file 清单.txt [同上的可选参数]     # 批量（串行，逐条一条命令跑到底）

抖音短链/URL：若 yt-dlp 被 cookie 签名拦截（“Fresh cookies needed”），会自动兜底调用
scripts/douyin_download.py 走浏览器 CDN 直链下载（需 pip install playwright，驱动本机 Edge/Chrome）。
图文帖（无视频轨）在批量模式下计为 NO_VIDEO 并跳过；单条模式下会报错并退出。

中间产物放在 <视频目录>/.vid_<名称>/；默认完成后自动清理（--keep-intermediate 保留）。
输出默认在视频旁；可用 --outdir 或配置 output_dir 指定目录。
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

# 兼容性自保：若被外部环境（如 Hermes 桌面 app）的 PYTHONPATH 污染，
# 会误加载别的 site-packages 里的 numpy 等导致 import 失败。此处移除外部
# 非本环境 site-packages 的路径注入，保证只用自己的依赖。
for _k in ("PYTHONPATH", "PYTHONHOME"):
    os.environ.pop(_k, None)

from common import (ProgressLog, load_config, get_intermediate_dir,
                    user_config_path)
from ingest import ingest, probe_duration
from transcribe import transcribe
from keyframes import keyframes
from ocr import ocr_frames
from describe import describe_frames
from assemble import assemble
from refine import refine as refine_md


def _cleanup_intermediate(inter, keep, plog):
    """完成后清理中间产物目录（默认开启；--keep-intermediate 保留）。
    仅清理 .vid_* 这样明确的中间目录，绝不碰用户输入的视频/输出 md。"""
    if keep:
        plog.log(f"[cleanup] 跳过（--keep-intermediate）: {inter}")
        return
    try:
        if Path(inter).exists():
            shutil.rmtree(inter)
            plog.log(f"[cleanup] 已清理中间产物: {inter}")
    except Exception as e:
        plog.log(f"[cleanup][!] 清理失败（保留）: {e}")


def _is_douyin(s):
    return ("v.douyin.com" in s) or ("iesdouyin" in s)


def _douyin_fallback(input_, work_dir, plog):
    """yt-dlp 被抖音拦截时，用浏览器 CDN 直链下载。返回本地 mp4 绝对路径；
    图文帖（无视频轨）返回 None（调用方计入 NO_VIDEO 跳过）。"""
    dl = str(Path(__file__).resolve().parent / "douyin_download.py")
    py = sys.executable
    env = dict(os.environ)
    for k in ("PYTHONPATH", "PYTHONHOME", "VIRTUAL_ENV"):
        env.pop(k, None)
    # 用独立子进程跑下载器：避免把 Playwright 塞进 video2md 已加载 torch/funasr 的环境
    r = subprocess.run([py, dl, input_, str(work_dir)], env=env,
                       capture_output=True, text=True)
    if r.returncode == 2:
        if plog:
            plog.log("图文帖无视频，跳过（NO_VIDEO）")
        return None, ""
    if r.returncode != 0:
        tail = (r.stdout or r.stderr or "").strip()[-200:]
        if plog:
            plog.log(f"[ingest][!] 抖音 CDN 直链下载失败(rc={r.returncode}): {tail}")
        raise RuntimeError(f"抖音 CDN 下载失败: {tail}")
    mp4 = r.stdout.strip().splitlines()[-1]  # 成品 mp4 绝对路径
    # 读取下载器写的标题旁车 (.meta.json)，拿真实视频标题（否则 md 会用数字 ID 当标题）
    title = ""
    try:
        mj = Path(mp4).with_suffix(".meta.json")
        if mj.exists():
            title = json.loads(mj.read_text(encoding="utf-8")).get("title") or ""
    except Exception:
        title = ""
    return mp4, title


def ingest_with_fallback(input_, work_dir, plog):
    """ingest，但在抖音链接被 yt-dlp cookie 拦截时自动落到 CDN 直链。
    返回 (mp4, meta)；图文帖返回 (None, None)。"""
    try:
        return ingest(input_, work_dir, progress=plog)
    except RuntimeError as e:
        if not _is_douyin(input_):
            raise
        if plog:
            plog.log(f"[ingest] 抖音 yt-dlp 失败({str(e)[-80:]})，走浏览器 CDN 直链兜底")
        mp4, dtitle = _douyin_fallback(input_, work_dir, plog)
        if mp4 is None:
            return None, None
        mp4, meta = ingest(mp4, work_dir, progress=plog)
        if dtitle:
            meta["title"] = dtitle  # 注入真实标题，assemble/refine 就不再拿数字 ID 当标题
        return mp4, meta


def process_input(input_, work_dir, outdir, cfg, keep, skip_existing_md=True):
    """跑通“下载→转录→组装→精修→清理”，返回状态字符串 ok / fail / no_video。"""
    work_dir = Path(work_dir)
    outdir = Path(outdir) if outdir else None
    try:
        res = ingest_with_fallback(input_, work_dir, None)
    except RuntimeError as e:
        print(f"  !! 下载失败: {str(e)[-140:]}", flush=True)
        return "fail"
    if res[0] is None:
        print("  !! 图文帖/无视频", flush=True)
        return "no_video"
    mp4, meta = res
    inter = get_intermediate_dir(mp4)
    plog = ProgressLog(inter)
    meta["duration"] = meta.get("duration") or probe_duration(mp4) or 0
    (Path(inter) / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    cfg["_duration"] = meta["duration"]
    plog.log(f"[total] 视频: {mp4} | 时长: {meta['duration']:.0f}s")

    # --- 输出目录解析：命令行 --outdir > 配置 output_dir；两者都不设 → 视频同目录 ---
    od = outdir or (Path(cfg.get("output_dir")) if cfg.get("output_dir") else Path(mp4).parent)
    od.mkdir(parents=True, exist_ok=True)
    out = str(od / f"{Path(mp4).stem}.md")

    # 批量幂等：同理 mp4 已存在、md 已生成 → 跳过转录
    if skip_existing_md and Path(out).exists():
        plog.log(f"[batch] md 已存在，跳过转录: {out}")
        _cleanup_intermediate(inter, keep, plog)
        return "ok"

    segs = transcribe(mp4, str(inter), cfg, plog)
    frames = keyframes(mp4, str(inter), cfg, plog)
    ocr_rows = ocr_frames(frames, str(inter), cfg, plog)
    if cfg.get("vlm", True):
        try:
            describe_frames(frames, ocr_rows, str(inter), cfg, plog)
        except Exception as e:
            plog.log(f"[vlm][!] 画面语义阶段失败（降级：仅保留 OCR）：{e}")
    out = assemble(str(inter), cfg, plog, out)
    # --- LLM 精修：把 OCR/ASR 原始材料送 agnes 等整合优化 → 最终 MD（失败回退原始组装） ---
    if cfg.get("refine", {}).get("enabled", True):
        try:
            refined = refine_md(str(inter), cfg, plog)
            Path(out).write_text(refined, encoding="utf-8")
            plog.log(f"[total] 精修完成 → {out}")
        except Exception as e:
            plog.log(f"[refine][!] 整理失败，保留原始组装结果：{e}")
    plog.log(f"[total] 完成 → {out}")
    print(f"\nMarkdown: {out}", flush=True)
    _cleanup_intermediate(inter, keep, plog)
    return "ok"


def main():
    ap = argparse.ArgumentParser(description="视频 → 带画面的 Markdown")
    ap.add_argument("input", nargs="?", help="本地视频路径 或 在线分享链接/URL")
    ap.add_argument("--urls-file", default=None,
                    help="批量清单文件：每行一个 本地路径/链接（串行，跳过已产出 md 的，末尾汇总 OK/FAIL/NO_VIDEO）")
    ap.add_argument("--depth", choices=["light", "standard", "deep"], default=None,
                    help="笔记深度（默认取配置 standard）")
    ap.add_argument("--engine", choices=["sensevoice", "faster-whisper",
                                         "cloud-sensevoice", "cloud-tele"],
                    default=None, help="ASR引擎：本地 sensevoice(默认)/faster-whisper；云端 cloud-sensevoice/cloud-tele")
    ap.add_argument("--vlm", choices=["on", "off"], default=None,
                    help="是否启用云端画面语义（默认 on）")
    ap.add_argument("--max-vlm-frames", type=int, default=None)
    ap.add_argument("--out", default=None, help="输出 md 路径（默认在输出目录，名为视频标题.md；批量模式无效）")
    ap.add_argument("--outdir", default=None, help="输出 md 目录（覆盖配置 output_dir；默认视频旁）")
    ap.add_argument("--work", default=None, help="工作目录（在线下载视频落地处）")
    ap.add_argument("--keep-intermediate", action="store_true",
                    help="完成后保留 .vid_* 中间产物（默认清理）")
    a = ap.parse_args()

    if not a.input and not a.urls_file:
        ap.error("必须给出 input，或 --urls-file 批量清单")

    cfg = load_config()
    if a.depth: cfg["depth"] = a.depth
    if a.engine: cfg["engine"] = a.engine
    if a.vlm: cfg["vlm"] = a.vlm == "on"
    if a.max_vlm_frames: cfg["max_vlm_frames"] = a.max_vlm_frames
    keep = a.keep_intermediate or cfg.get("keep_intermediate", False)

    if not user_config_path().exists():
        print("[提示] 未发现 ~/.video2md/config.json，画面语义(描述)将不可用。"
              "复制 config.example.yaml 改名并填入免费视觉模型 api_key 即可启用。")

    work_dir = a.work or "."
    outdir = a.outdir or cfg.get("output_dir")

    if a.urls_file:
        lines = [l.strip() for l in Path(a.urls_file).read_text(encoding="utf-8").splitlines()
                 if l.strip() and not l.lstrip().startswith("#")]
        total = len(lines)
        res = {"ok": 0, "fail": 0, "no_video": 0}
        print(f"==== 批量开始，共 {total} 条 ====", flush=True)
        for i, u in enumerate(lines, 1):
            print(f"\n==== [{i}/{total}] {u} ====", flush=True)
            st = process_input(u, work_dir, outdir, cfg, keep)
            res[st] += 1
            print(f"[{i}] {st.upper()}", flush=True)
        print(f"\n===== 批量结束: OK={res['ok']} FAIL={res['fail']} NO_VIDEO={res['no_video']} =====")
    else:
        st = process_input(a.input, work_dir, outdir, cfg, keep, skip_existing_md=False)
        if st != "ok":
            sys.exit(1 if st == "fail" else 0)


if __name__ == "__main__":
    main()