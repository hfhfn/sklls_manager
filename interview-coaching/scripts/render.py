#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
render.py — fill deterministic tokens into the analysis / gap-prep templates.

The coaching templates are written so the *reproducible* parts (metrics,
tech stack, ambiguous terms, question-bank pulls) are substituted here from
structured JSON, while the *semantic* prose is authored by the coaching LLM.
This keeps every session's evidence section uniform and comparable.

Token grammar in templates:
  {{a.field.nested}}      scalar from the analysis context
  {{list:a.path}}         each item as a bullet (str, or digest of dict)
  {{llm:a.path}}          dump the field's own markdown (already authored);
                            if empty, leave an explicit <!-- TODO LLM: x --> marker
Usage:
  python render.py --template defaults/analysis.md.j2 --context ctx.json --out X.md
where ctx.json = {"a": analysis, "e": extract, "b": bank}.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

_TOKEN = re.compile(r"\{\{\s*(list|llm)?:?(a|m|e|b)\.[^}]+?}}")


def resolve(ctx: dict, path: str):
    node = ctx
    for part in path.split("."):
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node


def render_item(item):
    if isinstance(item, str):
        return f"- {item}"
    if not isinstance(item, dict):
        return f"- {item}"
    # human-friendly known shapes
    if "questions" in item and "label" in item:  # bank group
        lines = [f"- **{item.get('label')}**"]
        for q in item.get("questions", []):
            if not isinstance(q, dict):
                continue
            lines.append(f"  - {q.get('question')}")
            if q.get("expected"):
                lines.append(f"    期望: {q.get('expected')}")
        return "\n".join(lines)
    if "question" in item:  # bank question
        head = f"- **{item.get('question')}**"
        exp = item.get("expected")
        return head if not exp else f"{head}\n  - 期望答案: {exp}"
    if "term" in item:      # tech stack canonical
        return f"- **{item.get('term')}**（occurrences={item.get('occurrences')}）"
    if "spoken" in item:    # ambiguous term
        return f"- `{item.get('spoken')}` → ?{item.get('possible')}（confidence={item.get('confidence')}）"
    if "name" in item or "summary" in item:  # project line
        t = item.get("time_range", "")
        head = f"- **{item.get('name', item.get('term', ''))}**" + (f"（{t}）" if t else "")
        summ = item.get("summary")
        return head if not summ else f"{head}: {summ}"
    bits = [f"{k}={v}" for k, v in item.items() if str(v)]
    return f"- " + (" · ".join(bits) if bits else json.dumps(item, ensure_ascii=False))


def expand(text: str, ctx: dict) -> str:
    def repl(m):
        prefix, mode, path = m.group(1), m.group(2), m.group(0)
        # rebuild clean path
        clean = path.strip("{} ").lstrip(": ")
        # drop the mode/prefix from the token body, keep the root (a/e/b) for resolve
        body = clean
        if prefix:
            body = body[len(prefix) + 1:]  # remove "list:" or "llm:"
        val = resolve(ctx, body)
        if prefix == "list":
            if isinstance(val, list):
                return "\n".join(render_item(v) for v in val if v)
            if isinstance(val, dict):  # e.g. metrics grouped by kind
                lines = []
                for k, v in val.items():
                    head = f"- **{k}**"
                    if isinstance(v, list):
                        lines.append(head)
                        lines += [f"  {render_item(i)}" for i in v if i]
                    else:
                        lines.append(f"{head}: {v}")
                return "\n".join(lines)
            return str(val) if val is not None else ""
        if prefix == "llm":
            if isinstance(val, str) and val.strip():
                return val.strip()
            return f"<!-- TODO LLM: {body} -->"
        # scalar
        if val is None:
            return ""
        if isinstance(val, (list, dict)):
            return json.dumps(val, ensure_ascii=False)
        return str(val)
    return _TOKEN.sub(repl, text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--template", required=True)
    ap.add_argument("--context", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    tmpl = Path(args.template).read_text(encoding="utf-8")
    ctx = json.loads(Path(args.context).read_text(encoding="utf-8"))
    out = expand(tmpl, ctx)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(out, encoding="utf-8")
    print(f"[render] -> {args.out}")


if __name__ == "__main__":
    main()