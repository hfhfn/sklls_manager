#!/usr/bin/env bash
# 准备依赖：解包 wecomdocs-cli（只用它的 client/session），装 playwright、openpyxl、pillow
set -euo pipefail

WORKDIR="${WECOM_WORKDIR:-$PWD/.wecom-work}"
mkdir -p "$WORKDIR"
cd "$WORKDIR"
echo "workdir: $WORKDIR"

if [ ! -d package/dist ]; then
  echo "[1/3] 拉取 wecomdocs-cli..."
  npm pack wecomdocs-cli 2>&1 | tail -1
  tar -xzf wecomdocs-cli-*.tgz
fi

if [ ! -d node_modules/playwright ]; then
  echo "[2/3] 安装 playwright 等依赖（跳过浏览器下载，复用系统 Chrome）..."
  [ -f package.json ] || npm init -y >/dev/null 2>&1
  PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm install --no-audit --no-fund --loglevel=error \
    chalk commander playwright qrcode-terminal
fi

echo "[3/3] 安装 python 依赖..."
python -m pip install --quiet --disable-pip-version-check openpyxl pillow 2>&1 | tail -2 || true

python - <<'PY'
import importlib
for m in ("openpyxl", "PIL"):
    try:
        mod = importlib.import_module(m)
        print(f"  {m} {getattr(mod, '__version__', 'ok')}")
    except Exception as e:
        print(f"  {m} 缺失: {e}")
PY
node -e "console.log('  playwright', require('playwright/package.json').version)" 2>/dev/null || true

cat <<'EOF'

就绪。下一步：
  node <skill>/scripts/login.mjs "<任意企业微信文档链接>"
  node <skill>/scripts/wc.mjs tabs "<文档链接>"
EOF
