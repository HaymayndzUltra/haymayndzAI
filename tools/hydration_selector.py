#!/usr/bin/env python3
"""
Hydration Selector — promotes matching MDC rules from .cursor/test-rules/** to .cursor/rules/**
based on rule_attach_log.json produced by rule_attach_detector.py
Usage:
  python3 tools/hydration_selector.py --attach-log rule_attach_log.json --source .cursor/test-rules --dest .cursor/rules
"""
from __future__ import annotations
import argparse, json, shutil
from pathlib import Path
from typing import Dict, List

def promote(selected: List[str], source_root: Path, dest_root: Path) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    dest_root.mkdir(parents=True, exist_ok=True)

    # Clean previous selections we managed
    managed_idx = dest_root / ".selected.json"
    if managed_idx.exists():
        try:
            prev = json.loads(managed_idx.read_text(encoding="utf-8")).get("files", [])
            for name in prev:
                fp = dest_root / name
                if fp.exists():
                    try:
                        fp.unlink()
                    except Exception:
                        pass
        except Exception:
            pass

    files_written: List[str] = []
    for key in selected:
        if "/" not in key:
            continue
        group, name = key.split("/", 1)
        src = source_root / group / f"{name}.mdc"
        if not src.exists():
            continue
        dst = dest_root / f"{name}_{group}.mdc"
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        files_written.append(dst.name)
        mapping[key] = str(dst)

    (dest_root / ".selected.json").write_text(json.dumps({"files": files_written}, indent=2), encoding="utf-8")
    return mapping

def main() -> int:
    ap = argparse.ArgumentParser(description="Hydration selector for MDC rules")
    ap.add_argument("--attach-log", required=True)
    ap.add_argument("--source", default=".cursor/test-rules")
    ap.add_argument("--dest", default=".cursor/rules")
    args = ap.parse_args()

    attach = json.loads(Path(args.attach_log).read_text(encoding="utf-8"))
    selected = [e["framework"] for e in attach.get("entries", []) if e.get("detected")]
    mapping = promote(selected, Path(args.source), Path(args.dest))
    print(json.dumps({"selected": selected, "mapping": mapping}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
