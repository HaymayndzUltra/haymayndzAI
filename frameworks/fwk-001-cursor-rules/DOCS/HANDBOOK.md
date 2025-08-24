# fwk-001-cursor-rules — Consolidated Handbook

## 1) Quick Start (Most Important)
- Core flow: product_owner_ai → planning_ai → codegen_ai → qa_ai → mlops_ai
- Master toggles:
  - Enable/disable roles: `/toggle <role> on|off`
  - Planner-first mode (answer-first + confirm-before-action): `/toggle planner_moderator_ai on` → `/planner_mode on`
- Run pipeline: `/run_pipeline`
- Check status: `/status`
- Key gates: Planning, Code Generation, QA (>= 80% coverage), Deployment

## 2) Roles & Toggles (Grouped)
### Orchestration
- execution_orchestrator: `/run_pipeline`, `/status`, `/halt`
- rules_master_toggle: `/toggle`, `/route`
- prompt_factory_ai: `/new_framework`, `/extend_framework`, `/template`
- planner_moderator_ai (optional): `/planner_mode on|off`

### Core
- product_owner_ai: `/backlog`, `/prioritize`, `/refine`
- planning_ai: `/plan`, `/architect`, `/estimate`
- codegen_ai: `/gen_code`, `/implement`, `/refactor`
- qa_ai: `/test`, `/review`, `/validate`
- mlops_ai: `/deploy`, `/rollback`, `/scale`

### Support
- documentation_ai: `/docs`, `/update_docs`, `/validate_docs`
- memory_ai: `/snapshot`, `/recall`, `/learn`
- observability_ai (optional): `/observe`, `/alert`, `/health`
- analyst_ai (optional): `/review`, `/analyze`, `/benchmark`
- security_ai (optional): `/security_scan`, `/threat_model`, `/compliance_check`
- prompt_linter_ai (optional): `/lint_prompts`, `/check_style`, `/suggest_improvements`
- l10n_i18n_ai (optional): `/l10n_setup`, `/generate_templates`, `/validate_locale`
- data_ai (optional): `/design_schema`, `/create_migration`, `/optimize_queries`

## 3) Command Routing (Reference)
See `rules_master_toggle.mdc` routing matrix. Example additions used in Café project:
- Data: `/design_schema`, `/create_migration`, `/optimize_queries` → data_ai
- Security: `/security_scan`, `/threat_model`, `/compliance_check` → security_ai
- Planner Mode: `/planner_mode` → planner_moderator_ai

## 4) Pipeline Gates & Policies (Important)
- Planning Gate: inputs `product_backlog.yaml`; validates acceptance criteria, completeness, dependencies
- Code Generation Gate: inputs `technical_plan.md`, `task_breakdown.yaml`; requires tests + docs
- QA Gate: inputs `source_code`, `acceptance_criteria.json`; requires “All tests pass (>= 80% coverage)” + no critical security issues
- Deployment Gate: inputs `validated_code`, `deployment_config`; requires health checks, rollback, monitoring
- Optional (can be disabled): Audit, Verification, Synthesis

## 5) Planner-first Mode (Single Toggle)
- Toggle: `/toggle planner_moderator_ai on` → `/planner_mode on`
- Behavior when ON: answer-first, human-like; echo intent; ask ≤3 focused questions if uncertain; require explicit “yes” before any code/edits; need scope/plan confirmation

## 6) Component Summaries (Grouped)
### Orchestration
- execution_orchestrator: coordinates pipeline, enforces gates, manages states, error handling, handoffs
- rules_master_toggle: central role activation + routing
- prompt_factory_ai: scaffolds frameworks/roles
- planner_moderator_ai: enforces confirm-before-action conversation policy

### Core
- product_owner_ai: backlog and acceptance criteria owner; outputs `product_backlog.yaml`, `acceptance_criteria.json`
- planning_ai: creates `technical_plan.md`, `task_breakdown.yaml`, `architecture_diagram.mermaid`
- codegen_ai: generates code+tests+docs; collaborates with qa_ai
- qa_ai: runs tests, coverage, quality assessment; owns `test_results.json`
- mlops_ai: deploys, owns `deployment_manifest.yaml`, sets monitoring config

### Support
- documentation_ai: `api_docs.yaml`, `user_guide.md`, `developer_guide.md`
- memory_ai: `knowledge_base.json`, `decision_log.md`, `context_snapshot.yaml`
- observability_ai: `monitoring_dashboard.json`, `alert_history.log`, `health_report.md`
- analyst_ai: `analysis_report.md`, `metrics_dashboard.json`, `optimization_plan.yaml`
- security_ai: `security_report.json`, `threat_model.md`, `compliance_checklist.yaml`
- prompt_linter_ai: `lint_report.json`, `style_violations.md`, `improvement_suggestions.yaml`
- l10n_i18n_ai: `translation_templates.json`, `locale_configs.yaml`, `l10n_guidelines.md`
- data_ai: `database_schema.sql`, `migration_scripts.sql`, `data_model.mermaid`

## 7) Operations Cheatsheet
- Toggle a role: `/toggle <role> on|off`
- Who handles a command: `/route <trigger>`
- Start/Stop pipeline: `/run_pipeline`, `/halt`, `/status`
- Planner-first: `/planner_mode on|off`

Note: Routing fix applied — `rules_master_toggle` handles `/toggle` and `/route`. Progressive mode is OFF; routing overrides are shadow-only.

Limited Progressive ON: active for `/route`, `/status`, `/health`, `/observe`, `/alert`, `/benchmark` via `DOCS/changes/routing_override.yaml` (rollback: restore `.bak`).

## 8) Files Index
- System prompts: `system-prompt/*.mdc` (+ OPTIONAL/*)
- Docs: this handbook
- Examples: sample files (if any)
 - End-to-end diagram: `DOCS/END_TO_END.mmd`

## 10) Recent Change Reports
- Consolidated (last 3 days): `frameworks/fwk-001-cursor-rules/DOCS/reports/Latest_Current.md`
- Git changes: `frameworks/fwk-001-cursor-rules/DOCS/changes/git_changes.md`
- Filesystem changes: `frameworks/fwk-001-cursor-rules/DOCS/changes/fs_changes.md`
- Labnotes changes: `frameworks/fwk-001-cursor-rules/DOCS/changes/labnotes_changes.md`
- Discrepancies: `frameworks/fwk-001-cursor-rules/DOCS/changes/discrepancies.md`

## 9) Change Impact & Safety
- All edits generate `.bak` backups where applicable
- Planner-first prevents unconfirmed changes
- Gates enforce quality and release safety

## 11) Memory (Pro) — GPU-preferred, CPU fallback
- CLI: `tools/memory/memory_cli.py`
- Config: `tools/memory/pro_config.yaml`
- Storage Root: `${MEMORY_STORAGE_ROOT:-storage/memory}`
- Common commands:
  - Save: `python3 tools/memory/memory_cli.py save "note" --tags project:default`
  - Recall: `python3 tools/memory/memory_cli.py recall "topic" --topk 5`
  - Reindex: `python3 tools/memory/memory_cli.py reindex`
  - Snapshot: `python3 tools/memory/memory_cli.py snapshot --summary "..."`
- Bridge mappings:
  - `/snapshot` → `python3 tools/memory/memory_cli.py snapshot`
  - `/recall` → `python3 tools/memory/memory_cli.py recall`
  - `/learn` → `python3 tools/memory/memory_cli.py save`