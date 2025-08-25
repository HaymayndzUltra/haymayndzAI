# Final Implementation Plan

## Gate Status
- Validation Verdict: GO

## Implementation Tasks (Sequenced)
### Default
- [01] BL-001 — Orchestrator role selection + rule attach logging (stabilize) → `.cursor/rules/execution_orchestrator.mdc`, `rule_attach_log.json`
  - Prerequisites: None
  - Traceability: Plan=memory-bank/plan/Action_Plan.md; Audit=memory-bank/plan/Summary_Report.md; Validation=memory-bank/plan/Validation_Report.md
- [02] BL-002 — Two-session audit → peer review gate (bias separation) → `frameworks/fwk-001-cursor-rules/examples/Summary_Report.md`, `frameworks/fwk-001-cursor-rules/examples/Validation_Report.md`
  - Prerequisites: Task 1
  - Traceability: Plan=memory-bank/plan/Action_Plan.md; Audit=memory-bank/plan/Summary_Report.md; Validation=memory-bank/plan/Validation_Report.md
- [03] BL-003 — Product backlog → technical plan → draft Action_Plan generator → `memory-bank/plan/Action_Plan.md`, `tools/generate_action_plan.py`
  - Prerequisites: Task 2
  - Traceability: Plan=memory-bank/plan/Action_Plan.md; Audit=memory-bank/plan/Summary_Report.md; Validation=memory-bank/plan/Validation_Report.md
- [04] BL-004 — Example project wiring for gates (audit/validation/synthesis) → `frameworks/fwk-001-cursor-rules/examples/Action_Plan.md`, `frameworks/fwk-001-cursor-rules/examples/Summary_Report.md`
  - Prerequisites: Task 3
  - Traceability: Plan=memory-bank/plan/Action_Plan.md; Audit=memory-bank/plan/Summary_Report.md; Validation=memory-bank/plan/Validation_Report.md
- [05] BL-005 — Security QA baseline (SQLi/XSS/Auth) integrated in qa_ai → `.cursor/rules/qa_ai.mdc`, `security_report.md`
  - Prerequisites: Task 4
  - Traceability: Plan=memory-bank/plan/Action_Plan.md; Audit=memory-bank/plan/Summary_Report.md; Validation=memory-bank/plan/Validation_Report.md
- [06] BL-006 — Observability starter pack (alerts + dashboards) validation → `frameworks/fwk-001-cursor-rules/observability/alerts.yaml`, `frameworks/fwk-001-cursor-rules/observability/dashboards.mmd`
  - Prerequisites: Task 5
  - Traceability: Plan=memory-bank/plan/Action_Plan.md; Audit=memory-bank/plan/Summary_Report.md; Validation=memory-bank/plan/Validation_Report.md
- [07] BL-007 — Memory learning loop (pattern_library.json) + storage layout → `.cursor/rules/memory_ai.mdc`, `storage/memory/knowledge_base.jsonl`
  - Prerequisites: Task 6
  - Traceability: Plan=memory-bank/plan/Action_Plan.md; Audit=memory-bank/plan/Summary_Report.md; Validation=memory-bank/plan/Validation_Report.md
- [08] BL-008 — Framework auto-attach globs coverage and tests → `.cursor/frameworks/**.mdc`, `tests for rule attach mapping`
  - Prerequisites: Task 7
  - Traceability: Plan=memory-bank/plan/Action_Plan.md; Audit=memory-bank/plan/Summary_Report.md; Validation=memory-bank/plan/Validation_Report.md
- [09] BL-009 — Onboarding & Quick Start for solo dev workflow → `/workspace/docs/inventories/*`, `/frameworks/fwk-001-cursor-rules/QUICK_START.md`
  - Prerequisites: Task 8
  - Traceability: Plan=memory-bank/plan/Action_Plan.md; Audit=memory-bank/plan/Summary_Report.md; Validation=memory-bank/plan/Validation_Report.md
- [10] BL-010 — Planner-first mode (+ confirmation prompts) validation → `confirmation logs`
  - Prerequisites: Task 9
  - Traceability: Plan=memory-bank/plan/Action_Plan.md; Audit=memory-bank/plan/Summary_Report.md; Validation=memory-bank/plan/Validation_Report.md
- [11] BL-011 — Promotion snapshots + rollback rehearsal → `promotion/snapshot_cli.py`, `promotion/rollback_playbook.md`
  - Prerequisites: Task 10
  - Traceability: Plan=memory-bank/plan/Action_Plan.md; Audit=memory-bank/plan/Summary_Report.md; Validation=memory-bank/plan/Validation_Report.md
- [12] BL-012 — Routing override progressive mode tests → `DOCS/changes/routing_override.yaml`, `DOCS/changes/routing_effective.shadow.json`
  - Prerequisites: Task 11
  - Traceability: Plan=memory-bank/plan/Action_Plan.md; Audit=memory-bank/plan/Summary_Report.md; Validation=memory-bank/plan/Validation_Report.md
- [13] BL-013 — Hydration selector scenarios → `hydration/hydration_selector.py`, `hydration/hydration_tests.yaml`
  - Prerequisites: Task 12
  - Traceability: Plan=memory-bank/plan/Action_Plan.md; Audit=memory-bank/plan/Summary_Report.md; Validation=memory-bank/plan/Validation_Report.md
- [14] BL-014 — Performance & concurrency thresholds → `pytest.ini updates`, `tests/concurrency`
  - Prerequisites: Task 13
  - Traceability: Plan=memory-bank/plan/Action_Plan.md; Audit=memory-bank/plan/Summary_Report.md; Validation=memory-bank/plan/Validation_Report.md
- [15] BL-015 — Freelance business templates (client onboarding, QA workflows) → `.cursor/templates/*`, `/workspace/docs/inventories/DECISION_GUIDE.md`
  - Prerequisites: Task 14
  - Traceability: Plan=memory-bank/plan/Action_Plan.md; Audit=memory-bank/plan/Summary_Report.md; Validation=memory-bank/plan/Validation_Report.md
- [16] BL-016 — Java/Spring Boot rules migration and attach coverage → `.cursor/frameworks/backend/java/**`, `rule_attach_log.json`
  - Prerequisites: Task 15
  - Traceability: Plan=memory-bank/plan/Action_Plan.md; Audit=memory-bank/plan/Summary_Report.md; Validation=memory-bank/plan/Validation_Report.md
- [17] BL-017 — Rust rules migration and attach coverage → `.cursor/frameworks/backend/rust/**`, `rule_attach_log.json`
  - Prerequisites: Task 16
  - Traceability: Plan=memory-bank/plan/Action_Plan.md; Audit=memory-bank/plan/Summary_Report.md; Validation=memory-bank/plan/Validation_Report.md
- [18] BL-018 — Unity (C#) game development rules and attach coverage → `.cursor/frameworks/specialized/unity/**`, `rule_attach_log.json`
  - Prerequisites: Task 17
  - Traceability: Plan=memory-bank/plan/Action_Plan.md; Audit=memory-bank/plan/Summary_Report.md; Validation=memory-bank/plan/Validation_Report.md
- [19] BL-019 — iOS/Swift mobile rules and attach coverage → `.cursor/frameworks/mobile/ios/**`, `rule_attach_log.json`
  - Prerequisites: Task 18
  - Traceability: Plan=memory-bank/plan/Action_Plan.md; Audit=memory-bank/plan/Summary_Report.md; Validation=memory-bank/plan/Validation_Report.md
- [20] BL-020 — E-commerce rules (Shopify/WordPress) and attach coverage → `.cursor/frameworks/specialized/ecommerce/**`, `rule_attach_log.json`
  - Prerequisites: Task 19
  - Traceability: Plan=memory-bank/plan/Action_Plan.md; Audit=memory-bank/plan/Summary_Report.md; Validation=memory-bank/plan/Validation_Report.md

- [21] BL-021 — Frontend rules migration (React/Next, Vue/Nuxt, Angular, Svelte) → `.cursor/frameworks/frontend/*`
  - Prerequisites: Task 20
  - Deliverables: ≥20 detailed points per tech, examples, security/perf/testing sections; attach tests
  - Traceability: Plan/Action_Plan.md; Audit/Summary_Report.md; Validation/Validation_Report.md

- [22] BL-022 — Backend rules migration (Python FastAPI/Django, PHP/Laravel, Node, Go) → `.cursor/frameworks/backend/*`
  - Prerequisites: Task 21
  - Deliverables: ≥20 detailed points per tech; attach tests
  - Traceability: Plan/Action_Plan.md; Audit/Summary_Report.md; Validation/Validation_Report.md

- [23] BL-023 — Mobile rules migration (React Native/Expo, Flutter) → `.cursor/frameworks/mobile/*`
  - Prerequisites: Task 22
  - Deliverables: ≥20 detailed points per tech; attach tests
  - Traceability: Plan/Action_Plan.md; Audit/Summary_Report.md; Validation/Validation_Report.md

- [24] BL-024 — Specialized rules migration (Blockchain, Terraform/DevOps) → `.cursor/frameworks/specialized/*`
  - Prerequisites: Task 23
  - Deliverables: ≥20 detailed points per tech; attach tests
  - Traceability: Plan/Action_Plan.md; Audit/Summary_Report.md; Validation/Validation_Report.md

- [25] BL-025 — Retire legacy `.cursor/test-rules/` safely (archive + conflict cleanup + rollback)
  - Prerequisites: Task 24
  - Deliverables: archive folder; conflict matrix; rollback note
  - Traceability: Plan/Action_Plan.md; Audit/Summary_Report.md; Validation/Validation_Report.md

- [26] BL-026 — UAT + success metrics validation (coverage, conflicts=0, <2s attach/resp)
  - Prerequisites: Task 25
  - Deliverables: UAT checklist; metrics report; CI perf checks
  - Traceability: Plan/Action_Plan.md; Audit/Summary_Report.md; Validation/Validation_Report.md

- [27] BL-027 — Docs, training, and handover (user guide, migration notes)
  - Prerequisites: Task 26
  - Deliverables: QUICK_START updates; migration guide; handover pack
  - Traceability: Plan/Action_Plan.md; Audit/Summary_Report.md; Validation/Validation_Report.md

## Risk Considerations (from Audit)
- R-001 (Medium): Missing rule_attach_log.json reduces observability of rule attach coverage.
- R-002 (Medium): security_report.md not yet generated; QA gate readiness unclear.
- R-003 (Low): pattern_library.json absent; learning loop incomplete.
- R-004 (Low): Some framework specialization directories not present; scope likely P2.

## Rollback and Contingency
- Maintain pre-change snapshots. Validate health checks post-rollback.
- Define revert steps per task; ensure idempotent migrations and feature-flag guardrails.

## References
- Action Plan: memory-bank/plan/Action_Plan.md
- Audit Report: memory-bank/plan/Summary_Report.md
- Validation Report: memory-bank/plan/Validation_Report.md

## Phase-by-Phase (Week-aligned)

- Phase 1 (Week 1): BL-001 to BL-006
  - Foundations: attach logging, audit/peer-review wiring, generator, security gate, observability

- Phase 2 (Week 2): BL-007 to BL-012
  - Memory learning loop, auto-attach coverage tests, onboarding docs, planner mode, snapshots/rollback, routing tests

- Phase 3 (Week 3): BL-013 to BL-020
  - Hydration, performance/concurrency, templates, and P2 migrations (Java/Spring, Rust, Unity, iOS, E-commerce)

- Phase 4 (Week 4): BL-021 to BL-027
  - Frontend/Backend/Mobile/Specialized migrations with ≥20 detailed points each; retire old rules; UAT; docs & handover
