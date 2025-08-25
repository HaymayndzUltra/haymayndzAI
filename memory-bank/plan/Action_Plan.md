# Action Plan: AI Orchestration System (Solo Freelance Dev Readiness)

## Inputs
- Backlog: `memory-bank/plan/product_backlog.yaml`
- Technical Plan: `memory-bank/plan/technical_plan.md`
- Task Breakdown: `memory-bank/plan/task_breakdown.yaml`

## Objectives
Establish a working end-to-end pipeline: backlog → plan → draft Action_Plan → audit → peer review → synthesis → implement → deploy → observe. Enforce gate discipline and session separation.

## Phases and Gates

### Phase 1 — Planning Readiness (Gate: planning_gate)
- Preconditions: `product_backlog.yaml` present; `technical_plan.md` + `task_breakdown.yaml` ready
- Outputs: Planning gate evidence captured in audit notes

### Phase 2 — Draft Action Plan (This document)
- Scope: Convert backlog items into actionable steps with artifacts and checks
- Outputs: This `Action_Plan.md`

### Phase 3 — Audit (auditor_ai) → Summary_Report.md
- Command:
```
/audit {"source":"memory-bank/plan/Action_Plan.md","context":["memory-bank/plan/technical_plan.md","memory-bank/plan/task_breakdown.yaml"],"outputs":{"report":"memory-bank/plan/Summary_Report.md"}}
```
- Criteria: Findings have traceable evidence lines to files/sections; risks include severity and mitigations

### Phase 4 — Peer Review (principal_engineer_ai) → Validation_Report.md
- Command:
```
/peer_review {"source":"memory-bank/plan/Summary_Report.md","plan":"memory-bank/plan/Action_Plan.md","outputs":{"report":"memory-bank/plan/Validation_Report.md"}}
```
- Criteria: Each audit risk marked CONFIRM/CHALLENGE with rationale; GO/NO-GO issued

### Phase 5 — Synthesis → Final_Implementation_Plan.md
- Preconditions: Validation GO
- Outputs: `Final_Implementation_Plan.md` with sequenced tasks and rollback notes

## Workstreams (from backlog)
- BL-001: Orchestrator role selection + rule attach logging (stabilize) → `.cursor/rules/execution_orchestrator.mdc`, `rule_attach_log.json`
- BL-002: Two-session audit → peer review gate (bias separation) → `frameworks/fwk-001-cursor-rules/examples/Summary_Report.md`, `frameworks/fwk-001-cursor-rules/examples/Validation_Report.md`
- BL-003: Product backlog → technical plan → draft Action_Plan generator → `memory-bank/plan/Action_Plan.md`, `tools/generate_action_plan.py`
- BL-016: Java/Spring Boot rules migration and attach coverage → `.cursor/frameworks/backend/java/**`, `rule_attach_log.json`
- BL-017: Rust rules migration and attach coverage → `.cursor/frameworks/backend/rust/**`, `rule_attach_log.json`
- BL-018: Unity (C#) game development rules and attach coverage → `.cursor/frameworks/specialized/unity/**`, `rule_attach_log.json`
- BL-019: iOS/Swift mobile rules and attach coverage → `.cursor/frameworks/mobile/ios/**`, `rule_attach_log.json`
- BL-020: E-commerce rules (Shopify/WordPress) and attach coverage → `.cursor/frameworks/specialized/ecommerce/**`, `rule_attach_log.json`
- BL-004: Example project wiring for gates (audit/validation/synthesis) → `frameworks/fwk-001-cursor-rules/examples/Action_Plan.md`, `frameworks/fwk-001-cursor-rules/examples/Summary_Report.md`
- BL-005: Security QA baseline (SQLi/XSS/Auth) integrated in qa_ai → `.cursor/rules/qa_ai.mdc`, `security_report.md`
- BL-006: Observability starter pack (alerts + dashboards) validation → `frameworks/fwk-001-cursor-rules/observability/alerts.yaml`, `frameworks/fwk-001-cursor-rules/observability/dashboards.mmd`
- BL-007: Memory learning loop (pattern_library.json) + storage layout → `.cursor/rules/memory_ai.mdc`, `storage/memory/knowledge_base.jsonl`
- BL-008: Framework auto-attach globs coverage and tests → `.cursor/frameworks/**.mdc`, `tests for rule attach mapping`
- BL-009: Onboarding & Quick Start for solo dev workflow → `/workspace/docs/inventories/*`, `/frameworks/fwk-001-cursor-rules/QUICK_START.md`
- BL-010: Planner-first mode (+ confirmation prompts) validation → `confirmation logs`
- BL-011: Promotion snapshots + rollback rehearsal → `promotion/snapshot_cli.py`, `promotion/rollback_playbook.md`
- BL-012: Routing override progressive mode tests → `DOCS/changes/routing_override.yaml`, `DOCS/changes/routing_effective.shadow.json`
- BL-013: Hydration selector scenarios → `hydration/hydration_selector.py`, `hydration/hydration_tests.yaml`
- BL-014: Performance & concurrency thresholds → `pytest.ini updates`, `tests/concurrency`
- BL-015: Freelance business templates (client onboarding, QA workflows) → `.cursor/templates/*`, `/workspace/docs/inventories/DECISION_GUIDE.md`

## Acceptance Criteria (Definition of Done)
- `Summary_Report.md` with evidence citations
- `Validation_Report.md` with GO/NO-GO and rationale
- `Final_Implementation_Plan.md` with task sequencing and rollback
- Security gate blocks on High issues; Observability configs lint/render cleanly

## IMPORTANT NOTE
Run audit and peer review in separate sessions to avoid bias. Treat planning and QA gates as blocking unless explicitly set to warn; include explicit evidence references in all findings.
