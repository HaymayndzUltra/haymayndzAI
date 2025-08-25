#!/usr/bin/env python3
"""
Security Gate — reads security_report.md and exits non-zero if any High issues.

Exit codes:
  0 — PASS (no High issues)
  3 — BLOCK (High issues found)
"""

from __future__ import annotations

import argparse
from pathlib import Path


def parse_summary(report_text: str) -> int:
    high = 0
    for line in report_text.splitlines():
        line = line.strip()
        if line.lower().startswith("- high:"):
            try:
                high = int(line.split(":", 1)[1].strip())
            except Exception:
                high = 0
            break
    return high


def main() -> int:
    ap = argparse.ArgumentParser(description="Security gate evaluator")
    ap.add_argument("--report", default="security_report.md", help="Path to security_report.md")
    args = ap.parse_args()

    p = Path(args.report)
    if not p.exists():
        print(f"❌ Report not found: {p}")
        return 3
    text = p.read_text(encoding="utf-8")
    high_count = parse_summary(text)
    if high_count > 0:
        print(f"SECURITY GATE: BLOCK — High issues: {high_count}")
        return 3
    print("SECURITY GATE: PASS — No High issues")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

