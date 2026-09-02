"""Shared, dependency-free helpers for the local transcription and terminology pipeline."""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence

RAW_SCHEMA_VERSION = "raw-transcript-v1"
TURNS_SCHEMA_VERSION = "transcript-turns-v1"
TERMS_SCHEMA_VERSION = "terms-v2"
TERM_PRECEDENCE = ("global", "project", "session", "explicit")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_json(value: Any) -> str:
    data = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def read_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: str | Path, value: Any) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def normalize_text(text: str) -> str:
    """Normalize only for matching/deduplication; never use it to overwrite transcripts."""
    text = unicodedata.normalize("NFKC", text or "")
    text = re.sub(r"<\|[^|]*\|>", "", text)
    text = re.sub(r"[\s　]+", "", text)
    return text.casefold()


def text_similarity(left: str, right: str) -> float:
    from difflib import SequenceMatcher
    return SequenceMatcher(None, normalize_text(left), normalize_text(right)).ratio()


def to_ms(value: Any, *, unit: str | None = None) -> int | None:
    if value is None:
        return None
    number = float(value)
    if unit == "ms":
        return round(number)
    if unit == "s":
        return round(number * 1000)
    return round(number if isinstance(value, int) or number > 10_000 else number * 1000)


def fmt_timestamp(ms: int | None) -> str:
    if ms is None:
        return "--:--"
    seconds = max(0, ms) // 1000
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def make_source_id(engine: str, index: int) -> str:
    return f"{engine}-{index:06d}"


def _alias_record(value: Any, *, default_status: str = "approved") -> dict[str, Any] | None:
    if isinstance(value, str):
        text = value.strip()
        record = {"text": text, "status": default_status, "type": "legacy_alias"}
    elif isinstance(value, dict):
        text = str(value.get("text", "")).strip()
        record = {"text": text, "status": value.get("status", default_status),
                  "type": value.get("type", "alias"), "source": value.get("source")}
    else:
        return None
    return record if text else None


def _normalize_term(item: Any, *, scope: str = "legacy") -> dict[str, Any] | None:
    if isinstance(item, str):
        raw = {"canonical": item}
    elif isinstance(item, dict):
        raw = item
    else:
        return None
    canonical = str(raw.get("canonical", "")).strip()
    status = raw.get("status", "approved")
    if not canonical or raw.get("enabled", True) is False or status not in {"approved", "published"}:
        return None
    aliases = [alias for alias in (_alias_record(value) for value in raw.get("aliases", []))
               if alias and alias["status"] in {"approved", "published"}]
    aliases = [alias["text"] for alias in aliases]
    return {
        "term_id": raw.get("term_id") or f"{scope}.{normalize_text(canonical)}",
        "canonical": canonical,
        "display": raw.get("display", canonical),
        "aliases": aliases,
        "category": raw.get("category", "general"),
        "scope": raw.get("scope", scope),
        "priority": int(raw.get("priority", 0)),
        "weight": raw.get("weight", 1.0),
        "enabled": True,
        "status": status,
        "sensitivity": raw.get("sensitivity", "normal"),
        "owner": raw.get("owner"),
    }


def _read_term_file(path: str | Path, *, expected_scope: str | None = None) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    source = Path(path)
    data = read_json(source)
    scope = data.get("scope", expected_scope or "legacy")
    if expected_scope and scope not in {expected_scope, "legacy"}:
        raise ValueError(f"{source}: expected scope {expected_scope}, got {scope}")
    terms = []
    for item in data.get("terms", data if isinstance(data, list) else []):
        term = _normalize_term(item, scope=scope)
        if term:
            terms.append(term)
    metadata = data if isinstance(data, dict) else {}
    return terms, {
        "path": str(source), "sha256": sha256_file(source), "scope": scope,
        "dictionary_id": metadata.get("dictionary_id", source.stem), "version": metadata.get("version"),
        "prompt_text": metadata.get("prompt_text", ""), "schema_version": metadata.get("schema_version", "hotwords-v1"),
    }


def load_terms(path: str | Path | None) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Legacy single-file reader. Returns only approved/enabled terms."""
    if not path:
        return [], {}
    return _read_term_file(path)


def _check_term_conflicts(terms: Sequence[dict[str, Any]]) -> list[dict[str, str]]:
    owners: dict[str, str] = {}
    conflicts = []
    for term in terms:
        forms = [term["canonical"]] + [alias if isinstance(alias, str) else alias["text"] for alias in term["aliases"]]
        for form in forms:
            key = normalize_text(form)
            existing = owners.get(key)
            if existing and existing != term["canonical"]:
                conflicts.append({"form": form, "canonical_a": existing, "canonical_b": term["canonical"]})
            else:
                owners[key] = term["canonical"]
    return conflicts


def load_term_layers(
    *,
    global_files: Iterable[str | Path] = (),
    project_files: Iterable[str | Path] = (),
    session_file: str | Path | None = None,
    explicit_terms: Iterable[str] = (),
    audio_sha256: str | None = None,
    allow_cross_session: bool = False,
    strict: bool = True,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Resolve global < project < session < explicit terms into one immutable snapshot."""
    layers: list[tuple[str, list[str | Path]]] = [
        ("global", list(global_files)), ("project", list(project_files)),
        ("session", [session_file] if session_file else []),
    ]
    merged: dict[str, dict[str, Any]] = {}
    source_meta = []
    all_terms: list[dict[str, Any]] = []
    for scope, files in layers:
        for path in files:
            terms, meta = _read_term_file(path, expected_scope=scope)
            document = read_json(path)
            bound_hash = document.get("session", {}).get("audio_sha256")
            if scope == "session" and bound_hash and audio_sha256 and bound_hash != audio_sha256:
                if not allow_cross_session:
                    raise ValueError("session terms audio_sha256 does not match input audio")
                meta["warning"] = "cross_session_terms_allowed"
            source_meta.append(meta)
            all_terms.extend(terms)
            for term in terms:
                key = normalize_text(term["canonical"])
                merged[key] = dict(term, scope=scope, origin_file=str(path))
    conflicts = _check_term_conflicts(list(merged.values()))
    if conflicts and strict:
        first = conflicts[0]
        raise ValueError(f"term collision: {first['form']} maps to {first['canonical_a']} and {first['canonical_b']}")
    explicit = []
    for value in explicit_terms:
        term = _normalize_term({"canonical": value, "scope": "explicit", "priority": 1000}, scope="explicit")
        if term:
            explicit.append(term)
            merged[normalize_text(term["canonical"])] = term
    resolved = sorted(merged.values(), key=lambda item: (-item["priority"], normalize_text(item["canonical"])))
    snapshot = {
        "schema_version": TERMS_SCHEMA_VERSION, "precedence": list(TERM_PRECEDENCE),
        "sources": source_meta, "terms": resolved, "conflicts": conflicts,
        "explicit_session_overrides": [term["canonical"] for term in explicit],
    }
    snapshot["resolved_sha256"] = sha256_json(snapshot)
    return resolved, snapshot


def resolve_cli_terms(args: Any, *, audio_sha256: str | None = None) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Resolve new layered CLI flags while keeping --hotwords-file compatible."""
    legacy = getattr(args, "hotwords_file", None)
    project_files = list(getattr(args, "project_terms_file", []) or [])
    if legacy:
        project_files.append(legacy)
    global_files = list(getattr(args, "global_terms_file", []) or [])
    session_file = getattr(args, "session_terms_file", None)
    explicit = [value for value in (getattr(args, "hotwords", "") or "").split(",") if value.strip()]
    return load_term_layers(global_files=global_files, project_files=project_files,
                            session_file=session_file, explicit_terms=explicit,
                            audio_sha256=audio_sha256,
                            allow_cross_session=getattr(args, "allow_cross_session_terms", False),
                            strict=not getattr(args, "allow_term_conflicts", False))

def merge_hotwords(terms: Iterable[dict[str, Any]], extra: Iterable[str] = ()) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in [term["canonical"] for term in terms] + list(extra):
        value = str(value).strip()
        key = normalize_text(value)
        if value and key not in seen:
            seen.add(key)
            result.append(value)
    return result


def build_whisper_prompt(terms: Iterable[dict[str, Any]], extra_prompt: str = "", *, max_chars: int = 900) -> str:
    canonical = ", ".join(term["canonical"] for term in terms)
    parts = [part.strip() for part in [extra_prompt, canonical] if part and part.strip()]
    if not parts:
        return ""
    return ("请保留人名、产品名、缩写及术语的标准拼写：" + "；".join(parts))[:max_chars]


def extract_segments(document: dict[str, Any], *, engine_hint: str | None = None) -> list[dict[str, Any]]:
    engine = engine_hint or document.get("source", {}).get("engine")
    source = document.get("sentences") or document.get("segments") or []
    result: list[dict[str, Any]] = []
    for index, item in enumerate(source, 1):
        text = str(item.get("text") or item.get("sentence") or "").strip()
        if not text:
            continue
        is_whisper = engine == "whisper" or ("start" in item and "start_ms" not in item)
        start = item.get("start_ms", item.get("start"))
        end = item.get("end_ms", item.get("end"))
        result.append({"id": item.get("id") or make_source_id(engine or "segment", index),
                       "start_ms": to_ms(start, unit="s" if is_whisper and "start_ms" not in item else "ms"),
                       "end_ms": to_ms(end, unit="s" if is_whisper and "end_ms" not in item else "ms"),
                       "spk": item.get("spk"), "text": text, "raw": item})
    return result


def _is_latin_term(value: str) -> bool:
    return bool(re.fullmatch(r"[a-z0-9][a-z0-9._+-]*", value, flags=re.I))


def term_matches(text: str, terms: Iterable[dict[str, Any]]) -> list[dict[str, str]]:
    """Longest-first, non-overlapping matching with Latin token boundaries."""
    normalized = normalize_text(text)
    candidates = []
    for term in terms:
        variants = [(term["canonical"], "exact")] + [(alias if isinstance(alias, str) else alias["text"], "alias") for alias in term.get("aliases", [])]
        for variant, kind in variants:
            needle = normalize_text(variant)
            if not needle:
                continue
            start = 0
            while True:
                index = normalized.find(needle, start)
                if index < 0:
                    break
                end = index + len(needle)
                if _is_latin_term(needle):
                    before = normalized[index - 1:index]
                    after = normalized[end:end + 1]
                    if (before and before.isalnum()) or (after and after.isalnum()):
                        start = index + 1
                        continue
                candidates.append((index, end, term["canonical"], variant, kind))
                start = index + max(1, len(needle))
    selected = []
    occupied: list[tuple[int, int]] = []
    for candidate in sorted(candidates, key=lambda x: (x[0], -(x[1] - x[0]), x[2])):
        if any(candidate[0] < end and start < candidate[1] for start, end in occupied):
            continue
        occupied.append((candidate[0], candidate[1]))
        selected.append({"canonical": candidate[2], "matched": candidate[3], "kind": candidate[4],
                         "start": candidate[0], "end": candidate[1]})
    return selected
