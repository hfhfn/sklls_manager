"""
Unit tests for the transcription pipeline. Standard-library only, never loads ASR models.
Run from project root with:  python -m pytest tests
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
SKILL_ROOT = Path(__file__).resolve().parent.parent.parent

import transcript_core as core
import turns as turns_mod
from align_transcripts import align


def load_hotwords():
    return core.load_terms(str(SKILL_ROOT / "config" / "hotwords.json"))


def test_hotwords_load_dedup():
    terms, meta = load_hotwords()
    assert len(terms) >= 10
    assert meta["sha256"]
    names = [t["canonical"] for t in terms]
    assert names.count("RAG") == 1
    assert "bert" in {a.lower() for t in terms for a in t["aliases"]}


def test_merge_hotwords_dedup():
    terms, _ = load_hotwords()
    merged = core.merge_hotwords(terms, ["RAG", "agent", "extra"])
    assert merged.count("RAG") == 1
    assert "extra" in merged


def test_prompt_built():
    terms, _ = load_hotwords()
    prompt = core.build_whisper_prompt(terms)
    assert "RAG" in prompt and "BERT" in prompt
    assert len(prompt) <= 900


def test_unit_conversion():
    assert core.to_ms(1234, unit="ms") == 1234
    assert core.to_ms(28.21, unit="s") == 28210
    assert core.fmt_timestamp(120500) == "02:00"


def test_normalize_text():
    assert core.normalize_text("ＢＥＲＴ 微调") == core.normalize_text("bert微调")
    assert core.normalize_text("a<|token|>b") == "ab"


def test_turn_boundaries():
    sents = [
        {"id": "a", "start_ms": 0, "end_ms": 300, "spk": 0, "text": "你好。BERT嘛。"},
        {"id": "b", "start_ms": 2000, "end_ms": 2300, "spk": 0, "text": "后面这句。"},
        {"id": "c", "start_ms": 2400, "end_ms": 2600, "spk": 1, "text": "嗯。"},
    ]
    result = turns_mod.segment_turns(sents, gap_ms=900)
    assert len(result) == 3  # silence gap splits a,b; speaker change splits c


def test_turn_filler_preserved():
    sents = [{"id": "a", "start_ms": 0, "end_ms": 200, "spk": 1, "text": "嗯嗯"}]
    result = turns_mod.segment_turns(sents)
    assert result[0]["is_filler"] is True
    assert turns_mod.render_turns(result, keep_fillers=False) == ""


def test_alignment_one_to_many_and_unmatched():
    funasr = [
        {"id": "f1", "start_ms": 0, "end_ms": 1500, "spk": 0, "text": "什么是RAG？"},
        {"id": "f2", "start_ms": 5000, "end_ms": 6000, "spk": 0, "text": "未录音对话"},
    ]
    whisper = [
        {"id": "w1", "start_ms": 0, "end_ms": 1500, "spk": None, "text": "什么是RAG？"},
        {"id": "w2", "start_ms": 9000, "end_ms": 10000, "spk": None, "text": "没有对应内容"},
    ]
    terms, _ = load_hotwords()
    pairs = align(funasr, whisper, terms)
    matched = [p for p in pairs if p["status"] == "candidate"]
    unmatched = [p for p in pairs if p["status"] == "unmatched"]
    assert matched and unmatched


def test_term_matches_alias():
    terms, _ = load_hotwords()
    hits = core.term_matches("拍的是喜察察的API吗", terms)
    assert any(h["canonical"] == "企查查" for h in hits)


def main():
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for fn in tests:
        fn()
        print(f"[ok] {fn.__name__}")
    print(f"all {len(tests)} passed")


if __name__ == "__main__":
    main()