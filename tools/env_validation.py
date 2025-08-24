#!/usr/bin/env python3
from __future__ import annotations
import os
import sys
from pathlib import Path


def validate_memory_storage_root() -> int:
    root = os.environ.get("MEMORY_STORAGE_ROOT", "")
    if not root:
        sys.stderr.write("MEMORY_STORAGE_ROOT not set; defaulting to ./memory-bank\n")
        root = str(Path.cwd() / "memory-bank")
    p = Path(root)
    try:
        p.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        sys.stderr.write(f"ERROR: cannot create/access MEMORY_STORAGE_ROOT at {p}: {e}\n")
        return 2
    # sanity files
    for sub in ["queue-system", "project-brain", "logs"]:
        try:
            (p / sub).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            sys.stderr.write(f"ERROR: cannot create/access {sub} under {p}: {e}\n")
            return 3
    sys.stdout.write(f"MEMORY_STORAGE_ROOT OK: {p}\n")
    return 0


def main() -> None:
    sys.exit(validate_memory_storage_root())


if __name__ == "__main__":
    main()

