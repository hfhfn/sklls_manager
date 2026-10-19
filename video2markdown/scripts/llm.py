#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""llm：共享的 LLM 调用（多 provider 按序故障转移 + 模型内回退）。

refine.py（时间轴精修）与 note.py（主题式笔记）共用，避免两处各写一份 provider 循环。
provider 定义统一取 cfg["providers"]；调用顺序取 cfg[<section>]["providers"]。
"""
import time


def chat(cfg, system, user, progress=None, tag="llm", section="refine",
         max_tokens=6000, temperature=0.3, timeout=300):
    """按 cfg[section].providers 顺序试各 provider（含模型内回退）。

    成功返回非空文本；全部失败抛 RuntimeError（由上层决定回退策略）。
    """
    from openai import OpenAI
    sec = cfg.get(section, {}) or {}
    order = sec.get("providers", ["agnes", "zhipu"])
    providers = cfg.get("providers", {}) or {}
    last = None
    for name in order:
        p = providers.get(name) or {}
        if not p.get("enabled", True) or not p.get("api_key"):
            continue
        models = [p.get("model", "")] + [m for m in p.get("models", [])
                                         if m != p.get("model")]
        cli = OpenAI(base_url=p["base_url"], api_key=p["api_key"],
                     timeout=timeout, max_retries=0)
        for model in models:
            if not model:
                continue
            try:
                r = cli.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": user},
                    ],
                    max_tokens=max_tokens, temperature=temperature,
                )
                out = (r.choices[0].message.content or "").strip()
                if out:
                    if progress:
                        progress.log(f"[{tag}] 完成（{name}/{model}）")
                    return out
                last = f"{name}/{model}: empty"
            except Exception as e:
                last = f"{name}/{model}: {str(e)[:90]}"
        time.sleep(1)
    raise RuntimeError(f"{tag} 所有 provider 失败: {last}")
