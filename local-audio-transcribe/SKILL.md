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

2. 本 skill 自包含：命令 `python "$SK\scripts\xxx.py" ...` 中的 `$SK` = 本 SKILL.md 所在目录（`~\.skills-manager\skills\local-audio-transcribe`）。
3. 数据/模型宿主：env `RECORD_REVIEW_ROOT`（==`TRANSCRIBE_ROOT`）指向存放 `models\`（FunASR/VAD 模型缓存）、`inputs\`（录音）、`runs\`（转录产物）的项目目录；`--cache-dir`/`MODELSCOPE_CACHE` 指到 `<数据根>\models\ms`，Whisper 模型在 `<数据根>\models\hf`。代码、词库、热词、模板都随 skill（全局），**只有模型权重与录音/产物留在项目**。
4. 默认离线：要求模型已在本地缓存或通过 `--model-path`/`--cache-dir` 指定。离线模式下模型缺失应立即失败，不能偷偷联网下载。
5. 输出写入用户指定的独立目录，例如 `runs\2026-08-20-interview\`，不要复用或覆盖项目的 `output\` 历史结果。

## 标准流程

### A. FunASR 主稿

```powershell
python "$env:SK\scripts\run_funasr.py" "C:\path\recording.m4a" `
  --out-dir "C:\path\run" --out-label funasr `
  --spk-num 2 --hotwords-file "$env:SK\config\hotwords.json" `
  --cache-dir "$env:RECORD_REVIEW_ROOT\models\ms" --offline
```

生成 `funasr.raw.json` 和逐句 `funasr.transcript.txt`。raw 中含音频哈希、模型、设备、参数、热词和每句 source ID。

### B. 轮次视图

```powershell
python "$env:SK\scripts\postprocess.py" `
  --json "C:\path\run\funasr.raw.json" `
  --out "C:\path\run\funasr.turns.txt" `
  --out-json "C:\path\run\funasr.turns.json"
```

默认按 speaker 变化、约 900ms 静音、强标点和最大轮次长度重切。纯 filler 只在 TXT 视图中过滤，turns JSON 仍保留并标记 `is_filler`。

### C. Whisper 术语复核（可选）

```powershell
python "$env:SK\scripts\run_whisper.py" "C:\path\recording.m4a" `
  --out-dir "C:\path\run" --out-label whisper `
  --hotwords-file "$env:SK\config\hotwords.json" `
  --word-timestamps --offline
```

### D. 对齐候选（双引擎时运行）

```powershell
python "$env:SK\scripts\align_transcripts.py" `
  --funasr-json "C:\path\run\funasr.raw.json" `
  --whisper-json "C:\path\run\whisper.raw.json" `
  --terms-file "$env:SK\config\hotwords.json" `
  --out-json "C:\path\run\alignment.json" `
  --out-md "C:\path\run\alignment.md"
```

只把时间重叠、文本相似度和术语不一致作为证据；`needs_review` 必须由人工确认，不能把 Whisper 结果自动拷贝进主稿。

### E. 质量评分（有人工参考稿时）

```powershell
python "$env:SK\scripts\score_transcript.py" `
  --ref "C:\path\reference.txt" --hyp-json "C:\path\run\funasr.raw.json" `
  --terms-file "$env:SK\config\hotwords.json" `
  --out-json "C:\path\run\funasr.score.json" --engine-label funasr
```

全文相似度只是粗粒度趋势；重点查看术语 occurrence recall、漏句、重复和 speaker/时间段异常。参考稿没有某术语时显示 N/A，不要解读为识别率为 0。

## 目标输出格式（对标人工优质转写）

最终 `reviewed` 稿应收敛到人工优质转写（见 `evals/reference/*.txt`）的格式约定，便于与 gold 直接回测：

- 头元信息：`YYYY年M月D日 下午/上午 HH:MM|<时长>分 <秒>秒`。
- `关键词:` 段：逗号分隔的核心领域词。
- `文字记录:` 后的正文按 `说话人 N MM:SS` 起段的轮次排版（补全标点）。
- 书面体规范：数字与英文前后留空格（如 `3 年`、`BERT`、`agent`），统一术语拼写，去掉 ASR 填充式重复与语气词噪声。
- **说话人编号 = 本文件内事件顺序，不固定角色**。不要假设"说话人 1=面试官/说话人 2=候选人"；参考稿各文件编号不一，甚至一个录音有 3 位说话人。需要角色意义时，用语义标签（`--speaker-map` 输出 `面试官/候选人`），候选人 = 做自我介绍/被提问者，且候选人的自介内容最可信。

## 参考稿驱动的质量回测（逐步提高转录质量）

这是把"人工优质参考稿"变成持续提升杠杆的闭环；项目在 `evals/` 保存增量的 benchmark 语料与指标。

1. **建档**：新录音若有对应人工参考稿，把参考稿拷入 skill（`evals/reference/<case>.txt`），并追加一条 `evals/evals.json` 用例记录 gold 路径与最低术语召回期望。
2. **互证**：对最终稿运行互证报告，定位差异段与漏掉的术语：
   ```powershell
   python "$env:SK\scripts\compare_ref.py" `
     --ref "C:\path\reference.txt" --hyp-json "C:\path\run\funasr.reviewed.json" `
     --terms-file "C:\path\config\terms\technical-interview.json" `
     --out-md "C:\path\run\reference.compare.md"
   ```
   `compare_ref.py` 输出：参考术语召回明细、参考稿有而引擎(含别名)遗漏/音译的术语、引擎有而参考稿无的存疑点、以及相似度低的差异段。
3. **补漏 & 重出**：按"上下文可确认、宁缺毋滥"把新的 spoken_variant 修复别名写进项目词库（升 version），重跑 `make_reviewed.py` 重新生成最终稿。示例：`lgurap/lang rup→LangGraph`、`chain point→checkpoint`、`bird→BERT`、`muvers→Milvus`、`BGM 三→bge-m3`、`BM 二五→BM25`、`regas→RAGAS`。
4. **复测并记录**：重跑 `score_transcript.py`（对 `funasr.reviewed.json` 打分），把指标更新到 `evals/quality-baseline.json`，标注相对基线的提升。重点追踪**术语召回**（最敏感），相似度受音频质量/口音限制只能逐步逼近。
5. **存疑点只提示、不改参考稿**：参考稿偶有非最优（如"朗国3 MySql"），若引擎按语境更合理（Milvus），在报告中标注，不要回写参考稿。

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
python "$env:SK\scripts\manage_terms.py" resolve `
  --global-file "$env:SK\config\global-terms.json" `
  --project-file "C:\path\project\config\terms\technical.json" `
  --session-file "C:\path\run\session-terms.json" `
  --out "C:\path\run\terms-snapshot.json"

python "$env:SK\scripts\suggest_terms.py" `
  --alignment-json "C:\path\run\alignment.json" `
  --terms-file "C:\path\project\config\terms\technical.json" `
  --out "C:\path\run\term-suggestions.json"
```

人工确认后才显式批准，并默认沉淀到 project：

```powershell
python "$env:SK\scripts\manage_terms.py" approve `
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
