#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""keyframes：从视频抓"代表帧"，避免逐帧分析。混合策略。

对"口播/教学/幻灯片"类内容，纯场景检测要么过稀(讲话画面相邻帧差异小，
scene 分数往往 <0.3)，要么靠间隔采样但会抓到大量雷同讲话帧。因此：
  1. 场景硬切检测：在多个阈值[0.35,0.2,0.1]里选能给出 ≥min_scene 个切点的档，
     抓"真变换点"(翻页/切镜头/进全新画面)——各档跑独立子目录避免互相覆盖；
  2. 间隔采样兜底：按 fallback_interval_s 均匀采样，保证覆盖(讲话进程也在变)；
  3. 合并 + 时间优先：切点帧优先保留，再按需补间隔帧；
  4. dHash 去重邻居近帧，收敛到真正"视觉不同"的帧；再截断到 max_keyframes。
核心收益：帧数少且都是"画面有变化"的瞬间 → OCR/VLM 调用省且质量高。

输出：<inter>/keyframes/frame_<pts_time>.jpg + <inter>/frames.jsonl [{t, path}]
"""
import argparse
import re
import subprocess
from pathlib import Path

from common import ProgressLog, ffmpeg_bin, write_jsonl, read_jsonl

SCENE_THRESH_LADDER = [0.35, 0.2, 0.1]   # 从严格到宽松逐个尝试
MIN_SCENE = 3                            # 切点数 ≥ 此数才采信该档
DEDUP_WINDOW_S = 3.0                     # 去重相邻时间窗


def _dhash(path, hash_size=8):
    """感知哈希：返回 int bit。PIL 不可用时返回 None(跳过去重)。"""
    try:
        from PIL import Image
        img = Image.open(path).convert("L").resize(
            (hash_size + 1, hash_size), Image.LANCZOS)
        px = list(img.getdata())
        hs = 0
        for row in range(hash_size):
            for col in range(hash_size):
                a = px[row * (hash_size + 1) + col]
                b = px[row * (hash_size + 1) + col + 1]
                hs = (hs << 1) | (1 if a > b else 0)
        return hs
    except Exception:
        return None


def extract_by_scene(video, run_dir, threshold, max_frames):
    """在 run_dir(独立子目录) 内跑场景检测。返回 [(t, path)]"""
    run_dir.mkdir(parents=True, exist_ok=True)
    for old in run_dir.glob("scene_*.jpg"):
        old.unlink()
    tmp = str(run_dir / "scene_%06d.jpg")
    cmd = [ffmpeg_bin(), "-i", video,
           "-vf", f"select='gt(scene,{threshold})',showinfo",
           "-vsync", "vfr", "-frames:v", str(max_frames * 2 + 8), tmp]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    times = []
    for m in re.finditer(r"pts_time:([0-9.]+)", r.stderr or ""):
        try:
            times.append(float(m.group(1)))
        except ValueError:
            pass
    frames = sorted(run_dir.glob("scene_*.jpg"))
    if not frames:
        return []
    n = min(len(frames), len(times))
    result = []
    for i in range(n):
        t = times[i] if i < len(times) else 0.0
        renamed = run_dir / f"scene_{t:09.2f}s.jpg"
        if renamed.exists():
            renamed.unlink()
        frames[i].rename(renamed)
        result.append((t, str(renamed)))
    return result


def extract_by_interval(video, out_dir, interval_s, duration, max_frames):
    """按时长均匀采样。返回 [(t, path)]"""
    out_dir.mkdir(parents=True, exist_ok=True)
    result = []
    n = min(int(duration // interval_s) + 1, max_frames)
    for idx in range(n):
        t = idx * interval_s
        out = out_dir / f"intv_{t:09.2f}s.jpg"
        subprocess.run(
            [ffmpeg_bin(), "-y", "-ss", str(t), "-i", video,
             "-frames:v", "1", "-vf", "scale='min(1280,iw)':-2", "-q:v", "2",
             str(out)],
            capture_output=True, check=True, timeout=120)
        result.append((t, str(out)))
    return result


def _hamming(h1, h2):
    return (h1 ^ h2).bit_count()


def dedupe(frames, window_s=DEDUP_WINDOW_S, max_diff_bits=5):
    """沿时间去重：与上一保留帧时间差<window 且 dHash 相近则丢弃。返回下降。"""
    if len(frames) <= 1:
        return frames
    kept = [frames[0]]
    prev_hash = _dhash(frames[0][1])
    prev_t = frames[0][0]
    for t, p in frames[1:]:
        if t - prev_t < window_s:
            h = _dhash(p)
            if h is not None and prev_hash is not None and _hamming(h, prev_hash) <= max_diff_bits:
                continue  # 相似近帧
        kept.append((t, p))
        prev_hash = _dhash(p)
        prev_t = t
    return kept


def keyframes(video, inter_dir, cfg, progress):
    out = Path(inter_dir) / "keyframes"
    meta_path = Path(inter_dir) / "frames.jsonl"
    if meta_path.exists():
        progress.log("[kf] 已有 frames.jsonl")
        return read_jsonl(meta_path)
    max_kf = cfg.get("max_keyframes", 120)
    interval = cfg.get("fallback_interval_s", 10)
    duration = cfg.get("_duration") or 0
    if duration <= 0:
        from ingest import probe_duration
        duration = probe_duration(video) or 0

    # 1) 场景硬切：多档探测第一个够密的
    scene_mode = "none"
    scene_frames = []
    cfg_thr = cfg.get("scene_threshold", SCENE_THRESH_LADDER[0])
    ladder = list(dict.fromkeys([cfg_thr] + SCENE_THRESH_LADDER))
    for idx, thr in enumerate(ladder):
        run_dir = out / f"scene_run_{idx}"
        sf = extract_by_scene(video, run_dir, thr, max_kf // 2)
        if len(sf) >= MIN_SCENE:
            scene_frames, scene_mode = sf, f"scene>{thr} x{len(sf)}"
            break
    if scene_frames:
        progress.log(f"[kf] 场景切点 {scene_mode}")

    # 2) 间隔采样兜底（保证覆盖讲话进程）
    intv_frames = extract_by_interval(video, out, interval, duration, max_kf)

    # 3) 合并：切点优先，间隔帧若时间上已接近切点则略去
    def dup_time(ts, tgt, tol=6.0):
        return any(abs(ts - t) <= tol for t in tgt)

    final = list(scene_frames)
    scene_ts = [t for t, _ in scene_frames]
    for t, p in intv_frames:
        if dup_time(t, scene_ts):
            continue
        final.append((t, p))
    final.sort(key=lambda x: x[0])

    # 4) 去重 + 截断
    final = dedupe(final)
    if len(final) > max_kf:
        # 均匀采样截断，保留稀疏且时间上均匀的机会
        step = len(final) / max_kf
        final = [final[int(i * step)] for i in range(max_kf)]
    meta = [{"t": round(t, 2), "path": p} for t, p in final]
    write_jsonl(meta_path, meta)
    progress.log(f"[kf] 关键帧 {len(meta)}（模式=scene:{scene_mode} + interval，去重后）")
    return meta


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--inter")
    a = ap.parse_args()
    from common import load_config, get_intermediate_dir
    cfg = load_config()
    inter = a.inter or get_intermediate_dir(a.video)
    plog = ProgressLog(inter)
    rows = keyframes(a.video, inter, cfg, plog)
    print(f"{len(rows)} keyframes -> {inter}/keyframes")