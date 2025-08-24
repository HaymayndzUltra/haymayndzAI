## Command Routing — Single Source of Truth (fwk-001-cursor-rules)

Purpose: One-page reference of all commands, mapped roles, and how to safely run/validate them.

### Global Controls (safe)
- Router status: `python3 /workspace/scripts/router.py status`
- Route (dry-run): `python3 /workspace/scripts/router.py route /<trigger>`
- Progressive monitor (read-only): `python3 /workspace/scripts/progressive_monitor.py --trigger /status | cat`
- JIT persona (optional, per-run): prefix command with `JIT_PERSONA=on` to inject persona after successful route

### Progressive & Allowlist
- Progressive=OFF (default): routes resolve; monitors may WARN; drift must be 0
- Progressive=ON: only `allowlist_triggers` can execute; set via `routing_override.yaml`
- Planner mode toggle (optional): `python3 /workspace/scripts/planner_mode.py on|off` (exposed in router status)

### Canonical Sources
- Matrix: `frameworks/fwk-001-cursor-rules/system-prompt/rules_master_toggle.mdc` (fallback: harvested copy)
- Overrides: `frameworks/fwk-001-cursor-rules/DOCS/changes/routing_override.yaml`
- Snapshots: `routing_baseline.json` (mdc only), `routing_effective.shadow.json` (baseline+override)

### Commands → Roles (authoritative mapping)
- Product/Planning:
  - `/backlog`, `/prioritize`, `/refine` → `product_owner_ai`
  - `/plan`, `/architect`, `/estimate` → `planning_ai`
- Codegen/QA/Deploy:
  - `/gen_code`, `/implement`, `/refactor` → `codegen_ai`
  - `/test`, `/review`, `/validate` → `qa_ai` (note: `/review` routed to `analyst_ai` for analysis)
  - `/deploy`, `/rollback`, `/scale` → `mlops_ai`
- Docs/Analysis/Memory/Observability:
  - `/docs`, `/update_docs`, `/validate_docs` → `documentation_ai`
  - `/review`, `/analyze`, `/benchmark` → `analyst_ai`
  - `/snapshot`, `/recall`, `/learn` → `memory_ai`
  - `/observe`, `/alert`, `/health` → `observability_ai`
- Orchestration/Factory/Toggles:
  - `/run_pipeline`, `/status`, `/halt` → `execution_orchestrator`
  - `/new_framework`, `/extend_framework`, `/template` → `prompt_factory_ai`
  - `/toggle`, `/route` → `rules_master_toggle`
- Data/Security/Planner:
  - `/design_schema`, `/create_migration`, `/optimize_queries` → `data_ai`
  - `/security_scan`, `/threat_model`, `/compliance_check` → `security_ai`
  - `/planner_mode` → `planner_moderator_ai`

### How to Use (step-by-step)
1) Check status (no side effects): `python3 /workspace/scripts/router.py status`
2) Dry-run a command: `python3 /workspace/scripts/router.py route /gen_code`
   - If `UNKNOWN_TRIGGER`: wala sa matrix → update needed
   - If `ROLE_DISABLED`: naka-disable ang role → enable via overrides
   - If `NOT_ALLOWLISTED` (Progressive=ON): idagdag sa allowlist
3) Optional: JIT persona per command (no repo edits): `JIT_PERSONA=on python3 /workspace/scripts/router.py route /gen_code`
4) For health checks (read-only): `python3 /workspace/scripts/progressive_monitor.py --trigger /status | cat`

### Notes
- Keep Progressive=OFF on main; turn ON only in canary branches with allowlist.
- Router is deterministic and file-driven; persona overlay is temporary and task-scoped.