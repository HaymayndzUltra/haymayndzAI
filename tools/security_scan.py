#!/usr/bin/env python3
"""
Security scanner (baseline) — generates security_report.md by performing:
- Heuristic scans for risky patterns (SQLi, XSS, secrets) across supported file types
- Dependency audit stub (placeholder; prints N/A if no lockfiles)

Exit code:
  0 on success (report generated)

Report format:
  ## Summary
  - High: N
  - Medium: N
  - Low: N

  ## Findings
  - [SEVERITY] Rule — path:line — context
"""

from __future__ import annotations

import argparse
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


SUPPORTED_EXTS = {".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".php", ".html", ".md"}
EXCLUDE_DIRS = {".git", "node_modules", ".venv", "venv", "dist", "build", ".cursor"}


@dataclass
class Finding:
    severity: str
    rule: str
    path: str
    line: int
    context: str


PATTERNS = [
    ("HIGH",   r"(exec\(|eval\(|subprocess\.Popen\(|os\.system\()", "Dangerous execution (RCE potential)"),
    ("HIGH",   r"(SELECT\s+.*\+\s*\w+|f\"SELECT.*\{|format\(.*SELECT|\%s.*SELECT)", "Possible SQL query string concatenation"),
    ("MEDIUM", r"request\.(args|get|POST)\[.*\]", "Direct use of request params without validation"),
    ("MEDIUM", r"innerHTML\s*=", "Potential XSS sink via innerHTML assignment"),
    ("LOW",    r"AKIA[0-9A-Z]{16}", "AWS access key pattern leaked"),
]


def iter_files(root: Path) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for name in filenames:
            p = Path(dirpath) / name
            if p.suffix.lower() in SUPPORTED_EXTS and p.stat().st_size < 1_500_000:
                yield p


def scan_file(path: Path) -> List[Finding]:
    findings: List[Finding] = []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return findings
    for sev, pattern, rule in PATTERNS:
        rx = re.compile(pattern, re.IGNORECASE)
        for i, line in enumerate(text.splitlines(), start=1):
            if rx.search(line):
                findings.append(Finding(severity=sev, rule=rule, path=str(path), line=i, context=line.strip()[:200]))
    return findings


def render_report(findings: List[Finding]) -> str:
    high = sum(1 for f in findings if f.severity.upper() == "HIGH")
    med = sum(1 for f in findings if f.severity.upper() == "MEDIUM")
    low = sum(1 for f in findings if f.severity.upper() == "LOW")
    lines: List[str] = []
    lines.append("# Security Report")
    lines.append("")
    lines.append("## Summary")
    lines.append(f"- High: {high}")
    lines.append(f"- Medium: {med}")
    lines.append(f"- Low: {low}")
    lines.append("")
    lines.append("## Dependency Audit (stub)")
    lines.append("- N/A (lockfile not found or audit tool not integrated in baseline)")
    lines.append("")
    lines.append("## Findings")
    if not findings:
        lines.append("- None")
    else:
        for f in findings[:1000]:
            lines.append(f"- [{f.severity}] {f.rule} — {f.path}:{f.line} — {f.context}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Baseline security scanner")
    ap.add_argument("--root", default=str(Path.cwd()), help="Repo root to scan")
    ap.add_argument("--output", default="security_report.md", help="Report path")
    args = ap.parse_args()

    root = Path(args.root)
    findings: List[Finding] = []
    for p in iter_files(root):
        findings.extend(scan_file(p))

    report = render_report(findings)
    out = Path(args.output)
    out.write_text(report, encoding="utf-8")
    print(f"✅ Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

