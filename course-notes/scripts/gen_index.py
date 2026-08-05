#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""重建 notes/总索引.md，覆盖全部 20 章。
主题（topic）来源优先级：
1. notes/topics.json 中人工凝练的短语（课时号 -> 主题）
2. 回退：从每篇笔记的“## 内容摘要”自动抽取首句
"""
import json
import os
import re
from pathlib import Path

# ⚠ 可移植副本（course-notes 技能自带）。复用到新课程时，把下面这行 ROOT 改成新课程根目录的绝对路径。
ROOT = Path(r"C:\Users\hfhfn\Desktop\其他\mksz955-MCP+A2A 从0到1构建类Manus多Agent全栈应用资源")
NOTES = ROOT / "notes"
INDEX = NOTES / "总索引.md"
TOPICS = NOTES / "topics.json"


def chapter_num(name: str):
    m = re.match(r"第(\d+)章", name)
    return int(m.group(1)) if m else 9999


def lesson_key(fname: str):
    m = re.match(r"(\d+)-(\d+)", fname)
    return (int(m.group(1)), int(m.group(2))) if m else (9999, 9999)


def lesson_id(fname: str):
    m = re.match(r"(\d+-\d+)", fname)
    return m.group(1) if m else fname


def note_title(path: Path, stem: str):
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return stem


def extract_topic(path: Path) -> str:
    """取“## 内容摘要”后的首句；无摘要则取首个正文段落。截断到 ~46 字。"""
    text = path.read_text(encoding="utf-8", errors="ignore")
    body = ""
    m = re.search(r"##\s*内容摘要\s*\n(.+?)(?:\n\s*\n|\n#)", text, re.S)
    if m:
        body = m.group(1)
    else:
        for para in re.split(r"\n\s*\n", text):
            p = para.strip()
            if p and not p.startswith("#") and not p.startswith("|"):
                body = p
                break
    body = re.sub(r"\s+", "", body)
    # 首句：中文句号/分号/换行截断
    sent = re.split(r"[。；]", body)[0]
    if len(sent) > 46:
        sent = sent[:46] + "…"
    return sent or "—"


def load_topics() -> dict:
    """读取 notes/topics.json（课时号 -> 人工凝练主题）。"""
    if TOPICS.exists():
        return json.loads(TOPICS.read_text(encoding="utf-8"))
    return {}


def enc(rel: str) -> str:
    # 空格与括号需转义，否则 markdown 链接会被 ')' 提前截断
    return rel.replace(" ", "%20").replace("(", "%28").replace(")", "%29")


def main():
    topics = load_topics()

    chapters = sorted(
        (d for d in NOTES.iterdir() if d.is_dir()),
        key=lambda d: chapter_num(d.name),
    )

    out = ["# MoManus 课程笔记总索引", ""]
    total = 0
    per_chapter = []

    body_lines = []
    for ch in chapters:
        notes = sorted(
            (f for f in ch.iterdir() if f.suffix == ".md"),
            key=lambda f: lesson_key(f.name),
        )
        if not notes:
            continue
        per_chapter.append((ch.name, len(notes)))
        body_lines.append(f"## {ch.name}（{len(notes)}篇）")
        body_lines.append("")
        body_lines.append("| 编号 | 笔记 | 主题 |")
        body_lines.append("|------|------|------|")
        for f in notes:
            stem = f.stem
            lid = lesson_id(stem)
            title = note_title(f, stem)
            topic = topics.get(lid) or extract_topic(f)
            link = f"{enc(ch.name)}/{enc(f.name)}"
            body_lines.append(f"| {lid} | [{title}]({link}) | {topic} |")
            total += 1
        body_lines.append("")
        body_lines.append("---")
        body_lines.append("")

    out.append(f"> 覆盖第1章至第20章，共 {total} 篇结构化 Markdown 笔记。")
    out.append("")
    out.append("---")
    out.append("")
    out.extend(body_lines)

    INDEX.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
    print(f"生成完成：{total} 篇，{len(per_chapter)} 章")
    for name, n in per_chapter:
        print(f"  {n:2d}  {name}")


if __name__ == "__main__":
    main()
