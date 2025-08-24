#!/usr/bin/env python3
from __future__ import annotations
import json
import sys
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    base = Path("/workspace/frameworks/fwk-001-cursor-rules/DOCS/changes/routing_baseline.json")
    eff = Path("/workspace/frameworks/fwk-001-cursor-rules/DOCS/changes/routing_effective.shadow.json")
    if not base.exists() or not eff.exists():
        sys.stderr.write("Baseline or effective routing JSON missing.\n")
        sys.exit(2)
    try:
        jb = load_json(base)
        je = load_json(eff)
    except Exception as e:
        sys.stderr.write(f"ERROR reading JSON: {e}\n")
        sys.exit(3)

    diffs = []
    keys = sorted(set(jb.keys()) | set(je.keys()))
    for k in keys:
        vb = jb.get(k)
        ve = je.get(k)
        if vb != ve:
            diffs.append({"command": k, "baseline": vb, "effective": ve})

    if diffs:
        print(json.dumps({"status": "DRIFT", "count": len(diffs), "diffs": diffs}, indent=2))
        sys.exit(1)
    else:
        print(json.dumps({"status": "OK", "count": 0}))
        sys.exit(0)


if __name__ == "__main__":
    main()

