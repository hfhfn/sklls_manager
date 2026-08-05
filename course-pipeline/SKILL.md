---
name: course-pipeline
description: 把一门视频课程端到端转化为「结构化笔记 + 图文讲义 + 参考代码库」的编排入口。当用户想把一套课程视频做成学习资料、复用「视频→笔记→讲义→代码」整条流水线、或将本流程应用到一门新课程时使用。本技能负责总览与约定，具体阶段分派给 course-transcribe / course-notes / course-handout / course-code。
---

# course-pipeline — 课程资料流水线（编排入口）

把一门"边讲边写代码"的视频课程，端到端转成可学习、可导航的资料。四个阶段各由一个子技能负责：

```
.mp4 ──course-transcribe──▶ .txt ──course-notes──▶ notes/*.md ─┬─course-handout──▶ handouts/*.md (+图)
 (源)                     (转录)                  (结构化笔记)  └─course-code   ──▶ reconstructed_code/
```

## 目录约定（所有阶段镜像章节结构）
```
<课程根>/
  videos/第N章 .../X-Y 标题.mp4   # 源视频（按章分目录）
  .notes_intermediates/第N章/…txt # 转录（镜像源，逐字，保留 &amp; 与后缀）
  notes/第N章/X-Y 标题.md          # 结构化笔记（干净命名）
  notes/topics.json、notes/总索引.md
  handouts/第N章/X-Y 标题.md       # 图文讲义（+ assets/ 截图）
  reconstructed_code/              # 参考代码库
  skills/course-*/                 # 本套技能
```

## ⚠ 命名坑：`&amp;` vs `&`（务必先读）
部分源视频目录/文件名含**字面 HTML 实体 `&amp;`**（解压产物），少数还带 `【公众号：…】` 后缀。源视频当前统一放在 `videos/` 下。两套约定按阶段并存：
- **转录 `.notes_intermediates/`**：逐字镜像源名 → 保留 `&amp;` 与后缀。
- **笔记/讲义（手写产物）**：用**干净命名** `&amp;`→`&`（或"和"）、去后缀。`总索引.md`/`topics.json` 也用干净名。
- 因此笔记与转录**不按路径 1:1 对应**，按"课时号 + 主题"对应。
- 代码库文件名用英文，不受影响。

## 自带脚本与文档（技能已自包含，复用无需回原项目找）
每个子技能都把它引用的**当前项目文件随身携带**了一份，复制 `skills/course-*` 即得完整工具箱：

| 技能 | 自带文件 | 作用 |
|------|----------|------|
| course-transcribe | `scripts/transcribe.py` | ffmpeg + FunASR 批量转录（顶部 `ROOT` 需按新课程改） |
| course-notes | `scripts/gen_index.py` | 重建 `notes/总索引.md`（顶部 `ROOT` 需按新课程改） |
| course-code | `scripts/collate_code.py` | 汇总笔记代码块为 code map（用相对路径，无需改） |
| course-handout | `scripts/extract_frames.py` | ffmpeg 场景抽帧（用相对路径，无需改） |
| course-pipeline | `references/执行流程.md` | 端到端权威工作流文档（环境规格、GPU 设置、各阶段流程） |

> 本仓库根目录另放了 `transcribe.py` / `gen_index.py` 便于就地运行；它们与技能自带副本逻辑一致。`transcribe.py`、`gen_index.py` 的 `ROOT` 是绝对路径常量，脚本放哪都行，但**换课程必须先改 `ROOT`**。

## 接入一门"新课程"的做法
1. 把整套 `skills/course-*`（含各自 `scripts/`、`references/`）复制到新课程根目录（或装到 `~/.claude/skills/` 全局用）——工具与文档一并带走。
2. 改两处绝对路径常量：`course-transcribe/scripts/transcribe.py` 与 `course-notes/scripts/gen_index.py` 顶部 `ROOT`（副本已在该行上方加提示）。
3. 依次触发：`course-transcribe` → `course-notes` → `course-handout` / `course-code`。
4. 建议**先在 1 个代表章试点**，质量满意后再全量。

## 批处理范式：并行子代理 fan-out（已在本仓库验证）
逐课时/逐文件的重复工作，用并行子代理成组分派，比串行快一个数量级：
- 按"章"或"课时区间"分组，每组一个子代理，各自读文件、产出、写盘或返回结构化结果。
- 一条消息里发多个 Agent 调用即并发执行；产出建议各写独立文件再由主代理合并校验（避免竞态）。
- 参考：本仓库曾用 5 个并行子代理为 204 个课时生成 `topics.json`，合并后 0 缺失 0 冗余。
- 体量极大且用户显式开启时，可改用 Workflow 工具做确定性编排（pipeline/parallel + schema）。

## 完整性自检
```bash
find videos -name "*.mp4" | wc -l     # 视频数
find .notes_intermediates -name "*.txt" | wc -l
find notes -name "*.md" ! -name "总索引.md" | wc -l
find handouts -name "*.md" | wc -l
```
四者应对齐（讲义可只覆盖已处理章节）。
