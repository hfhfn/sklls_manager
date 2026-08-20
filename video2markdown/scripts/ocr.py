#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""ocr：RapidOCR(CPU) 逐关键帧提取屏内文字 → 字幕/幻灯片/代码。

零显存、免费、离线。为控制成本与保证质量：
- 用 RapidOCR(rapidocr_onnxruntime.rapid_ocr.RapidOCR) 默认后处理；
- 低于 ocr_conf_threshold 的识别框丢弃；
- 长行用换行合并；输出合并为单段文本。

输出：合并进 <inter>/frames.jsonl 的每帧增加 {"ocr_text": "...", "ocr_confs": [...]}。
为了不改动 keyframes 写好的 frames.jsonl，另写 <inter>/ocr.jsonl：[{t, ocr_text}]。
"""
import argparse
import base64
from pathlib import Path

from common import ProgressLog, read_jsonl, write_jsonl


def _engine():
    try:
        from rapidocr_onnxruntime import RapidOCR
    except ImportError:
        from rapidocr import RapidOCR  # 兼容新包名
    return RapidOCR()


def run_ocr(engine, img_path, conf_thresh):
    res, _ = engine(str(img_path))
    if not res:
        return ""
    # rapidocr 每项 = [box, text, score]
    kept = [text for box, text, score in res if score >= conf_thresh and text]
    return "\n".join(kept)


def _cloud_ocr_candidates(cfg):
    """返回 [(base_url, api_key, model)]（按 cloud_model_pref 排序，只取 enabled）。"""
    ocr_cfg = cfg.get("ocr", {}) or {}
    pref = ocr_cfg.get("cloud_model_pref", [])
    provs = cfg.get("ocr_providers", {}) or {}
    cand = []
    for name, p in provs.items():
        if not p.get("enabled", False):
            continue
        m = p.get("model", "")
        if p.get("api_key") and p.get("base_url") and m:
            cand.append((p["base_url"], p["api_key"], m))
    # 按 pref 排序；未在 pref 的排在后面
    cand.sort(key=lambda c: pref.index(c[2]) if c[2] in pref else 999)
    return cand


def cloud_ocr(img_path, cfg):
    """用免费云端 VLM-OCR（DeepSeek-OCR / PaddleOCR-VL 等）提取文字。
    只用于"本地 OCR 弱"的升级帧；任一家失败自动换下一家。返回 markdown 文本。"""
    from openai import OpenAI
    b64 = base64.b64encode(Path(img_path).read_bytes()).decode()
    cand = _cloud_ocr_candidates(cfg)
    if not cand:
        raise RuntimeError("ocr.cloud_upgrade=true 但 ocr_providers 无已启用 provider")
    last = None
    for base_url, key, model in cand:
        try:
            cli = OpenAI(base_url=base_url, api_key=key, timeout=120, max_retries=0)
            r = cli.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": [
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/jpeg;base64,{b64}"}},
                    {"type": "text",
                     "text": "请完整提取图片中的全部文字，保留换行与列表/代码/表格结构，不要补充解释。"},
                ]}],
                max_tokens=1200, temperature=0.1,
            )
            txt = (r.choices[0].message.content or "").strip()
            if txt:
                return txt, model
            last = "empty"
        except Exception as e:
            last = str(e)[:120]
    raise RuntimeError(last or "cloud OCR 全部失败")


def ocr_frames(frames, inter_dir, cfg, progress):
    """frames: [{t, path}] → 返回 [{t, ocr_text}]"""
    ocr_path = Path(inter_dir) / "ocr.jsonl"
    if ocr_path.exists():
        progress.log("[ocr] 已有 ocr.jsonl，跳过")
        return read_jsonl(ocr_path)
    conf = cfg.get("ocr_conf_threshold", 0.45)
    ocr_cfg = cfg.get("ocr", {}) or {}
    cloud_upgrade = ocr_cfg.get("cloud_upgrade", False)
    min_chars = int(ocr_cfg.get("cloud_upgrade_min_ocr_chars", 0))
    progress.log("[ocr] 加载 RapidOCR(CPU) ...")
    eng = _engine()
    out = []
    N = len(frames)
    cloud_used = 0
    for i, fr in enumerate(frames, 1):
        t = fr["t"]
        text = run_ocr(eng, fr["path"], conf)
        # 合理调用：仅"本地弱帧"（几乎没字 → 复杂版式/代码/图表）才升级云端 OCR
        if cloud_upgrade and len(text.strip()) <= min_chars:
            try:
                ctext, cmodel = cloud_ocr(fr["path"], cfg)
                text = ctext + f"\n（云端OCR:{cmodel}）"
                cloud_used += 1
            except Exception as e:
                progress.log(f"[ocr][!] 帧@{t}s 云端OCR失败，用本地结果：{str(e)[:80]}")
        if text:
            out.append({"t": t, "ocr_text": text})
        if i % 20 == 0 or i == N:
            progress.log(f"[ocr] {i}/{N}")
    write_jsonl(ocr_path, out)
    extra = f"，云端升级 {cloud_used} 帧" if cloud_upgrade else ""
    progress.log(f"[ocr] 完成，{len(out)}/{N} 帧含文字{extra}")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--inter", required=True)
    a = ap.parse_args()
    from common import load_config
    cfg = load_config()
    plog = ProgressLog(a.inter)
    frames = read_jsonl(Path(a.inter) / "frames.jsonl")
    rows = ocr_frames(frames, a.inter, cfg, plog)
    for r in rows[:3]:
        print(r)