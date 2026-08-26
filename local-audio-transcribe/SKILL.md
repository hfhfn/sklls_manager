---
name: local-audio-transcribe
description: 将本地音频录音（.wav、.m4a、.mp3、.flac、.ogg、.aac 等）离线转成带时间戳的结构化文字稿；适用于中文会议、面试、访谈、双人或多人录音，以及需要说话人区分、中文/英文技术术语、热词、转录质量评估或人工修订候选的任务。只要用户给出本地音频路径并要求转文字、录音整理、ASR、区分说话人或提高术语准确率，即使没有明确说要使用 Skill，也优先使用本 Skill。不要用于视频画面 OCR/描述、在线视频字幕下载或默认云端上传。
---

# local-audio-transcribe — 本地离线音频转录

使用本地模型和当前项目的 CLI，把音频转为**可追溯**的原始识别结果、说话人轮次和可选的双引擎复核报告。模型和录音都保留在本机，不把音频上传到云端。

## 适用边界

- 输入必须是本地音频路径；先确认文件存在、格式和大致时长。
- 默认主引擎是 FunASR Paraformer：中文正文、毫秒时间戳和匿名说话人聚类。
- 需要中英混合技术术语时并行使用 faster-whisper large-v3；它是复核候选，不替换 FunASR，也不提供可信的 speaker 标签。
- 不把匿名 `spk=0/1` 当作真实姓名；角色映射只能由用户明确指定。
- 原始 JSON 永远不覆盖；任何纠错都只生成审核候选或新的 reviewed 文件。
- 视频需要画面 OCR/描述时使用 `video2markdown`；在线音频/视频下载不属于本 Skill。

## 前置检查

2. 查找工具根目录：优先使用环境变量 `RECORD_REVIEW_ROOT`，否则使用当前项目路径 `C:\Users\hfhfn\Desktop\code\students_project\record_review`。确认其中有 `run_funasr.py`、`run_whisper.py`、`manage_terms.py` 和 `suggest_terms.py`。
3. 使用已有 conda 环境（本机通常是 `llm_gpu`），确认 FunASR、torch 和可选 faster-whisper 已安装。
4. 默认离线：要求模型已在本地缓存或通过 `--model-path` 指定。离线模式下模型缺失应立即失败，不能偷偷联网下载。
5. 输出写入用户指定的独立目录，例如 `runs\2026-08-20-interview\`，不要复用或覆盖项目的 `output\` 历史结果。

## 标准流程

### A. FunASR 主稿

```powershell
python "$env:RECORD_REVIEW_ROOT\run_funasr.py" "C:\path\recording.m4a" `
  --out-dir "C:\path\run" --out-label funasr `
  --spk-num 2 --hotwords-file "$env:RECORD_REVIEW_ROOT\config\hotwords.json" `
  --cache-dir "$env:RECORD_REVIEW_ROOT\models\ms" --offline
```

生成 `funasr.raw.json` 和逐句 `funasr.transcript.txt`。raw 中含音频哈希、模型、设备、参数、热词和每句 source ID。

### B. 轮次视图

```powershell
python "$env:RECORD_REVIEW_ROOT\postprocess.py" `
  --json "C:\path\run\funasr.raw.json" `
  --out "C:\path\run\funasr.turns.txt" `
  --out-json "C:\path\run\funasr.turns.json"
```

默认按 speaker 变化、约 900ms 静音、强标点和最大轮次长度重切。纯 filler 只在 TXT 视图中过滤，turns JSON 仍保留并标记 `is_filler`。

### C. Whisper 术语复核（可选）

```powershell
python "$env:RECORD_REVIEW_ROOT\run_whisper.py" "C:\path\recording.m4a" `
  --out-dir "C:\path\run" --out-label whisper `
  --hotwords-file "$env:RECORD_REVIEW_ROOT\config\hotwords.json" `
  --word-timestamps --offline
```

### D. 对齐候选（双引擎时运行）

```powershell
python "$env:RECORD_REVIEW_ROOT\align_transcripts.py" `
  --funasr-json "C:\path\run\funasr.raw.json" `
  --whisper-json "C:\path\run\whisper.raw.json" `
  --terms-file "$env:RECORD_REVIEW_ROOT\config\hotwords.json" `
  --out-json "C:\path\run\alignment.json" `
  --out-md "C:\path\run\alignment.md"
```

只把时间重叠、文本相似度和术语不一致作为证据；`needs_review` 必须由人工确认，不能把 Whisper 结果自动拷贝进主稿。

### E. 质量评分（有人工参考稿时）

```powershell
python "$env:RECORD_REVIEW_ROOT\score_transcript.py" `
  --ref "C:\path\reference.txt" --hyp-json "C:\path\run\funasr.raw.json" `
  --terms-file "$env:RECORD_REVIEW_ROOT\config\hotwords.json" `
  --out-json "C:\path\run\funasr.score.json" --engine-label funasr
```

全文相似度只是粗粒度趋势；重点查看术语 occurrence recall、漏句、重复和 speaker/时间段异常。参考稿没有某术语时显示 N/A，不要解读为识别率为 0。

## 术语词库与自动管理

不要把某次录音的专名、业务词或 ASR 误识别写入全局词库。按以下层级加载，优先级从低到高为：

```text
global 通用词库 < project 项目词库 < session 本次录音词库 < 本次命令行临时词
```

- 全局词库：只放跨主题、低歧义、人工确认过的词，例如 API、JSON、Python、OCR。
- 项目词库：放当前客户/领域长期复用的术语；用户确认的新术语默认写入这里。
- session 词库：放本次录音的姓名、客户名、产品名、临时简称；绑定本次音频 SHA-256，默认不能跨音频使用。
- `term-suggestions.json`：双引擎产生的候选，状态为 `proposed`，不得直接传给 ASR。

候选只在可靠时间对齐、跨引擎重复或有用户提供的上下文锚点时生成。单次 ASR 错误、普通短词、语气词和未确认的人名/公司名都不能自动升级为术语。即使识别结果看起来像标准词，也要保留 observed variant 和音频时间证据。

需要管理词典时使用项目工具：

```powershell
python "$env:RECORD_REVIEW_ROOT\manage_terms.py" resolve `
  --global-file "$env:USERPROFILE\.claude\skills\local-audio-transcribe\config\global-terms.json" `
  --project-file "C:\path\project\config\terms\technical.json" `
  --session-file "C:\path\run\session-terms.json" `
  --out "C:\path\run\terms-snapshot.json"

python "$env:RECORD_REVIEW_ROOT\suggest_terms.py" `
  --alignment-json "C:\path\run\alignment.json" `
  --terms-file "C:\path\project\config\terms\technical.json" `
  --out "C:\path\run\term-suggestions.json"
```

人工确认后才显式批准，并默认沉淀到 project：

```powershell
python "$env:RECORD_REVIEW_ROOT\manage_terms.py" approve `
  --suggestions "C:\path\run\term-suggestions.json" `
  --candidate-id term-candidate-00001 --canonical "官方术语" `
  --scope project --target-file "C:\path\project\config\terms\technical.json" `
  --history "C:\path\project\config\terms\approved-history.jsonl"
```

批准术语不等于自动修改旧转录；正文修订仍走审核 patch 流程。
- 优先人工检查：姓名、公司名、数字、日期、金额、身份证号、法律/业务结论、抢话段和录音尾部。
- 术语表只产生偏置和候选，不保证识别正确。出现 `BERT→波尔特`、`RAG→IG`、`企查查→喜察察` 等情况时，先在 alignment 中确认时间和上下文，再决定修订。
- 审核 patch 使用 `apply_revisions.py`；默认只校验并写日志，只有显式 `--apply` 才产生新的 reviewed 文件。不要编辑 raw JSON。
- 输出中明确区分 `raw`（引擎原文）、`turns`（可追溯分段）、`alignment`（双引擎候选）、`reviewed`（人工确认后副本）。

## 常见故障

- 模型缺失：检查 `models\ms`、`models\hf` 或传入本地模型目录；不要在 `--offline` 下反复重试联网。
- GPU 显存不足：降低 FunASR `batch_size_s`（需要在引擎脚本中调整）或 Whisper `compute-type`，先单引擎运行。
- 开场/尾部漏字：做 FunASR 与 Whisper 的 VAD A/B；检查音频是否双声道，若左右声道分别对应两人，优先拆声道后独立识别。
- 中英术语不稳：使用 `config/hotwords.json` 并运行 Whisper 复核；不要只依赖全文字符相似度。
- 说话人标签漂移：speaker ID 是当前录音内的匿名聚类，不能跨录音比较；必要时显式提供 `--speaker-map`。
