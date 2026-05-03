#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 MCP webpage-to-markdown 的原始输出整理成最终成品。

做的事情：
  1) 清洗 mkdocs material 模板元素（导航/页脚/标题永久链接锚点）
  2) 解析 markdown 中的图片引用（![alt](path)）
  3) 把本地图片（相对路径）从源 HTML 目录复制到目标目录的 assets/ 下
  4) 重写图片路径为 assets/<basename>，让产物可以独立移动/打包
  5) 写到 <output-base>/<源 HTML 所在文件夹名>/<源 HTML 主名>.md

用法：
  python convert.py --source <源 HTML 绝对路径> --raw-md <MCP 原始输出文件，- 表示 stdin>
                    [--output-base <根目录，默认 C:\\Users\\hfhfn\\docker\\markdownify>]
                    [--no-clean]   # 跳过模板清洗，仅做图片处理

例：
  python convert.py --source "D:\\工作\\...\\01-大模型发展史.html" --raw-md mcp_raw.md
  → 产出：C:\\Users\\hfhfn\\docker\\markdownify\\① 大模型发展史\\01-大模型发展史.md
          C:\\Users\\hfhfn\\docker\\markdownify\\① 大模型发展史\\assets\\*.png
"""

import argparse
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import unquote

# 默认输出根目录（用户固定要求）
DEFAULT_OUTPUT_BASE = r'C:\Users\hfhfn\docker\markdownify'

# ---------------- 清洗 ----------------

# 标题尾巴的永久链接锚点：[¶](#xxx "Permanent link")
# 用 [ \t]* 而不是 \s*，避免吃掉行间空行
PERMALINK_RE = re.compile(
    r'[ \t]*\[¶\]\(#[^)]*[ \t]+"Permanent link"\)[ \t]*$',
    re.MULTILINE,
)

# mkdocs material 页脚标志，命中任意一个就认定页脚开始
FOOTER_MARKERS = ('©Copyright', 'Made with', '[Material for MkDocs]')


def find_content_start(lines):
    """找到第一个真正的 H1（# xxx）作为正文起点。"""
    for i, line in enumerate(lines):
        if line.startswith('# ') and not line.startswith('## '):
            return i
    return 0


def find_content_end(lines, start):
    """从 start 之后找页脚开始的行号，返回值不包含该行；同时去掉末尾连续空行。"""
    for i in range(start, len(lines)):
        if any(m in lines[i] for m in FOOTER_MARKERS):
            j = i - 1
            while j > start and lines[j].strip() == '':
                j -= 1
            return j + 1
    return len(lines)


def clean(raw):
    lines = raw.splitlines()
    start = find_content_start(lines)
    end = find_content_end(lines, start)
    body = '\n'.join(lines[start:end])
    body = PERMALINK_RE.sub('', body)
    body = re.sub(r'\n{3,}', '\n\n', body)
    return body.rstrip() + '\n'


# ---------------- 图片处理 ----------------

# 匹配 ![alt](path) 或 ![alt](path "title")
# path 用 [^)\s]+ 避免吃到空格分隔的 title
IMG_RE = re.compile(r'!\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)')


def is_external(url):
    return url.startswith(('http://', 'https://', 'data:', '//'))


def handle_images(md, source_dir, target_dir):
    """
    扫描 md 里所有图片引用：
      - 外链（http/https/data:）保持原样
      - 本地相对路径：解析为 source_dir 下的实际文件 → 复制到 target_dir/assets/ → 重写 md 路径
    返回重写后的 md 字符串。
    """
    assets_dir = target_dir / 'assets'
    seen = {}        # decoded 原路径 -> 新相对路径
    copied = []      # 实际拷贝过的源文件
    missing = []     # 找不到的图片

    def repl(m):
        alt = m.group(1)
        raw_path = m.group(2)

        if is_external(raw_path):
            return m.group(0)

        # 解码 URL 编码（中文/空格等），并去掉 #fragment 和 ?query
        decoded = unquote(raw_path.split('#')[0].split('?')[0])

        if decoded in seen:
            return f'![{alt}]({seen[decoded]})'

        src = (source_dir / decoded).resolve()
        if not src.exists():
            missing.append(str(src))
            # 找不到就保留原样，让用户能看到坏链
            return m.group(0)

        # 复制到 assets/，重名按文件大小判断是否同一个文件，不同则加序号
        assets_dir.mkdir(parents=True, exist_ok=True)
        dest = assets_dir / src.name
        n = 1
        while dest.exists() and dest.stat().st_size != src.stat().st_size:
            dest = assets_dir / f'{src.stem}-{n}{src.suffix}'
            n += 1
        if not dest.exists():
            shutil.copy2(src, dest)
            copied.append(str(src))

        new_path = f'assets/{dest.name}'
        seen[decoded] = new_path
        return f'![{alt}]({new_path})'

    rewritten = IMG_RE.sub(repl, md)

    # 报告
    print(f'  copied {len(copied)} image(s) to {assets_dir}', file=sys.stderr)
    if missing:
        print(f'  WARNING: {len(missing)} image(s) not found:', file=sys.stderr)
        for p in missing:
            print(f'    - {p}', file=sys.stderr)

    return rewritten


# ---------------- main ----------------

def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument('--source', required=True, help='源 HTML 绝对路径')
    ap.add_argument('--raw-md', required=True, help='MCP 原始 markdown 文件路径，- 表示从 stdin 读')
    ap.add_argument('--output-base', default=DEFAULT_OUTPUT_BASE, help='输出根目录')
    ap.add_argument('--no-clean', action='store_true', help='跳过模板清洗，仅做图片处理')
    args = ap.parse_args()

    source = Path(args.source).resolve()
    if not source.exists():
        print(f'ERROR: source HTML not found: {source}', file=sys.stderr)
        return 1

    # 读原始 markdown
    if args.raw_md == '-':
        raw = sys.stdin.read()
    else:
        raw = Path(args.raw_md).read_text(encoding='utf-8')

    # 清洗
    md = raw if args.no_clean else clean(raw)

    # 决定目标目录：<output-base>/<源 HTML 父目录名>
    target_dir = Path(args.output_base) / source.parent.name
    target_dir.mkdir(parents=True, exist_ok=True)

    # 处理图片
    md = handle_images(md, source.parent, target_dir)

    # 写最终 markdown
    out_md = target_dir / (source.stem + '.md')
    out_md.write_text(md, encoding='utf-8')

    print(f'Output: {out_md}', file=sys.stderr)
    print(f'  total lines: {len(md.splitlines())}', file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
