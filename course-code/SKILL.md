---
name: course-code
description: 从课程笔记（含代码块的 Markdown）重建一套结构化的「参考代码库」。当用户希望根据视频课程/笔记生成配套完整代码、把散落在各课时的代码片段整理成可导航的项目、或复原课程所讲项目的源码结构时使用。产出按 DDD/模块目录组织、命名一致、并明确标注「AI 重建·尽力还原」，不保证零改动即可运行。
---

# course-code — 笔记 → 结构化参考代码库

把一门编程课程散落在 `notes/**/*.md` 里的代码块，重建成一套结构完整、命名一致的**参考代码库**。适用于任何"边讲边写代码"的课程（本仓库的样例是 MoManus：FastAPI + DDD 后端、Next.js 前端、Docker 沙箱）。

## 重要前提与诚实声明
- 笔记里的代码是从视频转录 + Claude 重建而来，约 90% 完整，但存在**跨课时缺口**和**少量 ASR 错漏**（如 `store` 被听成 `story`、缺顶部 import、缺 `logger = logging.getLogger(...)`）。
- 目标是**结构化参考代码库**：能读、能导航、结构自洽、语法通过 `py_compile`；**不保证**缺少真实 DB/Redis/Docker 时零改动即可运行。产出必须在 `README.md` 里如实写明这一点与 known-gaps。
- **绝不臆造**笔记/转录中不存在的业务逻辑。缺口就在 known-gaps 里标注 `# TODO: 课程未展示完整实现`。

## 输入
- `notes/`：结构化课程笔记（每章一目录，课时 `X-Y 标题.md`）。
- 可选 `.notes_intermediates/`：原始转录，用于补全笔记中被省略的上下文。

## 步骤

### 1. 构建代码地图
```bash
python skills/course-code/scripts/collate_code.py --notes notes --lang python --out .code_map.json
# 试点单章：加 --chapter 8
```
输出 `.code_map.json`：每个代码块带 `lesson / heading / path_hints / symbols / code`。前端代码另跑一次 `--lang tsx`（及 `ts/js`）。

### 2. 规划目标目录树
读代码地图的 `path_hints` 与 `symbols`，结合 DDD 分层惯例，规划文件树。后端典型分层：
```
backend/app/
  interface/       # 协议(Protocol)、API 路由、schema
  application/     # 用例编排、TaskRunner
  domain/          # 领域模型、Agent、Tool 基类
  infrastructure/  # DB、Redis、COS、外部 SDK 封装
  core/            # 配置、日志、异常、依赖注入
  main.py
```
前端 `frontend/`（Next.js）、沙箱 `sandbox/`。包配置：`pyproject.toml`/`requirements.txt`（据 uv 相关课时）、`package.json`、`Dockerfile`（据部署章）。

### 3. 按目标文件跨课时综合合成（用并行子代理）
对每个目标文件派一个子代理，交给它该文件相关的**全部**代码块（同一类/模块常在多课时被逐步精修，**以最后最完整的版本为准**并合并增量）。要求子代理：
- 合并同一符号的多次迭代，取最终形态；补全顶部 import、`logger` 定义等明显遗漏。
- 修正 ASR/命名错漏，统一模块路径（如统一 `app.infrastructure.store`）。
- 缺口用 `# TODO: 课程未展示完整实现` 标注，**不臆造**。
- 返回：文件相对路径 + 完整文件内容 + 该文件的 known-gaps 列表。
参照本仓库已验证的并行 fan-out 做法（见 `course-pipeline`）。

### 4. 组装与体检
- 写入 `reconstructed_code/` 目录树；生成包配置文件。
- Python 语法体检：`python -m py_compile $(find reconstructed_code -name '*.py')`，修正报错。
- 写 `reconstructed_code/README.md`：项目结构说明 + **「AI 重建·尽力还原」声明** + 汇总的 known-gaps 清单 + 运行所需外部依赖（Postgres/Redis/Docker）。

## 约定
- 试点先做单章（`--chapter N`）验证质量，再全量。
- 输出目录 `reconstructed_code/` 与 `notes/`、`handouts/` 平级，互不覆盖。
- 命名坑：源视频目录含字面 `&amp;`，但代码库文件名用干净英文，不受影响。
