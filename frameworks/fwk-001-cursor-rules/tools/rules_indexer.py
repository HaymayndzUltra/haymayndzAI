#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

HARVESTED = Path("/workspace/frameworks/fwk-001-cursor-rules/DOCS/harvested")
OUT_INDEX = Path("/workspace/frameworks/fwk-001-cursor-rules/tools/rule_index.json")

SECTION_RE = re.compile(r"^\[([A-Za-z_]+)\]\s*$")
META_RE = re.compile(r"%%([\s\S]*?)%%", re.MULTILINE)

STOPWORDS = set("the a an and or for of to in with on at by from as is are be this that it".split())

def parse_sections(text: str) -> Dict[str, str]:
    lines = text.splitlines()
    sections: Dict[str, List[str]] = {}
    current = None
    for line in lines:
        m = SECTION_RE.match(line.strip())
        if m:
            current = m.group(1).upper()
            sections[current] = []
        elif current:
            sections[current].append(line)
    return {k: "\n".join(v).strip() for k, v in sections.items()}

def parse_meta(text: str) -> Dict[str, str]:
    m = META_RE.search(text)
    meta = {}
    if not m:
        return meta
    block = m.group(1)
    for line in block.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip().lower()] = v.strip()
    return meta

def keywords(s: str, limit: int = 12) -> List[str]:
    tokens = re.findall(r"[A-Za-z0-9_]+", s.lower())
    tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 2]
    # simple frequency sort
    freq: Dict[str, int] = {}
    for t in tokens:
        freq[t] = freq.get(t, 0) + 1
    return [k for k, _ in sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))[:limit]]

def build_index() -> List[Dict]:
    entries: List[Dict] = []
    for path in HARVESTED.rglob("*.mdc"):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        meta = parse_meta(text)
        sections = parse_sections(text)
        intent_raw = (sections.get("INTENT") or "").strip()
        intent = intent_raw.splitlines()[0].strip().lower() if intent_raw else ""
        instr = sections.get("INSTRUCTIONS", "")
        guardrails = sections.get("GUARDRAILS", "")
        tags = [t.strip().lower() for t in re.split(r"[,\s]+", meta.get("tags", "")) if t.strip()]
        entry = {
            "path": str(path),
            "hash": meta.get("hash", ""),
            "tags": tags,
            "intent": intent,
            "instructions_excerpt": instr[:400],
            "instructions_keywords": keywords(instr),
            "guardrails_present": bool(guardrails.strip()),
            "sections": {
                "INSTRUCTIONS": True if instr else False,
                "GUARDRAILS": True if guardrails else False
            }
        }
        entries.append(entry)
    return entries

def main(argv: List[str]) -> int:
    entries = build_index()
    OUT_INDEX.parent.mkdir(parents=True, exist_ok=True)
    OUT_INDEX.write_text(json.dumps(entries, indent=2), encoding="utf-8")
    print(f"Wrote index: {OUT_INDEX} ({len(entries)} entries)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

