---
name: course-transcribe
description: 用 ffmpeg + FunASR 批量把课程视频转成中文文字稿（ASR 转录）。当用户需要把 .mp4 课程视频转文字、生成转录 txt、或为后续做笔记准备语音识别文本时使用。基于本地 GPU、支持断点续传。
---

# course-transcribe — 视频 → 中文转录

批量把 `videos/第N章/X-Y 标题.mp4` 转成 `.notes_intermediates/第N章/X-Y 标题.txt`。核心脚本 `scripts/transcribe.py` **随技能自带**（可移植副本）。

> **自带文件（复用即可用）**：`scripts/transcribe.py`。本仓库根目录另放了一份便于直接 `python transcribe.py`；两份逻辑一致，脚本按顶部 `ROOT` 绝对路径常量定位素材，与文件所在位置无关。环境规格与 GPU 设置详见同套技能里的 `../course-pipeline/references/执行流程.md`（已随技能自带，无需回原项目查找）。

## 流水线
```
.mp4 ──ffmpeg──▶ 16kHz 单声道 .wav ──FunASR SenseVoiceSmall──▶ .txt（转录后删 wav）
```
- 镜像 `videos/` 下的章节目录结构；`.txt` 存到 `.notes_intermediates/`。
- **断点续传**：已存在且 >10 字节的 `.txt` 自动跳过；失败记入 `.transcribe_failed.log`。

## 环境（关键）
- conda 环境 `llm_gpu`：Python 3.12、CUDA PyTorch、FunASR 1.3.14、ffmpeg。
- **NVIDIA 控制面板**须把 `python.exe` 与 `ffmpeg.exe` 设为"高性能 NVIDIA 处理器"，否则 ffmpeg 走集显极慢。
- 详见随技能自带的 `../course-pipeline/references/执行流程.md`（完整环境规格与 GPU 设置）。

## 运行
```bash
conda activate llm_gpu
# 本项目根目录直接跑：
python transcribe.py 2>&1 | tee .transcribe_output.log
# 或跑技能自带副本（复用到新课程时改脚本顶部 ROOT 后）：
python skills/course-transcribe/scripts/transcribe.py 2>&1 | tee .transcribe_output.log
```
监控：
```bash
tail -f .transcribe_output.log     # 实时
cat  .transcribe_progress.log      # 带时间戳进度
cat  .transcribe_failed.log        # 失败清单
```

## 注意
- 脚本顶部 `ROOT` 为绝对路径常量，并优先读取 `ROOT/videos`；**换课程/移动目录必须先改这一行**（自带副本已在该行上方加了醒目提示）。
- 转录逐字镜像源视频名，**保留 `&amp;` 与 `【公众号：…】` 后缀**（清理留到 course-notes 阶段）。
- 首次运行会自动下载 ~1GB FunASR 模型。
- 转录质量抽检重点：MCP、A2A、FastAPI、Redis、Playwright 等术语是否正确。
