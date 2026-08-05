---
name: course-handout
description: 把纯文字课程笔记升级为「图文混排教学讲义」——按内容自动内嵌 Mermaid 图表（架构/流程/时序/数据模型），并对演示/UI/终端类课时用 ffmpeg 抽取关键截图配图。当用户希望把笔记做成讲义、增加便于理解的图、图文混排、生成配图版教程时使用。产出为增强版 Markdown，写入独立 handouts/ 目录，保持 notes/ 纯净。
---

# course-handout — 笔记 → 图文混排讲义

把 `notes/**/*.md` 的纯文字笔记，升级成带图的**教学讲义**（增强版 Markdown）。图有两类来源：
1. **Mermaid 图表**（主）：从笔记内容自动生成，GitHub/编辑器原生渲染，无需构建。
2. **关键截图**（辅）：仅对演示/UI/终端类课时，用 ffmpeg 抽帧 + 视觉筛选。

> 本环境无照片级 AI 生图，"配图"= 生成图表 + 抽视频截图，二者互补。

## 输入 / 输出
- 输入：`notes/<章>/<课时>.md`（正文）、`.notes_intermediates/<章>/<课时>.txt`（转录，补细节）、`videos/<章>/<课时>.mp4`（抽截图用）。
- 输出：`handouts/<章>/<课时>.md`（增强副本）+ `handouts/<章>/assets/<课时>-NN.png`（截图）。**不改动 `notes/`**。

## 步骤（建议用并行子代理，一课时一个）

### 1. 判断配图类型并生成 Mermaid
子代理读"笔记 + 转录"，按内容选图（可多张，插在对应小节后）：
| 内容特征 | 图类型 |
|---|---|
| 架构 / 模块关系 / 分层 | `flowchart` 或 `classDiagram` |
| 处理流程 / 调用链 / 步骤 | `flowchart` 或 `sequenceDiagram` |
| 交互时序（push/pop、请求-响应、Agent 循环）| `sequenceDiagram` |
| 数据库表 / 领域模型 / 字段关系 | `erDiagram` 或 `classDiagram` |
| 状态机 / 生命周期 | `stateDiagram-v2` |
| 对比 / 清单 | 保留原表格，不强行画图 |

规则：
- 图**服务理解**，宁缺毋滥；纯概念/口水课可以不加图。
- Mermaid 节点文案用中文；**只表达笔记里已有的信息，不臆造**。
- 每张图配一句 `> 图：<说明>` 标注。
- 校验语法：确保 ```mermaid 块能渲染（节点 id 用字母数字，中文放引号内，避免特殊字符破坏语法）。

### 2. 关键截图（仅演示/UI/终端类课时）
判定：课时含产品演示、前端 UI、Postman/终端输出、浏览器操作等"看画面才懂"的内容才做；纯代码讲解/纯概念**跳过**。
```bash
# 抽候选帧（场景检测）
python skills/course-handout/scripts/extract_frames.py \
  --video "videos/<章>/<课时>.mp4" --out "handouts/<章>/assets/_cand_<课时>" --threshold 0.35 --max 24
```
- 视觉子代理 `Read` 候选 PNG，挑 1–3 张真正有信息量的（幻灯片/架构图/终端结果/UI/Postman），其余忽略。
- 选中的重命名为 `handouts/<章>/assets/<课时>-01.png` 等，删除 `_cand_*` 临时目录。
- 正文相应位置内嵌：`![<中文标题>](assets/<课时>-01.png)`。

### 3. 组装讲义
- 以原笔记为骨架，在合适小节后插入 Mermaid 图与截图，保留原有摘要/正文/核心要点结构。
- 顶部可加一句"本讲义在笔记基础上补充图示，便于理解"。
- 写入 `handouts/<章>/<课时>.md`。

## 验证
- 抽查若干讲义：Mermaid 能渲染、截图切题且路径正确（相对 `assets/`）、图文与正文对应。
- 试点先做单章，质量满意后再全量（并行子代理）。

## 命名坑
源视频目录/文件名可能含字面 `&amp;`（见 `course-pipeline`）。`handouts/` 沿用与 `notes/` 一致的**干净命名**（`&amp;`→`&`），截图 `assets/` 路径用课时号，避免特殊字符。
