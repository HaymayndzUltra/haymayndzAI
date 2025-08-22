# Documentation Flow Analysis — codegen_ai → documentation_ai; analyst_ai support

## 1) Executive Summary
- **Primary flow**: Docs are drafted in parallel during implementation, then promoted after QA/gate pass. Analyst provides validation/enrichment before promotion when required.
- **Ownership**: `documentation_ai` is single-writer for canonical docs; `analyst_ai` is single-writer for analysis reports; `codegen_ai` may emit temporary specs that are handed off to `documentation_ai`.
- **Storage**: All role artifacts live under `memory-bank/roles/<role>/...` (additive to the system). Canonical docs are versioned in Git and carry provenance front matter.
- **Provenance**: Each artifact embeds `task_id`, `phase`, `commit`, `qa_status`, `source_paths`, and a link into the decision ledger (`memory-bank/decisions/index.jsonl`).
- **Gates**: Deep Analysis Gate remains authoritative on `exec --run` and `done`. Documentation promotion to canonical occurs only after QA/gate PASS.

## 2) Sources
- `PROPOSAL/proposal_3.md` (Consolidated Architectural Proposal; routing, gates, storage namespaces, decision ledger)
- `frameworks/fwk-001-cursor-rules/system-prompt/documentation_ai.mdc`
- `frameworks/fwk-001-cursor-rules/system-prompt/analyst_ai.mdc`
- `frameworks/fwk-001-cursor-rules/system-prompt/codegen_ai.mdc`

## 3) Trigger Model (When docs are generated/enriched)
- **Parallel draft (safe staging)**
  - Trigger: `/gen_code` preview or implementation in progress.
  - Action: `documentation_ai` generates draft docs in staging.
  - Storage: `memory-bank/roles/documentation_ai/staging/<component>/...`
  - Gate: None; drafts are non-canonical and marked `qa_status: pending`.
- **Post‑QA promotion (canonical)**
  - Trigger: After Deep Analysis Gate PASS on `exec --run` for the implementing phase and/or after `todo_manager.py done <TASK_ID> <PHASE_INDEX>`.
  - Action: `documentation_ai` promotes/creates canonical docs.
  - Storage: `memory-bank/roles/documentation_ai/<service_or_component>/...`
  - Gate: Requires QA/Gate PASS.
- **Manual update**
  - Trigger: `/update_docs <component>`.
  - Action: `documentation_ai` refreshes specific sections (canonical path), preserving provenance.
- **Validation sweep**
  - Trigger: `/validate_docs` or on state change (task phase `done:true`) or daily scheduled sweep.
  - Action: `documentation_ai` checks completeness/freshness; publishes validation artifacts.
  - Storage: `memory-bank/roles/documentation_ai/validations/<yyyymmdd>/...`
- **Analyst review/enrichment**
  - Trigger: `/review` (scoped to docs) or automatically after major doc updates.
  - Action: `analyst_ai` validates accuracy vs code/metrics and suggests enrichments; optional annotations applied by `documentation_ai`.
  - Storage: `memory-bank/roles/analyst_ai/` for reports; doc annotations merged by `documentation_ai` to canonical path.

## 4) Roles & Responsibilities
- **codegen_ai**: May emit preliminary API specs and endpoint inventories; does not own canonical docs.
- **documentation_ai**: Single writer for `api_docs.yaml`, `user_guide.md`, `developer_guide.md`; manages staging→canonical promotion; maintains provenance and validation outputs.
- **analyst_ai**: Single writer for `analysis_report.md`; validates doc completeness/accuracy and provides enrichment notes and SLO compliance checks.

## 5) Storage, Layout, and Versioning
- Root: `memory-bank/roles/documentation_ai/`
  - `staging/<component>/` — draft docs
  - `<service_or_component>/` — canonical docs
  - `validations/<yyyymmdd>/` — validation outputs
- Root: `memory-bank/roles/analyst_ai/`
  - `reports/<yyyymmdd>/` — analysis reports
  - `dashboards/` — metrics dashboards
- Versioning via Git; canonical docs include commit SHA in front matter and link to decision ledger record.

## 6) Provenance (embedded + ledger)
- Embedded in each doc (YAML front matter):
```yaml
provenance:
  task_id: "<TASK_ID>"
  phase_index: <K>
  commit: "<GIT_SHA>"
  qa_status: "pending|pass|fail"
  source_paths:
    - "path/to/src_or_spec"
  generated_by: "documentation_ai"
  reviewed_by: ["analyst_ai"]
  decision_ledger_ref: "memory-bank/decisions/index.jsonl#<offset_or_id>"
```
- Decision ledger append per update: timestamp, role, inputs, outputs, related task IDs (per proposal_3).

## 7) Review Loop & Orchestrator Linkage
- On `plan_next.py` → identify next phase; drafts allowed in staging.
- On Deep Analysis Gate PASS (via `todo_manager.py exec --run` or `done`): promote canonical docs.
- `tasks_active.json` linkage: docs front matter carries `<TASK_ID>` and `<PHASE_INDEX>`; validation runs on transitions to `done:true`.
- `analysis_active.json` linkage: presence and `done:true` phases unblock executions; optional check to require `validate_docs` success before marking a feature’s documentation phase done (configurable policy).

## 8) Risks & Edge Cases
- **Docs for code that later fails QA**: Keep drafts in staging; mark `qa_status: fail`; do not promote.
- **Stale docs**: Daily `/validate_docs` sweep; flag artifacts older than `stale_doc_max_age_days`; open decision ledger entry and create/update task if needed.
- **Merge conflicts**: Single-writer policy for canonical docs; enforce role-owned paths; use ledger notes when manual conflict resolution occurs.

## 9) Acceptance Criteria Mapping
- **Clear triggers and storage path**: Defined in Sections 3 and 5.
- **Provenance captured**: Front matter + decision ledger (Section 6).
- **Review loop defined**: Sections 7 and 8.

## 10) Appendix
- Example directory layout
```
memory-bank/roles/documentation_ai/
  staging/payments/user_guide.md
  payments/api_docs.yaml
  payments/developer_guide.md
  validations/2025-08-22/validation_report.json
memory-bank/roles/analyst_ai/
  reports/2025-08-22/analysis_report.md
  dashboards/metrics_dashboard.json
```
- Example validation report outline (`validations/<date>/validation_report.json`)
```json
{
  "component": "payments",
  "commit": "<GIT_SHA>",
  "task_id": "<TASK_ID>",
  "phase_index": 3,
  "checks": {
    "freshness": "pass|warn|fail",
    "completeness": "pass|warn|fail",
    "consistency_vs_code": "pass|warn|fail"
  },
  "notes": ["..."],
  "provenance_ref": "memory-bank/decisions/index.jsonl#<id>"
}
```