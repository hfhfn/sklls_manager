---
name: video2markdown
description: 把「本地或在线」视频（抖音/B站/YouTube/本地mp4）转成带「画面内容」的结构化 Markdown。语音识别(本地FunASR)+屏内文字OCR+画面语义描述(免费云端视觉模型)三重提取，按时间线互操作成一份含逐字稿/字幕/幻灯片/代码/画面描述的笔记。当用户给出一段视频文件路径、抖音/B站/YouTube链接，或要求"把视频转成markdown/生成笔记/转录+画面注释"时使用。
---

# video2markdown — 视频 → 带画面的 Markdown

把**本地视频文件**或**在线视频链接/分享口令**转成一份结构化的 Markdown 文档。
不只转录说话内容，还提取**画面里出现的文字**（字幕/幻灯片/代码）和**画面语义**（图表/UI/场景/动作），按时间线交错排布。

- **免费优先**：语音=本地 FunASR，画面文字=本地 RapidOCR（离线/零显存），画面语义=免费云端视觉模型（智谱 GLM-4V-Flash / 硅基流动 Qwen2.5-VL / Agnes-25-Flash，多提供商自动故障转移）。
- **GPU 显存 < 8G**：各阶段串行、互斥使用 GPU，ASR 档 ≈0.5G，全程远低于 8G。
- **不逐帧分析**：场景检测把帧收敛到 ~40–70 代表帧，OCR 全量本地跑，VLM 仅 ~30–50 次/30min，免费档可承受。

## 触发

用户表达以下任一意图时调用：

- "把这个视频转成 markdown / 生成笔记" / "转录一下，最好带画面内容"
- 给出**本地视频路径**（`.mp4/.mkv/.webm/.mov`…）
- 给出**在线链接/分享口令**（抖音 `v.douyin.com` / B站 `b23.tv` / YouTube `youtube.com`…）
- "把这条课程视频整理成笔记，把 PPT、代码、讲的东西都收进去"

## 用法（命令行）

```bash
cd "工作目录"

# 本地视频
python C:/Users/hfhfn/.claude/skills/video2markdown/scripts/video2md.py "C:/path/to/视频.mp4"

# 在线视频（抖音/B站/YouTube 分享口令或链接）
python C:/Users/hfhfn/.claude/skills/video2markdown/scripts/video2md.py "https://v.douyin.com/xxxx/"

# 常用参数
--depth standard|light|deep      # 笔记深度，默认 standard
--engine sensevoice|faster-whisper|cloud-sensevoice|cloud-tele  # ASR 引擎
#   本地默认 sensevoice(中文最优)；cloud-sensevoice/cloud-tele 走硅基云端(需余额)
--vlm on|off                     # 是否启用云端画面语义，默认 on
--max-vlm-frames N               # VLM 最多分析帧数，默认 60
```
> 建议在 `llm_gpu` conda 环境下运行（含 FunASR/PyTorch）。首次运行自动下载模型。

## 流水线（scripts/video2md.py 一键串联）

```
输入(本地路径 或 分享链接/URL)
  ├─[ingest.py]      本地→校验/探测时长；在线→yt-dlp(代理感知)下载成 mp4
  ├─[transcribe.py]  ffmpeg→16k WAV → FunASR SenseVoiceSmall(fsmn-vad分段) → transcript.jsonl [{t0,t1,text}]
  ├─[keyframes.py]   ffmpeg 场景检测→代表帧(去重, 30min≈40–70帧)
  ├─[ocr.py]         RapidOCR(CPU) 逐帧→屏内文字(字幕/PPT/代码) + 时间戳；本地弱帧可升云端OCR(需余额)
  ├─[describe.py]    (vlm=on) 去重加点筛非纯文本帧→送免费云端VLM→画面语义 caption + 故障转移
  └─[assemble.py]    按时间线交错 语音+OCR+VLM → 原始Markdown
  └─[refine.py]      (可选) 把原始材料送 agnes 等 LLM 整合：错别字修正/OCR去重/要点归纳 → 最终MD
```

产出：`<视频名>.md` + 中间目录 `.vid_intermediates/`（wav/keyframes/frame_meta.json 等，可删）。

## Markdown 产物结构（standard 档）

```
---
title, source, duration, 引擎, 模型…
---
# 标题
## 摘要
## 时间轴/画面注释   ← 每段: [mm:ss] 语音逐字稿 + 🔤OCR字幕 + 🖼画面描述
## 幻灯片 / 代码快照   ← OCR抓到的PPT要点、代码块按时间归类
## 逐字稿(完整)         ← 全文，带时间戳
## 关键要点
```

## 配置（画面语义后端）

默认三档视觉模型自动故障转移，Key 与端点**只存本地** `~/.video2md/config.json`（复制 `config.example.yaml` 改名并填 key）：

| 提供商 | 模型 | 说明 |
|---|---|---|
| 智谱 bigmodel.cn | `glm-4.6v-flash`（限流自动退 `glm-4v-flash`）| 免费视觉模型，实测 4v-flash 可用 |
| 硅基流动 siliconflow.cn | `Qwen/Qwen3-VL-8B-Instruct` | Qwen2.5-VL 已下架；免费档随运营变化 |
| Agnes apihub.agnes-ai.com | `agnes-2.5-flash` | 免费模型，偶发空返回（自动切换）|

任一家限流/报错自动切换到下一家，无需中断。完全离线时 `--vlm off` 只保留 OCR 画面内容。
各参数与免费额度的更新说明见 `references/providers.md`。

## 注意

- 在线下载走外网，抖音/B站多数可直连；YouTube 需走本机代理 `127.0.0.1:7890`（脚本自动识别内网/外网）。
- 请遵守平台条款与著作权，仅用于个人学习/研究等合法用途。
- 断点续传：已生成的中间产物自动跳过，可断点重跑。