---
name: zhipu-glm-vision-api
description: Query/test Zhipu GLM vision models on 429s or wrong names.
---

# Zhipu GLM Vision API

Query and evaluate Zhipu's GLM vision models through the OpenAI-compatible endpoint
`https://open.bigmodel.cn/api/paas/v4/chat/completions`. Authentication is a plain
`Authorization: Bearer <API_KEY>` header.

## Correct vision model names (critical — many are misremembered)

Authoritative list (confirmed from the official docs page; the `/v4/models` endpoint
only returns models the account is *subscribed* to, so it is NOT a complete name list):

| Model code | Status |
|------------|--------|
| `glm-4v-flash` / `GLM-4V-Flash` | ✅ exists, fast, stable |
| `glm-4.1v-thinking-flash` / `GLM-4.1V-Thinking-Flash` | ✅ exists, verbose + slow on parse (~16s), fast OCR (~3s) |
| `glm-4.6v-flash` / `GLM-4.6V-Flash` | ✅ exists, **intermittent 429** |
| `glm-4.6v` / `GLM-4.6V` (non-flash) | exists but often not subscribed → 429 "余额不足" |
| `glm-5v-turbo` / `GLM-5V-Turbo` | exists but paid, often not subscribed → 429 "余额不足" |
| `view-3-flash`, `view-4` | exist in docs |
| **`GLM-4.5V-Flash`** | ❌ **DOES NOT EXIST** — returns 400 code 1214 "modelCode：不存在" |

Pitfalls:
- **`glm-4.5` / `glm-4.6` (no V) are TEXT models**, not vision. Adding a `-V` to a text
  model name is how people invent `GLM-4.5V-Flash`. Verify against the docs page before
  trusting a user's model name.
- The `/v4/models` list endpoint (`https://open.bigmodel.cn/api/paas/v4/models`) shows
  only *subscribed* models. A model absent there may still exist (just not enabled).

## GLM-4.6V-Flash 429 (rate limit) — the real behavior

429 on `GLM-4.6V-Flash` is **intermittent, not a ban**. In a 4-run test: 2 successes,
1× 429, 1 success. Error body: `{"error":{"code":"1305","message":"该模型当前访问量过大，请您稍后再试"}}`.
It routes through a free/shared-quota lane that randomly rejects under load.

**Fix: retry with exponential backoff** (1s / 2s / 4s, up to 3-4 attempts). Do NOT
switch models or treat the account as broken on a single 429.

## Implemented production fix — dual-model 429 fallback (vision.js)

The user's `claude-vision-skill` (source at `~/.skills-manager/skills/claude-vision-skill/`,
symlinked into `.claude/`, `.codex/`, `.config/opencode/`, `.trae-cn/` skill dirs) was
upgraded so `vision.js` does **primary + fallback** model selection:

- `VISION_MODEL_PRIMARY` (default `GLM-4.6V-Flash`) — tried first, fast but intermittent 429.
- `VISION_MODEL_FALLBACK` (default `GLM-4.1V-Thinking-Flash`) — used only when primary returns HTTP 429.
- `VISION_MODEL` (legacy) — if set, forces a single model, disabling fallback.
- `VISION_MAX_RETRIES` (default 1) — how many fallback attempts.
- On 429 it logs `[vision] <model> 返回 429 限流，切换备用模型重试...` to stderr and retries the fallback. Non-429 errors (400/401/404/5xx) are NOT retried — they fail fast.

This is the recommended pattern for any GLM-flash vision integration that hits the
free-lane 429: **keep the smart+fast primary, add a free/stable fallback, only switch on 429.**

## Hermes native `auxiliary.vision` does NOT support dual-model fallback

Checked `hermes-agent` source: `auxiliary.vision.model` is a **single string**, not a list.
Hermes auxiliary fallback is **provider-chain based** (openrouter→nous→local/custom→api-key),
NOT same-provider multi-model switching. So you cannot configure "GLM-4.6V-Flash, fall back
to GLM-4.1V-Thinking-Flash" in `config.yaml` for Hermes' own vision. Options:
- Put the fallback logic in your own script (like vision.js above) wrapping the API.
- Or set `auxiliary.vision.model` to a never-429 model (`GLM-4V-Flash`).
- Hermes' `vision_tools.py` 429-retry logic only covers *image URL download*, not the LLM call.

## Deterministic fallback verification (no token cost)

To verify a fallback path without hitting the real API, point `VISION_BASE_URL` at a local
mock HTTP server that returns 429 for the primary model and 200 for the fallback, then assert
the tool retried. This is repeatable and free — use it instead of relying on catching a real 429.
`scripts/verify_vision_fallback.py` is a ready-made version of this probe (run it with the
path to a `vision.js`-style tool; asserts primary-429→fallback-switch and non-429-no-retry).

## Standard image request shape

```python
payload = {
  "model": "GLM-4V-Flash",
  "messages": [{"role": "user", "content": [
      {"type": "image_url", "image_url": {"url": "data:image/png;base64,<b64>"}},
      {"type": "text", "text": "describe this image"},
  ]}],
  "stream": False,
}
```

## Reusable test harness

`scripts/test_glm_vision.py` — generates a synthetic test image (Chinese OCR +
shape/color + digit sequence) and runs every candidate model through parse + OCR,
reporting status/time/tokens and surfacing 429s. Run it to verify which models work
and measure latency before recommending one.

## Estimating capability

For a quick pass: generate a synthetic image with `PIL` (large Chinese text via a
Windows font like `msyh.ttc`, colored shapes, a digit sequence), then send two prompts:
(1) "describe the image" (parse), (2) "copy all text verbatim" (OCR). This distinguishes
models that hallucinate from those that read accurately.

## Notes for this user's environment

- API key lives in env var `CUSTOM_GLM_API_KEY` (not `.env` necessarily; read from env).
- Hermes `auxiliary.vision` defaults to `GLM-4.6V-Flash` via `key_env: CUSTOM_GLM_API_KEY`
  — swaps to `GLM-4V-Flash` (stable) or `GLM-4.1V-Thinking-Flash` (smarter) to avoid 429s.
- Docs pages under `open.bigmodel.cn` are JS-rendered; `curl` + regex on the raw HTML
  still surfaces the model-code list (works when `web_search`/`web_extract` are unavailable).