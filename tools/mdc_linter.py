#!/usr/bin/env python3
"""
MDC Linter/Formatter
Validates and auto-fixes MDC frontmatter:
- description: <string>
- globs: <list>
- alwaysApply: false
Usage:
  python3 tools/mdc_linter.py --paths .cursor/test-rules .cursor/rules --write
"""
from __future__ import annotations
import argparse, json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple
try:
    import yaml  # type: ignore
except Exception:
    yaml = None

@dataclass
class LintResult:
    path: Path
    changed: bool
    issues: List[str]
    before_keys: List[str]
    after_keys: List[str]

def find_frontmatter_blocks(text: str) -> Tuple[Optional[Tuple[int, int]], Optional[str]]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, None
    for i in range(1, min(len(lines), 400)):
        if lines[i].strip() == "---":
            return (0, i), "\n".join(lines[1:i])
    return None, None

def parse_yaml(s: str) -> Dict:
    if yaml is None:
        out: Dict[str, object] = {}
        for ln in s.splitlines():
            if ":" in ln:
                k, v = ln.split(":", 1)
                out[k.strip()] = v.strip()
        return out
    try:
        return yaml.safe_load(s) or {}
    except Exception:
        # invalid YAML → treat as empty so we can rebuild safely
        return {}

def dump_yaml(obj: Dict) -> str:
    if yaml is None:
        lines = []
        for k, v in obj.items():
            if isinstance(v, list):
                lines.append(f"{k}: {json.dumps(v)}")
            else:
                lines.append(f"{k}: {v}")
        return "\n".join(lines) + "\n"
    return yaml.safe_dump(obj, sort_keys=False).strip() + "\n"

def ensure_frontmatter(text: str) -> Tuple[str, LintResult]:
    issues: List[str] = []
    block, fm_text = find_frontmatter_blocks(text)
    changed = False
    before_keys: List[str] = []
    after_keys: List[str] = []

    if block is None:
        fm: Dict[str, object] = {"description": "", "globs": [], "alwaysApply": False}
        new_fm = f"---\n{dump_yaml(fm)}---\n"
        return new_fm + text.lstrip("\n"), LintResult(Path(), True, ["added-frontmatter"], [], list(fm.keys()))

    start, end = block
    lines = text.splitlines()
    current_fm = parse_yaml(fm_text or "")
    before_keys = list(current_fm.keys())

    if "description" not in current_fm or current_fm.get("description") in (None, ""):
        current_fm["description"] = ""
        issues.append("missing-description"); changed = True

    val = current_fm.get("globs")
    if isinstance(val, str):
        current_fm["globs"] = [x.strip().strip("'\"") for x in val.split(",") if x.strip()]
        issues.append("globs-normalized-from-string"); changed = True
    if "globs" not in current_fm or not isinstance(current_fm.get("globs"), list):
        current_fm["globs"] = []
        issues.append("missing-globs"); changed = True

    if "alwaysApply" not in current_fm or not isinstance(current_fm.get("alwaysApply"), bool):
        current_fm["alwaysApply"] = False
        issues.append("alwaysApply-normalized-false"); changed = True

    after_keys = list(current_fm.keys())
    if changed:
        new_fm_body = dump_yaml(current_fm).rstrip("\n")
        new_lines = []
        new_lines.extend(lines[: start + 1])         # keep opening ---
        new_lines.extend(new_fm_body.splitlines())   # normalized body
        new_lines.extend(lines[end:])                # keep closing --- and rest
        return "\n".join(new_lines), LintResult(Path(), True, issues, before_keys, after_keys)

    return text, LintResult(Path(), False, issues, before_keys, after_keys)

def process_file(fp: Path, write: bool) -> LintResult:
    raw = fp.read_text(encoding="utf-8")
    fixed, res = ensure_frontmatter(raw)
    res.path = fp
    if write and fixed != raw:
        tmp = fp.with_suffix(fp.suffix + ".tmp")
        tmp.write_text(fixed, encoding="utf-8")
        tmp.replace(fp)
    return res

def main() -> int:
    ap = argparse.ArgumentParser(description="MDC linter/auto-fixer")
    ap.add_argument("--paths", nargs="*", default=[".cursor/test-rules", ".cursor/rules"], help="Directories to scan")
    ap.add_argument("--write", action="store_true", help="Apply fixes in-place")
    args = ap.parse_args()

    roots = [Path(p) for p in args.paths]
    results: List[LintResult] = []
    for root in roots:
        if not root.exists():
            continue
        for fp in root.rglob("*.mdc"):
            results.append(process_file(fp, args.write))

    summary = {
        "checked": len(results),
        "changed": sum(1 for r in results if r.changed),
        "issues": {
            k: sum(1 for r in results if k in r.issues)
            for k in ["added-frontmatter","missing-description","missing-globs","alwaysApply-normalized-false","globs-normalized-from-string"]
        },
        "files": [{
            "path": str(r.path),
            "changed": r.changed,
            "issues": r.issues,
            "before_keys": r.before_keys,
            "after_keys": r.after_keys,
        } for r in results],
    }
    print(json.dumps(summary, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
