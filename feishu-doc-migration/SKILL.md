---
name: "feishu-doc-migration"
description: "使用 lark-cli 将飞书知识库文档完整迁移到目标知识库，支持 macOS/Linux/Windows，递归子文档、图片附件、格式保留、内部引用修复、子节点排序。当用户需要迁移飞书文档/知识库时调用。"
---

# 飞书文档迁移工具

使用 lark-cli API 将飞书 Wiki 文档完整迁移到目标知识库，保留全部格式、图片、附件、内部引用和子节点顺序。支持 macOS / Linux / Windows 多平台。

## 何时使用

- 用户要求迁移飞书文档/知识库到另一个空间
- 需要批量迁移文档树（父文档 + 所有子文档）
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

## 平台环境搭建

### Windows

Windows 自带 PowerShell 5.1，直接使用即可。lark-cli 通常已通过安装包配置到 PATH。

验证：
```powershell
lark-cli --version
$PSVersionTable.PSVersion
```

### macOS

macOS 下使用纯 Bash 脚本，依赖 `lark-cli` 和 `jq`，**不需要 PowerShell**。

#### 1. 安装依赖

**Homebrew（推荐，一条命令搞定）：**
```bash
brew install lark-cli jq
```

**手动安装：**
- lark-cli：从飞书开放平台下载 macOS 版本，放到 `/usr/local/bin/`
- jq：从 [jq 官网](https://stedolan.github.io/jq/) 下载二进制，放到 `/usr/local/bin/`

验证安装：
```bash
lark-cli --version
jq --version
```

#### 2. 完成认证

```bash
lark-cli auth login
```
按提示在浏览器中完成授权。

验证认证状态：
```bash
lark-cli auth status
```

#### 3. 脚本执行权限

```bash
chmod +x migrate.sh
```

> **注意**：macOS 下使用正斜杠 `/` 作为路径分隔符，不要使用 Windows 的反斜杠 `\`。
>
> **关于依赖**：`jq` 是一个极轻量的 JSON 处理工具（单文件二进制，约 1MB），macOS 开发者几乎都装过。如果你的 Mac 上没有，`brew install jq` 几秒钟就能装好。

### Linux

Linux 下和 macOS 一样使用纯 Bash 脚本，依赖 `lark-cli` 和 `jq`。

#### 安装依赖

**Ubuntu / Debian:**
```bash
sudo apt install jq
# lark-cli 需要从飞书开放平台下载 Linux 版本
```

**CentOS / RHEL:**
```bash
sudo yum install jq
```

**Arch Linux:**
```bash
sudo pacman -S jq
```

然后从飞书开放平台下载 lark-cli 的 Linux 版本，放到 `/usr/local/bin/`。

验证安装：
```bash
lark-cli --version
jq --version
```

其余步骤（认证、脚本权限等）与 macOS 相同。

## 核心脚本

提供两种脚本，功能完全一致：

| 文件 | 平台 | 依赖 | 说明 |
|------|------|------|------|
| `Migrate-FeishuDocs.ps1` | Windows | lark-cli + PowerShell | v3.1，含所有修复（方括号通配符 / partial_success / 父失败跳子 / 路径自动检测） |
| `migrate.sh` | macOS / Linux | lark-cli + jq | v3.1，纯 Bash 脚本，核心功能与容错特性已对齐 |

### macOS / Linux 推荐方式

使用 `migrate.sh`（纯 bash，仅依赖 `lark-cli` 和 `jq`）：
```bash
./migrate.sh -s "https://source.feishu.cn/wiki/xxx" -t 7687020534646754274
```

### Windows 推荐方式

使用 PowerShell 脚本：
```powershell
.\Migrate-FeishuDocs.ps1 -SourceWikiUrls @("https://source.feishu.cn/wiki/xxx") -TargetSpaceId "7687020534646754274"
```

> **为什么用 bash + jq？** `jq` 是 macOS/Linux 上极轻量的 JSON 处理工具（brew 一键安装），配合 bash 可以零依赖 PowerShell 完成所有迁移逻辑。两个平台的脚本功能、输出格式、结果文件结构完全一致。

### 功能特性

| 功能 | 说明 |
|------|------|
| 递归迁移 | 自动遍历并迁移整棵文档树（父 + 所有子文档） |
| 格式保留 | XML 直搬，不经过 Markdown 转换，保留标题/列表/表格/代码块/引用 |
| 图片迁移 | 下载 → 上传 → 替换引用，复制保护文档自动回退到 media-preview |
| 文件附件 | 支持 file 类型节点迁移（下载 + 上传 + 自动创建 wiki 子节点） |
| 内部引用修复 | sub-page-list、@文档引用、文档链接全部更新为新文档地址 |
| 子节点排序 | 按源文档顺序依次创建，保持完全一致的排列顺序 |
| 根目录/子节点 | 支持迁移到知识库根目录，或指定父节点下 |
| 错误重试 | 指数退避重试机制，默认 3 次 |
| 部分成功处理 | overwrite 时部分资源上传失败不回滚文档，内容已写入视为成功 |
| 失败防护 | 父节点迁移失败时自动跳过所有子节点，避免孤儿节点 |
| 进度输出 | 实时进度条 + 彩色日志 |
| 结果日志 | 生成 JSON 结果映射表 + 日志文件 |

### 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `-SourceWikiUrls` | ✅ | 源 Wiki URL 数组，可传入多个根文档 |
| `-TargetSpaceId` | ✱ | 目标知识库空间 ID（迁移到根目录时用） |
| `-TargetParentWikiUrl` | ✱ | 目标父节点 Wiki URL（迁移到指定节点下时用） |
| `-WorkDir` | - | 临时工作目录（默认 `.\lark_migration_temp`） |
| `-MaxRetries` | - | API 最大重试次数（默认 3） |
| `-RetryBaseDelay` | - | 重试基础延迟秒数（默认 3，指数退避） |
| `-AsUser` | - | 调用身份：`user` / `bot`（默认 `user`） |
| `-FixInternalRefs` | - | 是否修复内部引用（默认 `$true`） |

> ✱ `-TargetSpaceId` 和 `-TargetParentWikiUrl` 二选一

### 使用示例

#### 示例 1：迁移到知识库根目录

**Windows (PowerShell):**
```powershell
.\Migrate-FeishuDocs.ps1 `
  -SourceWikiUrls @("https://source.feishu.cn/wiki/xxxxxxxx") `
  -TargetSpaceId "7687020534646754274"
```

**macOS / Linux (推荐，shell 包装):**
```bash
./migrate.sh -s "https://source.feishu.cn/wiki/xxxxxxxx" -t 7687020534646754274
```

#### 示例 2：迁移到指定父节点下

**Windows (PowerShell):**
```powershell
.\Migrate-FeishuDocs.ps1 `
  -SourceWikiUrls @("https://source.feishu.cn/wiki/xxxxxxxx") `
  -TargetParentWikiUrl "https://my.feishu.cn/wiki/yyyyyyyy"
```

**macOS / Linux (推荐，shell 包装):**
```bash
./migrate.sh -s "https://source.feishu.cn/wiki/xxxxxxxx" -p "https://my.feishu.cn/wiki/yyyyyyyy"
```

#### 示例 3：批量迁移多个根文档

**Windows (PowerShell):**
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

**macOS / Linux (推荐，shell 包装):**
```bash
./migrate.sh \
  --sources "https://source.feishu.cn/wiki/aaaaaaa,https://source.feishu.cn/wiki/bbbbbbb,https://source.feishu.cn/wiki/ccccccc" \
  -t 7687020534646754274 \
  -w ./my_migration \
  -r 5
```

#### 示例 4：macOS 下查看帮助
```bash
./migrate.sh --help
```

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
3. 仅修复迁移范围内的文档引用，外部链接保持不变

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

**Windows / macOS 通用（lark-cli 命令本身跨平台）：**
```bash
# 查看目标知识库根目录
lark-cli wiki +node-list --space-id <SPACE_ID> --as user

# 查看某节点的子节点
lark-cli wiki +node-list --space-id <SPACE_ID> --parent-node-token <NODE_TOKEN> --as user

# 获取文档内容（XML）
lark-cli docs +fetch --doc <DOC_TOKEN> --doc-format xml --detail full --as user
```

## 常见问题

### Q: 为什么图片下载提示 "does not have export permission"？
A: 源文档开启了复制保护，`media-download` 不可用。脚本会自动回退到 `media-preview`，不影响迁移结果。

### Q: 文档标题含方括号（如 `[拓展]`）时迁移失败？
A: **PowerShell 特有问题**。PowerShell 的 `Out-File`、`Test-Path` 等 cmdlet 会把路径中的 `[]` 当作通配符解析，导致 `content.xml` 写入失败。v3.1 版本已修复，改用 .NET 的 `[System.IO.File]::WriteAllText()` 和 `-LiteralPath` 参数绕过此问题。如果遇到类似问题，请确保使用最新版脚本。

### Q: 迁移后发现部分文档跑到根目录了，层级不对？
A: 通常是父节点迁移失败导致的。v3 版本已加入「父失败 → 子节点全部跳过」的防护逻辑。如果遇到此问题，请检查日志中父节点的失败原因，修复后重新迁移。

### Q: 什么是 "partial_success"？迁移算成功了吗？
A: `partial_success` 表示文档内容已成功写入，但部分资源（图片/附件）上传失败。这种情况**文档主体是完整可用的**，只是个别图片可能显示为占位符。脚本会将其视为成功并继续迁移子节点，不会回滚已创建的文档。

### Q: 迁移后子文档顺序不对？
A: v3 版本已修复。脚本按源文档深度优先遍历的原始顺序依次创建节点，确保顺序一致。

### Q: 内部引用没有全部更新？
A: 脚本只更新**本次迁移范围内**的文档引用。指向其他外部文档的链接会保持原样，这是预期行为。

### Q: 可以迁移 sheet / bitable / mindnote 等类型吗？
A: 当前版本仅支持 docx（文档）和 file（文件附件）。其他类型会被跳过，需要时可扩展。

### Q: 迁移失败了怎么办？
A: 查看日志文件中的具体错误。常见原因：
- 权限不足（确认源文档可读、目标空间可写）
- 网络问题（已自动重试，仍失败可增大 `-MaxRetries`）
- 特殊格式不兼容（查看 warnings 字段）

### Q: macOS 下运行脚本报错 "command not found: jq"？
A: 说明未安装 jq（JSON 处理工具）。执行 `brew install jq` 安装，几秒钟搞定。`migrate.sh` 启动时会自动检测并给出安装提示。

### Q: macOS 下 lark-cli 找不到？
A: 确认 lark-cli 已安装并在 PATH 中。Homebrew 安装：`brew install lark-cli`。手动安装的话，将二进制文件放到 `/usr/local/bin/` 并执行 `chmod +x /usr/local/bin/lark-cli`。

### Q: macOS 下运行 `./migrate.sh` 提示 "Permission denied"？
A: 需要给脚本添加执行权限：
```bash
chmod +x migrate.sh
```

### Q: macOS 和 Windows 下的迁移结果完全一致吗？
A: 完全一致。两个脚本虽然实现语言不同（bash vs PowerShell），但迁移逻辑、API 调用、输出格式、结果文件结构都是对齐的，迁移结果没有差异。

### Q: Linux 下能用吗？
A: 可以。`migrate.sh` 是纯 bash 脚本，只要装了 `lark-cli` 和 `jq` 就能跑，Linux 各发行版通用。

## 迁移 SOP 步骤

> **⚠️ 重要原则：先测一个，再批量。** 始终先用一篇较小的文档跑通全流程，确认结构、内容、引用都没问题后，再批量迁移剩余文档。

1. **确认平台环境**
   - Windows：使用 `Migrate-FeishuDocs.ps1`，需 PowerShell + lark-cli
   - macOS / Linux：使用 `migrate.sh`，需 lark-cli + jq（`brew install lark-cli jq`）
   - 参考「平台环境搭建」章节

2. **确认前置条件**：lark-cli 认证状态、源文档可访问、目标空间有写权限
   - 验证：`lark-cli auth status`
   - 验证目标空间：`lark-cli wiki +node-list --space-id <SPACE_ID> --as user`

3. **获取源文档 URL**：从用户处收集所有需要迁移的根文档 Wiki URL

4. **确定目标位置**：是迁移到知识库根目录，还是某个父节点下

5. **获取目标 Space ID**：
   - 根目录迁移：需要目标知识库的 space-id
   - 父节点迁移：解析目标父节点 URL 自动获取

6. **准备脚本**
   - Windows：使用 `Migrate-FeishuDocs.ps1`
   - macOS / Linux：使用 `migrate.sh`，执行 `chmod +x migrate.sh`

7. **清理残留（重要）**
   - 如果之前有失败的迁移，先清理目标知识库中的残留节点
   - 保留用户已有的文档（如首页等），只删除迁移失败的产物
   - 检查根目录和各层级是否有孤儿节点

8. **执行测试迁移**：先迁移一个**较小**的文档做验证
   - 选择节点数少、结构简单的文档
   - 迁移后立即验证层级、内容、引用

9. **验证测试结果**：
   - **结构**：根目录节点数是否正确？子节点是否归位？有没有跑到根目录？
   - **内容**：抽样检查图片、表格、代码块是否正常
   - **引用**：内部文档链接是否指向新地址？
   - **顺序**：子节点排列顺序是否与源文档一致？

10. **正式批量迁移**：确认无误后执行全量迁移
    - 可以一次传入多个源 URL
    - 建议使用单独的工作目录，便于排查

11. **验证最终结果**：
    - 检查所有根文档是否在正确位置
    - 抽查 2-3 个深层级文档的结构
    - 查看日志中的成功/失败统计
    - 如有失败文档，单独分析并重试

12. **交付结果**：提供根文档链接、迁移统计、结果文件

## 版本历史

| 版本 | 主要变更 |
|------|---------|
| v3.1 | 修复 PowerShell 方括号通配符问题（`[拓展]` 等标题导致 `content.xml` 写入失败）；`Test-Path` 加 `-LiteralPath`；改用 .NET `WriteAllText` 写文件 |
| v3.0 | wiki node-create + overwrite 方案；支持根目录迁移；内部引用修复（sub-page-list / cite / a 链接）；子节点排序；部分资源失败不回滚；父失败跳子；lark-cli 路径自动检测 |
| v2.0 | 新增 macOS / Linux 纯 Bash 版本（migrate.sh），不依赖 PowerShell |
| v1.0 | 初始版本，Windows PowerShell 脚本，基础文档 + 图片迁移 |
