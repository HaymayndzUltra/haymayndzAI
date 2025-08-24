## Migration Plan — T-07 (Schema/Routing/Index Backfill)

### 1) Scope
- Artifacts in scope for this repo snapshot:
  - `frameworks/fwk-001-cursor-rules/examples/*.{md}` (Action_Plan, Summary_Report, Validation_Report, Final_Implementation_Plan, migration_plan)
  - Optional (flagged): `legacy/.cursor-rules-archived/*.mdc` (read-only dry-run preview by default)
- Goals:
  - Ensure every artifact has a sidecar conforming to `schemas/artifact.schema.json`
  - Backfill `artifacts_index.json` with entries for all sidecars (idempotent; single-writer)

### 2) Data Model Mapping
- id: derived from filename without extension (e.g., `Final_Implementation_Plan.md` → `Final_Implementation_Plan`)
- version: default `1.0.0` if missing
- status: default `review` (safer than `approved` for precedence)
- framework: `fwk-001-cursor-rules`
- kind: inferred by filename (e.g., `action_plan`, `summary_report`, `validation_report`, `final_implementation_plan`, `migration_plan`)
- checksumSha256: SHA-256 of primary artifact contents
- createdAt/updatedAt: file mtime in UTC (RFC3339 `YYYY-MM-DDTHH:MM:SSZ`)

### 3) Execution Steps
- Dry-run (no writes):
  - `python3 frameworks/fwk-001-cursor-rules/sync/backfill_script.py --dry-run`
- Apply backfill (writes sidecars, updates index):
  - `python3 frameworks/fwk-001-cursor-rules/sync/backfill_script.py --write-index`
- Include legacy preview (still dry-run unless `--apply-legacy` set):
  - `python3 frameworks/fwk-001-cursor-rules/sync/backfill_script.py --dry-run --include-legacy`

### 4) Rollback / Recovery
- Sidecars: per-file `.bak` snapshots written before first-time creation; restore by moving back
- Index: `artifacts_index.json` uses journaled writes (`*.journal`); recovery:
  1. If present, run: `python3 frameworks/fwk-001-cursor-rules/sync/index_cli.py verify` (safe)
  2. For crash recovery: `python3 frameworks/fwk-001-cursor-rules/sync/index_cli.py simulate_crash` then auto-recover on next run; or copy `artifacts_index.json.journal` over `artifacts_index.json`
- Idempotency: re-running backfill yields identical index state for same inputs

### 5) Validation & Acceptance
- Schema validation: sidecars match `schemas/artifact.schema.json`
- Index verification: `python3 frameworks/fwk-001-cursor-rules/sync/index_cli.py verify`
- Hydration determinism unchanged: run `python3 frameworks/fwk-001-cursor-rules/hydration/run_hydration_tests.py`
- Acceptance (per T-07):
  - Zero data loss in dry-run (no write operations; summarized plan shows all artifacts accounted for)
  - Rollback path documented (above)

### 6) Risks & Mitigations
- Concurrent index writers → mitigated by lock + atomic replace
- Misclassified kinds for legacy `.mdc` → legacy migration is opt-in
- Time skew on createdAt/updatedAt → use file mtime to ensure reproducibility

### 7) Traceability
- Inputs: Summary_Report B-001; `artifacts_index.json`
- Outputs: `migration_plan.md`; `sync/backfill_script.py`
- Depends on: T-01, T-02, T-03