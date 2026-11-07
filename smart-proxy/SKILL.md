---
name: smart-proxy
description: USE WHEN 网络请求超时/被墙/Claude Code 或 Hermes 报"网络不可达"。智能代理回退：外网走代理、内网不走代理、失败退避重试。附 API key 环境变量约定。
---

# Smart Proxy Fetch — 智能代理感知网络访问

## 解决的痛点

在**直连外网被墙、必须经本地 Clash/代理（如 127.0.0.1:7890）才能出网**的机器上，
很多工具会报"网络不可达"或超时，原因是它们**不读 Windows 系统代理注册表**：

- **Claude Code / 任何 Node 工具**：`fetch` 默认不看系统代理，直连被墙 → 网络不可达。
- **Hermes 的 brave-free web_search**：用 `httpx.get()`，`trust_env` 默认真但**只读环境变量代理**，不读注册表 → 若进程无 `HTTPS_PROXY` 也超时。

**判断你的机器是否这种情况**：`curl -m 8 https://github.com` 超时，
但 `curl -m 8 -x http://127.0.0.1:7890 https://github.com` 返回 200 → 就是它。

## 策略（用户指定）

1. **直连优先**：先不带代理直连目标。
2. **判内外网**：
   - **内网**（`localhost`、`127.x`、`10.x`、`192.168.x`、`172.16-31.x`、`*.local/.lan/.internal/.corp`、解析到私有 IP 的域名）→ **绝不走代理**，直连失败即真失败。
   - **外网**（其余所有）→ 直连失败则**自动走系统/本地代理**重试。
3. **退避重试**：直连失败走代理，代理也失败可再回退直连（默认最多 2 轮）。
4. 代理缺失时，外网直连失败则退避重试 `max_rounds` 次。

## 快速使用

```bash
# 脚本路径
SCRIPT="$HOME/AppData/Local/hermes/skills/smart-proxy/scripts/smart-proxy-fetch.py"

# 自检：看内网/外网/代理判定和连通性
python "$SCRIPT" --test

# 探测单个 URL 是否可达（200=成功，打印走的是直连还是代理）
python "$SCRIPT" https://github.com

# 带超时
python "$SCRIPT" https://example.com --timeout 20
```

## 代理来源（自动解析，无需配置）

优先级从高到低读取代理：

1. 环境变量 `HTTPS_PROXY` / `HTTP_PROXY`（含小写）。
2. Windows 系统代理注册表 `HKCU\...\Internet Settings` 的 `ProxyServer`（脚本自动读取）。

> 若你的 Clash 端口不是 7890，脚本会自动从注册表读到，无需改脚本。

## 内网域名自定义

默认已覆盖常见内网后缀。若你的公司/校园内网域名不在白名单，用环境变量追加：

```bash
export SMART_PROXY_PRIVATE_SUFFIXES=".mycorp.com,.intra"
```

## API Key 约定（本 skill/相关 skill 统一遵守）

| 用途 | 环境变量 | 位置 |
|------|---------|------|
| Brave 网页搜索 | `BRAVE_SEARCH_API_KEY` | Windows **用户变量** `HKCU\Environment`，或 Hermes `AppData\Local\hermes\.env` |
| 代理 | `HTTPS_PROXY` / `HTTP_PROXY` | Windows 用户变量（可选，脚本会读注册表兜底） |

**设置方式（Windows 用户变量，永久生效）：**
```cmd
setx BRAVE_SEARCH_API_KEY "你的key"
setx HTTPS_PROXY "http://127.0.0.1:7890"
setx HTTP_PROXY  "http://127.0.0.1:7890"
```
> `setx` 只影响**之后**新开的进程，需重启终端/应用才生效。改注册表用 `setx` 即可（写入 `HKCU\Environment`）。

**给 Claude Code / Node 工具临时生效**（不全局改，直接注入当前会话）：
```bash
export HTTPS_PROXY="http://127.0.0.1:7890"
export HTTP_PROXY="http://127.0.0.1:7890"
```

## 给各种工具"通电"的速查

| 工具 | 走代理方式 |
|------|-----------|
| **Claude Code** | 设 `HTTPS_PROXY`/`HTTP_PROXY` 环境变量后重启终端 |
| **Hermes web_search** | 设 `HTTPS_PROXY`/`HTTP_PROXY` 环境变量后重启 Hermes（its httpx 只读 env） |
| **curl** | `-x http://127.0.0.1:7890` 或设环境变量 |
| **本脚本** | 自动（直连→代理回退） |

## 常见坑

- **改了环境变量但工具还超时**：进程没重启，旧进程不读新变量。Claude Code 必须开新终端。
- **内网服务被误判走代理**：把其域名加入 `SMART_PROXY_PRIVATE_SUFFIXES`，或确认 `is_private()` 已覆盖。
- **`setx` 后 PowerShell/cmd 里读不到**：`setx` 写注册表，当前 shell 不更新，重开即可。
- **代理本身挂了**：端口不监听时脚本会直连失败→代理失败→回退直连，最终报失败，符合预期。

## 验证

```bash
python "$HOME/AppData/Local/hermes/skills/smart-proxy/scripts/smart-proxy-fetch.py" --test
```
期望：内网行显示 `[直连(内网)]`，外网行显示 `[直连]` 或 `[代理(...)]`，Brave 行显示 `[代理(...)] HTTP 422`（422 是因为自检未带 key，属正常连通证明）。