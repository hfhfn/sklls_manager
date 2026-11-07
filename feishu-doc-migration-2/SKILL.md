---
name: "feishu-doc-migration"
description: "使用 lark-cli 将飞书文档（知识库节点或独立云文档）完整迁移到目标知识库，支持递归子文档、图片附件、格式保留、内部引用修复、子节点排序。当用户需要迁移飞书文档/知识库时调用。"
---

# 飞书文档迁移工具

使用 lark-cli API 将飞书文档完整迁移到目标知识库，保留全部格式、图片、附件、内部引用和子节点顺序。

支持两种源：
- **知识库节点**（`/wiki/` 链接，或已在知识库中的文档）→ 递归迁移整棵文档树
- **独立云文档**（`/docx/` 链接但不在任何知识库中）→ 按单篇文档迁移，无子节点

## 何时使用

- 用户要求迁移飞书文档/知识库到另一个空间
- 需要批量迁移文档树（父文档 + 所有子文档）
- 源链接是 `/docx/` 独立云文档（不在知识库中），需要归入某个知识库
- 源文档有复制保护，无法直接复制粘贴
- 需要保留表格、代码块、引用、图片等所有格式
- 需要修复迁移后的内部文档引用链接

## 前置条件

1. **lark-cli 已安装并认证**（用户身份）
   - 验证命令：`lark-cli auth status`
   - 未认证时先引导用户完成授权

2. **源文档访问权限**：当前用户需能读取源文档内容
   - 复制保护的文档也可以迁移（使用 media-preview 回退机制）

3. **目标知识库权限**：当前用户需有目标知识库的编辑/创建权限

## 核心脚本

脚本位置（同目录下）：

| 脚本 | 用途 |
|------|------|
| `Migrate-FeishuDocs.ps1` | 主迁移脚本：扫描文档树、创建节点、填充正文、绑图、修内部引用、写 checkpoint |
| `Verify-MigrationTree.ps1` | 迁移后层级校验与修正（只 move 不删） |
| `Fix-EmbeddedBlocks.ps1` | 迁移后补全内嵌表格数据与画板（块级插入，不重写整篇） |

### 功能特性

| 功能 | 说明 |
|------|------|
| 递归迁移 | 自动遍历并迁移整棵文档树（父 + 所有子文档） |
| 独立云文档 | 源链接不在知识库中时，自动回退 `drive +inspect` 解析，按单篇迁移 |
| 格式保留 | XML 直搬，不经过 Markdown 转换，保留标题/列表/表格/代码块/引用 |
| 图片迁移 | 下载 → 上传 → 替换引用，复制保护文档自动回退到 media-preview |
| 文件附件 | 支持 file 类型节点迁移（下载 + 上传 + 自动创建 wiki 子节点） |
| 内部引用修复 | sub-page-list、@文档引用、文档链接全部更新为新文档地址 |
| 子节点排序 | 按源文档顺序依次创建，保持完全一致的排列顺序 |
| 根目录/子节点 | 支持迁移到知识库根目录，或指定父节点下 |
| 失败清理 | 内容填充失败时自动删除刚创建的空节点，不留重复空文档 |
| 事务与续跑 | checkpoint 三态（success / partial / failed），断点续跑复用已存在节点，不跳过错漏节点 |
| 内嵌块规范化 | 迁移前把跨空间必然失败的 `<sheet token>` / `<whiteboard token>` 转成可重建形态，避免内容静默丢失 |
| 按图分块 | 自动按「字符数 + 图片数」切批，同步块/网格内多图不再因绑定歧义整篇失败 |
| 错误重试 | 指数退避重试机制，默认 3 次 |
| 进度输出 | 实时进度条 + 彩色日志 |
| 结果日志 | 生成 JSON 结果映射表 + 日志文件 |

### 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `-SourceWikiUrls` | ✅ | 源文档 URL 数组，可混传 `/wiki/` 与 `/docx/` 链接 |
| `-TargetSpaceId` | ✱ | 目标知识库空间 ID（迁移到根目录时用） |
| `-TargetParentWikiUrl` | ✱ | 目标父节点 Wiki URL（迁移到指定节点下时用） |
| `-WorkDir` | - | 临时工作目录（默认 `.\lark_migration_temp`）。可放在任意位置：图片下载时子进程会在输出目录内运行，以满足 lark-cli 的写入白名单限制 |
| `-MaxRetries` | - | API 最大重试次数（默认 3） |
| `-RetryBaseDelay` | - | 重试基础延迟秒数（默认 3，指数退避） |
| `-AsUser` | - | 调用身份：`user` / `bot`（默认 `user`） |
| `-FixInternalRefs` | - | 是否修复内部引用（默认 `$true`） |
| `-MaxImgsPerChunk` | - | 每次写入最多携带的图片数（默认 1）。同步块 / 网格内多图时，单个 chunk 带多张图会触发 `bind_ambiguous`，保持默认 1 最稳 |
| `-OnlyRetryFailed` | - | 续跑时只重试 `status=failed`，把 `partial`（正文已写入、图片无导出权限）视为完成，避免反复重跑已迁好的文档 |

> ✱ `-TargetSpaceId` 和 `-TargetParentWikiUrl` 二选一

### 使用示例

#### 示例 1：迁移到知识库根目录

```powershell
.\Migrate-FeishuDocs.ps1 `
  -SourceWikiUrls @("https://source.feishu.cn/wiki/xxxxxxxx") `
  -TargetSpaceId "7687020534646754274"
```

#### 示例 2：迁移到指定父节点下

```powershell
.\Migrate-FeishuDocs.ps1 `
  -SourceWikiUrls @("https://source.feishu.cn/wiki/xxxxxxxx") `
  -TargetParentWikiUrl "https://my.feishu.cn/wiki/yyyyyyyy"
```

#### 示例 3：批量迁移多个根文档

```powershell
.\Migrate-FeishuDocs.ps1 `
  -SourceWikiUrls @(
    "https://source.feishu.cn/wiki/aaaaaaa",
    "https://source.feishu.cn/wiki/bbbbbbb",
    "https://source.feishu.cn/wiki/ccccccc"
  ) `
  -TargetSpaceId "7687020534646754274" `
  -WorkDir ".\my_migration" `
  -MaxRetries 5
```

#### 示例 4：迁移独立云文档（不在知识库中的 /docx/ 链接）

```powershell
.\Migrate-FeishuDocs.ps1 `
  -SourceWikiUrls @(
    "https://your.feishu.cn/docx/KiKCdQyhwo1qI8x5odpcdTc1nsb",
    "https://your.feishu.cn/docx/CHSsdWwVxo8mTqxcDU3c6CLAn7d"
  ) `
  -TargetSpaceId "7687104089611602876"
```

脚本会先用 `wiki +node-get` 判断是否为知识库节点；返回 `131005 document is not in wiki` 时自动回退到 `drive +inspect`，按单篇文档迁移。

## 工作流程

### 两阶段迁移

**第一阶段：文档迁移**
1. 扫描源文档树（深度优先遍历，保持原始顺序）
2. 按顺序逐个迁移节点：
   - **docx 文档**：读取 XML → 下载图片/附件 → 创建 wiki 节点 → overwrite 填充内容
   - **file 附件**：下载文件 → 上传到目标 wiki 节点下 → 自动成为子节点
3. 记录新旧 token 映射表

**第二阶段：内部引用修复**
1. 遍历所有迁移后的 docx 文档
2. 修复以下类型的内部引用：
   - `<sub-page-list>` 的 space-id / wiki-token
   - `<sub-page doc-id="...">`
   - `<cite type="doc" doc-id="...">`（@文档引用）
   - `<a href="...feishu.cn/wiki/TOKEN">`（Wiki 链接）
   - `<a href="...feishu.cn/docx/TOKEN">`（Docx 链接）
3. `doc-id` 既可能是文档 `obj_token`，也可能是 wiki 节点 token，脚本对两种都做映射
4. 仅修复迁移范围内的文档引用，外部链接保持不变

### 输出文件

每次运行会在工作目录生成：
- `migration_YYYYMMDD_HHMMSS.log` — 完整执行日志
- `migration_results_YYYYMMDD_HHMMSS.json` — 迁移结果映射表

JSON 结果包含：
```json
{
  "total_migrated": 21,
  "total_failed": 0,
  "documents": { "source_node_token": { "title": "...", "target_obj_token": "...", ... } },
  "doc_id_mapping": { "source_doc_id": "target_doc_id" },
  "wiki_token_mapping": { "source_wiki_token": "target_wiki_token" }
}
```

## 已知平台限制与降级策略

这些限制**不会返回错误**，块会被服务端静默丢弃或降级（`ok=true`，只在 `data.warnings` 里提示），是迁移后"文档看起来少了内容"的主要原因。脚本已内置防护，手工补迁时需按同样方式处理。

| 源内容 | 现象 | 根因 | 正确处理 |
|--------|------|------|----------|
| `<sub-page-list space-id wiki-token>` | 该块及其后内容整段丢失 | 跨空间 sub-page-list 不兼容 | 必须收敛为 `<sub-page-list/>`（脚本自动做），不要带 space-id/wiki-token |
| `<synced-source>` 内的 `<img>` | `1061044 / bind_ambiguous`，图片不显示 | 同步块内部节点不允许绑定本地图片 | 把图片移到同步块之后（`Normalize-EmbeddedBlocks` 已自动处理） |
| `<grid>` 列内的 `<img>` | 同上 | 列容器内的图片绑定歧义 | 含图 grid 扁平化：列内子节点按顺序插到 grid 之后 |
| `<sheet token sheet-id>` | `degrade_code 2113 Sheet content copy failed`，表格消失 | 跨空间电子表格不随文档复制 | 改为 `<sheet type="blank"/>`，迁移后用 `sheets +csv-get / +csv-put` 回填数据（保持可编辑） |
| `<whiteboard token>` | `2105 Whiteboard clone failed`，画板空白 | 跨空间画板不能 clone | mermaid 类型：`<whiteboard type="mermaid">源码</whiteboard>` 内联重建；手绘画板：`whiteboard +export --output-type raw` → 新建 blank 画板 → `whiteboard +update --input_format raw --overwrite` |
| `<synced_reference>` | 目标里只剩空占位 | 它是**引用块**（内容在公共区块文档里），不是子文档；跨空间引用失效 | 先判断业务属性：正文类可静态复制内容进来，广告/导航类通常不补 |
| 单篇 overwrite 很大 | `server time out error` | 单次请求负载过大 | 首块 `overwrite` + 后续 `append` 分块（脚本自动，默认 200000 字符/批） |
| 一个 chunk 多张图 | `bind_ambiguous` | 图片绑定按顺序对位，批量大易歧义 | `-MaxImgsPerChunk 1`（默认），按图片数也切批 |

### PowerShell 调用 lark-cli 的固定写法

- **含 `[ ]` 的标题/目录**：`Set-Location`、`Test-Path`、`Out-File -FilePath`、`Get-ChildItem -Path` 都会按通配符解析并报"路径未解析"。一律用 `-LiteralPath`；切目录用 `Start-Process -WorkingDirectory` 或 `-LiteralPath`。
- **`@./content.xml` 的相对路径基准**：由子进程的 `WorkingDirectory` 决定，不是调用方 cwd。自己封装 `Invoke-LarkCli` 时必须显式设置 `ProcessStartInfo.WorkingDirectory`。
- **函数传参**：`Get-DocContent($token, $dir)` 会把逗号表达式当成**一个数组参数**传入，导致 `$WorkingDir` 为空。必须用命名参数 `Get-DocContent -DocToken $t -WorkingDir $d`。
- **运行 PowerShell 7**：读取 UTF-8 的 `migration_checkpoint.jsonl` 必须用 `pwsh -NoProfile -File`；Windows PowerShell 5.1 会乱码、JSON 解析失败，统计数量凭空少一半。

## 事务语义与断点续跑

checkpoint 位于 `<WorkDir>/migration_checkpoint.jsonl`，每完成一个节点**追加**一行，同一 `source_node_token` 后写的覆盖先写的。

| status | 含义 | 续跑行为 |
|--------|------|----------|
| `success` | 正文完整、图片全部绑定 | 跳过 |
| `partial` | 正文已写入，但有图片未绑定 / 内嵌块被降级 | **复用已存在节点**重试填充，不重复创建节点；`-OnlyRetryFailed` 时视为完成 |
| `failed` | 正文未写入 | 清理刚创建的空节点后重建（有子节点的保留节点，只重填内容） |

规则：
- 续跑就是**用同样的命令再跑一次**，脚本按 checkpoint 决定跳过 / 重填；需要只补失败项时加 `-OnlyRetryFailed`。
- 绝不"因为节点已存在就无条件跳过"——那是旧版丢内容的原因。
- 调整层级**只做 move**（`Verify-MigrationTree.ps1 -Fix`），不删除、不重建。删除会连带子节点，代价远高于移动。
- 中断（Ctrl+C）不会触发空节点清理，重跑前先看目标目录有没有同名空文档。

## 迁移后强制核验清单

四项全部通过才算迁移完成，缺一项都可能藏着静默丢失：

1. **节点数 1:1**：checkpoint 去重后的条目数 == 源树节点数 == 目标树节点数
2. **层级无错位**：`Verify-MigrationTree.ps1` 输出 `mismatch = 0`，且 `status != success = 0`
3. **图片零失败**：每篇 `image_bind_failed = 0`，源/目标 `<img` 计数一致，源图片 src 在目标中重叠数为 0
4. **内嵌对象逐篇计数一致**：源与目标的 `<sheet` / `<whiteboard` 数量必须相同（数量相同 ≠ 有数据，还要抽查表格内容）

### 层级校验：Verify-MigrationTree.ps1

```powershell
pwsh -NoProfile -File .\Verify-MigrationTree.ps1 `
  -CheckpointFile ".\migrate\migration_checkpoint.jsonl" `
  -TargetParentToken "LtigwlhiCirA24ksMAGc3KvwnCh" `
  -SpaceId "7687104096158878649"
```

- 一次性 `wiki +node-list --page-all --page-limit 0` 拉全目标树再比对，不做逐节点 `node-get`，大知识库也很快。
- 输出 `checkpoint unique / target nodes / mismatch / status != success` 四项统计。
- 加 `-Fix` 只对 `parent mismatch` 执行 `wiki +move`，**不删除任何节点**；`MISSING` 和"父节点未迁移"会跳过并打印。
- 必须用 `pwsh` 运行。

### 内嵌块补全：Fix-EmbeddedBlocks.ps1

迁移脚本只保证"块在、可编辑"，表格数据与手绘画板内容需要这个脚本补：

```powershell
pwsh -NoProfile -File .\Fix-EmbeddedBlocks.ps1 `
  -WorkRoot ".\migrate" `
  -CheckpointFile ".\migrate\migration_checkpoint.jsonl" `
  -FillSheets `
  -MarkSuccess `
  -ContinueOnError
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `-WorkRoot` | ✅ | 迁移工作目录，递归查找每篇文档子目录里的 `content.xml`（子目录名以源 token 前 8 位开头） |
| `-CheckpointFile` | ✅ | checkpoint 路径，用于取 `target_obj_token` 与标题 |
| `-OnlyTitle` | - | 只处理标题包含该子串的文档 |
| `-DryRun` | - | 只打印"计划修复几个块、插入模式与锚点"，不写入 |
| `-FillSheets` | - | 建完空白表后回填源表 CSV 数据 |
| `-MarkSuccess` | - | 全部修复成功且回填 0 失败时，把 checkpoint 的 `partial` 归位为 `success` |
| `-ContinueOnError` | - | 单篇失败继续下一篇 |

实现要点（手工修复时同理）：
- **块级插入，不重写整篇**：用 `block_insert_after` / `block_replace`，绝不用 `overwrite`，避免二次破坏正文和已绑定图片。
- **锚点对齐**：源/目标顶层块按 `tag|文本` 签名顺序对齐；`ul/ol/grid/callout` 等容器**没有 block id**，`block_insert_after` 会静默"插入 0/1 块"。此时改用 `block_replace`，把"下一个有 id 的块"替换为 `[新块 + 原块 OuterXml（去掉 id）]`，位置与内容都不丢。
- **顺序**：同一文档多个缺失块用 `$curAnchor` 串联（上一块插入返回的 `block_id` 作为下一块的锚点）。
- **已存在即回填**：迁移阶段已把 token 表格/画板规范化为 blank，目标侧块通常已存在。脚本会识别这种情况，直接对已有块 `csv-put` 回填 / 画板 raw 导入，不重复插入；只有块真的丢了才走插入路径。两条路径互补，规范化块被服务端再丢弃也不会漏。
- **回填表格**：`sheets +csv-get` 拿 `annotated_csv`，用 `(?m)^\[row=\d+\] ` 去掉行前缀（不要用 `--include-row-prefix=false`，会留下前导空格）；`sheets +csv-put` **必须带 `--start-cell A1`**，否则报 `at least one of the flags in the group [start-cell range] is required`。空白表默认 5 列，回填后多出的空列/空行属预期。

## 测试与验证

迁移完成后，建议从以下维度验证：

### 1. 结构验证
- 根目录/父节点下的文档数量是否正确
- 子文档层级深度是否一致
- 子节点排列顺序是否与源文档一致

### 2. 内容验证
- 抽样检查几个文档：图片数量、表格数量、列表项数是否一致
- 对比 XML 标签统计（数量级应完全一致）
- 文件附件大小是否一致

### 3. 引用验证
- 检查文档内的飞书链接是否指向新域名
- 迁移范围内的文档链接是否已更新为新 token
- 外部链接是否保持不变

### 常用验证命令

```powershell
# 查看目标知识库根目录
lark-cli wiki +node-list --space-id <SPACE_ID> --as user

# 查看某节点的子节点
lark-cli wiki +node-list --space-id <SPACE_ID> --parent-node-token <NODE_TOKEN> --as user

# 获取文档内容（XML）
lark-cli docs +fetch --doc <DOC_TOKEN> --doc-format xml --detail full --as user
```

### 图片数量核对（迁移后必做）

最有效的验收指标是**源/目标图片数量一致**，可一次比对多个文档：

```powershell
foreach ($pair in @(
    @{ src = "SOURCE_DOC_TOKEN"; dst = "TARGET_DOC_TOKEN" }
)) {
    foreach ($side in @('src','dst')) {
        $j = lark-cli docs +fetch --doc $pair[$side] --doc-format xml --detail full --as user | ConvertFrom-Json
        $x = $j.data.document.content
        Write-Host "$side imgs=$(([regex]::Matches($x,'<img\s')).Count) len=$($x.Length)"
    }
}
```

数量一致即可判定图片全部迁移成功；若目标少于源，回看日志中 `图片下载失败` 的 token。

### 图片是否重新上传（更严格）

数量一致只说明标签数量对，还要确认图片确实传到了新文档，而不是仍引用源文档的 token：

```powershell
$sx = (lark-cli docs +fetch --doc <SOURCE_TOKEN> --doc-format xml --detail full --as user --format json | ConvertFrom-Json).data.document.content
$tx = (lark-cli docs +fetch --doc <TARGET_TOKEN> --doc-format xml --detail full --as user --format json | ConvertFrom-Json).data.document.content
$sSet = [regex]::Matches($sx,'<img[^>]*src="([^"]+)"') | ForEach-Object { $_.Groups[1].Value }
$tSet = [regex]::Matches($tx,'<img[^>]*src="([^"]+)"') | ForEach-Object { $_.Groups[1].Value }
"重叠=$((@($sSet | Where-Object { $tSet -contains $_ })).Count) 目标path残留=$(([regex]::Matches($tx,'path=\"')).Count)"
```

正常结果：**重叠 = 0** 且 **path 残留 = 0**（overwrite 会把本地路径转成新的图片 token）。若重叠 > 0，说明这些图仍指向源文档，需重跑对应文档。

## 常见问题

### Q: 报错 `131005 document is not in wiki`？
A: 说明源链接是**独立云文档**，不是知识库节点。脚本已自动回退到 `drive +inspect` 按单篇迁移，无需手动处理。若 `drive +inspect` 也失败，通常是当前账号对源文档没有阅读权限。

### Q: 迁移中途失败，知识库里多了个空文档？
A: 旧版本会残留空节点。当前脚本在内容填充失败时自动 `wiki +node-delete` 清理刚创建的空节点；若清理也失败，日志会打印该节点 URL，需手动删除。**中断（Ctrl+C）不会触发清理**，重跑前先检查目标目录有没有同名空文档。

### Q: 迁移后图片不显示？
A: 检查 XML 里图片是否用了 `path="@./images/xxx.png"`。`path` 值**必须以 `@` 开头**，否则会报 `local image #N: path must start with @`。图片较多时应分批确认，避免整篇 overwrite 失败。

### Q: 迁移后标题少了首尾空格？
A: 飞书创建节点时会自动裁剪标题首尾空格，属于平台行为，不影响内容。

### Q: 为什么图片下载提示 "does not have export permission"？
A: 源文档开启了复制保护，`media-download` 不可用。脚本会自动回退到 `media-preview`，不影响迁移结果。

### Q: 报错 `unsafe output path: ... is outside the built-in allowlist`？
A: lark-cli 只允许把文件写到「当前工作目录 / 账号临时目录 / 家目录 files」之内。旧版脚本对 `-WorkDir` 绝对路径直接下载会触发该错误，表现为**整篇图片 0 成功**。当前脚本已在每次下载时把子进程工作目录切到输出目录，`-WorkDir` 放哪都可以；若自己写脚本调用 `docs +media-download`，请先把 cwd 切到输出目录，或把 `-WorkDir` 放到临时目录下。

### Q: 大文档填充报 `server time out error`？
A: 通常不是文档太大，而是**图片全部下载失败**后 XML 里仍是源 token，导致 overwrite 负载异常。先确认日志里该文档是 `图片下载完成: N/N 成功`，再重跑；单篇 400+ 图时填充本身也需要数十秒到数分钟，属正常耗时。

### Q: `lark-cli auth status` 报 "credentials are provided externally"？
A: 该环境凭据由外部注入，不支持交互式登录/查询状态。跳过认证检查，直接调用业务命令即可（`--as user`）。

### Q: 迁移后子文档顺序不对？
A: v3 版本已修复。脚本按源文档深度优先遍历的原始顺序依次创建节点，确保顺序一致。

### Q: 内部引用没有全部更新？
A: 脚本只更新**本次迁移范围内**的文档引用，指向外部文档的引用保持原样（预期行为，也是迁移范围的边界）。若范围内的引用仍指向旧 token，多为 `cite` 的 `doc-id` 写成 wiki 节点 token 的历史情况——当前版本已同时映射 obj_token 与节点 token。可用下面的命令排查目标文档里是否残留源 token：

```powershell
lark-cli docs +fetch --doc <TARGET_TOKEN> --doc-format xml --detail full --as user --format json |
  ForEach-Object { ([regex]::Matches($_.data.document.content,'<旧源TOKEN>')).Count }
```

> 若需要把外部引用文档也一起搬过来，把它们加入 `-SourceWikiUrls` 再跑一次，或单独迁移后再修引用。

### Q: 可以迁移 sheet / bitable / mindnote 等类型吗？
A: 当前版本仅支持 docx（文档）和 file（文件附件）。其他类型会被跳过，需要时可扩展。

### Q: 迁移"成功"了，但文档里的表格/画板没了？
A: 跨空间复制内嵌对象会被服务端静默降级：表格返回 `degrade_code 2113`、画板返回 `2105`，`ok` 仍是 `true`，只在 `data.warnings` 提示。这是最常见的"内容静默丢失"。处理：`Migrate-FeishuDocs.ps1` 已把 token 表格/画板转成 blank，迁移后用 `Fix-EmbeddedBlocks.ps1`（带 `-FillSheets`）补数据与画板内容。验收时逐篇比对源/目标 `<sheet`、`<whiteboard` 数量。

### Q: `block_insert_after` 返回成功但块没进去（"插入 0/1 块"）？
A: 锚点是无 id 的容器块（`ul`/`ol`/`grid`/`callout`），`--block-id` 传空被跳过。改用 `block_replace`：把**下一个有 id 的块**替换为「新块 + 原块 OuterXml（去掉 id）」，位置和原内容都保得住。

### Q: 迁移后发现层级错位，要全部删掉重迁吗？
A: 不要。用 `Verify-MigrationTree.ps1 -Fix` 只做 `wiki +move` 调整父节点；内容问题用 `-OnlyRetryFailed` 续跑。删除会连带子节点，代价远高于移动。

### Q: `sheets +csv-put` 报 "at least one of the flags in the group [start-cell range] is required"？
A: 加 `--start-cell A1`。另外 `csv-get` 的 `annotated_csv` 每行带 `[row=N] ` 前缀，用 `(?m)^\[row=\d+\] ` 正则剥离（`--include-row-prefix=false` 会留多余前导空格，不要用）。

### Q: 文档里的"导航页/目录/广告位"迁移后是空的？
A: 那是 `<synced_reference>` 引用块，内容存放在**公共区块文档**里，不是子文档。跨空间引用失效后只剩空占位，迁移子文档也不会自动补上。按业务判断：正文类可静态复制内容进来，广告/导航类一般不必补。

### Q: 统计 checkpoint 时数量明显偏少（例如 887 变成 530）？
A: 用了 Windows PowerShell 5.1 读 UTF-8 文件导致中文乱码、JSON 解析失败被跳过。改用 `pwsh -NoProfile -File` 运行。

### Q: 迁移失败了怎么办？
A: 查看日志文件中的具体错误。常见原因：
- 权限不足（确认源文档可读、目标空间可写）
- 网络问题（已自动重试，仍失败可增大 `-MaxRetries`）
- 特殊格式不兼容（查看 warnings 字段）

## 迁移 SOP 步骤

1. **确认前置条件**：源文档可访问、目标空间有写权限；lark-cli 凭据可用（凭据由外部注入时 `auth status` 会报错，直接跳过）
2. **获取源文档 URL**：收集所有需迁移的链接，`/wiki/` 与 `/docx/` 均可混传（脚本自动判别）
3. **确定目标位置**：是迁移到知识库根目录，还是某个父节点下
4. **获取目标 Space ID**：
   - 根目录迁移：需要目标知识库的 space-id
   - 父节点迁移：解析目标父节点 URL 自动获取
5. **执行测试迁移**：先迁移一个较小的文档做验证
6. **验证结果**：按「迁移后强制核验清单」四项检查（节点数 1:1 / mismatch=0 / 图片零失败 / 内嵌对象逐篇计数一致）
7. **补全内嵌对象**：`Fix-EmbeddedBlocks.ps1 -FillSheets -ContinueOnError`，完成后 `-DryRun` 复查应无待修块
8. **正式批量迁移**：确认无误后执行全量迁移；中断或报错时原命令重跑（必要时加 `-OnlyRetryFailed`），不要删除已迁节点
9. **层级纠偏**：`Verify-MigrationTree.ps1 -Fix` 只 move
10. **交付结果**：提供根文档链接、迁移统计、结果文件、核验四项数据
