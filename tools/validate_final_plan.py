#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    p = Path("memory-bank/plan/Final_Implementation_Plan.md")
    if not p.exists():
        print("FAIL: Final_Implementation_Plan.md not found")
        return 2
    text = p.read_text(encoding="utf-8")
    ok = "## Phase-by-Phase" in text and "BL-001" in text and "BL-021" in text
    if ok:
        print("FINAL PLAN VALIDATION: PASS — Phase-by-Phase present")
        return 0
    print("FINAL PLAN VALIDATION: FAIL — Missing Phase-by-Phase section or ranges")
    return 3


if __name__ == "__main__":
    raise SystemExit(main())

