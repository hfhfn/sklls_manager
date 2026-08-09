---
name: claude-vision-skill
description: "识图能力：底层模型无原生视觉时，用 vision.js 调用智谱 GLM-4.6V-Flash 识别图片。Use when the user shares/asks about an image (local path or URL) and the active model cannot see images natively."
version: 1.0.0
author: asuojun (adapted for Hermes + Zhipu GLM)
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [vision, image, glm, zhipu, multimodal]
    related_skills: [hermes-agent]
---

# 识图能力 (claude-vision-skill)

你的底层模型若不具备原生识图能力，遇到图片时用 `vision.js` 调用**智谱 GLM-4.6V-Flash** 识别，返回文字描述。

## 配置（已就绪）

- 模型: `GLM-4.6V-Flash`
- API Base: `https://open.bigmodel.cn/api/paas/v4`（OpenAI 兼容）
- API Key: 从环境变量 `CUSTOM_GLM_API_KEY` 读取（Hermes `.env` 已配置），也可用 `VISION_API_KEY` / `VISION_MODEL` / `VISION_BASE_URL` 覆盖。

## 用法

识别本地图片:
```bash
node vision.js "/path/to/image.png" "用中文描述这张图片"
```

识别网络图片 URL:
```bash
node vision.js --url "https://example.com/photo.jpg" "这张图里有什么?"
```

## 触发场景

- 用户分享图片路径（本地或网络 URL）
- 消息中出现 "Saved attachments:" 并列出图片
- 用户要求分析、描述、识别图片内容

## 实现说明

- `vision.js` 读取图片 → base64 → 调用 OpenAI 兼容的 vision 接口 → 返回文字描述。
- 支持本地文件（自动转 base64 data URL）和 `--url` 网络图片。