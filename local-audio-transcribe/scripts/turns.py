"""Deterministic, traceable turn segmentation for FunASR sentence output."""
from __future__ import annotations

import re
from collections import defaultdict
from typing import Any, Iterable

from transcript_core import fmt_timestamp

FILLER = set("呃嗯啊哦诶哎吧哈嗨")


def is_filler(text: str) -> bool:
    text = text.strip()
    return bool(text) and all(ch in FILLER or ch in " ，。、！？!?,.~—-… \t\n" for ch in text)


def segment_turns(
    sentences: Iterable[dict[str, Any]],
    *,
    gap_ms: int = 900,
    max_turn_ms: int = 30_000,
    max_chars: int = 180,
) -> list[dict[str, Any]]:
    """Group sentences without deleting or rewriting source text."""
    turns: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None

    def flush(reason: str | None = None) -> None:
        nonlocal current
        if current is None:
            return
        if reason:
            current["boundary_reason"].append(reason)
        current["text"] = "".join(current.pop("_parts"))
        current["is_filler"] = is_filler(current["text"])
        turns.append(current)
        current = None

    for index, sentence in enumerate(sentences):
        text = re.sub(r"<\|[^|]*\|>", "", str(sentence.get("text", ""))).strip()
        if not text:
            continue
        start = sentence.get("start_ms")
        end = sentence.get("end_ms")
        spk = sentence.get("spk")
        if current is None:
            current = {
                "id": f"turn-{len(turns) + 1:06d}",
                "spk": spk,
                "start_ms": start,
                "end_ms": end,
                "gap_before_ms": None,
                "boundary_reason": ["start"],
                "source_sentence_ids": [sentence.get("id") or f"sentence-{index + 1:06d}"],
                "_parts": [text],
            }
            continue

        gap = None if start is None or current["end_ms"] is None else max(0, start - current["end_ms"])
        reasons: list[str] = []
        if spk != current["spk"]:
            reasons.append("speaker_change")
        if gap is not None and gap > gap_ms:
            reasons.append("silence_gap")
        duration = (end or current["end_ms"] or 0) - (current["start_ms"] or 0)
        chars = len("".join(current["_parts"]))
        if duration > max_turn_ms:
            reasons.append("max_duration")
        if chars + len(text) > max_chars:
            reasons.append("max_chars")
        previous = "".join(current["_parts"])
        if previous.endswith(("。", "！", "？", "!", "?")) and gap and gap > 250:
            reasons.append("punctuation")
        if reasons:
            flush()
            current = {
                "id": f"turn-{len(turns) + 1:06d}",
                "spk": spk,
                "start_ms": start,
                "end_ms": end,
                "gap_before_ms": gap,
                "boundary_reason": reasons,
                "source_sentence_ids": [sentence.get("id") or f"sentence-{index + 1:06d}"],
                "_parts": [text],
            }
        else:
            current["_parts"].append(text)
            current["end_ms"] = end or current["end_ms"]
            current["source_sentence_ids"].append(sentence.get("id") or f"sentence-{index + 1:06d}")
    flush()
    return turns


def render_turns(turns: Iterable[dict[str, Any]], *, speaker_map: dict[str, str] | None = None, keep_fillers: bool = False) -> str:
    speaker_map = speaker_map or {}
    lines: list[str] = []
    for turn in turns:
        if turn.get("is_filler") and not keep_fillers:
            continue
        spk = speaker_map.get(str(turn.get("spk")), str(turn.get("spk")))
        lines.extend([f"说话人 {spk} {fmt_timestamp(turn.get('start_ms'))}", turn["text"], ""])
    return "\n".join(lines)
