## Final Implementation Plan — fwk-001-cursor-rules

Sources: `examples/Action_Plan.md`, `examples/Summary_Report.md`, `examples/Validation_Report.md`

### 1) Objectives & Scope
- Close Low/Medium risks identified in peer review while keeping scope diagnostic-only.
- Add minimal, reversible artifacts to enable plan validations and gates.

### 2) Assumptions & Constraints
- Changes confined to `frameworks/fwk-001-cursor-rules/examples/`, `frameworks/fwk-001-cursor-rules/DOCS/changes/`, and `frameworks/fwk-001-cursor-rules/routing/`.
- Idempotent: re-running tasks should be safe; overwrites are explicit.
- No external services; local file artifacts only.

### 3) Work Breakdown (Tasks)

- Task ID: FIP-001 (P0)
  - Title: Minimal unified command router (simulation) for core workflow
  - Description: Create a small script to simulate `/backlog → /plan → /gen_code → /test` and emit artifacts into `examples/`.
  - Inputs: none
  - Outputs: `examples/product_backlog.yaml`, `examples/technical_plan.md` (update if needed), `examples/task_breakdown.yaml` (update if needed), `examples/test_results.json`
  - Owner/Role: tooling_engineer_ai
  - Preconditions: repo checkout
  - Source refs: Plan L31-37; Risks R-003, NEW-RISK-001
  - Rollback: delete generated files in `examples/`.

- Task ID: FIP-002 (P0)
  - Title: Deployment manifest template for gate validation
  - Description: Add `examples/deployment_manifest.yaml` with a minimal valid schema to satisfy deployment gate checks.
  - Outputs: `examples/deployment_manifest.yaml`
  - Owner/Role: release_engineer_ai
  - Source refs: Plan L39-42; Risk R-004
  - Rollback: remove the file.

- Task ID: FIP-003 (P1)
  - Title: Roles state snapshot
  - Description: Produce a static `examples/roles_status.json` capturing expected toggle states for validation.
  - Outputs: `examples/roles_status.json`
  - Owner/Role: systems_engineer_ai
  - Source refs: Plan L6-9; Risk R-001
  - Rollback: remove the file.

- Task ID: FIP-004 (P1)
  - Title: Routing rollback artifact (.bak)
  - Description: Create `DOCS/changes/routing_effective.shadow.json.bak` from current `routing_effective.shadow.json` to enable rollback testing.
  - Outputs: `DOCS/changes/routing_effective.shadow.json.bak`
  - Owner/Role: config_manager_ai
  - Source refs: Plan L60-63; NEW-RISK-002
  - Rollback: remove the `.bak` file.

- Task ID: FIP-005 (P1)
  - Title: Routing baseline/effective/override diff checker
  - Description: Add `routing/diff_routing_effective.py` to summarize diffs across `routing_baseline.json`, `routing_effective.shadow.json`, and `routing_override.yaml`.
  - Outputs: CLI summary (stdout), optional `DOCS/changes/routing_diff_report.md`
  - Owner/Role: tooling_engineer_ai
  - Source refs: Plan L14-17, L60-63; Alignments A-001, A-005
  - Rollback: remove script and report if generated.

- Task ID: FIP-006 (P2)
  - Title: Doc alignment for role matrix sources
  - Description: Update `DOCS/ROLES_MATRIX.md` to note canonical repo paths and link harvested `system-prompt/rules_master_toggle.mdc`.
  - Outputs: updated `DOCS/ROLES_MATRIX.md`
  - Owner/Role: docs_engineer_ai
  - Source refs: Risk R-002
  - Rollback: revert doc update.

### 4) Execution Phases
- Phase M1 (P0 tasks): FIP-001, FIP-002
  - Entrance: repo ready
  - Exit: core artifacts generated; deployment manifest present
- Phase M2 (P1 tasks): FIP-003, FIP-004, FIP-005
  - Entrance: M1 complete
  - Exit: roles snapshot present; `.bak` present; diff tool run at least once
- Phase M3 (P2 task): FIP-006
  - Entrance: M2 complete
  - Exit: docs aligned

### 5) Rollback & Recovery Playbooks
- Rollback Strategy: delete generated artifacts and added files; no stateful side‑effects remain.
- Decision Points:
  - If diff check detects unexpected deltas → restore from `.bak` and re-run.
  - If gates fail due to schema issues → revert the specific artifact to last known good.

### 6) Risk-to-Task Mapping
- R-001 → FIP-003
- R-002 → FIP-006
- R-003 → FIP-001
- R-004 → FIP-002
- NEW-RISK-001 → FIP-001
- NEW-RISK-002 → FIP-004, FIP-005

### 7) Observability & Validation
- Checks:
  - Schema: validate `schemas/artifact.schema.json` against new artifacts where applicable.
  - Routing: run `routing/check_routing_conflicts.py` and the new diff checker.
  - Coverage: honor `pytest.ini` `--cov-fail-under=80` (unchanged).
- Example command (non-destructive):
```bash
python frameworks/fwk-001-cursor-rules/routing/check_routing_conflicts.py | cat
```

### 8) Appendix: Traceability Index
- Plan §Phase 1 (L14-17) → FIP-005
- Plan §Phase 1 (L6-9) → FIP-003
- Plan §Phase 2 (L31-37) → FIP-001
- Plan §Phase 2 (L39-42) → FIP-002
- Plan §Phase 3 (L60-63) → FIP-004, FIP-005
- Alignments A-001/A-005 → FIP-005

<!-- Reporting Rules: Every task must have at least one Source reference. Keep commands idempotent and safe. -->