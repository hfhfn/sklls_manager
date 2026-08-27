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
--outdir DIR                     # 输出 md 目录（覆盖配置 output_dir；默认视频旁）
--keep-intermediate              # 完成后保留 .vid_* 中间产物（默认自动清理）
```
> 建议在 `llm_gpu` conda 环境下运行（含 FunASR/PyTorch）。首次运行自动下载模型。

**本机默认输出**：`~/.video2md/config.json` 已设 `output_dir=C:\Users\hfhfn\Desktop\vid_work`，
转录完成后 md 自动落到桌面，且中间产物 `.vid_*` 默认自动清理（需保留时加 `--keep-intermediate`）。

## ⚠ 运行时关键坑（务必先读）

- **PYTHONPATH 污染**：在 Hermes 桌面 app 的终端里运行本脚本时，外层环境把
  `PYTHONPATH` 设成 hermes venv 的 site-packages，会导致 `import torch`/`import numpy`
  误加载 hermes 的 numpy（报 `No module named 'numpy._core._multiarray_umath'` 或
  `WinError 206 路径太长`）。脚本已在入口自动清除 PYTHONPATH/PYTHONHOME 自保；
  若仍异常，手动 `unset PYTHONPATH VIRTUAL_ENV` 后再跑。
- **抖音网页版下载需 cookies**：yt-dlp 直连 `www.douyin.com/video/<id>` 常报
  `Fresh cookies needed`。绕过方案见下方「抖音下载」。
- **抖音国内站点不走代理**：本地 Clash 代理(127.0.0.1:7890)会绕挂国内站，
  下载/探测抖音用**直连**即可（curl 直连返回 200）。

## ⚠ 无命令行环境降级指南（DSH / 浏览器沙箱 agent 务必先读）

> 适用：agent 所在会话**无法执行 shell 命令**（bash 返回
> `terminal inspection is unsupported on platform win32`，或没有 bash 工具可调）。
> 典型 = DeepSeek Harness / 浏览器 Web 沙箱。**先判断，再动手，别浪费轮次。**

### 第一步：立刻识别环境（1 次 bash 探测即可）
调一次 `bash`（任意命令，如 `echo ok`）。若报 `terminal inspection is unsupported`
或 `only run_code is callable directly`，立即认定**无命令执行能力**——
`echo`/`cmd`/`powershell`/`python` 全都一样，**不要再反复验证**，直接走下方降级路径。

### 第二步：在无命令行环境下，转录无法由 agent 完成——按"自动化程度"分级，尽量少让用户动手

无 bash = agent 无法直接跑 `video2md.py`，也无法用 yt-dlp。**用户的核心诉求是"你帮我操作、最多让我授权"，不要让用户复制/粘贴任何命令**。按 agent 可用工具分三档：

**档 1：agent 有浏览器/Playwright 工具 → 自动抓 CDN 直链（最少用户介入）**
1. 用浏览器打开 `https://www.douyin.com/video/<modal_id>`（或分享短链转出的 video 页）。
2. 控制台执行，抓 `douyinvod.com` 直链（video 轨 + audio 轨）：
   ```js
   performance.getEntriesByType('resource').map(e=>e.name).filter(n=>n.includes('douyinvod.com'))
   ```
3. 拿到 `media-video-avc1/...` + `media-audio-und-mp4a/...` 两条 URL 后，**自动写一个一键启动器
   到用户工作区**（见档 2），把 URL 填进去，让用户在本机只"双击/授权"即可下载+转录，不用复制命令。
   完整脚本见 `references/douyin-cdn-direct.md`。

**档 2：agent 有文件写入能力（如 workspace-write）→ 自动落一个一键启动器**
在用户的**工作区**（DSH 的 workspace-write 空间，如 `temp_project`）自动生成两个文件，
用户只需**双击/授权一次**，全程不复制命令：
- `download_douyin.py`：yt-dlp 下载脚本，依次尝试 cookies.txt → 各浏览器 cookies → 直连，
  输出本地 `video/*.mp4`（脚本内容见 skill 根目录 `templates/download_douyin.py`）。
- `run_transcribe.bat`：先调 `download_douyin.py` 下载，再把本地 mp4 交给 `video2md.py` 转录。
  **必须纯 ASCII、CRLF 结尾**（UTF-8 中文会被 cmd 按 GBK 解析成乱码拆行——实测踩坑）。
- 把抖音 URL 直接写死在 `.bat` 的 `set URL=...`（或让脚本从 drag-drop 的第 1 参数取）。

> 为什么要"落启动器"而非"给命令"：用户已明确"顶多让我授权"，双击一个已就绪的 .bat
> 比复制长命令更接近"授权"。启动器落在工作区即可，用户在本机对应路径双击。

**档 3：agent 连文件写入都没有 → 才退化为给单行命令（最后手段）**
实在无法生成启动器时，才把这一行交给用户在**本机 PowerShell/CMD** 粘：
```
conda activate llm_gpu && python C:/Users/hfhfn/<BASE>/skills/video2markdown/scripts/video2md.py "https://v.douyin.com/xxxx/" --work C:/Users/hfhfn/Desktop/vid_work
```
> `<BASE>` = agent 自己的 skill 基目录，`.claude`、`.dsh`、`.skills-manager` 三处指向同一份
> 物理脚本（本机已验证 symlink/inode 一致），用哪个都行；不知道就用 `.claude`。
> 本地视频就把 URL 换成文件路径，`--work` 目录可改。输出到 `~/.video2md/config.json` 的
> `output_dir`（本机 = 桌面 `vid_work`）。

### 第三步：别再碰这些死路
- ❌ 反复 `--cookies-from-browser`：Windows 上 Chrome/Edge cookie 是 DPAPI 加密的，
  yt-dlp 直读常常拿不到有效值，6 个浏览器全失败是常态。别再循环试。
- ❌ 让用户手动装扩展导出 `cookies.txt`：复杂度高、成功率低，除非是最后手段。
- ❌ 生成 .bat 让用户双击：编码坑多，且把本该是 agent 的活外包回用户，用户要的是"你帮我操作"。

### 沙箱读不到关键文件
DSH 的 workspace-write 沙箱只放行工作区内的文件，`~/.video2md/config.json`、
`C:\Users\hfhfn\.claude\skills\...` 可能 read 不到。读不到就按"配置未就绪"处理，
直接给用户单行命令（config 默认即可跑，视觉模型 key 缺省时脚本会 fallback）。

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
- 抖音 web 接口须有效 cookie，yt-dlp 常报 `Fresh cookies needed`；此时改用浏览器抓 CDN 直链下载，
  完整步骤见 `references/douyin-cdn-direct.md`。抖音国内 CDN 走**直连**（勿走代理）。
- 请遵守平台条款与著作权，仅用于个人学习/研究等合法用途。
- 断点续传：已生成的中间产物自动跳过，可断点重跑。完成后默认自动清理 `.vid_*` 中间产物
  （需保留加 `--keep-intermediate`）。