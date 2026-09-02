#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
本地免费语音转录服务 (FastAPI) - FunASR paraformer + cam++ 说话人区分
启动时加载一次模型并复用；HTTP 请求只附加热词，不切换已加载的说话人能力。

接口：
  GET  /health                健康检查（含真实配置）
  POST /transcribe            上传音频 (multipart file), 返回带说话人的 JSON 转录
       --form file=@xxx.m4a   可选 --data hotwords=a,b,c

环境要求：llm_gpu 里已装 funasr + torch(CUDA)。
启动：D:\\software\\miniconda3\\envs\\llm_gpu\\python.exe -u transcribe_server.py --host 127.0.0.1 --port 8000
"""
import argparse, re, threading, time, tempfile, os
from typing import List, Optional

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse

import torch
from funasr import AutoModel

from transcript_core import load_terms, merge_hotwords, utc_now

app = FastAPI(title="Local Free Transcribe (FunASR+diarization)")
_lock = threading.Lock()
_DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"

# Fixed at process start; a request cannot switch model speaker capability.
_server_cfg = {"spk_on": True, "cache_dir": None, "hotwords_file": None, "offline": False,
               "model_path": None, "spk_num": None}
_MODEL = None
_LOAD_COUNT = 0
_loaded_signature = None


def _signature():
    cfg = _server_cfg
    return (cfg["spk_on"], cfg["cache_dir"], cfg["hotwords_file"], cfg["offline"],
            cfg["model_path"], cfg["spk_num"])


def load_model():
    global _MODEL, _LOAD_COUNT, _loaded_signature
    cfg = _server_cfg
    sig = _signature()
    if _MODEL is not None and _loaded_signature == sig:
        return _MODEL  # already loaded with identical config (startup + __main__)
    if cfg["cache_dir"]:
        os.environ.setdefault("MODELSCOPE_CACHE", cfg["cache_dir"])
    if cfg["offline"]:
        os.environ.setdefault("MODELSCOPE_OFFLINE", "1")
        os.environ.setdefault("HF_HUB_OFFLINE", "1")
    opts = dict(
        model=cfg["model_path"] or "paraformer-zh",
        vad_model="fsmn-vad",
        punc_model="ct-punc",
        disable_update=True,
        device=_DEVICE,
    )
    if cfg["spk_on"]:
        opts["spk_model"] = "cam++"
    if cfg["spk_num"]:
        opts["spk_num"] = cfg["spk_num"]
    _MODEL = AutoModel(**opts)
    _LOAD_COUNT += 1
    _loaded_signature = sig
    return _MODEL


def _clean(t):
    return re.sub(r"<\|[^|]*\|>", "", t or "").strip()


def infer(audio_path: str, hotwords: Optional[List[str]] = None):
    with _lock:
        res = _MODEL.generate(
            input=audio_path,
            batch_size_s=300,
            sentence_timestamp=True,
            hotwords=hotwords or [],
        )
    r = res[0]
    segs = []
    for s in r.get("sentence_info", []):
        raw = _clean(s.get("sentence") or s.get("text") or "")
        if not raw:
            continue
        segs.append({"spk": s.get("spk"), "start": s.get("start"),
                     "end": s.get("end"), "text": raw})
    return {"text": _clean(r.get("text", "")), "segments": segs,
            "device": _DEVICE}


@app.on_event("startup")
def _startup():
    load_model()


@app.get("/health")
def health():
    return {"ok": True, "device": _DEVICE, "loaded": _MODEL is not None,
            "load_count": _LOAD_COUNT, "config": _server_cfg}


@app.post("/transcribe")
def transcribe(file: UploadFile = File(...),
               spk_on: bool = Form(True),
               hotwords: str = Form("")):
    if spk_on != _server_cfg["spk_on"]:
        return JSONResponse(
            {"error": f"speaker pipeline fixed at server start (spk_on={_server_cfg['spk_on']}); "
                      f"restart server to change it"}, status_code=409)
    terms, _ = load_terms(_server_cfg["hotwords_file"])
    hw = merge_hotwords(terms, [w.strip() for w in hotwords.split(",") if w.strip()])
    suffix = os.path.splitext(file.filename or "a.wav")[1] or ".wav"
    fd, tmp = tempfile.mkstemp(suffix=suffix, prefix="dsh_tr_")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(file.file.read())
        t0 = time.time()
        out = infer(tmp, hw)
        out["processing_s"] = round(time.time() - t0, 2)
        out["applied_hotwords"] = hw
        out["created_at"] = utc_now()
    finally:
        try:
            os.remove(tmp)
        except OSError:
            pass
    return JSONResponse(out)


if __name__ == "__main__":
    import uvicorn
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--no-spk", action="store_true")
    ap.add_argument("--cache-dir", default=None)
    ap.add_argument("--hotwords-file", default=None)
    ap.add_argument("--model-path", default=None)
    ap.add_argument("--spk-num", type=int, default=None)
    ap.add_argument("--offline", action="store_true")
    a = ap.parse_args()
    _server_cfg.update(spk_on=not a.no_spk, cache_dir=a.cache_dir,
                       hotwords_file=a.hotwords_file, offline=a.offline,
                       model_path=a.model_path, spk_num=a.spk_num)
    load_model()
    uvicorn.run(app, host=a.host, port=a.port)