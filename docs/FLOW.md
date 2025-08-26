# Complete End-to-End Flow

This document describes the full workflow from rules activation to CI, execution pipeline, promotion/rollback, and routing. It is written to be runnable and auditable.

## 0) Rules model: where rules live and when they apply
- Global Always rules (apply everywhere): `.cursor/rules/*.mdc` with `alwaysApply: true` (e.g., `development-excellence.mdc`, `security-and-compliance.mdc`).
- Auto Attached rules (by file patterns): `.cursor/rules/*.mdc` with focused `globs` (e.g., `python-development-standards.mdc` for `**/*.py`).
- Nested rules (area-specific auto-attach):
  - `src/frontend/.cursor/rules/frontend-standards.mdc`
  - `src/backend/.cursor/rules/backend-standards.mdc`

## 1) Curated rule generation (local & CI)
- Purpose: Move the most relevant curated rules from `.cursor/test-rules` into `.cursor/rules` based on detected stacks, then normalize frontmatter.
- Command (repo root):
```bash
python tools/generate_cursor_rules.py --lint
```
- Under the hood:
  1. Detector scans repo and writes `rule_attach_log.json` (markers per stack).
  2. Curated selector picks top matching rules from `.cursor/test-rules` (framework match → add-on rules for security/testing/devops; deterministic tie-break by newest mtime then name), writes `.cursor/rules/.selected.json` and copies the files as `curated_*.mdc`.
  3. Linter validates/normalizes MDC frontmatter, preserving explicit `alwaysApply: true`.
- Artifacts:
  - `rule_attach_log.json`
  - `.cursor/rules/.selected.json` (index of promoted curated rules)

## 2) CI integration
- Workflow: `.github/workflows/ci.yml`
  - Step: Generate Cursor Rules (detector → curated selector → linter)
  - Upload artifacts: `rule_attach_log.json`, `.cursor/rules/.selected.json`
  - Run tests:
    - Attach mapping tests: base + extended stacks (`tests/unit/test_rule_attach_mapping*.py`)
    - Hydration tests (`hydration/run_hydration_tests.py`)
    - Concurrency smoke test (`tests/unit/test_concurrency_smoke.py`)

## 3) Orchestrated multi-role pipeline
- Roles (simplified):
  - `product_owner_ai` → `planning_ai` → [Audit: `auditor_ai` → `principal_engineer_ai`] → `codegen_ai` → `qa_ai` → `mlops_ai` → `observability_ai`
- Orchestrator: `.cursor/rules/execution_orchestrator.mdc` defines:
  - Phases, gates, error handling, state transitions
  - Handoff protocols and session handoff expectations (write `handoff_log.json`-style records)
- Gates (examples):
  - Planning gate: design completeness
  - QA gate: tests pass, security checks OK, performance OK
  - Deployment gate: health checks, rollback plan, monitoring

## 4) Memory bridge and knowledge persistence
- `framework_memory_bridge.mdc` integrates with `memory-bank/` and coordinates state sync.
- Persisted artifacts (examples): `memory-bank/queue-system/tasks_active.json`, observability and decisions logs.

## 5) Promotion and rollback safety
- Create snapshot with metadata (from framework dir):
```bash
cd frameworks/fwk-001-cursor-rules
python promotion/snapshot_cli.py create --trigger manual --environment development
```
- Rehearse rollback end-to-end:
```bash
python promotion/rollback_rehearsal.py
```
- Rehearsal verifies: index restoration, contract validation, hydration tests, routing conflicts.

## 6) Routing overrides & progressive mode
- Files: `frameworks/fwk-001-cursor-rules/DOCS/changes/`
  - `routing_override.yaml` (progressive_mode + allowlist_triggers)
  - `routing_effective.shadow.json`, `routing_baseline.json`
- Monitor and write reports:
```bash
python scripts/progressive_monitor.py --trigger /route
```
- Toggle override safely (repo root):
```bash
python tools/routing_override_toggle.py on --allow /route /status /review
python tools/routing_override_toggle.py off
```

## 7) Guardrails and refinements implemented
- Linter: preserves explicit `alwaysApply: true`; only normalizes when missing/invalid.
- Detector:
  - `specialized/ecommerce`: requires Shopify (`**/*.liquid`) or WordPress (`wp-content/**` or keywords) markers.
  - `backend/php`: now gated by `composer.json` to avoid overlap with ecommerce-only repos.
- Curated selector: deterministic ranking; adds security/testing/devops add-ons.
- Nested rules: area-focused auto-attach for frontend/backend.

## 8) Validation quick runbook
- Generate curated rules:
```bash
python tools/generate_cursor_rules.py --lint
cat .cursor/rules/.selected.json
head -n 60 rule_attach_log.json
```
- Run attach mapping tests:
```bash
cd frameworks/fwk-001-cursor-rules
pytest -q tests/unit/test_rule_attach_mapping.py \
        tests/unit/test_rule_attach_mapping_more.py \
        tests/unit/test_rule_attach_mapping_new_stacks.py
```
- Hydration tests:
```bash
python hydration/run_hydration_tests.py hydration/hydration_tests.yaml
```
- Concurrency smoke:
```bash
pytest -q tests/unit/test_concurrency_smoke.py
```
- Snapshot & rollback rehearsal:
```bash
python promotion/snapshot_cli.py create --trigger manual --environment development
python promotion/rollback_rehearsal.py
```
- Routing progressive monitor:
```bash
cd /workspace
python scripts/progressive_monitor.py --trigger /route
```

## 9) How rules “take effect” in Cursor
- Always rules: automatic; included in context across the workspace.
- Auto Attached rules: applied when files matching `globs` are opened/edited.
- Nested rules: applied when working inside directories that contain `.cursor/rules`.
- Curated promotions: selected rules copied into `.cursor/rules` and become attachable (by globs or via agent requested).

## 10) Troubleshooting
- Frontmatter issues → fix via linter:
```bash
python tools/mdc_linter.py --paths .cursor/rules .cursor/test-rules --write
```
- Unexpected attach overlap → inspect `rule_attach_log.json` markers; tighten globs or add gating conditions.
- CI red → download artifact `cursor-rules-artifacts` to review `.selected.json` + `rule_attach_log.json`; run unit tests locally with a venv.