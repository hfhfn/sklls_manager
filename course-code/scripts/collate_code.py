#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""collate_code.py — 从课程笔记里抽取所有代码块，构建一份"代码地图"(JSON)。

用途：course-code 技能的第一步。它**不**直接生成代码库，而是把散落在
notes/**/*.md 里的 fenced code blocks 连同上下文线索(所属课时、就近标题、
路径/类名/导入线索)统一汇总，交给子代理做"按目标文件跨课时综合合成"。

用法：
    python collate_code.py --notes "<notes 目录>" [--chapter 8] [--lang python]
                           [--out .code_map.json]

输出 JSON 结构：
    {
      "meta": {"notes_dir": ..., "chapter_filter": ..., "total_blocks": N},
      "blocks": [
        {
          "lesson": "8-8",
          "chapter": 8,
          "note": "<相对路径>",
          "lang": "python",
          "heading": "Pop — 读取并删除（带分布式锁）",
          "path_hints": ["app/interface/protocol.py", "app.infrastructure.store"],
          "symbols": ["RedisStreamMessageQueue", "pop", "_acquire_lock"],
          "code": "..."
        }, ...
      ]
    }
"""
import argparse
import json
import re
from pathlib import Path

# fenced code block: ```lang\n...\n```
FENCE = re.compile(r"```([A-Za-z0-9_+.-]*)\n(.*?)\n```", re.S)
# 路径线索：a/b/c.py, app/xxx/yyy, main.py, package.json, Dockerfile 等
PATH_HINT = re.compile(
    r"(?:[\w./-]+/)?[\w-]+\.(?:py|ts|tsx|js|jsx|json|toml|txt|yaml|yml|sql|sh)\b"
    r"|(?:app|src)[./][\w./]+"
    r"|\bDockerfile\b"
)
# 顶层符号：class X / def x / async def x / (前端) function x / export ...
SYMBOL = re.compile(
    r"^\s*(?:async\s+def|def|class)\s+([A-Za-z_]\w*)"
    r"|^\s*export\s+(?:default\s+)?(?:function|const|class)\s+([A-Za-z_]\w*)"
    r"|^\s*function\s+([A-Za-z_]\w*)",
    re.M,
)
HEADING = re.compile(r"^#{1,6}\s+(.*)$")


def lesson_id(name: str) -> str:
    m = re.match(r"(\d+-\d+)", name)
    return m.group(1) if m else name


def chapter_of(name: str):
    m = re.match(r"第(\d+)章", name)
    return int(m.group(1)) if m else None


def nearest_heading(text: str, upto: int) -> str:
    """返回 code block 之前最近的一个 markdown 标题文本。"""
    best = ""
    for m in HEADING.finditer(text, 0, upto):
        best = m.group(1).strip()
    return best


def collect(notes_dir: Path, chapter_filter, lang_filter):
    blocks = []
    for note in sorted(notes_dir.glob("第*/*.md")):
        ch = chapter_of(note.parent.name)
        if chapter_filter is not None and ch != chapter_filter:
            continue
        text = note.read_text(encoding="utf-8", errors="ignore")
        lid = lesson_id(note.name)
        for m in FENCE.finditer(text):
            lang = (m.group(1) or "").lower()
            code = m.group(2)
            if lang_filter and lang != lang_filter:
                continue
            # 上下文线索
            heading = nearest_heading(text, m.start())
            window = text[max(0, m.start() - 400): m.start()] + "\n" + code
            hints = sorted(set(PATH_HINT.findall(window)))
            syms = sorted(set(
                g for tup in SYMBOL.findall(code) for g in tup if g
            ))
            blocks.append({
                "lesson": lid,
                "chapter": ch,
                "note": str(note.relative_to(notes_dir.parent)),
                "lang": lang or "text",
                "heading": heading,
                "path_hints": hints,
                "symbols": syms,
                "code": code,
            })
    return blocks


def main():
    ap = argparse.ArgumentParser(description="构建课程笔记代码地图")
    ap.add_argument("--notes", required=True, help="notes 目录")
    ap.add_argument("--chapter", type=int, default=None, help="只处理某一章（数字）")
    ap.add_argument("--lang", default=None, help="只保留某语言，如 python/tsx")
    ap.add_argument("--out", default=".code_map.json", help="输出 JSON 路径")
    args = ap.parse_args()

    notes_dir = Path(args.notes)
    if not notes_dir.is_dir():
        raise SystemExit(f"notes 目录不存在: {notes_dir}")

    lang = args.lang.lower() if args.lang else None
    blocks = collect(notes_dir, args.chapter, lang)

    out = {
        "meta": {
            "notes_dir": str(notes_dir),
            "chapter_filter": args.chapter,
            "lang_filter": lang,
            "total_blocks": len(blocks),
        },
        "blocks": blocks,
    }
    Path(args.out).write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    # 摘要（stdout）
    by_lang = {}
    for b in blocks:
        by_lang[b["lang"]] = by_lang.get(b["lang"], 0) + 1
    print(f"代码块总数: {len(blocks)}  -> {args.out}")
    for k, v in sorted(by_lang.items(), key=lambda x: -x[1]):
        print(f"  {v:4d}  {k}")


if __name__ == "__main__":
    main()
