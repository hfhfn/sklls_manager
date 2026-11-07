#!/usr/bin/env python3
"""
smart-proxy-fetch.py — 智能代理感知网络探测/抓取脚本 (Windows)

用途：解决"直连外网被墙、必须走 Clash/本地代理"环境下，各工具（Claude Code 的
Node fetch、Hermes 的 httpx 等）因不读 Windows 系统代理而超时的问题。

策略（用户指定）：
  1. 直连：先尝试不带代理直连目标。
  2. 判内外网：若直连失败，判断目标域名是"外网"还是"内网"。
       - 内网（localhost、127.x、192.168.x、10.x、172.16-31.x、*.local、
         公司/校园内网域名）→ 绝不该走代理，直连本就该通，失败即真失败。
       - 外网 → 走系统/本地代理重试。
  3. 退避重试：直连失败走代理后，若代理也失败，可再回退重试（默认最多 2 轮）。
  4. 外网域名判定：若域名不在内网白名单内，默认视为外网（走代理）。

API key 约定（本 skill 的约定）：
  - Brave Search: 环境变量 BRAVE_SEARCH_API_KEY
    （Windows 用户变量 HKCU\\Environment 或 Hermes 的 ~/.hermes/.env）
  - 通用代理代理：环境变量 HTTPS_PROXY / HTTP_PROXY 优先，
    否则读取 Windows 系统代理注册表 HKCU\\...\\Internet Settings 的 ProxyServer。

用法：
  python smart-proxy-fetch.py https://example.com [--timeout 15] [--probe]
  python smart-proxy-fetch.py --test        # 自检：探测 内网/外网/代理 三种

依赖：仅标准库（urllib + winreg），无需 pip 安装。
"""

import argparse
import re
import socket
import sys
import urllib.error
import urllib.request

# ── 内网判定（RFC1918 + 常见本地/保留段）──────────────────────────────
_PRIVATE_IP_RE = re.compile(
    r"^(127\.|10\.|192\.168\.|172\.(1[6-9]|2[0-9]|3[01])\.|"
    r"169\.254\.|0\.|fe80:|::1$)"
)
_LOCAL_TLDS = (".local", ".lan", ".internal", ".corp", ".home.arpa", ".intranet")
_WINDOWS_HOSTS_PATTERNS = [".local", ".lan", ".internal", ".corp"]


def _parse_host(url: str) -> str:
    """从 URL 提取 host（去掉 scheme 和端口）。"""
    m = re.match(r"^(?:https?|ftp)://([^/:]+)", url.strip())
    if m:
        return m.group(1)
    # 无 scheme 时按 host[:port] 解析
    return url.strip().split(":")[0].split("/")[0]


def is_private(host: str) -> bool:
    """判 host 是否为内网/本地地址。"""
    host = host.lower().strip()
    if not host:
        return True
    if host in ("localhost", "localhost6"):
        return True
    # IP 形式
    if _PRIVATE_IP_RE.match(host):
        return True
    # 尝试解析 IP：若解析到私有 IP 也判内网
    try:
        for info in socket.getaddrinfo(host, None):
            ip = info[4][0]
            if _PRIVATE_IP_RE.match(ip):
                return True
    except socket.gaierror:
        return False  # 解析失败，按外网处理（让其走代理尝试）
    # 常见本地域名后缀
    if host.endswith(_LOCAL_TLDS):
        return True
    # Windows hosts 自定义内网域名，可通过环境变量追加
    extra = _env("SMART_PROXY_PRIVATE_SUFFIXES", "")
    for suf in (extra.split(",") if extra else []):
        if suf.strip() and host.endswith(suf.strip().lower()):
            return True
    return False


def _env(name: str, default: str = "") -> str:
    return __import__("os").environ.get(name, default or "")


# ── 系统/本地代理解析 ─────────────────────────────────────────────────
def get_proxy() -> str | None:
    """返回可用代理 URL。优先级：环境变量 > Windows 系统代理注册表。"""
    for var in ("HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy"):
        v = _env(var)
        if v:
            return v if "://" in v else f"http://{v}"
    return _windows_system_proxy()


def _windows_system_proxy() -> str | None:
    """读取 Windows 系统代理注册表 ProxyEnable/ProxyServer。"""
    try:
        import winreg

        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
        )
        enable, _ = winreg.QueryValueEx(key, "ProxyEnable")
        server, _ = winreg.QueryValueEx(key, "ProxyServer")
        winreg.CloseKey(key)
        if enable and server:
            return server if "://" in server else f"http://{server}"
    except (OSError, FileNotFoundError, KeyError):
        pass
    return None


# ── 核心取回逻辑 ─────────────────────────────────────────────────────
def fetch(url: str, timeout: int = 15, max_rounds: int = 2) -> tuple[int, str]:
    """
    带智能代理回退的 GET 请求。
    返回 (状态, 简短信息)。状态: 200=成功, 其他HTTP码, 或 -1=网络失败。
    """
    host = _parse_host(url)
    private = is_private(host)
    proxy = get_proxy()

    # 尝试序列: 直连 → (若外网且代理可用) 走代理 → 再直连(回退)
    attempts: list[dict] = []

    if not private:
        # 外网: 直连优先，失败走代理
        attempts.append({"proxies": None, "label": "直连"})
        if proxy:
            attempts.append({"proxies": {"http": proxy, "https": proxy}, "label": f"代理({proxy})"})
    else:
        # 内网: 只直连，绝不走代理
        attempts.append({"proxies": None, "label": "直连(内网)"})

    # 若代理不可用，最多直连 max_rounds 次做退避
    if not proxy and not private:
        while len(attempts) < max_rounds:
            attempts.append({"proxies": None, "label": f"直连(重试{len(attempts)+1})"})

    last_err = ""
    for attempt in attempts:
        try:
            handler = urllib.request.ProxyHandler(attempt["proxies"])
            opener = urllib.request.build_opener(handler)
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0 smart-proxy-fetch"},
            )
            with opener.open(req, timeout=timeout) as resp:
                code = getattr(resp, "status", resp.getcode() or 200)
                return code, f"[{attempt['label']}] HTTP {code}"
        except urllib.error.HTTPError as e:
            return e.code, f"[{attempt['label']}] HTTP {e.code}"
        except (urllib.error.URLError, OSError, socket.timeout) as e:
            last_err = f"[{attempt['label']}] 失败: {e}"
            if private:
                # 内网直连失败 = 真失败，立刻返回
                return -1, last_err
            continue  # 外网: 换下一个尝试（代理/回退）

    return -1, last_err or "所有尝试均失败"


# ── 探测模式 ─────────────────────────────────────────────────────────
def _test() -> None:
    print("Smart Proxy Fetch 自检")
    print("-" * 55)
    print(f"检测到代理: {get_proxy() or '(无，仅直连)'}")
    for name, url in [
        ("内网(localhost)", "http://127.0.0.1:7890"),  # 内网应直连
        ("外网(example.com)", "https://example.com"),
        ("外网(GitHub)", "https://github.com"),
        ("Brave API", "https://api.search.brave.com/res/v1/web/search?q=test"),
    ]:
        host = _parse_host(url)
        code, msg = fetch(url)
        priv = "内网" if is_private(host) else "外网"
        print(f"  {name:22s} [{priv}] {code} {msg}")
    print("-" * 55)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="智能代理感知网络探测/抓取")
    ap.add_argument("url", nargs="?", help="要访问的 URL")
    ap.add_argument("--timeout", type=int, default=15)
    ap.add_argument("--probe", action="store_true", help="探测模式")
    ap.add_argument("--test", action="store_true", help="自检")
    args = ap.parse_args()

    if args.test:
        _test()
    elif args.probe:
        _test()
    elif args.url:
        code, msg = fetch(args.url, timeout=args.timeout)
        print(f"{code} {msg}")
        sys.exit(0 if code == 200 else 1)
    else:
        ap.print_help()