---
name: claude-vision-skill
description: "识图能力：底层模型无原生视觉时，用 vision.js 调用智谱 GLM 视觉模型识别图片（GLM-4.6V-Flash 优先，限流 429 时自动回退 GLM-4.1V-Thinking-Flash）。Use when the user shares/asks about an image (local path or URL) and the active model cannot see images natively."
version: 1.1.0
author: asuojun (adapted for Hermes + Zhipu GLM, dual-model fallback)
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [vision, image, glm, zhipu, multimodal, fallback]
    related_skills: [hermes-agent]
---

# 识图能力 (claude-vision-skill)

你的底层模型若不具备原生识图能力，遇到图片时用 `vision.js` 调用**智谱 GLM 视觉模型**识别。默认**双模型自动回退**：优先 `GLM-4.6V-Flash`，若遭遇 HTTP 429 限流（“访问量过大”），自动切换 `GLM-4.1V-Thinking-Flash` 重试。

## 配置（已就绪）

- 主模型: `GLM-4.6V-Flash`（`VISION_MODEL_PRIMARY`）— 快，识别准确，但高峰易 429
- 回退模型: `GLM-4.1V-Thinking-Flash`（`VISION_MODEL_FALLBACK`）— 更聪明，429 时自动顶上
- API Base: `https://open.bigmodel.cn/api/paas/v4`（OpenAI 兼容）
- API Key: 从环境变量 `CUSTOM_GLM_API_KEY` 读取（Hermes `.env` 已配置），也可用 `VISION_API_KEY` 覆盖
- 回退次数: `VISION_MAX_RETRIES`（默认 1，即最多切 1 个备用模型）

### 环境变量速查

| 变量 | 默认 | 说明 |
|------|------|------|
| `VISION_MODEL_PRIMARY` | `GLM-4.6V-Flash` | 主视觉模型 |
| `VISION_MODEL_FALLBACK` | `GLM-4.1V-Thinking-Flash` | 429 限流时的回退模型 |
| `VISION_MODEL` | (空) | 若设置，则固定用这一个模型，**不启用回退**（旧单模型行为） |
| `VISION_MAX_RETRIES` | 1 | 429 时回退尝试次数 |
| `VISION_API_KEY` | `CUSTOM_GLM_API_KEY` | API Key |
| `VISION_BASE_URL` | 智谱官方 | OpenAI 兼容 base url |

## 用法

识别本地图片:
```bash
node vision.js "/path/to/image.png" "用中文描述这张图片"
```

识别网络图片 URL:
```bash
node vision.js --url "https://example.com/photo.jpg" "这张图里有什么?"
```

限流时自动回退（无需手动指定）:
```bash
# 主模型 429 → 自动尝试 GLM-4.1V-Thinking-Flash
node vision.js "/path/to/image.png" "描述内容"
```

强制指定主模型（测试时可用）:
```bash
VISION_MODEL_PRIMARY="GLM-4V-Flash" node vision.js "/path/to/image.png" "描述"
```

## 触发场景

- 用户分享图片路径（本地或网络 URL）
- 消息中出现 "Saved attachments:" 并列出图片
- 用户要求分析、描述、识别图片内容

## 实现说明

- `vision.js` 读取图片 → base64 → 调用 OpenAI 兼容的 vision 接口 → 返回文字描述。
- 支持本地文件（自动转 base64 data URL）和 `--url` 网络图片。
- **双模型回退**：主模型返回 HTTP 429 时，自动切换备用模型重试；非 429 错误（400/401/404/5xx）不重试，直接报错。
- 回退成功后会在 stderr 打印 `[vision]` 日志，方便排查用到了哪个模型。