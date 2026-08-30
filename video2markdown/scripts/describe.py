#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""describe：免费云端视觉模型(多提供商自动故障转移)为关键帧生成画面语义描述。

应对"免费模型并发小/限流"的关键设计：
- 每家是一个独立 OpenAI 兼容 client(config.providers)。
- 起始顺序随机化(randomize)，分摊各家瞬时限流。
- 单帧内：当前 provider 失败(429/5xx/超时) → 按 failover.retries 尝试下一家。
- 429 退避 min_delay_s；同一家连续失败 ≥ consecutive_fail_to_sleep 次 → 冷却暂停一段时间。
- 纯文本长帧(OCR 已完整捕捉的整页幻灯片)跳过描述，节约调用次数。

输入：frames.jsonl + ocr.jsonl（取同时间 OCR 文本作为上下文，避免 VLM 重复读屏内字）。
输出：<inter>/describe.jsonl [{t, caption, provider}]，并记失败/切换日志。
"""
import argparse
import base64
import json
import random
import re
import threading
import time
from pathlib import Path

from common import ProgressLog, read_jsonl, write_jsonl, load_config, user_config_path

PROMPT_TMPL = (
    "你是一个严谨的视频画面解说员。请只描述这张图片里'非文字'的视觉内容："
    "图表/结构/示意图、界面UI布局、现场场景、人物动作、物体等。\n"
    "【该帧已由OCR提取到的文字，请不要再重复】：\n{ocr_text}\n\n"
    "若画面主要就是文字/字幕/幻灯片、没有额外视觉信息，直接回复"
    "“（无额外视觉信息）”。\n用简短中文，1-3 句，不要编造。"
)

# 帧 OCR 文本超过此长度视为"整页文字"，跳过 VLM（省调用）
SKIP_OCR_LEN = 300

# 冷却上限（秒）：连续失败越多冷却越长，封顶此值，避免对坏 provider 反复撞
DEFAULT_MAX_COOLDOWN_S = 120
# "稳定故障"（空响应/超时/连接错误，非纯限流 429）多为持续状态：
# 冷却直接取 max_cooldown 的硬性比例，一次就把坏 provider 压下去，不再每帧空转重试
STABLE_FAIL_COOLDOWN_RATIO = 0.8


# 推理模型内容开头的"脚手架"词（"所以/总结/要简洁，1-3句"等），剥掉
_LEAD = (r"(?:所以|那么|因此|于是|总结|综上|简单说|可以说|答案是|"
         r"答案[：:]|检查|要简洁|用户现在需要|根据[^。]{0,12}[：:]?)")
_LEAD_RE = re.compile(
    r"^(?:%s[：:，,]?\s*|%s[^。！？]{0,30}[。！？][：:，,]?\s*)+" % (_LEAD, _LEAD))


def _clean_caption(txt):
    """清洗模型返回的描述：剥 XML 标签；剥推理脚手架；若内容超长（如
    glm-4.1v-thinking 把"推理+答案"焊进未闭合 <think>，答案在末尾），取末尾两句。"""
    txt = re.sub(r"<[^>]+>", "", txt or "", flags=re.S).strip()
    txt = _LEAD_RE.sub("", txt)
    if len(txt) > 300:
        sents = [s.strip() for s in re.split(r"(?<=[。！？!?])", txt) if s.strip()]
        if len(sents) >= 3:
            txt = "".join(sents[-2:])
            txt = _LEAD_RE.sub("", txt)
    return txt


class Provider:
    def __init__(self, name, conf, failover_cfg):
        self.name = name
        self.conf = conf
        self.base_url = conf.get("base_url", "")
        self.model = conf.get("model", "")
        self.api_key = conf.get("api_key", "")
        self.max_retries = conf.get("max_retries", failover_cfg.get("retries", 2))
        self._client = None
        self.consecutive_fail = 0
        self.suspended_until = 0.0
        self.uses = 0
        self.ok = 0
        self.fail = 0
        # 累计成功/失败用于稳定分排序；最近一次冷却长度(供日志参考)
        self.last_cooldown_s = 0.0

    def client(self):
        if self._client is None:
            if not self.api_key:
                raise RuntimeError(f"provider[{self.name}] 未配置 api_key")
            from openai import OpenAI
            self._client = OpenAI(base_url=self.base_url, api_key=self.api_key,
                                  timeout=60, max_retries=0)  # 手动控制重试
        return self._client

    def available(self, now):
        return now >= self.suspended_until

    def suspend(self, seconds, now):
        self.suspended_until = now + seconds
        self.last_cooldown_s = seconds

    def stability(self):
        """稳定分 [0,1]，用于候选排序：成功率越高分越高，连续失败有额外惩罚。
        未用过的 provider 给中性 0.5，始终有机会被尝试。"""
        if self.uses == 0:
            return 0.5
        base = self.ok / self.uses
        # 连续 1 次失败 -0.2，连续 2+ 再额外 -0.3，把烂货明显压后
        penalty = 0.0
        if self.consecutive_fail >= 1:
            penalty += 0.2
        if self.consecutive_fail >= 2:
            penalty += 0.3
        if self.uses >= 3 and self.ok == 0:
            penalty += 0.2  # 用过多次却 0 成功，几乎判死
        return max(0.0, base - penalty)

    def describe(self, prompt):
        import openai
        cli = self.client()
        # 支持的模型有序列表：主 model + 配置里的 models 回退（如智谱
        # glm-4.6v-flash 限流时自动退到 glm-4v-flash）。全部失败才上抛。
        models = [self.model] + [m for m in self.conf.get("models", [])
                                 if m != self.model]
        text = prompt["text"]
        img_b64 = prompt["image_b64"]
        last_err = None
        for model in models:
            try:
                resp = cli.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": [
                        {"type": "image_url", "image_url": {
                            "url": f"data:image/jpeg;base64,{img_b64}"}},
                        {"type": "text", "text": text},
                    ]}],
                    max_tokens=200,
                    temperature=0.3,
                )
                raw = (resp.choices[0].message.content or "").strip()
                caption = _clean_caption(raw)
                if not caption:
                    # 空返回 / 清洗后为空（纯推理无答案）→ 视为故障 → 换下一模型/provider
                    self.fail += 1
                    self.uses += 1
                    self.consecutive_fail += 1
                    last_err = "empty response"
                    continue
                self.ok += 1
                self.uses += 1
                self.consecutive_fail = 0
                return caption
            except Exception as e:
                self.fail += 1
                self.uses += 1
                self.consecutive_fail += 1
                last_err = str(e)[:160]
                # 429/5xx 多为限流，继续下一个模型（同 provider 内），最后交 Dispatcher 切换
        raise RuntimeError(last_err or "模型均返回空")  # 交由 Dispatcher 判断降级/冷却


class Dispatcher:
    """多 provider 故障转移调度器（进程内，非线程安全的锁外使用）。"""
    def __init__(self, providers, failover):
        self.providers = [p for p in providers if p.api_key and p.base_url]
        if not self.providers:
            raise RuntimeError("没有任何已配置的可用 provider（config.json 里填 api_key）")
        self.failover = failover
        self.cool = failover.get("consecutive_fail_to_sleep", 3)
        self.min_delay = failover.get("min_delay_s", 2)
        self.max_cooldown = failover.get("max_cooldown_s", DEFAULT_MAX_COOLDOWN_S)
        self.lock = threading.Lock()

    def _cooldown(self, p, msg, stable=False):
        """按连续失败次数指数退避冷却。稳定故障（空响应/超时/连接错）直接取
        max_cooldown 的高比例，一次把坏 provider 压到底，避免每帧空转重试；\
        普通限流(429/5xx)则指数增长、封顶 max_cooldown。"""
        if stable:
            secs = max(self.min_delay * 2,
                       int(self.max_cooldown * STABLE_FAIL_COOLDOWN_RATIO))
        else:
            secs = min(self.min_delay * (2 ** min(p.consecutive_fail - 1, 8)),
                       self.max_cooldown)
        p.suspend(secs, time.time())
        kind = "稳定故障" if stable else "限流/超时"
        return f"冷却 {p.name} {secs}s[{kind}]：{msg}"

    def _candidate_order(self):
        now = time.time()
        avail = [i for i, p in enumerate(self.providers) if p.available(now)]
        if not avail:
            return avail
        # 稳定分降序：把成功率高的排前面，频繁失败的坏 provider 排到末尾，
        # 且每帧仍带随机位移分摊限流（不会只怼同一个好 provider）。
        avail.sort(key=lambda i: self.providers[i].stability(), reverse=True)
        if self.failover.get("randomize", True) and len(avail) > 2:
            # 只对前 half 好 provider 做随机起始位移；坏 provider 永远垫底
            good = avail[:max(1, len(avail) // 2)]
            rest = avail[len(good):]
            start = good[random.randrange(len(good))]
            good_rot = [start] + [i for i in good if i != start]
            return good_rot + rest
        return avail

    def describe_one(self, frame, ocr_text):
        """针对单帧调度：逐家尝试(可选随机起始)，429/5xx/超时自动切换，返回 (caption, provider_name, switched_logs)"""
        prompt = {"text": PROMPT_TMPL.replace("{ocr_text}", ocr_text or "（无）"),
                  "image_b64": base64.b64encode(Path(frame["path"]).read_bytes()).decode()}
        logs = []
        max_attempts = max(1, self.failover.get("retries", 2))
        last_err = None
        # 活跃候选（随机起始顺序）；第一阶段尽用
        with self.lock:
            order = self._candidate_order()
            if not order:
                sl = self.min_delay
                time.sleep(sl)
                logs.append(f"全部 provider 在冷却，等待 {sl}s")
                order = self._candidate_order()

        # 至少试 max_attempts 家；不足就退避后补尝
        tries = 0
        while tries < max_attempts and order:
            for idx in range(len(order)):
                p = self.providers[order[idx]]
                tries += 1
                try:
                    cap = p.describe(prompt)
                    return cap, p.name, logs
                except Exception as e:
                    last_err = str(e)[:160]
                    cls = type(e).__name__
                    # 稳定故障：空响应/超时/连接错误（多为 provider 持续状态，
                    # 不是瞬时限流）→ 立即长冷却压下去，避免每帧反复空转
                    stable = ("empty" in last_err.lower()
                              or cls in ("Timeout", "APITimeoutError",
                                         "APIConnectionError", "ConnectionError")
                              or "timed out" in last_err.lower())
                    rate = "429" in last_err or cls == "RateLimitError"
                    srv = str(getattr(e, "status_code", ""))[:1] == "5"
                    timeout = cls in ("Timeout", "APITimeoutError", "APIConnectionError")
                    with self.lock:
                        # 稳定故障:一次压死；否则 429/连续 N 次失败才冷却
                        if stable or p.consecutive_fail >= self.cool or rate:
                            logs.append(self._cooldown(
                                p, f"{cls}: {last_err}", stable=stable))
                            # 稳定故障本帧即跳过该 provider，不再在同一帧内反复试它
                            break
                    if timeout:
                        time.sleep(0.5)
            # 一轮都失败：刷新候选（可能有的冷却结束）、退避再试
            time.sleep(self.min_delay)
            with self.lock:
                order = self._candidate_order()
        raise RuntimeError(f"所有可用 provider 均失败: {last_err or '无候选'}")

    def stats(self):
        return {p.name: {"uses": p.uses, "ok": p.ok, "fail": p.fail,
                         "consecutive_fail": p.consecutive_fail} for p in self.providers}


def build_providers(cfg):
    provs = []
    for name, c in (cfg.get("providers") or {}).items():
        if c.get("enabled", True):
            provs.append(Provider(name, c, cfg.get("failover", {})))
    return provs


def describe_frames(frames, ocr_rows, inter_dir, cfg, progress):
    out_path = Path(inter_dir) / "describe.jsonl"
    if not cfg.get("vlm", True):
        progress.log("[vlm] vlm=off，跳过画面语义")
        return []
    # 断点续传：加载已有结果，跳过已完成帧
    existing = read_jsonl(out_path) if out_path.exists() else []
    done_t = {r["t"] for r in existing}
    ocr_by_t = {r["t"]: r["ocr_text"] for r in ocr_rows}
    max_vlm = cfg.get("max_vlm_frames", 60)

    # 候选帧：跳过纯文本长帧，再按时长等距取 ≤ max_vlm 帧
    cand = [f for f in frames
            if len(ocr_by_t.get(f["t"], "")) < SKIP_OCR_LEN and f["t"] not in done_t]
    if not cand:
        cand = [f for f in frames if f["t"] not in done_t]
    if len(cand) > max_vlm:
        step = len(cand) / max_vlm
        cand = [cand[int(i * step)] for i in range(max_vlm)]

    dispatcher = Dispatcher(build_providers(cfg), cfg.get("failover", {}))
    progress.log(f"[vlm] 计划描述 {len(cand)} 帧（已有 {len(existing)} 跳过；{len(dispatcher.providers)} 家 provider 轮转+故障转移）")
    pause = float(cfg.get("frame_pause_s", 1.0))  # 成功帧间间隔，体贴免费档限流
    out = list(existing)
    failed = 0
    N = len(cand)
    for i, fr in enumerate(cand, 1):
        try:
            cap, prov, logs = dispatcher.describe_one(fr, ocr_by_t.get(fr["t"], ""))
            for lg in logs:
                progress.log(f"[vlm][!] {lg}")
            row = {"t": fr["t"], "caption": cap, "provider": prov}
            out.append(row)
            with open(out_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
        except Exception as e:
            failed += 1
            progress.log(f"[vlm][!] 帧@{fr['t']}s 所有 provider 失败，跳过该帧：{str(e)[:100]}")
        if i % 10 == 0 or i == N:
            progress.log(f"[vlm] {i}/{N}")
        time.sleep(pause)
    if failed:
        progress.log(f"[vlm] {failed} 帧失败被跳过（免费档限流常见，可在 config 调大 frame_pause_s 缓解）")
    return out
    progress.log(f"[vlm] 完成 {len(out)} 帧；统计: {dispatcher.stats()}")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--inter", required=True)
    a = ap.parse_args()
    cfg = load_config()
    plog = ProgressLog(a.inter)
    import os
    frames = read_jsonl(Path(a.inter) / "frames.jsonl")
    ocr_rows = read_jsonl(Path(a.inter) / "ocr.jsonl")
    rows = describe_frames(frames, ocr_rows, a.inter, cfg, plog)
    for r in rows[:3]:
        print(r)