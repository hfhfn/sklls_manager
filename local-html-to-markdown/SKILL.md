---
name: local-html-to-markdown
description: 把本地 HTML 文件（file:// 协议、本机绝对路径上的 .html）通过 MCP 的 webpage-to-markdown 工具转为 Markdown，并把结果**统一归档到 `C:\Users\hfhfn\docker\markdownify\<原文件夹名>\`** 下，同时复制相关图片到该目录的 `assets/` 子目录、重写图片路径成 `assets/<basename>` 让产物可独立移动。MCP 出于安全策略拒绝 file:// 和所有私有 IP（localhost / 127.0.0.1 / 192.168.x / 172.x），所以必须先用 Python HTTP 服务器 + localtunnel 把文件暴露成公网 URL 才能调用 MCP。当用户提供本地 .html 路径或 file:/// URL 要求"转 markdown / 转 md"，或明确要求"用 mcp 转换本地 html / 用 mcp 把这个网页转成 markdown"时务必使用本技能。涵盖完整流程：服务器启动、隧道暴露、MCP 调用、内容清洗（去导航/页脚/锚点）、图片提取与路径重写、文件归档到固定目录、进程清理。
---

# Local HTML → Markdown via MCP

把本地 HTML 文件转为 Markdown，统一归档到 `C:\Users\hfhfn\docker\markdownify\` 下，并把图片一起带过去。

## 为什么需要这个技能

MCP 的 webpage-to-markdown 基于 markitdown，但有两条硬性安全限制：

- 拒绝 `file://` 协议 → 报 `Only http: and https: schemes are allowed`
- 拒绝所有私有/回环 IP（localhost、127.0.0.1、192.168.x、172.16-31.x、169.254.x、10.x）→ 报 `Fetching ... is potentially dangerous, aborting`

所以本地 HTML 必须先变成**公网可达的 https URL** 才能让 MCP 抓取。最轻量的方式是 Python 内置 HTTP 服务器 + localtunnel（无需注册、无需安装全局工具）。

转出来的 markdown 还要做后处理：去除站点骨架、把图片归档到固定位置、重写图片路径，这些用 `scripts/convert.py` 一步搞定。

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

### 1. 解析输入路径

用户给的可能是：

- Windows 绝对路径：`D:\工作\...\01-xxx.html`
- file:// URL：`file:///D:/%E5%B7%A5%E4%BD%9C/.../01-xxx.html`（带 URL 编码）

要做的：
1. 拿到 HTML 文件**所在目录**（HTTP 服务器要在这里启动，相对路径资源才能加载）
2. 拿到 HTML **文件名**（用来拼隧道 URL）
3. 文件名里的中文/特殊字符要 URL 编码再拼接（`①` → `%E2%91%A0`，空格 → `%20`）

### 2. 启动本地 HTTP 服务器（后台）

```bash
cd "<HTML 所在目录>" && python -m http.server 8765
```

用 `run_in_background: true`。端口选 8765 这种不常用的，避免冲突。

### 3. 用 localtunnel 暴露为公网 URL（后台）

```bash
npx --yes localtunnel --port 8765
```

用 `run_in_background: true`，然后**等 8-10 秒**让 localtunnel 完成握手。

读取后台输出，找到形如 `your url is: https://xxx-yyy-zzz.loca.lt` 的行，提取 URL。

如果 8 秒还没看到 URL，再多等几秒。如果一直没出来，可能是网络问题，杀掉重试。

### 4. 验证隧道可达

```bash
curl -s -o NUL -w "HTTP %{http_code}\n" "<tunnel URL>/<URL编码后的文件名>"
```

期望 `HTTP 200`。

如果是 `503 Tunnel Unavailable`：localtunnel 后端跟本地的连接断了。**杀掉 npx 进程重启** localtunnel（HTTP 服务器不用动），会拿到新的 URL。

### 5. 调用 MCP 转换

```
mcp__mcp-router__webpage-to-markdown(url="<tunnel URL>/<URL编码文件名>")
```

成功的话会返回完整的网页 markdown，里面**会带一堆站点骨架**（导航栏、页脚、目录、搜索框等）。

### 6. 把 MCP 原始输出落盘到临时文件

MCP 返回是字符串，要传给 `convert.py` 处理。最稳的做法：用 `Write` 工具把内容原样写到一个临时 `.md` 文件，比如：

```
C:\Users\hfhfn\docker\markdownify\.tmp_mcp_raw.md
```

放到输出根目录下用点号开头的隐藏文件即可，处理完可以删掉。

### 7. 跑 convert.py 一步到位

```bash
python "C:\Users\hfhfn\.claude\skills\local-html-to-markdown\scripts\convert.py" \
    --source  "<源 HTML 绝对路径>" \
    --raw-md  "<上一步保存的临时 .md>"
```

脚本做的事：

1. 清洗 mkdocs material 模板（找到第一个真正的 H1 作为正文起点；遇到 `©Copyright` / `Made with` / `Material for MkDocs` 视为页脚结束；移除标题尾巴的 `[¶](#xxx "Permanent link")` 锚点；折叠多余空行）
2. 扫描所有 `![alt](path)` 引用：
   - 外链（`http://`、`https://`、`data:`）保持原样
   - 本地相对路径基于源 HTML 目录解析为绝对路径
   - 复制到 `<output-base>/<父目录名>/assets/<basename>`，遇到同名+不同内容自动加 `-1` 序号
3. 重写 markdown 中的图片路径为 `assets/<basename>`
4. 写到 `<output-base>/<父目录名>/<源主名>.md`

可选参数：

- `--output-base <dir>`：覆盖默认根目录 `C:\Users\hfhfn\docker\markdownify`
- `--no-clean`：跳过模板清洗，只做图片处理（适用于源不是 mkdocs material 的情况）

脚本通过 stderr 报告：复制了多少张图、找不到的图片有哪些、最终 .md 路径和行数。

### 8. 清理后台进程和临时文件

按下面的顺序停掉服务：

```bash
# 1. 找到 8765 端口监听的进程 PID
netstat -ano | findstr ":8765"

# 2. 杀掉 Python 进程（Windows 双斜杠语法）
taskkill //F //PID <python_pid>
```

杀掉 Python 服务器后，localtunnel 后端会因为本地连接断开而退出。如果它还残留：

```bash
tasklist | findstr "node"
taskkill //F //PID <node_pid>
```

最后删掉临时的 `.tmp_mcp_raw.md`。

**Linux/Mac** 上等价命令：`lsof -i :8765` + `kill -9 <pid>`。

## 错误排查速查

| 现象 | 原因 | 处理 |
|---|---|---|
| `Only http: and https: schemes are allowed` | 直接传了 file:// 给 MCP | 走隧道方案 |
| `Fetching ... is potentially dangerous, aborting` | 传了 localhost / 127.0.0.1 / 192.168.x.x | 必须用 .loca.lt 这类公网 URL |
| `503 Tunnel Unavailable` | localtunnel 后端断连 | 重启 npx localtunnel |
| 中文文件名 MCP 返回 404 | URL 没编码 | 把文件名做 percent-encoding |
| convert.py 报 `image not found` | 源 HTML 引用的图片确实不存在，或路径错 | 看脚本 stderr 输出的具体路径，手工补图或忽略 |
| `--no-clean` 何时用 | 源不是 mkdocs material（例如纯静态页面、其他文档生成器） | 加 `--no-clean` 避免误剪正文 |
| Windows `taskkill /F` 报错 | 单斜杠在 git-bash 里被当路径解析 | 改用 `taskkill //F //PID` |
| markitdown 命令行可用但用户拒绝 | 用户明确要求用 MCP | 严格走 MCP，不要绕回 markitdown CLI |

## 完整示例

**用户输入**：
> 把 `D:\工作\...\① 大模型发展史\01-大模型发展史.html` 转 markdown

**执行步骤**：

1. `cd "D:\工作\...\① 大模型发展史" && python -m http.server 8765`（后台）
2. `npx --yes localtunnel --port 8765`（后台）
3. `sleep 8 && cat <tunnel 输出文件>` → 拿到 `https://xxx.loca.lt`
4. `curl ... 01-%E5%A4%A7%E6%A8%A1%E5%9E%8B%E5%8F%91%E5%B1%95%E5%8F%B2.html` → 200
5. `mcp__mcp-router__webpage-to-markdown(url=...)` → 拿到完整 markdown
6. `Write` 工具把返回的字符串落到 `C:\Users\hfhfn\docker\markdownify\.tmp_mcp_raw.md`
7. 跑 `convert.py --source "D:\工作\...\01-大模型发展史.html" --raw-md "C:\Users\hfhfn\docker\markdownify\.tmp_mcp_raw.md"`
   → 产出：
   ```
   C:\Users\hfhfn\docker\markdownify\① 大模型发展史\01-大模型发展史.md
   C:\Users\hfhfn\docker\markdownify\① 大模型发展史\assets\image-20251125081938055.png
   C:\Users\hfhfn\docker\markdownify\① 大模型发展史\assets\image-20251125082031725.png
   C:\Users\hfhfn\docker\markdownify\① 大模型发展史\assets\c6eaa88def344a298cc3d3cba20da218.png
   C:\Users\hfhfn\docker\markdownify\① 大模型发展史\assets\v2-9c85e98338c5e879328cd78e0925d757_r.jpg
   ... （其他图片）
   ```
8. `taskkill //F //PID <python pid>`，删 `.tmp_mcp_raw.md`

## 设计原则与注意事项

- **不要回退到非 MCP 路径**：用户明确说"用 MCP"时，遇到困难也不要直接 `markitdown input.html` 或自己根据 HTML 内容手写 markdown。这两种都不是用户想要的"用 MCP"。
- **公网 URL 必须**：MCP 的安全策略硬卡，没有任何本地 IP/loopback 能绕过去。localtunnel 是免费 + 零配置的最优解；ngrok / cloudflared 需要登录或安装。
- **进程清理是基本礼仪**：localtunnel 不关，会一直占公网域名；HTTP 服务器不关，会一直占端口。每次任务完都要清掉。
- **图片落地是核心价值**：用户固定输出到 `C:\Users\hfhfn\docker\markdownify\` 是为了集中管理。**不要**保留 `../img/xxx` 这种向上引用的相对路径——脚本会全部扁平化到该目录的 `assets/`。这样产物可以直接打包/拷贝/分享。
- **同名图片处理**：脚本按文件大小判定是否同一文件，不同则加 `-N` 后缀。如果用户碰到大量同名（不同内容）图片需要更精确的判定，可以改成 sha256 比对，但目前没必要。
