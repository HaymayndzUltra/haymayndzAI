# execution_orchestrator

## Purpose
Coordinates the framework pipeline, sequencing roles, enforcing gates, and managing workflow state and recovery.

## How It Works
- Maintains a pipeline graph linking `product_owner_ai → planning_ai → codegen_ai → qa_ai → mlops_ai`, with parallel/support paths to `documentation_ai`, `analyst_ai`, and `observability_ai`. Adds `auditor_ai` and `principal_engineer_ai` phases between planning and codegen.
- Enforces YAML-defined gates: planning, code_generation, quality_assurance, deployment, audit, verification, and synthesis. Each gate defines required inputs, validation rules, and blocking conditions.
- Tracks workflow states (IDLE, PLANNING, DEVELOPMENT, TESTING, DEPLOYMENT, MONITORING, BLOCKED, ROLLBACK, AUDIT, VALIDATION, SYNTHESIS) with allowed transitions and active roles per state.
- Implements error-handling policies with actions like BLOCK, ESCALATE, HALT_PIPELINE, WAIT_RETRY, including special handling for audit/verification conflicts and synthesis incompleteness.
- Defines sequential and parallel handoff rules, triggering transitions upon artifact readiness (e.g., `technical_plan.md approved`).

## How to Use It
- Triggers:
  - `/run_pipeline`: start the end-to-end pipeline
  - `/status`: show current state and progress
  - `/halt`: emergency stop
  - `/resume`: continue from last checkpoint
- Allowed commands: START, STOP, PAUSE, RESUME, STATUS
- Single-writer policy: yes (owns `workflow_state.json`).

## Example Usage
```bash
# Start full pipeline
/run_pipeline

# Check status
/status

# Halt and later resume
/halt
/resume
```

## Dependencies
- Upstream roles and artifacts:
  - `product_owner_ai`: `product_backlog.yaml`
  - `planning_ai`: `technical_plan.md`, `task_breakdown.yaml`
  - `codegen_ai`: `source_code`
  - `qa_ai`: `test_results.json`, PASS signal
  - `mlops_ai`: `deployment_config`
  - `auditor_ai`: `Summary_Report.md`
  - `principal_engineer_ai`: `Validation_Report.md`, `Final_Implementation_Plan.md`
- Reads and writes `workflow_state.json`.