---
name: interview-coaching
description: 把面试录音转录的成果往前推进两级——自动做「面试分析 + 应试者备考清单」，并用「候选人跨场档案」把同一候选人的多场面试串起来。适用于：拿到一段面试/访谈录音或已转录的 run，想要自动得出该应试者的优劣势、被追问的技术纵深、下一场该怎么准备的场景；也适用于把同一候选人多场（如魏新龙×3）合并对比以判断其技术栈是否套路单一。依赖 local-audio-transcribe 做转录（先跑它或已产出 funasr.reviewed.*）。不要在未转录的孤立音频上凭空写分析、不要偏离"供应试者本人使用"的定位、不要跨场把不同候选人混为一个档案。
---

# interview-coaching — 面试分析 + 备考 + 跨场档案

在 `local-audio-transcribe` 的转录产物之上，把同一套流程跑到底：**转录 → 类型化分析 → 应试者备考清单 → 候选人跨场档案**。这是供**应试者本人**指导后续面试准备用的，不是给评审下结论。

## 定位与边界

- **输入**：一段已转录（`<run>/funasr.reviewed.json` + `<run>/alignment.json`）的面试，或一段原始音频（则先把转录委托给 `local-audio-transcribe`）。
- **输出**（都在 `<run>/interview/`，转录产物不动）：
  - `interview/analysis.json`（类型化，机器可比）
  - `interview/analysis.md`（可读分析稿）
  - `interview/备考清单.md`（应试者可背的备考交付物）
  - 以及 skill `profiles/<候选人>.json` 的**合并更新**（跨项目全局沉淀）。
- **跨项目复用**：术语词库、深挖题库、模板、候选人档案全部放在 skill 内（全局）；项目的转录器和项目术语经 env 解析、本地 `.coaching/coaching-settings.json` 可覆盖。换项目只需要让转录工具可被定位，积累的东西自动带过去。
- 说话人编号 = 本文件内事件顺序，**不是固定角色**；候选人是"说话最多的自介/被提问方"，其余为面试官/HR。

## 前置

1. 转录工具根：`TRANSCRIBE_ROOT` > `RECORD_REVIEW_ROOT` > record_review 默认。确认 `run_funasr.py`/`run_whisper.py` 等在。
2. 翻译已完成：存在 `funasr.reviewed.json` 与 `alignment.json`（否则按 `local-audio-transcribe` 先跑，48k/立体声输入先过 `scripts/transcode.py` 转 16k mono，兜住 Whisper 448 坑）。
3. skill 内脚本路径：本 SKILL.md 所在目录的 `scripts/`。记 `$SK = <skill dir>`。

## 流水线（一次性跑完整套；每步有产出，不阻塞）

### S0 预处理（如输入是原始音频）
```bash
python "$SK/scripts/transcode.py" <audio> --out <run>/audio_16k.wav   # 自动兜 48k/多声道
```
再按 `local-audio-transcribe` 生成 funasr/whisper/align/`make_reviewed`，得到 `funasr.reviewed.json`+`alignment.json`。

### S1 自动分析（脚本抽证据 + 你填语义）
```bash
# 1) 抽确定性证据
python "$SK/scripts/extract.py" \
  --reviewed <run>/funasr.reviewed.json --alignment <run>/alignment.json \
  --terms <project terms> --out <run>/interview/evidence.json
# 2) 初始化类型化分析骨架
python "$SK/scripts/analyze_schema.py" --schema "$SK/defaults/analysis-schema.json" \
  --init --target <run>/interview/analysis.json
```
然后由你（编排 LLM）**读 `funasr.reviewed.txt` + `evidence.json` + 候选人跨场档案**，把 analysis.json 的语义字段填成结论：
- `session` / `candidate.speaker_map`（说话最多=候选人）/ `role`（面试/跟进/HR收尾）
- `projects_note`、`qa_note`、`terms_note`：写成 markdown 语义段
- `tech_stack_summary`（候选主观技术栈）、`ambiguous_terms`（双引擎分歧/读音含糊、**宁缺毋滥**）、`pending_confirm`
- `strengths` / `strengths_note`、`risks` / `risks_note`、`depth_gaps`（{gap,evidence,priority}）
- `data_claims`（{metric,value,context}，供跨场一致性比对）、`recommended_prep`、`recommendation`
- 定期用 `analyze_schema.py --validate --target <run>/interview/analysis.json` 校验 schema 完整。

### S2 自动备考（bank + 本场缺口 + 档案，生成应试者清单）
```bash
python "$SK/scripts/bank.py" --bank "$SK/config/depth-questions.json" \
  --context "<含糊词/技术栈逗号串>" --gap "<深度缺口逗号串>" \
  --out <run>/interview/bank.json
```
由你按 `defaults/gap-prep.md.j2` + `analysis.json` 的语义字段，结合档案，**写 `<run>/interview/备考清单.md`**（应试者可背：深挖点、怎么答、示例话术）。渲染确定性骨架可用：
```bash
python "$SK/scripts/render.py" --template "$SK/defaults/gap-prep.md.j2" \
  --context <run>/interview/render-ctx.json --out <run>/interview/备考清单.md
```
`render-ctx.json = {"m": {meta}, "e": evidence, "a": analysis, "b": bank}`；`{{llm:...}}` 由你亲手填，`{{list:...}}` 自动展开。

### S3 沉淀（跨场档案合并，"成熟"核心）
```bash
python "$SK/scripts/profile.py" --analysis <run>/interview/analysis.json \
  --profiles "$SK/profiles" --project-tag <项目标识>
```
合并后档案自动给出：该候选人已在几场反复用同一批技术栈（`deep_terms`）、哪些含糊词尚未核清、指标跨场是否一致、`pattern_note`（"多人场同栈→警惕套路单一"）。同一候选人的下一场分析**必须先读档案**再写分析，别当新人。

## 积累约定（跨项目复用）

- **术语**：沿用 global(跨项目)<project(项目)<session(本次) 分层；全局放在 skill，项目放在项目 terms。保留既有积累不动。
- **题库**：`config/depth-questions.json` 全局累计；每发现一类可持续追问的缺口，向对应 group 增题（记 question/expected/triggers）。
- **档案**：`profiles/<候选名>.json` 全局累计，跨项目/跨场合并。
- **模板/schema**：`defaults/` 全局，项目可用 `.coaching/coaching-settings.json` 覆盖。
- **产物**：`<run>/interview/` 只放本次；仅档案写回 skill（全局）。原始 `funasr.raw.*` 永不覆盖。

## 质量原则（宁缺毋滥）

- 含糊词（boat/bot/define/CC三零这类读音含糊、说不出型号的）只在**双引擎互证或上下文极明确**时定案；否则记进 `ambiguous_terms` + `pending_confirm`，供复试当面核，**不强行判定**。
- 指标/技术栈来自转录可确认处；抽取证据（metrics/tech_stack）只是锚点，语义结论由你读文本判断——抽取不背锅，你也别只照着 evidence 复述。

## 验证

1. `python "$SK/scripts/analyze_schema.py" --validate --target <run>/interview/analysis.json` 通过。
2. 在 `<run>/interview/` 看到 `analysis.json`、`analysis.md`、`备考清单.md` 三件套 + `profiles/<候选名>.json` 被合并。
3. 一句话触发即可从一段音频一路跑完整个链条（本 SKILL.md 即单一编排点）。
4. 换项目：把 env 指向另一转录根，题库/档案/模板仍可用（跨项目自检）。