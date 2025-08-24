#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHANGES = ROOT / "frameworks" / "fwk-001-cursor-rules" / "DOCS" / "changes"

def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def summarize():
    baseline = CHANGES / "routing_baseline.json"
    effective = CHANGES / "routing_effective.shadow.json"
    override = CHANGES / "routing_override.yaml"  # only presence check; not parsed

    out = {
        "baseline_exists": baseline.exists(),
        "effective_exists": effective.exists(),
        "override_exists": override.exists(),
        "diff": {},
    }

    if baseline.exists() and effective.exists():
        try:
            b = load_json(baseline)
            e = load_json(effective)
            # shallow diff of top-level keys
            bk = set(b.keys())
            ek = set(e.keys())
            out["diff"]["added_keys_in_effective"] = sorted(list(ek - bk))
            out["diff"]["removed_keys_in_effective"] = sorted(list(bk - ek))
        except Exception as ex:
            out["error"] = f"failed to diff: {ex}"

    print(json.dumps(out, indent=2))

def main(argv: list[str]) -> int:
    summarize()
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

