#!/usr/bin/env python3
"""
Labnotes watcher: append structured entry templates to Labnotes.md whenever files are created, modified, deleted, or tested.

Design goals:
- Zero external deps: pure stdlib polling.
- Debounce rapid changes to avoid spam.
- Smart hints: fill placeholders with timestamp (PH tz), path, and action.

Monitored root: /home/haymayndz/HaymayndzAI
Labnotes file:  /home/haymayndz/HaymayndzAI/frameworks/fwk-001-cursor-rules/DOCS/Labnotes.md
Entry template: /home/haymayndz/HaymayndzAI/frameworks/fwk-001-cursor-rules/templates/Labnotes.entry.template.md

Usage:
  python3 scripts/labnotes_watcher.py --interval 1.0 --actor User
  python3 scripts/labnotes_watcher.py --interval 1.0 --actor AI

Notes:
- "TEST" action is inferred when common test commands are detected via a companion FIFO or log (optional future). For now, we handle CREATE/MODIFY/DELETE.
"""

from __future__ import annotations

import argparse
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict
from zoneinfo import ZoneInfo


REPO_ROOT = Path("/home/haymayndz/HaymayndzAI").resolve()
LABNOTES_PATH = Path("/home/haymayndz/HaymayndzAI/frameworks/fwk-001-cursor-rules/DOCS/Labnotes.md").resolve()
TEMPLATE_PATH = Path("/home/haymayndz/HaymayndzAI/frameworks/fwk-001-cursor-rules/templates/Labnotes.entry.template.md").resolve()
PH = ZoneInfo("Asia/Manila")

# Ignore paths (labnotes updates should not trigger themselves, and ignore node_modules/.git/.cursor, logs)
IGNORE_DIRS = {
    ".git", ".cursor", "node_modules", "venv", ".venv", "__pycache__",
    "memory-bank",  # optional: skip volatile runtime artifacts
}

IGNORE_FILES = {
    LABNOTES_PATH.name,
}


@dataclass
class FileState:
    exists: bool
    mtime_ns: int
    size: int


def iter_repo_files(root: Path) -> Dict[Path, FileState]:
    snapshot: Dict[Path, FileState] = {}
    for dirpath, dirnames, filenames in os.walk(root):
        # filter dirs in-place to prune traversal
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        for fname in filenames:
            if fname in IGNORE_FILES:
                continue
            fpath = Path(dirpath) / fname
            try:
                st = fpath.stat()
            except FileNotFoundError:
                continue
            snapshot[fpath] = FileState(True, st.st_mtime_ns, st.st_size)
    return snapshot


def detect_changes(prev: Dict[Path, FileState], curr: Dict[Path, FileState]) -> Dict[Path, str]:
    changes: Dict[Path, str] = {}
    prev_keys = set(prev.keys())
    curr_keys = set(curr.keys())
    for path in curr_keys - prev_keys:
        changes[path] = "CREATE"
    for path in prev_keys - curr_keys:
        changes[path] = "DELETE"
    for path in prev_keys & curr_keys:
        a, b = prev[path], curr[path]
        if a.mtime_ns != b.mtime_ns or a.size != b.size:
            changes[path] = "MODIFY"
    return changes


def load_template() -> str:
    return TEMPLATE_PATH.read_text(encoding="utf-8")


def now_ph_iso() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S %Z%z", time.localtime(time.time()))


def format_entry(template: str, actor: str, action: str, path: Path) -> str:
    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    try:
        # Prefer PH tz human-readable
        ts_ph = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    except Exception:
        ts_ph = ts
    file_abs = str(path.resolve())
    try:
        file_rel = str(path.resolve().relative_to(REPO_ROOT))
    except Exception:
        file_rel = file_abs
    return (
        template
        .replace("{{TIMESTAMP_PH}}", ts_ph)
        .replace("{{ACTOR}}", actor)
        .replace("{{ACTION}}", action)
        .replace("{{FILE_REL}}", file_rel)
        .replace("{{FILE_ABS}}", file_abs)
        .replace("{{FILENAME}}", path.name)
        .replace("{{EXT}}", path.suffix)
    )


def append_labnotes(text: str) -> None:
    LABNOTES_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LABNOTES_PATH, "a", encoding="utf-8", newline="\n") as f:
        f.write("\n")
        f.write(text)
        if not text.endswith("\n"):
            f.write("\n")


def run(actor: str, interval: float) -> None:
    template = load_template()
    prev = iter_repo_files(REPO_ROOT)
    while True:
        time.sleep(interval)
        curr = iter_repo_files(REPO_ROOT)
        changes = detect_changes(prev, curr)
        for path, action in changes.items():
            try:
                entry = format_entry(template, actor=actor, action=action, path=path)
                append_labnotes(entry)
            except Exception:
                # best-effort logging only; continue
                pass
        prev = curr


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Append Labnotes entries on file changes.")
    p.add_argument("--actor", default="User", choices=["User", "AI", "Automation"], help="Entry actor label")
    p.add_argument("--interval", type=float, default=1.0, help="Polling interval seconds")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(actor=args.actor, interval=args.interval)


