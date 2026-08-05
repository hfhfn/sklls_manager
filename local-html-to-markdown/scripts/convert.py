#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把本地 HTML 转成干净、可独立移动的 Markdown，统一归档到
C:\\Users\\hfhfn\\docker\\markdownify\\<原文件夹名>\\ 下，图片复制到 assets/。

两种转换引擎：

  1) 本地 markdownify（默认，推荐）
     --engine local：直接用 markdownify 解析源 HTML，代码/表格/图片都能
     完整还原。对 mkdocs material 站点，效果与项目里的 convert_html_to_md.py
     （docs/ 正源）逐字节一致。不需要 MCP、不需要公网隧道。

  2) MCP webpage-to-markdown（备用）
     --engine mcp：把 MCP 原始输出作为输入做清洗（markitdown 固有缺陷——
     丢 <img>、表格错位、代码块退化、空行爆炸——会在清洗和告警中兜底，
     但内容级缺失无法补回）。仅当本地 markdownify 不可用时才用这条。

步骤：
  1) [local] 提取 <article> → markdownify → 代码块语言推断（python/sql/bash/json）
              → 代码块感知的 setext→ATX 标题转换
     [mcp]   读 MCP 原始 markdown → 去导航/页脚/锚点 → 修空行/空列表/孤立 >
  2) 解析图片引用，把本地相对路径图片复制到 <输出>/assets/，重写为 assets/<basename>
  3) 写到 <output-base>/<源 HTML 所在文件夹名>/<源 HTML 主名>.md

用法：
  python convert.py --source <源 HTML 绝对路径>
                    [--engine local|mcp]        # 默认 local
                    [--raw-md <MCP 原始输出文件，- 表示 stdin>]  # 仅 --engine mcp 需要
                    [--output-base <根目录，默认 C:\\Users\\hfhfn\\docker\\markdownify>]
                    [--no-clean]                # 跳过模板清洗，仅做图片处理

例：
  # 本地直转（推荐）
  python convert.py --source "D:\\工作\\...\\01-大模型发展史.html"
  → 产出：C:\\Users\\hfhfn\\docker\\markdownify\\① 大模型发展史\\01-大模型发展史.md
          C:\\Users\\hfhfn\\docker\\markdownify\\① 大模型发展史\\assets\\*.png

  # MCP 备用
  python convert.py --source "..." --engine mcp --raw-md mcp_raw.md
"""

import argparse
import html as html_mod
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import unquote

# 默认输出根目录（用户固定要求）
DEFAULT_OUTPUT_BASE = r'C:\Users\hfhfn\docker\markdownify'

# ======================================================================
# 代码块语言推断
#
# 原始 mkdocs HTML 里每个代码块都是 <pre><code>…</code></pre> 且没有语言
# 类。markdownify 会把它转成裸 ``` 围栏，mkdocs 构建时就渲染成不带任何
# Pygments span 的 <pre><code>——没有语法高亮。
#
# 所以用 markdownify 的 code_language_callback 给围栏打语言标签。分类器
# 刻意保守：只有明显像 Python/shell/SQL/JSON 的块才打语言，终端输出、
# ASCII 图表、纯文字保持裸 ```（仍等宽，但不会误导性上色）。
# 与项目里 convert_html_to_md.py 的 infer_code_language 完全同源。
# ----------------------------------------------------------------------

_PY_LINE_RE = re.compile(r'^(def|class|async\s+def)\s+\w')
_ASYNCIO_RE = re.compile(r'\b(import\s+asyncio|asyncio\.run|await\s+)\b')
# 真正的 Python import："import time"、"from x.y import z"。要求带 "import"，
# 避免裸的 "FROM table"（SQL）被误判成 Python。
_PY_IMPORT_RE = re.compile(r'^(from\s+\w[\w.]*\s+import|import\s+\w[\w.]*)')
# 强 Python 信号：块内出现 def/class 或独立 import 行（多行模式，前面有
# "# 注释" 也挡不住）。
_IS_PY_RE = re.compile(r'^\s*(def|class|async\s+def)\s+\w|^import\s+\w[\w.]*', re.M)
_SQL_STRONG_RE = re.compile(
    r'^(CREATE\s+TABLE|INSERT\s+INTO|SELECT\b|UPDATE\b|DELETE\s+FROM|ALTER\s+TABLE|'
    r'DROP\s+TABLE|BEGIN\s*(;|$)|COMMIT\b|SHOW\s)', re.I)
_SQL_KW_RE = re.compile(
    r'\b(SELECT|INSERT\s+INTO|UPDATE\b|DELETE\s+FROM|CREATE\s+TABLE|ALTER\s+TABLE|'
    r'DROP\s+TABLE|GROUP\s+BY|ORDER\s+BY|JOIN\s+\w+\s+ON|VALUES\s*\(|PRIMARY\s+KEY)\b',
    re.I)
# Shell 命令动词，必须匹配在行首（多行）。刻意用锚点，让终端输出
# （如 "INFO: Uvicorn running…"、"Python 3.12.2"）不会因为提到某个工具
# 就被打成 bash。
_BASH_LINE_RE = re.compile(
    r'^\s*(?:\$|sudo|pip3?|uvicorn|conda|npm|git\s+clone|curl|docker|psql|mysql|'
    r'source|export|cd\s|chmod|systemctl|service|brew|apt|make|kill|pkill|echo)\b',
    re.M | re.I)
_BASH_FIRST_RE = re.compile(
    r'^(?:\$|sudo|pip3?|uvicorn|conda|npm|git\s+clone|curl|docker|psql|mysql|'
    r'python3?\s+(?:-\S|[\w./]+\.py)|cd\s+\S|source|export)\b', re.I)
_JSON_STRONG_RE = re.compile(r'^\{|^\[')
_GARBLED_RE = re.compile(r'�')


def _is_strong_python(t):
    """块内含 def/class 或独立 import 行即判为 Python。兜底用：首行没有
    信号但确实是 Python 的块仍会被打标。避免把只是「提到」python 的
    shell 输出（如 SQL 示例里的 'import'）误判成 Python。"""
    return bool(_IS_PY_RE.search(t))


def _first_content(t, max_comment=3):
    """返回代码块里第一个非注释行（最多跳过 max_comment 个注释行），
    让开头的 `# 注释` / `# 文件头` 不遮住真正的首条语句。t 保持原始
    换行文本。"""
    for line in t.split('\n'):
        s = line.strip()
        if not s:
            continue
        if s.startswith('#'):
            max_comment -= 1
            if max_comment < 0:
                return None
            continue
        return s
    return None


def infer_code_language(el):
    """为 <pre> 元素返回 markdown 围栏语言，或返回 '' 保持裸围栏（不高亮）。
    刻意保守——见模块 docstring。"""
    try:
        txt = el.get_text() or ''      # 保留原始换行，供行锚点正则用
    except (AttributeError, TypeError):
        return ''
    txt = html_mod.unescape(txt).strip()
    if not txt:
        return ''
    t = txt.lstrip()
    first = _first_content(t)

    # 编码损坏 -> 绝不打标（渲染会显示替换字符 �）
    if _GARBLED_RE.search(t):
        return ''

    # 强首行信号（跳过前导注释行）
    if first:
        if _PY_LINE_RE.match(first) or _PY_IMPORT_RE.match(first) or _ASYNCIO_RE.search(t[:120]):
            return 'python'
        if _SQL_STRONG_RE.match(first):
            return 'sql'
        if _BASH_FIRST_RE.match(first) or first.startswith('$ '):
            return 'bash'
        if _JSON_STRONG_RE.match(first) and '──' not in t[:60]:
            return 'json'

    # 首行无信号 -> 只有块内被无歧义代码关键字主导时才打标，
    # 防止终端输出 / 图表 / 散文被误标。
    if _is_strong_python(t):
        return 'python'
    if _SQL_KW_RE.search(t):
        return 'sql'
    if _BASH_LINE_RE.search(t):
        return 'bash'
    return ''

# ======================================================================
# 引擎 1：本地 markdownify（默认）
# ======================================================================

def convert_html_local(html):
    """源 HTML → markdown（markdownify + 代码块感知的 setext→ATX 标题转换）。

    与本地 convert_html_to_md.py 的 convert_and_normalize 同源：
      - 提取 <article>（mkdocs material 正文容器）
      - markdownify 转换（不转义 * / _，保留中文内容的强调）
      - 去掉标题尾的 [¶](#xxx "Permanent link") 永久链接锚点
      - setext 下划线标题 → ATX（# / ##），且跳过代码块内部——
        代码块里的 `======` 装饰分隔线不能误判成标题下划线
    """
    from markdownify import markdownify as md

    m = re.search(r'<article[^>]*>(.*?)</article>', html, re.S)
    body = m.group(1) if m else html
    conv = md(body, escape_asterisks=False, escape_underscores=False,
              code_language_callback=infer_code_language)
    conv = re.sub(r'\[¶\]\(#[^)]*\)', '', conv)

    lines = conv.split('\n')
    out = []
    i = 0
    in_code = False
    while i < len(lines):
        l = lines[i]
        nxt = lines[i + 1].strip() if i + 1 < len(lines) else ''
        # 跟踪围栏，代码块内部不做任何标题转换
        if l.strip().startswith('```'):
            in_code = not in_code
            out.append(l)
            i += 1
            continue
        # setext -> ATX（下一行是纯下划线；行首是列表/引用/表格则跳过）
        if (not in_code and l.strip() and nxt
                and ((nxt[0] == '=' and set(nxt) <= set('=') and len(nxt) >= 3)
                     or (nxt[0] == '-' and set(nxt) <= set('-') and len(nxt) >= 3))
                and not l.startswith(('*', '-', '>', '|'))):
            level = 1 if nxt.startswith('=') else 2
            out.append('#' * level + ' ' + l.strip())
            i += 2
            continue
        out.append(l)
        i += 1
    return '\n'.join(out)


# ======================================================================
# 引擎 2：MCP markitdown 输出清洗（备用）
# ======================================================================

# 标题尾巴的永久链接锚点：[¶](#xxx "Permanent link")
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


def remove_empty_list_items(body):
    """删除 markitdown 产生的空列表项（`- `、`* `、`1. ` 后面没内容）。"""
    lines = body.splitlines()
    out = []
    in_code = False
    for line in lines:
        stripped = line.strip()
        if stripped == '```' or stripped.startswith('```'):
            in_code = not in_code
            out.append(line)
            continue
        if in_code:
            out.append(line)
            continue
        if re.match(r'^[-*](\s+)?$', stripped) or re.match(r'^\d+\.(\s+)?$', stripped):
            continue
        out.append(line)
    return '\n'.join(out)


def fix_orphan_quotes(body):
    """修复 markitdown 产生的孤立 `>` 行（下一行才是引用正文）。

    典型形态：
        >
        （空行）
        💡 **xxx**
    合并为：
        > 💡 **xxx**
    """
    lines = body.splitlines()
    out = []
    i = 0
    n = len(lines)
    while i < n:
        stripped = lines[i].strip()
        if stripped == '>':
            j = i + 1
            while j < n and lines[j].strip() == '':
                j += 1
            if j < n and not lines[j].strip().startswith('>'):
                out.append('> ' + lines[j].strip())
                i = j + 1
                continue
            out.append('>')
            i += 1
            continue
        out.append(lines[i])
        i += 1
    return '\n'.join(out)


def collapse_blank_lines(body):
    """把 markitdown 产生的连续空行压成 1 个；列表项之间不留空行；围栏内保留。"""
    lines = body.splitlines()
    out = []
    in_code = False
    for line in lines:
        stripped = line.strip()
        if stripped == '```' or stripped.startswith('```'):
            in_code = not in_code
            out.append(line)
            continue
        if in_code:
            out.append(line)
            continue
        if stripped == '':
            if out and out[-1].strip() == '':
                continue
            out.append('')
            continue
        is_list_item = re.match(r'^([-*]|\d+\.)\s+\S', stripped) is not None
        if is_list_item and out and out[-1].strip() == '':
            out.pop()
        out.append(line)
    while out and out[-1].strip() == '':
        out.pop()
    return '\n'.join(out)


def clean_mcp(raw):
    """MCP 原始 markdown → 清洗后的正文。"""
    lines = raw.splitlines()
    start = find_content_start(lines)
    end = find_content_end(lines, start)
    body = '\n'.join(lines[start:end])
    body = PERMALINK_RE.sub('', body)
    body = remove_empty_list_items(body)
    body = fix_orphan_quotes(body)
    body = collapse_blank_lines(body)
    return body.rstrip() + '\n'


# ======================================================================
# 图片处理（两种引擎共用）
# ======================================================================

IMG_RE = re.compile(r'!\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)')


def is_external(url):
    return url.startswith(('http://', 'https://', 'data:', '//'))


def handle_images(md, source_dir, target_dir):
    """把本地图片复制到 target_dir/assets/，重写引用为 assets/<basename>。"""
    assets_dir = target_dir / 'assets'
    seen = {}
    copied = []
    missing = []

    def repl(m):
        alt = m.group(1)
        raw_path = m.group(2)

        if is_external(raw_path):
            return m.group(0)

        decoded = unquote(raw_path.split('#')[0].split('?')[0])

        if decoded in seen:
            return f'![{alt}]({seen[decoded]})'

        src = (source_dir / decoded).resolve()
        if not src.exists():
            missing.append(str(src))
            return m.group(0)

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

    print(f'  copied {len(copied)} image(s) to {assets_dir}', file=sys.stderr)
    if missing:
        print(f'  WARNING: {len(missing)} image(s) not found:', file=sys.stderr)
        for p in missing:
            print(f'    - {p}', file=sys.stderr)

    return rewritten


# ======================================================================
# 质量检测（告警，不修改内容）
# ======================================================================

def warn_table_misalignment(md):
    """检测表格列数不一致（markitdown 的缺陷；markdownify 引擎几乎不会触发）。"""
    lines = md.splitlines()
    in_code = False
    tbl = []
    tbl_start = 0
    warnings = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == '```' or stripped.startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue
        if line.startswith('|'):
            if not tbl:
                tbl_start = i + 1
            tbl.append(line)
        else:
            if len(tbl) >= 3:
                cols = {ln.count('|') for ln in tbl}
                if len(cols) > 1:
                    warnings += 1
                    print(f'  WARNING: 表格可能在 {tbl_start} 行附近列数不一致 '
                          f'(单元格含 | 或长文本): 行内 | 数量={sorted(cols)}',
                          file=sys.stderr)
            tbl = []
    return warnings


def warn_missing_images_from_source(md, source_dir, engine, source_stem=None):
    """对比源 HTML <img> 数与产物图片引用数，提示图片丢失（markitdown 会丢）。

    只统计「与当前源 HTML 同名」的那个文件里的 <img>，避免把目录里其他页面/
    导航 logo 也算进去。engine 决定告警措辞（本地 markdownify 引擎不该丢图）。
    """
    if source_stem is None:
        return 0, 0
    hf = source_dir / (source_stem + '.html')
    if not hf.exists():
        return 0, 0
    try:
        txt = hf.read_text(encoding='utf-8')
    except Exception:
        return 0, 0
    total_imgs = len(re.findall(r'<img[^>]+src=', txt))
    md_imgs = len(re.findall(r'!\[[^\]]*\]\(', md))
    if total_imgs and md_imgs < total_imgs:
        who = '本地 markdownify' if engine == 'local' else 'markitdown'
        print(f'  WARNING: 源 HTML 含 {total_imgs} 个 <img>，但 markdown 里只有 '
              f'{md_imgs} 张图片引用。若正文有插图，需对照源 HTML 手动补 '
              f'`![alt](assets/xxx.png)`。', file=sys.stderr)
    return total_imgs, md_imgs


# ======================================================================
# main
# ======================================================================

def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument('--source', required=True, help='源 HTML 绝对路径')
    ap.add_argument('--engine', choices=['local', 'mcp'], default='local',
                    help='转换引擎：local=markdownify 本地直转（默认，推荐）；'
                         'mcp=用 MCP 原始输出清洗')
    ap.add_argument('--raw-md', help='MCP 原始 markdown 文件路径（仅 --engine mcp），- 表示 stdin')
    ap.add_argument('--output-base', default=DEFAULT_OUTPUT_BASE, help='输出根目录')
    ap.add_argument('--no-clean', action='store_true', help='跳过模板清洗，仅做图片处理')
    args = ap.parse_args()

    source = Path(args.source).resolve()
    if not source.exists():
        print(f'ERROR: source HTML not found: {source}', file=sys.stderr)
        return 1

    if args.engine == 'local':
        html = source.read_text(encoding='utf-8')
        md = html if args.no_clean else convert_html_local(html)
    else:
        if not args.raw_md:
            print('ERROR: --engine mcp 需要 --raw-md（MCP 原始输出文件，- 表示 stdin）',
                  file=sys.stderr)
            return 1
        if args.raw_md == '-':
            raw = sys.stdin.read()
        else:
            raw = Path(args.raw_md).read_text(encoding='utf-8')
        md = raw if args.no_clean else clean_mcp(raw)

    # 质量告警（不自动改内容）
    warn_table_misalignment(md)
    warn_missing_images_from_source(md, source.parent, args.engine, source.stem)

    # 目标目录：<output-base>/<源 HTML 父目录名>
    target_dir = Path(args.output_base) / source.parent.name
    target_dir.mkdir(parents=True, exist_ok=True)

    # 处理图片
    md = handle_images(md, source.parent, target_dir)

    out_md = target_dir / (source.stem + '.md')
    out_md.write_text(md, encoding='utf-8')

    print(f'Output: {out_md}', file=sys.stderr)
    print(f'  total lines: {len(md.splitlines())}', file=sys.stderr)
    print(f'  engine: {args.engine}', file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
