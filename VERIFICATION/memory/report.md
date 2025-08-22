Status: WARN

# Memory Bridge Verification Report

Component under review: `framework_memory_bridge.mdc` with `memory-bank/queue-system/*`, `memory-bank/cursor_state.json`, `memory-bank/current-session.md`

## Scope & Inputs
- Framework: `frameworks/fwk-001-cursor-rules/system-prompt/framework_memory_bridge.mdc`
- Queue system: `memory-bank/queue-system/{tasks_active.json,tasks_queue.json,tasks_done.json,tasks_interrupted.json,analysis_active.json}`
- Session state: `memory-bank/cursor_state.json`, `cursor_state.json` (root mirror)
- Session markdown: `memory-bank/current-session.md`
- Reference modules: `todo_manager.py`, `plan_next.py`, `plain_hier.py`, `auto_sync_manager.py`, `cursor_memory_bridge.py`, `cursor_session_manager.py`, `task_state_manager.py`, `task_interruption_manager.py`, `memory_system/cli.py`

## Rationale
- RACI ownership defined for all target files; single source for execution established (`tasks_active.json`).
- Timezone policy requires +08:00; nonconformance observed in `cursor_session_manager` and `cursor_memory_bridge` header (findings.json consistency section).
- Atomicity/locking not yet implemented for task JSON writes; integrity checks specify temp+replace and fcntl locks.
- Single-writer policy for `current-session.md` not enforced; multiple writers identified (Conflict Resolution).
- Continuity checklist coherent and actionable; retention rotation policy described but pending implementation.

## Read/Write Map (observed)
- `tasks_active.json`
  - Read: `plan_next.py`, `plain_hier.py`, `auto_sync_manager.py`
  - Write: `todo_manager.py` (save path; non-atomic write_text)
- `analysis_active.json`
  - Read: Deep Analysis Gate via `todo_manager.enforce_deep_analysis_gate`, `plain_hier.py --mode analysis`, `plan_next.py --mode analysis`
  - Write: n/a in codebase (expected via analysis scaffolder/ingest)
- `current-session.md`
  - Write: `cursor_memory_bridge.dump_markdown()` (full snapshot), `auto_sync_manager._update_current_session()` (direct write), `memory_system/cli.py` (append)
  - Read: n/a (human-readable)
- `memory-bank/cursor_state.json` and root `cursor_state.json`
  - Write: `auto_sync_manager._update_cursor_state()` (primary to memory-bank + optional root mirror)
  - Write: `cursor_session_manager` (atomic writes to root `cursor_state.json` by default)
  - Read: various helpers; `cursor_memory_bridge` pulls from `cursor_session_manager`
- `tasks_queue.json` / `tasks_done.json` / `tasks_interrupted.json`
  - Read: tooling and docs; no active writers observed for queue/done; `tasks_interrupted.json` exists but is empty

## Ownership & Write Constraints (RACI)
- `tasks_active.json`
  - Responsible/Accountable: `todo_manager.py`
  - Consulted: `plan_next.py`, `plain_hier.py`, `auto_sync_manager.py`
  - Informed: framework roles/bridge
  - Constraints: Single SOT for execution; writes MUST be atomic with file locks; PH `+08:00` timestamps in `created`/`updated`.
- `analysis_active.json`
  - Responsible/Accountable: Analysis ingestion tool (mirror), enforced by Deep Analysis Gate in `todo_manager.py`
  - Consulted: `plan_next.py`, `plain_hier.py`
  - Informed: framework roles/bridge
  - Constraints: Must include `source_task_id` link; each phase ends with `IMPORTANT NOTE:` and Decision Gate content.
- `current-session.md`
  - Responsible/Accountable: `cursor_memory_bridge.dump_markdown()`
  - Consulted: `auto_sync_manager` (should delegate), `memory_system/cli.py` (append-only under Memory Note)
  - Informed: all tools/users
  - Constraints: Single-writer policy for full snapshot; append-only sections must not overwrite snapshot.
- `memory-bank/cursor_state.json` (canonical) and root `cursor_state.json` (mirror)
  - Responsible/Accountable: `cursor_session_manager` (canonical writer)
  - Consulted: `auto_sync_manager` (may mirror only if root exists and session manager inactive)
  - Informed: framework roles/bridge
  - Constraints: Canonical path under `memory-bank/`; root is compatibility mirror only; PH `+08:00` timestamps.
- Queue/archive files
  - Responsible/Accountable: Queue/retention logic owned by `todo_manager.py` (until a dedicated engine exists)
  - Consulted: `auto_sync_manager`
  - Constraints: Archive to `tasks_done.json` instead of purging; implement rotation rules.

## Consistency & Timestamp Policy (PH +08:00)
- Policy: All persisted timestamps MUST be ISO8601 with `+08:00` offset.
- Conformance (observed):
  - `todo_manager._timestamp()` emits `+08:00` ✔
  - `auto_sync_manager` uses `+08:00` ✔
  - `cursor_session_manager` uses UTC naive for `last_activity`/`disconnected_at` ✖
  - `current-session.md` header: `cursor_memory_bridge` prints `... UTC` ✖; `auto_sync_manager` prints `PH`-formatted header ✔
- Expectation: Normalize `cursor_session_manager` and `cursor_memory_bridge` to PH `+08:00` for parity with queue/system files.

## Integrity & Recovery Checks (planned)
- Atomicity & Locking
  - Use temp-file + `os.replace` for `tasks_active.json` and `analysis_active.json` writes.
  - Wrap critical reads/writes in advisory `fcntl` locks.
- Schema & Lint
  - `plan_next.py` lint: Phase 0 first, `IMPORTANT NOTE:` present, monotonic completion.
  - Deep Analysis Gate: enforce `analysis_active.json` mirror and Decision Gate content before `exec --run`/`done`.
- Reference linkage
  - `analysis_active.json.source_task_id` must map to an active execution task.
- Session continuity on crash
  - On restart: `auto_sync_manager.sync_all_states()`; ensure `cursor_state` and session markdown reflect latest active task.
  - If divergence detected (root vs memory-bank cursor state): treat memory-bank version as canonical; mirror to root if present.

## Retention & Compaction
- Completed tasks: Archive to `tasks_done.json` instead of deleting.
- Rotation: Define size/time caps (e.g., retain 90 days or 10k entries); compact oldest first.
- Backlog performance: Prefer streaming reads for very large archives; paginate UI.

## Conflict Resolution
- Bridge policy: `existing_system_precedence: true` (framework doc). Existing system wins conflicts.
- Current conflicts (observed):
  - `current-session.md`: writers = `cursor_memory_bridge` (snapshot), `auto_sync_manager` (direct write), `memory_system/cli.py` (append). Resolution: only bridge writes snapshot; `auto_sync_manager` must call bridge; `memory_system/cli.py` append-only under a distinct section.
  - `cursor_state.json`: `auto_sync_manager` and `cursor_session_manager` both write. Resolution: canonicalize to `memory-bank/cursor_state.json` via session manager; `auto_sync_manager` mirrors only when root exists and session manager is inactive.
  - Atomicity: `todo_manager._save()` is non-atomic. Resolution: adopt temp + replace and `fcntl` locking.

## Continuity Checklist (Crash/Restart)
- Load active tasks: read `memory-bank/queue-system/tasks_active.json`.
- Sync state: run `auto_sync_manager.auto_sync()`; verify `memory-bank/cursor_state.json` and `memory-bank/current-session.md` updated.
- Gate check: `plan_next.py --gate --task-id <ACTIVE_TASK_ID>` for Deep Analysis Gate status.
- Mirror: if root `cursor_state.json` exists, mirror from canonical.
- Audit: verify timestamps include `+08:00` across state/markdown.

## Findings Summary
- `PH +08:00` normalization: PARTIAL — fix `cursor_session_manager` and `cursor_memory_bridge`.
- Single-writer policies: NEEDS CHANGE — eliminate direct markdown writes in `auto_sync_manager`; restrict `memory_system/cli.py` to append-only.
- Atomic writes/locking: NEEDS CHANGE — implement for task JSON files.
- Retention: NEEDS CHANGE — archive completed tasks to `tasks_done.json` with rotation.
- Deep Analysis Gate: PRESENT — `analysis_active.json` exists with all phases done:true for current task.