---
name: local-html-to-markdown
description: 把本地 HTML 文件（file:// 协议、本机绝对路径上的 .html）转为 Markdown，并把结果**统一归档到 `C:\Users\hfhfn\docker\markdownify\<原文件夹名>\`** 下，同时复制相关图片到该目录的 `assets/` 子目录、重写图片路径成 `assets/<basename>` 让产物可独立移动。**默认用本地 markdownify 直接转源 HTML（无需 MCP、无需公网隧道），对 mkdocs material 站点效果与项目内 convert_html_to_md.py（docs/ 正源）逐字节一致**；转换时给 python/sql/bash/json 代码块自动推断并写入语言标签，后续 `mkdocs build` 会渲染**语法高亮**。只有本地 markdownify 不可用、或用户明确要求"用 MCP 转换"时才走 MCP 备用路径（markitdown，需 HTTP 服务器 + localtunnel 暴露公网）。当用户提供本地 .html 路径或 file:/// URL 要求"转 markdown / 转 md"时务必使用本技能。涵盖两条路径：本地直转与 MCP 备用、图片提取与路径重写、代码块语言推断、文件归档到固定目录。
---

# Local HTML → Markdown

把本地 HTML 文件转为 Markdown，统一归档到 `C:\Users\hfhfn\docker\markdownify\` 下，并把图片一起带过去。

## 两条转换路径（默认本地，MCP 备用）

| | **本地 markdownify（默认，推荐）** | **MCP webpage-to-markdown（备用）** |
|---|---|---|
| 转换核心 | `markdownify` 直接解析源 HTML | markitdown，需先暴露公网 URL |
| 代码块 | **完整还原 + 语言推断**：python/sql/bash/json 围栏自动打语言标签，后续 `mkdocs build` 会渲染语法高亮；终端输出/图表/散文保持裸 ```（不高亮，避免误导） | 代码块退化、语言丢失（不可修复） |
| 表格 | **完整还原**（与 docs/ 正源一致） | 列错位（不可修复） |
| 图片 | **正常保留** | 默认丢弃 `<img>` |
| 需要网络/隧道 | 不需要 | HTTP 服务器 + localtunnel |
| 何时用 | **优先**，几乎总是用这个 | 本地 markdownify 不可用，或用户明确要求 MCP |

**判断规则**：
- 用户给本地 HTML 路径/`file://` URL 要求转 md → **默认走本地 markdownify**，一条命令搞定，不需要起服务器、不需要等隧道。
- 用户明确说"用 MCP" / "用 mcp 转换" → 走 MCP 路径。
- 本地没有 `markdownify`（`pip install markdownify beautifulsoup4` 可装）→ 降级到 MCP 路径。

> 为什么默认本地？实测 markitdown 对代码/表格/图片密集的 mkdocs material 站点有**不可修复的内容级缺陷**：丢 `<img>`（源 261 张图转出 0 张）、表格列错位（86 页 101 处）、代码高亮块退化成 `<span>` HTML 文本。本地 markdownify 没有这些问题，且不需要公网暴露，转换在毫秒级完成。

## 输出规约

固定输出根目录：`C:\Users\hfhfn\docker\markdownify`

最终目录结构：

```
C:\Users\hfhfn\docker\markdownify\
└── <源 HTML 父目录的名字>\           ← 比如 "① 大模型发展史"
    ├── <源 HTML 主名>.md             ← 比如 "01-大模型发展史.md"
    └── assets\
        ├── <图片1>.png
        ├── <图片2>.jpg
        └── ...
```

要点：

- 文件夹名 = 源 HTML 所在目录的**最后一级名字**（不是完整路径）。
- 所有图片（不管原始路径是 `assets/xxx.png` 还是 `../img/yyy.png`）都被**扁平化**复制到同一个 `assets\` 下，文件名以 basename 为准。
- markdown 中所有图片引用都被重写为 `assets/<basename>`，让整个文件夹可以打包/移动而不破坏链接。
- 外链图片（`http://`、`https://`、`data:`）保持原样。
- 同名但内容不同的图片（按文件大小判断）会自动加 `-1`、`-2` 后缀避免覆盖。

## 工作流程

### 路径 A：本地 markdownify（默认，一条命令）

```bash
python "C:\Users\hfhfn\.claude\skills\local-html-to-markdown\scripts\convert.py" \
    --source "<源 HTML 绝对路径>"
```

`convert.py` 内部做：
1. 提取 `<article>`（mkdocs material 正文容器；找不到则用整页）
2. markdownify 转换（`escape_asterisks=False, escape_underscores=False`，保留中文强调）
3. **代码块语言推断**（`code_language_callback`）：源 HTML 的 `<pre><code>` 不带语言类，markdownify 会转成裸 ``` 围栏，导致后续 `mkdocs build` 不出语法高亮。脚本用启发式给 python/sql/bash/json 围栏打语言标签；**保守起见**只有明显像代码的块才打标——终端输出、ASCII 图表、散文保持裸 ```（仍等宽，但不会误导性上色）
4. 去掉标题尾的 `[¶](#xxx "Permanent link")` 永久链接锚点
5. **代码块感知的 setext→ATX 标题转换**：`xxx\n====` → `# xxx`、`xxx\n----` → `## xxx`；跳过代码块内部，避免把代码里的 `======` 装饰线误判成标题
6. 处理图片（复制到 assets/ + 重写路径）
7. 写到 `<output-base>/<父目录名>/<源主名>.md`

**不用起 HTTP 服务器、不用等隧道、不用调 MCP。** 秒级完成。

### 路径 B：MCP webpage-to-markdown（备用）

当本地 markdownify 不可用或用户明确要求 MCP 时：

1. **启动本地 HTTP 服务器（后台）**
   ```bash
   cd "<HTML 所在目录>" && python -m http.server 8765
   ```
   （端口选 8765 这种不常用的，避免冲突）

2. **用 localtunnel 暴露为公网 URL（后台）**
   ```bash
   npx --yes localtunnel --port 8765
   ```
   等 8-10 秒握手，读输出找 `your url is: https://xxx-yyy-zzz.loca.lt`。没出现就多等几秒或杀掉重试。

3. **验证隧道可达**
   ```bash
   curl -s -o NUL -w "HTTP %{http_code}\n" "<tunnel URL>/<URL编码后的文件名>"
   ```
   期望 `HTTP 200`。`503` 说明 localtunnel 后端断连，杀 npx 重启。

4. **调用 MCP 转换**
   ```
   mcp__mcp-router__webpage-to-markdown(url="<tunnel URL>/<URL编码文件名>")
   ```

5. **把 MCP 原始输出落盘到临时文件**
   用 `Write` 工具原样写到 `C:\Users\hfhfn\docker\markdownify\.tmp_mcp_raw.md`。

6. **跑 convert.py 的 MCP 引擎**
   ```bash
   python "C:\Users\hfhfn\.claude\skills\local-html-to-markdown\scripts\convert.py" \
       --source  "<源 HTML 绝对路径>" \
       --engine  mcp \
       --raw-md  "C:\Users\hfhfn\docker\markdownify\.tmp_mcp_raw.md"
   ```

7. **清理后台进程和临时文件**
   ```bash
   netstat -ano | findstr ":8765"      # 找 PID
   taskkill //F //PID <python_pid>     # Windows 双斜杠
   tasklist | findstr "node"
   taskkill //F //PID <node_pid>
   ```
   删掉 `.tmp_mcp_raw.md`。**Linux/Mac**：`lsof -i :8765` + `kill -9 <pid>`。

### 两种路径共用的转换细节

- `--engine local`（默认）输入是源 HTML；`--engine mcp` 输入是 MCP 原始 markdown。
- 图片处理对两条路径都生效：扫描 `![alt](path)`，外链保持原样，本地相对路径复制到 `assets/` 并重写为 `assets/<basename>`。
- 脚本通过 stderr 报告：复制了多少张图、找不到的图片、最终 .md 路径和行数。
- 可选参数：
  - `--output-base <dir>`：覆盖默认根目录
  - `--no-clean`：跳过清洗（本地路径则跳过标题转换，MCP 路径则跳过模板清洗），只做图片处理

## 错误排查速查

| 现象 | 原因 | 处理 |
|---|---|---|
| `No module named 'markdownify'` | 本地没装 markdownify | `pip install markdownify beautifulsoup4`，或降级走 MCP 路径 |
| `Only http: and https: schemes are allowed`（仅 MCP 路径） | 直接传了 file:// 给 MCP | 走隧道方案 |
| `Fetching ... is potentially dangerous, aborting`（仅 MCP 路径） | 传了 localhost / 127.0.0.1 / 192.168.x.x | 必须用 .loca.lt 这类公网 URL |
| `503 Tunnel Unavailable`（仅 MCP 路径） | localtunnel 后端断连 | 重启 npx localtunnel |
| 中文文件名 MCP 返回 404（仅 MCP 路径） | URL 没编码 | 把文件名做 percent-encoding |
| convert.py 报 `image not found` | 源 HTML 引用的图片确实不存在，或路径错 | 看脚本 stderr 输出的具体路径，手工补图或忽略 |
| 本地引擎转换结果里表格列对不齐 | 极少见（markitdown 才常见）；可能是表格单元格含 `\|` | 对照源 HTML 人工校验；convert.py 有告警提示行号 |
| 本地引擎转换结果里正文插图少了 | markitdown 路径才会丢图；本地 markdownify 保留 `<img>` | 若是 MCP 路径：对照源 HTML 手动补 `![alt](assets/xxx.png)` |
| 某段真实代码围栏没打上语言（比如漏判） | 分类器保守，首行/块内信号不足时保持裸 ``` | 手动补 ` ```python ` 等；如反复漏判，可调整 `convert.py` 里的 `infer_code_language` 正则 |
| 终端输出/图表被高亮了（不该有颜色） | 罕见；分类器对含 `import`、`SELECT` 等词的文本块可能过触发 | 手动去掉围栏语言；也可收紧 `infer_code_language` 里的强关键词 |
| `--no-clean` 何时用 | 源不是 mkdocs material（例如纯静态页面、其他文档生成器） | 加 `--no-clean` 避免误剪正文/标题转换 |
| Windows `taskkill /F` 报错 | 单斜杠在 git-bash 里被当路径解析 | 改用 `taskkill //F //PID` |

## 完整示例（本地路径，推荐）

**用户输入**：
> 把 `D:\工作\...\① 大模型发展史\01-大模型发展史.html` 转 markdown

**执行步骤**：

```bash
python "C:\Users\hfhfn\.claude\skills\local-html-to-markdown\scripts\convert.py" \
    --source "D:\工作\...\① 大模型发展史\01-大模型发展史.html"
```

→ 产出：
```
C:\Users\hfhfn\docker\markdownify\① 大模型发展史\01-大模型发展史.md
C:\Users\hfhfn\docker\markdownify\① 大模型发展史\assets\image-20251125081938055.png
C:\Users\hfhfn\docker\markdownify\① 大模型发展史\assets\v2-9c85e98338c5e879328cd78e0925d757_r.jpg
... （其他图片）
```

## 完整示例（MCP 路径，备用）

**用户输入**：
> 用 MCP 把 `D:\工作\...\01-大模型发展史.html` 转 markdown

**执行步骤**：

1. `cd "D:\工作\...\① 大模型发展史" && python -m http.server 8765`（后台）
2. `npx --yes localtunnel --port 8765`（后台）
3. `sleep 8 && cat <tunnel 输出文件>` → 拿到 `https://xxx.loca.lt`
4. `curl ... 01-%E5%A4%A7%E6%A8%A1%E5%9E%8B%E5%8F%91%E5%B1%95%E5%8F%B2.html` → 200
5. `mcp__mcp-router__webpage-to-markdown(url=...)` → 拿到完整 markdown
6. `Write` 工具把返回的字符串落到 `C:\Users\hfhfn\docker\markdownify\.tmp_mcp_raw.md`
7. `convert.py --source "..." --engine mcp --raw-md "C:\Users\hfhfn\docker\markdownify\.tmp_mcp_raw.md"`
8. `taskkill //F //PID <python pid>`，删 `.tmp_mcp_raw.md`

## 设计原则与注意事项

- **本地优先，MCP 是兜底**：默认走本地 markdownify。只有本地没装、或用户明确要 MCP 才用 MCP 路径。MCP 的 markitdown 对代码/表格/图片密集页面有不可修复的内容缺陷（丢图、表格错位、代码退化），本地没有。
- **代码块语言推断是保守的**：`infer_code_language` 只对首行/块内信号明确的 python/sql/bash/json 打标。终端输出、ASCII 流程图、纯文字块保持裸 ```。这是有意的——给终端输出硬打 `python` 会产生误导性的错误高亮。若某段真实代码漏打了语言，手动补 ` ```python ` 即可；`convert.py` 的可选 `code_language_callback` 参数随时可调。
- **MCP 路径不要回退到非 MCP 工具**：用户明确说"用 MCP"时，遇到困难也不要直接 `markitdown input.html` 或手写 markdown。但**本地 markdownify 不是"非 MCP 工具"**——它是本技能的默认路径，用户没明确要 MCP 时直接用即可。
- **图片落地是核心价值**：所有本地图片扁平化到 `assets/`，重写为 `assets/<basename>`，产物可直接打包/拷贝/分享。**不要**保留 `../img/xxx` 这类向上引用。
- **同名图片处理**：脚本按文件大小判定是否同一文件，不同则加 `-N` 后缀。
- **转换后做一次质量抽查**：本地引擎的结果与 `docs/` 正源一致（代码块、表格、图片都完整），一般无需抽查；若用了 MCP 路径，markitdown 有固定缺陷（空行、表格错位、图片丢失、代码退化），跑完要核对一遍，特别是表格和图片。
