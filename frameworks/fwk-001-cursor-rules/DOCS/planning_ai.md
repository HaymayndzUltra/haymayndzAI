# planning_ai

## Purpose
Converts product requirements into a detailed, feasible technical plan.

## How It Works
- Consumes `product_backlog.yaml` plus constraints and preferences.
- Produces `technical_plan.md`, `architecture_diagram.mermaid`, `task_breakdown.yaml`.
- Success requires plan passes review with clear tasks and dependencies.
- Single-writer policy: owns `technical_plan.md`.

## How to Use It
- Commands:
  - `/plan`: generate implementation plan from backlog
  - `/architect <feature>`: design architecture
  - `/estimate <task>`: effort estimation
- Allowed verbs: DESIGN, PLAN, ESTIMATE, ARCHITECT.

## Example Usage
```bash
/plan
/architect FEAT-001
/estimate TASK-001
```

## Dependencies
- Depends on `product_owner_ai` output; upstream to `codegen_ai` and `auditor_ai`.