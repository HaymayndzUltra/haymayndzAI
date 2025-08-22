Status: PASS

### Routing Analysis Report (vertical: routing)

**Scope & Inputs**
- **Component Under Review**: `.cursor/rules/rules_master_toggle.mdc` driven router → `product_owner_ai` → `planning_ai` → `codegen_ai` → `qa_ai` (success path); branch to `documentation_ai`; `analyst_ai` support
- **Goal**: Precise, auditable routing matrix from commands to target AIs, including enable/disable semantics and fallback behavior
- **Inputs/Artifacts**:
  - `PROPOSAL/proposal_3.md` (end-to-end workflow)
  - `.cursor/rules/rules_master_toggle.mdc`, `.cursor/rules/trigger_phrases*.mdc`
  - `frameworks/fwk-001-cursor-rules/system-prompt/*.mdc` (role contracts, framework toggle + routing matrix)
- **Out‑of‑Scope**: Implementing routing changes; creating new agents/APIs; performance tuning beyond measurement points

## Rationale
- Unique primary handler per command with ≤1 fallback verified; only `/review` declares `qa_ai` fallback (see Routing Matrix).
- Toggle policy explicitly documented (master and per‑role) with canonical messages (rules_master_toggle.mdc).
- Error paths enumerated and deterministic (ROLE_DISABLED, MISSING_DEPENDENCY, MASTER_TOGGLE_OFF, UNRECOGNIZED_COMMAND, AMBIGUOUS_ROUTE) with remediation.
- Dependency awareness declared and consistent with framework matrix; failure behaviors specified.
- Observability guidance present (correlation_id, sink path) enabling auditability.

## Deterministic Routing Policy
- **Single‑dispatch**: Exactly one primary handler per command; ≤1 fallback.
- **Slash‑command domain**: Commands starting with `/` route via the framework routing matrix.
- **Family precedence & tie‑break**: Follow `.cursor/rules/trigger_phrases.mdc` — family precedence then right‑most occurrence. For slash commands, direct map wins.
- **Dependency awareness**: Roles may require upstream artifacts (see dependencies). If unmet, return deterministic error.

## Toggle Policy (Enable/Disable Semantics)
- **Master Toggle** (`.cursor/rules/rules_master_toggle.mdc`):
  - OFF → Suspend other `.cursor/rules/*`; no tool runs or edits; reply: `Rules disabled by user. Say "[cursor-rules:on]" to re-enable.`
  - ON → Normal behavior resumes.
- **Framework Role Toggles** (`frameworks/.../rules_master_toggle.mdc`):
  - `roles.<role>.enabled` governs route availability.
  - If primary disabled and fallback enabled → route to fallback.
  - If both disabled → user‑visible error with remediation hint (`/toggle <role> on`).

## Routing Matrix (Primary → Fallback) — Source of Truth: `frameworks/.../rules_master_toggle.mdc`
- `/backlog` → `product_owner_ai` → (none)
- `/prioritize` → `product_owner_ai` → (none)
- `/refine` → `product_owner_ai` → (none)
- `/plan` → `planning_ai` → (none)
- `/architect` → `planning_ai` → (none)
- `/estimate` → `planning_ai` → (none)
- `/gen_code` → `codegen_ai` → (none)
- `/implement` → `codegen_ai` → (none)
- `/refactor` → `codegen_ai` → (none)
- `/test` → `qa_ai` → (none)
- `/review` → `analyst_ai` (default; may delegate) → `qa_ai` (fallback for code review)
- `/validate` → `qa_ai` → (none)
- `/deploy` → `mlops_ai` → (none)
- `/rollback` → `mlops_ai` → (none)
- `/scale` → `mlops_ai` → (none)
- `/docs` → `documentation_ai` → (none)
- `/update_docs` → `documentation_ai` → (none)
- `/validate_docs` → `documentation_ai` → (none)
- `/analyze` → `analyst_ai` → (none)
- `/benchmark` → `analyst_ai` → (none)
- `/snapshot` → `memory_ai` → (none)
- `/recall` → `memory_ai` → (none)
- `/learn` → `memory_ai` → (none)
- `/observe` → `observability_ai` → (none)
- `/alert` → `observability_ai` → (none)
- `/health` → `observability_ai` → (none)
- `/run_pipeline` → `execution_orchestrator` → (none)
- `/status` → `execution_orchestrator` → (none)
- `/halt` → `execution_orchestrator` → (none)
- `/new_framework` → `prompt_factory_ai` → (none)
- `/extend_framework` → `prompt_factory_ai` → (none)
- `/template` → `prompt_factory_ai` → (none)
- `/toggle` → `rules_master_toggle` → (none)

## Dependencies (from framework matrix)
- `planning_ai` depends on `product_owner_ai`
- `codegen_ai` depends on `planning_ai`
- `qa_ai` depends on `codegen_ai`
- `mlops_ai` depends on `qa_ai`
- `documentation_ai` depends on `codegen_ai`
- `observability_ai` depends on `mlops_ai`

## Failure Handling & Error Paths
- **ROLE_DISABLED**: Primary disabled → if fallback enabled, route fallback; else error: `Role '<role>' disabled; try "/toggle <role> on"`.
- **MISSING_DEPENDENCY**: Dependency not satisfied → error: `Missing dependency '<dep>' for '<role>'`; suggest upstream command.
- **AMBIGUOUS_ROUTE**: Multiple roles claim a command → matrix decides; if user intent unclear, prefer explicit command or include target (e.g., `/review qa`).
- **MASTER_TOGGLE_OFF**: Print canonical disabled message; do not route.
- **UNRECOGNIZED_COMMAND**: Error: `Unknown command`; suggest `help` with known slash commands.

## Idempotency & Retries
- Slash command handlers should be idempotent where safe (re‑running should not corrupt state). Retries are user‑driven (re‑issue command) with clear messages on transient vs terminal errors.

## Observability (Routing Boundaries)
- Attach a correlation/trace ID per routed request; log: command, resolved role, fallback_used, enabled_flags, dependencies_state, and outcome.
- Suggested sink: `memory-bank/decisions/index.jsonl` (append‑only) with timestamp and role.

## Risks / Edge Cases
- Toggle misconfiguration causing partial pipelines (e.g., `codegen_ai` OFF but `/gen_code` used) → deterministic errors and remediation hints.
- Race conditions on multi‑match phrases → single‑dispatch + right‑most tie‑break avoids non‑determinism.
- Backlog starvation if support roles monopolize `/review` → default primary = `analyst_ai`, explicit `/validate` to `qa_ai` for test gating.

## Acceptance Criteria Verification
- **One primary + ≤1 fallback per command**: Satisfied above.
- **Toggle combinations enumerated**: Covered under Toggle Policy and error paths (master ON/OFF; role enabled/disabled; fallback enabled/disabled).
- **Explicit error/retry policy**: Defined under Failure Handling & Idempotency.