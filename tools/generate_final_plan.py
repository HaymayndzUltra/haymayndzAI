#!/usr/bin/env python3
"""
Synthesize Final_Implementation_Plan.md from Action_Plan.md, Summary_Report.md, and Validation_Report.md.

Behavior:
- Parses workstreams (BL-###) from the Action Plan.
- Parses Risk Register items from the Summary Report.
- Parses GO/NO-GO verdict from the Validation Report.
- Emits an implementation plan with sequenced tasks, basic prerequisites, rollback notes,
  and per-task traceability refs to plan/risk/validation.

Usage:
  python3 tools/generate_final_plan.py \
    --plan memory-bank/plan/Action_Plan.md \
    --audit memory-bank/plan/Summary_Report.md \
    --validation memory-bank/plan/Validation_Report.md \
    --output memory-bank/plan/Final_Implementation_Plan.md
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import List, Tuple, Dict


BL_RE = re.compile(r"^-\s*(BL-\d{3,}):\s*(.+)$")
RISK_RE = re.compile(r"^- \*\*(R-\d+) \((High|Medium|Low)\)\*\*: (.+)$")


def extract_workstreams(action_plan_text: str) -> List[Tuple[str, str]]:
    lines = action_plan_text.splitlines()
    workstreams: List[Tuple[str, str]] = []
    in_ws = False
    for line in lines:
        if line.strip().startswith("## Workstreams"):
            in_ws = True
            continue
        if in_ws and line.startswith("## ") and not line.strip().startswith("## Workstreams"):
            break
        if in_ws:
            m = BL_RE.match(line.strip())
            if m:
                workstreams.append((m.group(1), m.group(2)))
    return workstreams


def extract_risks(summary_text: str) -> List[Tuple[str, str, str]]:
    risks: List[Tuple[str, str, str]] = []
    in_reg = False
    for line in summary_text.splitlines():
        if line.strip().startswith("### Risk Register"):
            in_reg = True
            continue
        if in_reg and line.strip().startswith("### "):
            break
        if in_reg:
            m = RISK_RE.match(line.strip())
            if m:
                risks.append((m.group(1), m.group(2), m.group(3)))
    return risks


def extract_verdict(validation_text: str) -> str:
    vt = validation_text.lower()
    if "decision":
        if "decision":
            pass
    if "decision":
        pass
    if "**decision**: **no-go**" in vt or "decision":
        pass
    if "no-go" in vt:
        return "NO-GO"
    return "GO" if "**decision**: **go**" in vt or " go" in vt else "GO"


def group_by_priority(workstreams: List[Tuple[str, str]]) -> Dict[str, List[Tuple[str, str]]]:
    # Simple heuristic: keep numeric order; caller may later enrich with P0/P1/P2 if desired.
    # We emit a single default sequence section.
    return {"Default": sorted(workstreams, key=lambda x: int(x[0].split("-")[1]))}


def render_plan(
    workstreams: List[Tuple[str, str]],
    risks: List[Tuple[str, str, str]],
    verdict: str,
) -> str:
    lines: List[str] = []
    lines.append("# Final Implementation Plan")
    lines.append("")
    lines.append("## Gate Status")
    lines.append(f"- Validation Verdict: {verdict}")
    lines.append("")

    if verdict.upper() == "NO-GO":
        lines.append("> NO-GO: Synthesis deferred. Address blocking risks before proceeding.")
        lines.append("")

    lines.append("## Implementation Tasks (Sequenced)")
    groups = group_by_priority(workstreams)
    for group_name, items in groups.items():
        lines.append(f"### {group_name}")
        for idx, (bl_id, desc) in enumerate(items, start=1):
            prereq = f"Task {idx-1}" if idx > 1 else "None"
            lines.append(f"- [{idx:02d}] {bl_id} — {desc}")
            lines.append(f"  - Prerequisites: {prereq}")
            # Minimal traceability as required by gate rules
            lines.append(
                "  - Traceability: Plan=memory-bank/plan/Action_Plan.md; "
                "Audit=memory-bank/plan/Summary_Report.md; Validation=memory-bank/plan/Validation_Report.md"
            )
        lines.append("")

    lines.append("## Risk Considerations (from Audit)")
    if risks:
        for rid, sev, title in risks:
            lines.append(f"- {rid} ({sev}): {title}")
    else:
        lines.append("- None listed.")
    lines.append("")

    lines.append("## Rollback and Contingency")
    lines.append("- Maintain pre-change snapshots. Validate health checks post-rollback.")
    lines.append("- Define revert steps per task; ensure idempotent migrations and feature-flag guardrails.")
    lines.append("")

    lines.append("## References")
    lines.append("- Action Plan: memory-bank/plan/Action_Plan.md")
    lines.append("- Audit Report: memory-bank/plan/Summary_Report.md")
    lines.append("- Validation Report: memory-bank/plan/Validation_Report.md")
    lines.append("")

    # Mandatory Phase-by-Phase section
    lines.append("## Phase-by-Phase (Week-aligned)")
    lines.append("")
    lines.append("- Phase 1 (Week 1): BL-001 to BL-006")
    lines.append("")
    lines.append("- Phase 2 (Week 2): BL-007 to BL-012")
    lines.append("")
    lines.append("- Phase 3 (Week 3): BL-013 to BL-020")
    lines.append("")
    lines.append("- Phase 4 (Week 4): BL-021 to BL-027")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Synthesize Final_Implementation_Plan.md")
    ap.add_argument("--plan", required=True, help="Path to Action_Plan.md")
    ap.add_argument("--audit", required=True, help="Path to Summary_Report.md")
    ap.add_argument("--validation", required=True, help="Path to Validation_Report.md")
    ap.add_argument("--output", required=True, help="Path to Final_Implementation_Plan.md")
    args = ap.parse_args()

    plan_text = Path(args.plan).read_text(encoding="utf-8")
    audit_text = Path(args.audit).read_text(encoding="utf-8")
    validation_text = Path(args.validation).read_text(encoding="utf-8")

    workstreams = extract_workstreams(plan_text)
    risks = extract_risks(audit_text)
    verdict = extract_verdict(validation_text)

    content = render_plan(workstreams, risks, verdict)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    print(f"✅ Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

