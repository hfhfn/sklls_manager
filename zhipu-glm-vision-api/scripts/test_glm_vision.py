#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Zhipu GLM vision model benchmark harness.

Generates a synthetic test image (Chinese OCR + colored shapes + digit sequence),
then runs each candidate model through (1) a general parse prompt and (2) a pure OCR
prompt, reporting HTTP status / latency / token usage and surfacing 429s.

Usage:
    CUSTOM_GLM_API_KEY=<key> python test_glm_vision.py
    # or set the key in your shell/env before running.

Edit MODELS below to the set you want to test. Requires a working PIL/Pillow.
"""
import os, base64, json, time, urllib.request, urllib.error
from io import BytesIO

API_KEY = os.environ.get("CUSTOM_GLM_API_KEY", "")
BASE = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

MODELS = [
    "GLM-4.1V-Thinking-Flash",
    "GLM-4V-Flash",
    "GLM-4.6V-Flash",
    # "GLM-4.5V-Flash",  # does NOT exist (400 code 1214)
    # "GLM-5V-Turbo",    # paid, often 429 "余额不足" if unsubscribed
]


def make_synthetic_image():
    """Build a test image: Chinese header, colored shapes, digit sequence."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        raise SystemExit("PIL/Pillow required: pip install pillow")
    W, H = 900, 620
    img = Image.new("RGB", (W, H), (240, 244, 248))
    d = ImageDraw.Draw(img)
    font = None
    for f in ["C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/simhei.ttf",
              "C:/Windows/Fonts/arial.ttf"]:
        try:
            font = ImageFont.truetype(f, 44)
            break
        except Exception:
            continue
    d.rounded_rectangle([30, 30, W - 30, H - 30], radius=18, fill="white",
                        outline=(200, 205, 210), width=3)
    if font:
        d.text((60, 60), "智谱视觉模型测试", fill=(20, 20, 20), font=font)
    d.rectangle([70, 180, 270, 360], fill=(230, 60, 60))
    d.ellipse([330, 180, 530, 360], fill=(60, 180, 90))
    d.polygon([(600, 360), (700, 180), (800, 360)], fill=(70, 110, 230))
    if font:
        d.text((70, 410), "红色方形  绿色圆形  蓝色三角形", fill=(20, 20, 20), font=font)
        d.text((70, 490), "数字序列: 1 2 3 4 5 6 7 8 9", fill=(60, 60, 60), font=font)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()


def call(model, image_b64, prompt, timeout=90):
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": [
            {"type": "image_url",
             "image_url": {"url": f"data:image/png;base64,{image_b64}"}},
            {"type": "text", "text": prompt},
        ]}],
        "stream": False,
    }
    req = urllib.request.Request(
        BASE, data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {API_KEY}",
                 "Content-Type": "application/json"},
        method="POST",
    )
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            b = json.loads(resp.read().decode())
            dt = time.time() - t0
            msg = b.get("choices", [{}])[0].get("message", {})
            usage = b.get("usage", {})
            return {"status": resp.status, "time": round(dt, 2),
                    "content": msg.get("content", ""),
                    "prompt_tokens": usage.get("prompt_tokens"),
                    "completion_tokens": usage.get("completion_tokens"),
                    "total_tokens": usage.get("total_tokens")}
    except urllib.error.HTTPError as e:
        dt = time.time() - t0
        detail = ""
        try:
            detail = e.read().decode()
        except Exception:
            pass
        return {"status": e.code, "time": round(dt, 2), "error": detail[:500]}
    except Exception as e:
        return {"status": "EXC", "time": round(time.time() - t0, 2),
                "error": str(e)[:500]}


def main():
    if not API_KEY:
        raise SystemExit("Set CUSTOM_GLM_API_KEY env var first.")
    syn = make_synthetic_image()
    results = {}
    for m in MODELS:
        print(f"\n{'=' * 60}\n模型: {m}\n{'=' * 60}")
        line = {}
        r1 = call(m, syn, "请描述这张图片。图中有什么文字、形状、颜色？逐个列出。")
        line["synthetic_parse"] = r1
        print(f"[合成图] status={r1.get('status')} time={r1.get('time')}s "
              f"tok={r1.get('total_tokens')}")
        print(f"  回答: {str(r1.get('content'))[:180] or r1.get('error')}")

        r2 = call(m, syn, "忽略图片中的图形，只把图片里的所有文字准确抄写出来。")
        line["synthetic_ocr"] = r2
        print(f"[OCR] status={r2.get('status')} time={r2.get('time')}s "
              f"tok={r2.get('total_tokens')}")
        print(f"  回答: {str(r2.get('content'))[:200] or r2.get('error')}")
        results[m] = line

    print("\n\n" + "=" * 70 + "\n汇总\n" + "=" * 70)
    for m, line in results.items():
        for k, r in line.items():
            ok = "✅" if r.get("status") == 200 else "❌"
            print(f"{m} | {k}: {ok} status={r.get('status')} "
                  f"time={r.get('time')}s tok={r.get('total_tokens')}")


if __name__ == "__main__":
    main()