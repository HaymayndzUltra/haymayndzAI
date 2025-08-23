#!/usr/bin/env python3
import argparse
import os
import re
import sys
from pathlib import Path
from typing import List, Tuple


PURPOSE_PATTERNS = [
    re.compile(r"^##\s*1\.\s*PURPOSE\b", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^#\s*Purpose\b", re.IGNORECASE | re.MULTILINE),
]

OUTPUT_PATTERNS = [
    re.compile(r"^##\s*3\.\s*OUTPUT\s+CONTRACT\b", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^#\s*Output\s+Artifact\b", re.IGNORECASE | re.MULTILINE),
]

INTERACTION_PATTERNS = [
    re.compile(r"^##\s*4\.\s*INTERACTION\s+RULES\b", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^#\s*Triggers\s*/\s*Commands\b", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^#\s*Modes\s*&\s*Commands\b", re.IGNORECASE | re.MULTILINE),
]

CHANGELOG_PATTERNS = [
    re.compile(r"CHANGELOG", re.IGNORECASE),
]

ABSOLUTE_PATH_PATTERNS = [
    re.compile(r"/home/[\w\-]+/[^\s`]+"),
    re.compile(r"/workspace/[^\s`]+"),
]


def has_any(text: str, patterns: List[re.Pattern]) -> bool:
    return any(p.search(text) for p in patterns)


def validate_file(path: Path) -> List[str]:
    content = path.read_text(encoding="utf-8", errors="ignore")
    issues: List[str] = []

    if not has_any(content, PURPOSE_PATTERNS):
        issues.append("Missing Purpose section (## 1. PURPOSE or # Purpose)")

    if not has_any(content, OUTPUT_PATTERNS):
        issues.append("Missing Output section (## 3. OUTPUT CONTRACT or # Output Artifact)")

    if not has_any(content, INTERACTION_PATTERNS):
        issues.append("Missing Interaction/Commands section")

    if not has_any(content, CHANGELOG_PATTERNS):
        issues.append("Missing Changelog reference")

    for p in ABSOLUTE_PATH_PATTERNS:
        m = p.search(content)
        if m:
            issues.append(f"Found absolute path: {m.group(0)}")

    return issues


def discover_repo_root() -> Path:
    env = os.getenv("REPO_ROOT")
    if env:
        try:
            return Path(env).resolve()
        except Exception:
            pass
    ws = Path("/workspace")
    if ws.exists():
        return ws.resolve()
    return Path.cwd().resolve()


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate .mdc files for contract structure and portability")
    ap.add_argument("--paths", nargs="*", default=["frameworks/fwk-001-cursor-rules/system-prompt"], help="Paths or files to scan")
    args = ap.parse_args()

    repo = discover_repo_root()
    targets: List[Path] = []
    for p in args.paths:
        path = (repo / p).resolve() if not Path(p).is_absolute() else Path(p)
        if path.is_file() and path.suffix == ".mdc":
            targets.append(path)
        elif path.is_dir():
            targets.extend(path.rglob("*.mdc"))

    if not targets:
        print("No .mdc files found to validate.")
        return 1

    total = 0
    failed = 0
    for f in sorted(targets):
        total += 1
        issues = validate_file(f)
        if issues:
            failed += 1
            print(f"[FAIL] {f}")
            for i in issues:
                print(f"  - {i}")
        else:
            print(f"[OK]   {f}")

    print(f"\nChecked: {total}, Failures: {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())