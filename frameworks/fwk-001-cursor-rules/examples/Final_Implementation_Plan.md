## Final Implementation Plan — Governance/Config Artifacts Integration

### 1) Objectives & Scope
- Integrate governance/config artifacts into the framework with safe rollouts and strong traceability:
  - `artifact_schema.mdc`, `artifact_routing.mdc`, `artifact_sync_rules.mdc` (introduces `artifacts_index.json`), `hydration_rules.mdc`, `framework_contract_framework1.mdc`, `promotion_rules.mdc`.
- Outcomes:
  - Uniform artifact metadata schema; deterministic artifact routing; deterministic hydration with explicit tie-breakers; crash-safe artifact index with single-writer guarantees; enforceable framework contract; promotion governance with snapshots/rollback.
- Out of scope (for this phase): Cross-repo rollout; non-fwk-001 frameworks unless explicitly listed in migration tasks.

### 2) Assumptions Acknowledged & Constraints
- A-001 — Orchestrator operates single-writer only (fragile under parallelization). Ref: Summary A-001; Validation confirms R-002.
- A-002 — PASS semantics exist for gates (audit/verification/synthesis). Ref: Summary A-002.
- A-003 — States draft/review/approved and promotion tagging standardized org-wide. Ref: Summary A-003.
- A-004 — `routing_matrix.json` remains canonical for command routing; artifact routing is separate. Ref: Summary A-004, R-003.
- A-005 — Memory-bridge sync present and will coexist with new index. Ref: Summary A-005.
- Constraints: CI may spawn parallel jobs; storage must fsync durable writes; changes must be idempotent and revertible.

### 3) Work Breakdown
- Task Table (Task ID | Description | Owner/Role | Inputs | Outputs | Prereqs | Priority | Source refs)

| Task ID | Description | Owner/Role | Inputs | Outputs | Prereqs | Priority | Source refs |
|---|---|---|---|---|---|---|---|
| T-01 | Define and adopt uniform artifact frontmatter/sidecar schema (ids, versions, status) | Platform Eng | AP L1 | `artifact_schema.mdc`; example schema blocks | — | P0 | AP L1; SR R-006; VR confirms R-006 |
| T-02 | Introduce deterministic artifact routing separate from command routing; conflict detection and precedence rules | Principal Engineer | AP L2 | `artifact_routing.mdc`; routing validation checks | T-01 | P0 | AP L2; SR R-003; VR R-003 |
| T-03 | Implement `artifacts_index.json` with single-writer semantics: atomic temp+rename, fsync, lockfile, crash recovery journal | Orchestrator/Infra | AP L3 | `artifact_sync_rules.mdc`; index writer lib; recovery docs | T-01 | P0 | AP L3; SR R-002; VR R-002 |
| T-04 | Finalize hydration precedence with explicit tie-breakers (approved > latest non-draft > solo; break ties by commit-time, then filename) | Platform Eng | AP L4 | `hydration_rules.mdc`; test vectors | T-01 | P1 | AP L4; SR R-004; VR R-004 |
| T-05 | Formalize framework contract for `framework1` (allowed artifacts, states, gate checks) | Principal Engineer | AP L5 | `framework_contract_framework1.mdc` | T-01, T-02, T-04 | P1 | AP L5; SR R-001 |
| T-06 | Define promotion governance: snapshot format, retention, sign/verify, rollback triggers | DevOps/Release Eng | AP L6 | `promotion_rules.mdc`; runbooks | T-03, T-05 | P1 | AP L6; SR R-005; VR R-005 |
| T-07 | Plan and execute migration/backfill for existing artifacts to schema/routing/index | Platform Eng | SR B-001 | Migration plan; migration scripts; backfill report | T-01, T-02, T-03 | P1 | SR B-001 |
| T-08 | Testing strategy: unit + contract + e2e + gate checks (pre-merge, CI) | QA/Platform | SR B-002 | Test plan; automated checks; coverage report | T-01..T-06 | P0 | SR B-002 |
| T-09 | Access control and security for new metadata and snapshots | Security/Platform | SR B-003 | Access policies; ACLs; secret handling docs | T-01, T-06 | P1 | SR B-003 |
| T-10 | Hardening for multi-writer/distributed scenarios (queueing/leases; detect concurrent writers) | Orchestrator/Infra | SR B-004 | Concurrency guard design; simulation tests | T-03 | P2 | SR B-004 |
| T-11 | Telemetry/observability for hydration, routing, and promotions (drift detection, MTTR) | SRE/Platform | SR B-005 | Metrics/alerts dashboards; audit logs | T-04, T-06 | P1 | SR B-005 |
| T-12 | Governance fields and acceptance mechanics (owners, estimates, acceptance criteria, SLOs) | Program Mgmt | SR R-006 | RACI; estimates; acceptance checklist | — | P0 | SR R-006; VR R-006 |

### 4) Execution Phases
- Phase 0 — Plan Finalization
  - Entrance Criteria: Action Plan, Summary, Validation present (synthesis_gate inputs); owners identified.
  - Exit Criteria: T-12 complete (owners/estimates/acceptance), phase plan approved.
- Phase 1 — Foundations (Schema + Routing)
  - Entrance Criteria: Phase 0 complete.
  - Exit Criteria: T-01, T-02 complete; audit_gate PASS for routing conflicts.
- Phase 2 — Index & Hydration
  - Entrance Criteria: T-01, T-02 complete.
  - Exit Criteria: T-03, T-04 complete; verification_gate PASS with deterministic hydration tests.
- Phase 3 — Contracts & Promotions
  - Entrance Criteria: Phase 2 complete.
  - Exit Criteria: T-05, T-06 complete; promotion simulations pass.
- Phase 4 — Migration & Testing
  - Entrance Criteria: Phase 3 complete.
  - Exit Criteria: T-07, T-08, T-09 complete with green CI.
- Phase 5 — Hardening & Observability
  - Entrance Criteria: Phase 4 complete.
  - Exit Criteria: T-10, T-11 complete; SLOs met for drift detection/MTTR.

### 5) Rollback & Recovery Playbooks
- Promotions (T-06)
  - Decision Points: Promotion gate failure; post-deploy health degradation.
  - Triggers: Failed validation; SLO breach; drift alarm.
  - Steps: Freeze promotions → select last signed snapshot → verify signature/hash → restore artifacts → warm caches → re-run verification_gate → unfreeze.
- Index Writer (T-03)
  - Decision Points: Crash during write; lockfile stale; checksum mismatch.
  - Steps: Detect stale lock → replay journal → verify checksums → rebuild index from artifacts → rotate journal → resume with exponential backoff.
- Routing/Schema Changes (T-01, T-02)
  - Decision Points: Routing conflict; schema validation failures.
  - Steps: Revert to last known-good routing map and schema version; run full hydration dry-run; re-apply incrementally.

### 6) Risk-to-Task Mapping
- R-001 → T-01, T-02, T-05, T-12
- R-002 → T-03, T-10
- R-003 → T-02
- R-004 → T-04
- R-005 → T-06
- R-006 → T-12

### 7) Observability & Validation
- Metrics: policy coverage %, drift incidents/week, index write failure rate, promotion rollback count, MTTR.
- Alerts: drift detection, conflicting routing entries, hydration tie-breaker non-determinism, unsigned snapshot usage.
- QA gates: audit_gate (schema/routing quality), verification_gate (determinism, integrity), synthesis_gate (inputs present, plan consistency).

### 8) Appendix: Traceability Index
- Inputs
  - Action_Plan: L1 schema; L2 artifact routing; L3 index; L4 hydration; L5 framework contract; L6 promotions.
  - Summary_Report: R-001..R-006; B-001..B-005; A-001..A-005; M-001..M-004.
  - Validation_Report: Confirms R-001..R-006.
- Task ↔ Source
  - T-01 ↔ AP L1; SR R-006
  - T-02 ↔ AP L2; SR R-003
  - T-03 ↔ AP L3; SR R-002
  - T-04 ↔ AP L4; SR R-004
  - T-05 ↔ AP L5; SR R-001
  - T-06 ↔ AP L6; SR R-005
  - T-07 ↔ SR B-001
  - T-08 ↔ SR B-002
  - T-09 ↔ SR B-003
  - T-10 ↔ SR B-004
  - T-11 ↔ SR B-005
  - T-12 ↔ SR R-006; VR R-006

<!-- Reporting Rules: Every task must have at least one Source reference. Keep commands idempotent and safe. -->
