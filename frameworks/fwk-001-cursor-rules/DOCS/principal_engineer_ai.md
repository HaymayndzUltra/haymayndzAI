# principal_engineer_ai

## Purpose
Validates the auditor’s risk report and synthesizes a final, executable plan.

## How It Works
- Mode 1 (Peer Review `/peer_review`):
  - Inputs: `Action_Plan.md`, `Summary_Report.md`.
  - Process: Confirm/Challenge each risk with rationale and traceability; log contested findings; identify NEW-RISKs; produce `Validation_Report.md` with required sections.
- Mode 2 (Synthesis `/synthesize_plan`):
  - Inputs: `Action_Plan.md`, `Summary_Report.md`, `Validation_Report.md`.
  - Process: Derive tasks, sequence with prerequisites, assign priorities, include rollback/contingency, define gates and metrics, and maintain traceability.
  - Output: `Final_Implementation_Plan.md` with recommended sections.
- Constraints: Do not invent risks without NEW-RISK labels; preserve contested findings; respect plan intent.

## How to Use It
- Commands:
  - `/peer_review <Action_Plan.md> <Summary_Report.md>`
  - `/synthesize_plan <Action_Plan.md> <Summary_Report.md> <Validation_Report.md>`
- Reporting rules: explicit, stepwise, measurable; every task has at least one Source reference.

## Example Usage
```bash
/peer_review frameworks/fwk-001-cursor-rules/examples/Action_Plan.md frameworks/fwk-001-cursor-rules/examples/Summary_Report.md
/synthesize_plan frameworks/fwk-001-cursor-rules/examples/Action_Plan.md frameworks/fwk-001-cursor-rules/examples/Summary_Report.md frameworks/fwk-001-cursor-rules/examples/Validation_Report.md
```

## Dependencies
- Consumes outputs from `auditor_ai`; feeds `codegen_ai` and the orchestrator via `Final_Implementation_Plan.md`.