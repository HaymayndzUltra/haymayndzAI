#!/usr/bin/env python3
"""
Auto-restore templates for specific Markdown artifacts when files are deleted or emptied.

Behavior:
- Polls target files on an interval.
- If a target is missing or has only whitespace, it restores from the corresponding template.
- Writes are atomic via same-dir temp file and os.replace; file perms set to 0600.

Targets:
- Summary_Report.md
- Validation_Report.md
- Final_Implementation_Plan.md
- Action_Plan.md
- memory-bank/plan/ versions of the above

Usage:
  python3 /workspace/scripts/auto_restore_templates.py --interval 1.0

Notes:
- Pure standard library, no external deps.
"""

from __future__ import annotations

import argparse
import os
import tempfile
import time
from pathlib import Path


def resolve_repo_root() -> Path:
    env_root = os.getenv("REPO_ROOT")
    if env_root:
        try:
            return Path(env_root).resolve()
        except Exception:
            pass
    workspace = Path("/workspace")
    if workspace.exists():
        return workspace.resolve()
    return Path.cwd().resolve()


REPO_ROOT = resolve_repo_root()
TEMPLATES_ROOT = Path(os.getenv(
    "TEMPLATES_ROOT",
    str(REPO_ROOT / "frameworks/fwk-001-cursor-rules/templates"),
))
EXAMPLES_ROOT = Path(os.getenv(
    "EXAMPLES_ROOT",
    str(REPO_ROOT / "frameworks/fwk-001-cursor-rules/examples"),
))
MEMORY_BANK_PLAN_ROOT = Path(os.getenv(
    "MEMORY_BANK_PLAN_ROOT",
    str(REPO_ROOT / "memory-bank/plan"),
))


TARGETS = {
    # Examples directory targets
    EXAMPLES_ROOT / "Summary_Report.md": TEMPLATES_ROOT / "Summary_Report.template.md",
    EXAMPLES_ROOT / "Validation_Report.md": TEMPLATES_ROOT / "Validation_Report.template.md",
    EXAMPLES_ROOT / "Final_Implementation_Plan.md": TEMPLATES_ROOT / "Final_Implementation_Plan.template.md",
    EXAMPLES_ROOT / "Action_Plan.md": TEMPLATES_ROOT / "Action_Plan.template.md",
    
    # Memory bank plan directory targets
    MEMORY_BANK_PLAN_ROOT / "Summary_Report.md": TEMPLATES_ROOT / "Summary_Report.template.md",
    MEMORY_BANK_PLAN_ROOT / "Validation_Report.md": TEMPLATES_ROOT / "Validation_Report.template.md",
    MEMORY_BANK_PLAN_ROOT / "Final_Implementation_Plan.md": TEMPLATES_ROOT / "Final_Implementation_Plan.template.md",
    MEMORY_BANK_PLAN_ROOT / "Action_Plan.md": TEMPLATES_ROOT / "Action_Plan.template.md",
}


def is_effectively_empty(path: Path) -> bool:
    if not path.exists():
        return True
    try:
        content = path.read_text(encoding="utf-8")
    except Exception:
        # If unreadable, treat as empty to trigger repair
        return True
    return len(content.strip()) == 0


def atomic_write_text(path: Path, content: str, perm: int = 0o600) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # Same-directory temporary file to ensure atomic os.replace on same filesystem
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as tmpf:
            os.fchmod(tmpf.fileno(), perm)
            tmpf.write(content)
            tmpf.flush()
            os.fsync(tmpf.fileno())
        os.replace(tmp_name, path)
        # fsync directory to persist rename
        dfd = os.open(path.parent, os.O_DIRECTORY)
        try:
            os.fsync(dfd)
        finally:
            os.close(dfd)
    finally:
        if os.path.exists(tmp_name):
            try:
                os.unlink(tmp_name)
            except Exception:
                pass


def restore_from_template(target: Path, template: Path) -> bool:
    if not template.exists():
        return False
    try:
        template_content = template.read_text(encoding="utf-8")
    except Exception:
        return False
    try:
        atomic_write_text(target, template_content)
        return True
    except Exception:
        return False


def seed_missing_targets() -> None:
    for target, template in TARGETS.items():
        if is_effectively_empty(target):
            restore_from_template(target, template)


def run(interval_seconds: float) -> None:
    seed_missing_targets()
    last_sizes: dict[Path, int] = {}
    while True:
        for target, template in TARGETS.items():
            try:
                if is_effectively_empty(target):
                    restore_from_template(target, template)
                # Track sizes to detect shrink-to-empty dynamics between checks
                if target.exists():
                    try:
                        size = target.stat().st_size
                        last_sizes[target] = size
                    except Exception:
                        pass
            except Exception:
                # Best-effort; continue monitoring other files
                pass
        time.sleep(interval_seconds)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Auto-restore Markdown templates when targets are empty or missing.")
    parser.add_argument("--interval", type=float, default=1.0, help="Polling interval in seconds (default: 1.0)")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(interval_seconds=args.interval)


