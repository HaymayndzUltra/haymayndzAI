### Consolidated Architectural Proposal — fwk-001-cursor-rules Integration (proposal_3)

#### Workflow Diagram (End-to-End)

```mermaid
graph TD
  U[User] -->|Triggers| R{Command Router}

  R -->|Slash Commands (e.g., /backlog, /plan, /gen_code, /test, /deploy)| FR[Framework Role Router]
  R -->|Existing Commands (python3 ... / plain text)| TCC[task_command_center.py]

  %% Existing system path
  TCC -->|Create/Manage Tasks| TM[todo_manager.py]
  TCC -->|Intelligent execution| WMI[workflow_memory_intelligence_fixed.py]
  TM -->|Read-only checks| PN[plan_next.py]
  TM -->|Hierarchy view| PH[plain_hier.py]
  PN -->|Preview next phase & lint| TM
  PH -->|Preview commands| TM
  TM -->|Exec (preview)| PREVIEW((Preview only))
  TM -->|Exec (--run)| GATE{Deep Analysis Gate}
  GATE -->|PASS| RUN[Run commands]
  GATE -->|BLOCK| ABORT[Stop; print reason]

  %% Shared persistence
  TM --> MB[(memory-bank/queue-system/tasks_active.json)]
  GATE -. requires .-> AMB[(memory-bank/queue-system/analysis_active.json)]
  TCC --> AS[auto_sync_manager.py]
  TM --> AS
  AS --> CS[cursor_state.json + current-session.md]

  %% New framework path (additive)
  FR --> PO[product_owner_ai]
  FR --> PL[planning_ai]
  FR --> CG[codegen_ai]
  FR --> QA[qa_ai]
  FR --> MLO[mlops_ai]
  FR --> DOC[documentation_ai]
  FR --> ANA[analyst_ai]
  FR --> MEM[memory_ai]
  FR --> OBS[observability_ai]

  %% Role outputs
  PO --> RB[(memory-bank/roles/product_owner_ai/...)]
  PL --> RB
  CG --> RB
  QA --> RB
  MLO --> RB
  DOC --> RB
  ANA --> RB
  MEM --> RB
  OBS --> RB

  %% Optional: roles can create/augment tasks via TM
  FR -->|Create/Update Phases| TM
  FR -->|Append decisions| DL[(memory-bank/decisions/index.jsonl)]
```

### Comparative Analysis

This analysis measures the proposals against the current operational logic and scripts: `todo_manager.py` (Deep Analysis Gate, placeholder substitution, exec/done gating), `plan_next.py` (next-phase preview + lint), `plain_hier.py` (hierarchy viewer), `task_command_center.py` (interactive hub + intelligent executor), `auto_sync_manager.py` (state sync), `cursor_memory_bridge.py` (session persistence), and `frameworks/fwk-001-cursor-rules/README.md` (role catalog/commands).

- Strengths in proposal_1.md (System Preservation Strategy):
  - Preserves proven core (todo manager, memory-bank, auto-sync, Cursor bridge) and advocates config-over-code changes. Aligns with non-disruptive integration constraint.
  - Introduces Solo vs Team Enforcement Modes (Warn → Soft-block → Hard-block) that can be layered on top of the existing Deep Analysis Gate without removing it.
  - Defines role trigger grammar and memory namespaces; proposes a decision ledger and structured handoffs. These are additive and compatible with current flows.
  - Provides a phased roadmap with risk controls (feature flags, additive schemas). Matches incremental adoption.

- Weaknesses/risks in proposal_1.md:
  - Requires additional scaffolding (dispatcher, role storage namespaces, decision ledger) but does not specify wiring to existing gating (must retain Deep Analysis Gate semantics on exec/done).
  - SLA and KPI constructs are process-level and require minimal, careful coupling to avoid runtime complexity creep.

- Strengths in proposal_2.md (Hybrid Integration):
  - Clear additive routing: existing commands continue to the proven hub; slash-prefixed commands go to role handlers. Compatible with non-disruptive integration.
  - Expands role set consistent with the framework’s README. Unifies memory targets.
  - Provides a command routing sketch and hybrid diagram that map well to current boundaries.

- Weaknesses/risks in proposal_2.md:
  - Conflicting “Quick Fix” steps (remove blocking rules, simplify gate validation to warnings). This breaks the existing `todo_manager.py` Deep Analysis Gate on `exec --run` and `done`. Must be rejected or modified.
  - References to non-existent tools in the current repository (e.g., `memoryctl`, `analyzer.py`, `execution_orchestrator` CLI). Must be deferred or replaced with existing equivalents (`plan_next.py`, `plain_hier.py`, `todo_manager.py exec`).

- Synergies across both proposals:
  - Role router + memory namespaces + decision ledger (proposal_1) fit the hybrid command routing and role catalog (proposal_2 and fwk-001 README) while preserving `tasks_active.json` as SOT.
  - Incremental rollout with feature flags and preserving auto-sync/session files meets the non-disruptive constraint.

- Conflicts with ground truth (explicit):
  - “Remove blocking rules” (proposal_2) conflicts with `todo_manager.py`’s enforced Deep Analysis Gate and `plan_next.py` linting expectations. Keep gating intact; optionally introduce policy modes that never default to weaker gating.
  - New CLIs not present (e.g., `memoryctl`) cannot be assumed; use existing Python entry points and add thin adapters later.

### Consolidated Architectural Proposal (Synthesized)

Principles:
- Preserve the proven execution path and gates by default (Team Mode = status quo). Add-on capabilities must be strictly additive.
- Enhance via configuration flips and thin routers; do not refactor core modules in the first phase.

Key Design Decisions:
1) Command Routing (Additive)
   - Add a lightweight prefix router inside `task_command_center.py` that routes slash-prefixed commands to a `framework_role_router` module. Non-prefixed commands route as-is to the existing menus and flows.
   - Map role commands to the framework catalog in `frameworks/fwk-001-cursor-rules/README.md` (e.g., `/backlog`, `/plan`, `/gen_code`, `/test`, `/deploy`).

2) Role Outputs and Memory Namespaces (Additive)
   - Persist role artifacts under `memory-bank/roles/<role>/` and cross-link to `memory-bank/project-brain/` where applicable.
   - Do not change `memory-bank/queue-system/tasks_active.json` SOT; roles may create or update tasks via `todo_manager.py` APIs to ensure compatibility with plan tooling and gating.

3) Decision Ledger and Handoffs (Additive)
   - Append decisions to `memory-bank/decisions/index.jsonl` with minimal schema (timestamp, role, summary, inputs, outputs, related task IDs).
   - Support role-to-role handoffs by writing structured records; execution remains user-driven or task-driven through existing tooling.

4) Enforcement Modes (Config-Over-Code)
   - Introduce `AI_ENFORCEMENT_MODE` env/config with values: `team` (default, current behavior), `solo` (advisory mode). In `solo`, only read-only tools (`plan_next.py`, `plain_hier.py`) relax to surface warnings prominently; the Deep Analysis Gate on `exec --run` and `done` remains hard-block for safety in the initial release. Future iteration may soften non-critical checks, but “analysis missing” and “conflict/duplicate findings” must remain blocked.

5) Analysis Mirror (Explicit)
   - Encourage generation of `analysis_active.json` as a formal mirror with done:true analysis phases to satisfy the Deep Analysis Gate. Provide a helper to scaffold analysis tasks from execution tasks; keep it read-only-safe unless explicitly invoked.

6) Observability and Auto-Sync
   - Keep `auto_sync_manager.py` calls after state changes; add lightweight counters/health logs. Do not modify timestamp or PH timezone invariants.

End-to-End Flow (Correct-by-Construction):
1. User issues a command (existing or role-prefixed).
2. Router dispatches to the proven hub or to role handlers; role outputs persist to role namespaces and may create/update tasks.
3. Execution uses `plan_next.py`/`plain_hier.py` for read-only previews and `todo_manager.py exec` for previews; `--run` goes through Deep Analysis Gate.
4. On pass, commands run; on block, print reason and suggest generating/finishing analysis mirror phases.
5. All changes trigger `auto_sync_manager.py` to update session and state files.

Rationale:
- This plan adopts proposal_1’s preservation, policy-switching, and ledger ideas while leveraging proposal_2’s hybrid routing and role catalog. It explicitly rejects proposal_2’s removal of blocking rules to maintain safety and compatibility with current gates.

### Recommendations for Automation Enhancements

- Execution Macros: Provide short commands that chain `plan_next.py` → `plain_hier.py` → `todo_manager.py exec <K.N>` previews for the next phase.
- Auto Phase Runner (opt-in): A wrapper that previews, runs with `--run` (after gate), shows status, and prompts to mark done; respects gate outcomes.
- Analysis Mirror Scaffolder: Generate `analysis_active.json` stubs from `tasks_active.json`, including required sections (Decision Gate, IMPORTANT NOTE) to satisfy the gate when ready.
- Role Acceptance Checklists: Per-role YAML checklists stored under `memory-bank/roles/<role>/checklists/` to improve consistency without altering execution flow.
- Decision Ledger Indexer: Nightly job to summarize decisions and surface conflicts/duplicates across artifacts.
- Observability: Minimal metrics emitted by `auto_sync_manager.py` (counts, last sync, open tasks) to a local `memory-bank/observability/state.json`.

### Implementation Checklist (Prioritized)

1) Add slash-command router in `task_command_center.py` that delegates to `framework_role_router` (new module), leaving existing menu and flows intact.
2) Implement `framework_role_router` with mappings for `/backlog`, `/plan`, `/gen_code`, `/test`, `/deploy`, `/remember`, etc.; persist outputs under `memory-bank/roles/<role>/...` and (optionally) create/update tasks via `todo_manager.py` APIs.
3) Create `memory-bank/roles/` namespaces and initialize minimal README/structure for each enabled role; no changes to `tasks_active.json` format.
4) Introduce `AI_ENFORCEMENT_MODE` configuration with default `team`. In the initial release, do not weaken Deep Analysis Gate; only improve messaging and previews in `solo` mode.
5) Provide an `analysis_mirror_scaffold.py` utility to generate `analysis_active.json` entries from execution tasks (read-only preview by default; explicit flag to write).
6) Implement `memory-bank/decisions/index.jsonl` writer helper; call it from role router after producing artifacts.
7) Add optional observability write in `auto_sync_manager.py` (non-blocking, try/except) to `memory-bank/observability/state.json`.
8) Documentation: Update framework README/QUICK_START to describe routing, gates, analysis mirror, and safe usage.

Non-Disruptive Integration Notes:
- No default behavior changes to `todo_manager.py`, `plan_next.py`, `plain_hier.py`, or `auto_sync_manager.py`.
- Routing and role features are additive and triggered only by explicit slash commands.
- Deep Analysis Gate remains authoritative for `exec --run` and `done`.


