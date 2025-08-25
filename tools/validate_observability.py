#!/usr/bin/env python3
"""
Validate observability artifacts:
- YAML lints cleanly for alerts.yaml
- Mermaid content has basic structure (flowchart / graph) for dashboards.mmd
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def validate_yaml(path: Path) -> bool:
    try:
        import yaml  # type: ignore
    except Exception:
        print("WARN: PyYAML not installed; skipping strict YAML parse. Assuming OK.")
        return path.exists() and path.read_text(encoding="utf-8").strip() != ""
    try:
        yaml.safe_load(path.read_text(encoding="utf-8"))
        return True
    except Exception as e:
        print(f"YAML ERROR: {e}")
        return False


def validate_mermaid(path: Path) -> bool:
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    if not text.strip():
        return False
    # Basic heuristic: contains a flowchart/graph declaration
    lowered = text.lower()
    return ("flowchart" in lowered) or ("graph" in lowered)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--alerts", required=True)
    ap.add_argument("--dashboards", required=True)
    args = ap.parse_args()

    alerts_ok = validate_yaml(Path(args.alerts))
    dashboards_ok = validate_mermaid(Path(args.dashboards))

    if alerts_ok and dashboards_ok:
        print("OBS VALIDATION: PASS")
        return 0
    if not alerts_ok:
        print("OBS VALIDATION: FAIL — alerts.yaml invalid")
    if not dashboards_ok:
        print("OBS VALIDATION: FAIL — dashboards.mmd invalid")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

