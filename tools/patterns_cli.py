#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


REPO_ROOT = Path(__file__).resolve().parent.parent
PATTERN_FILE = REPO_ROOT / "pattern_library.json"


def _atomic_write_json(path: Path, payload: Any) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _load_patterns() -> List[Dict[str, Any]]:
    if not PATTERN_FILE.exists():
        return []
    try:
        data = json.loads(PATTERN_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception:
        return []


def cmd_add(args: argparse.Namespace) -> int:
    items = _load_patterns()
    rec = {
        "pattern": args.pattern,
        "tags": [t for t in (args.tags or []) if t],
        "source": args.source or "",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    items.append(rec)
    PATTERN_FILE.parent.mkdir(parents=True, exist_ok=True)
    _atomic_write_json(PATTERN_FILE, items)
    print(f"✅ Added pattern to {PATTERN_FILE}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    items = _load_patterns()
    for i, it in enumerate(items, start=1):
        print(f"{i:03d} | {it.get('created_at','')} | {','.join(it.get('tags',[]))} | {it.get('pattern','')[:120]}")
    if not items:
        print("(empty)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Pattern library CLI")
    sub = ap.add_subparsers(dest="cmd", required=True)

    add = sub.add_parser("add", help="Add a pattern")
    add.add_argument("--pattern", required=True)
    add.add_argument("--tags", nargs="*", default=[])
    add.add_argument("--source")
    add.set_defaults(func=cmd_add)

    lst = sub.add_parser("list", help="List patterns")
    lst.set_defaults(func=cmd_list)

    args = ap.parse_args()
    return int(args.func(args) or 0)


if __name__ == "__main__":
    raise SystemExit(main())

