# auditor_ai

## Purpose
Performs pre-mortem risk analysis of the Action Plan and produces a concise risk summary.

## How It Works
- Inputs: `Action_Plan.md` (from planning or author), supporting context if provided.
- Process: Identify risks, blind spots, and assumptions; assess severity/likelihood; ensure traceability to plan sections; generate `Summary_Report.md`.
- Output: `Summary_Report.md` containing risks table and verdict; if no issues, includes explicit confirmation line.
- Gate: Feeds `audit_gate` (required before Principal Engineer validation).

## How to Use It
- Commands:
  - `/audit <Action_Plan.md>`: run pre-mortem audit and produce `Summary_Report.md`.
- Reporting rules: risks must be traceable to plan sections; ambiguous verdicts are rejected by the gate.

## Example Usage
```bash
/audit frameworks/fwk-001-cursor-rules/examples/Action_Plan.md
```

## Dependencies
- Runs after `planning_ai` has produced `technical_plan.md`/`Action_Plan.md`.
- Upstream for `principal_engineer_ai` peer review and synthesis.