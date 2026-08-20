#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""video2md：视频 → 带画面的 Markdown 编排器（一键串联全流程）。

用法：
  python video2md.py <本地视频路径> [--depth standard|light|deep] [--engine sensevoice|faster-whisper] [--vlm on|off] [--out xxx.md]
  python video2md.py <在线URL/分享口令>

中间产物放在 <视频目录>/.vid_<名称>/；断点续传：已有产物自动跳过。
"""
import argparse
import json
import sys
from pathlib import Path

from common import (ProgressLog, load_config, get_intermediate_dir,
                    user_config_path)
from ingest import ingest, probe_duration
from transcribe import transcribe
from keyframes import keyframes
from ocr import ocr_frames
from describe import describe_frames
from assemble import assemble


def main():
    ap = argparse.ArgumentParser(description="视频 → 带画面的 Markdown")
    ap.add_argument("input", help="本地视频路径 或 在线分享链接/URL")
    ap.add_argument("--depth", choices=["light", "standard", "deep"], default=None,
                    help="笔记深度（默认取配置 standard）")
    ap.add_argument("--engine", choices=["sensevoice", "faster-whisper",
                                         "cloud-sensevoice", "cloud-tele"],
                    default=None, help="ASR引擎：本地 sensevoice(默认)/faster-whisper；云端 cloud-sensevoice/cloud-tele")
    ap.add_argument("--vlm", choices=["on", "off"], default=None,
                    help="是否启用云端画面语义（默认 on）")
    ap.add_argument("--max-vlm-frames", type=int, default=None)
    ap.add_argument("--out", default=None, help="输出 md 路径（默认在视频旁）")
    ap.add_argument("--work", default=None, help="工作目录（在线下载视频落地处）")
    a = ap.parse_args()

    cfg = load_config()
    if a.depth: cfg["depth"] = a.depth
    if a.engine: cfg["engine"] = a.engine
    if a.vlm: cfg["vlm"] = a.vlm == "on"
    if a.max_vlm_frames: cfg["max_vlm_frames"] = a.max_vlm_frames

    if not user_config_path().exists():
        print("[提示] 未发现 ~/.video2md/config.json，画面语义(描述)将不可用。"
              "复制 config.example.yaml 改名并填入免费视觉模型 api_key 即可启用。")

    # --- ingest ---
    work_dir = a.work or "."
    mp4, meta = ingest(a.input, work_dir, progress=None)
    inter = get_intermediate_dir(mp4)
    plog = ProgressLog(inter)
    # 记 meta
    meta["duration"] = meta.get("duration") or probe_duration(mp4) or 0
    (Path(inter) / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    cfg["_duration"] = meta["duration"]
    plog.log(f"[total] 视频: {mp4} | 时长: {meta['duration']:.0f}s")

    # --- 各阶段（断点续传：各模块已检查已有产物） ---
    segs = transcribe(mp4, str(inter), cfg, plog)
    frames = keyframes(mp4, str(inter), cfg, plog)
    ocr_rows = ocr_frames(frames, str(inter), cfg, plog)
    if cfg.get("vlm", True):
        try:
            describe_frames(frames, ocr_rows, str(inter), cfg, plog)
        except Exception as e:
            plog.log(f"[vlm][!] 画面语义阶段失败（降级：仅保留 OCR）：{e}")
    out = assemble(str(inter), cfg, plog, a.out)
    # --- LLM 精修：把 OCR/ASR 原始材料送 agnes 等整合优化 → 最终 MD（失败回退原始组装） ---
    if cfg.get("refine", {}).get("enabled", True):
        try:
            from refine import refine as refine_md
            refined = refine_md(str(inter), cfg, plog)
            Path(out).write_text(refined, encoding="utf-8")
            plog.log(f"[total] 精修完成 → {out}")
        except Exception as e:
            plog.log(f"[refine][!] 整理失败，保留原始组装结果：{e}")
    plog.log(f"[total] 完成 → {out}")
    print(f"\nMarkdown: {out}")
    print(f"  Intermediate files (can delete): {inter}")


if __name__ == "__main__":
    main()