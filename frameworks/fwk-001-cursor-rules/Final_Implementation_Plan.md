## Final Implementation Plan — Memory System Hardening and Consistency

### 1) Scope & Goals
- **Scope**: Apply IO, locking, logging, timezone, state unification, and archival hardening across memory-related modules.
- **Primary Goals**: Prevent corruption via atomic writes + advisory locks; enforce single-writer for `current-session.md`; unify cursor state; normalize PH timezone; add structured run logs; ensure recall fallback; archive tasks instead of purge.

### 2) Architecture & Invariants
- **Single Source of Truth**:
  - `memory-bank/cursor_state.json` is canonical; optional mirror to repo root if present (best-effort, non-transactional).
- **Locking Model**:
  - Advisory `flock(2)` using sidecar lock files `<target>.lock`; single lock per SoT file.
  - Bounded wait with jittered backoff; define a consistent acquisition order if multiple locks are ever taken.
- **Atomicity & Durability**:
  - Same-dir temp file; fsync file then atomic `os.replace`; fsync parent directory post-rename.
  - Files 0600, directories 0700.
- **Timezone**:
  - Use `zoneinfo.ZoneInfo("Asia/Manila")`; require aware timestamps; reject naive inputs.
- **Logging**:
  - `memory-bank/logs/` contains `.out`, `.err`, and `.json` metadata with redaction; 0600 permissions.
- **Archival**:
  - Append-only `tasks_done.jsonl` with `{task_id, finished_at, source}`; retention configured.

### 3) Work Plan (Phased)
1. Atomic IO + Locking Foundation
   - Create `atomic_io.py`: `atomic_write_json`, `safe_update_json`, `locked` context.
   - Refactor `todo_manager.py`, `auto_sync_manager.py` to use atomic IO.
   - Add mp stress + chaos tests (see Gates G1/G2).

2. Single-Writer Enforcement for `current-session.md`
   - Remove direct writes in `AutoSyncManager`.
   - Centralize via `cursor_memory_bridge.dump_markdown()` with lock.
   - Feature flag for transition; emit warnings before hard enforcement.

3. Cursor State Unification
   - Canonicalize to `memory-bank/cursor_state.json`.
   - Optional mirror to root if file exists; treat mirror as best-effort.
   - Avoid double-writes when `CursorSessionManager` is active.

4. PH Timezone Normalization
   - Add `tz_utils.py`: `now_ph_iso`, `parse_iso_aware`, `days_since` using `zoneinfo`.
   - Replace naive `datetime.utcnow()` usages and naive arithmetic.

5. Execution Run Logging
   - Add `exec_logging.py`: `run_logged()` for `todo_manager.exec_substep`.
   - Write `.out/.err/.json` per run; apply redaction filters.

6. Memory CLI Recall Fallback + Portability
   - Recall supports substring/tag fallback without embeddings; define complexity and case handling.
   - Add `MEMORY_STORAGE_ROOT` env override; validate via `Path.resolve()`.

7. Archival Policy for Completed Tasks
   - Append to `memory-bank/queue-system/tasks_done.jsonl`.
   - Provide `archive_tasks.py` and integrate into cleanup.

### 4) Risks and Mitigations
- **Deadlocks from locks**: Single lock per file; bounded waits; telemetry for p95/p99; acquisition ordering if multi-lock is introduced.
- **Breaking scripts on single-writer**: Transition flag + warning period; docs and examples updated.
- **Ordering change from timezone**: Enforce aware timestamps; provide one-time migration guidance; sort by explicit aware keys.
- **Sensitive output in logs**: Redaction filters; opt-out for highly sensitive steps; retention/rotation policies.
- **Network FS semantics**: Document non-goals; detect non-local FS and warn; recommend local FS for SoT.

### 5) Acceptance Gates (Verification)
- G1 Locking latency: Under 8 workers × 500 iterations, p95 lock acquisition < 50 ms; 0 deadlocks in 5-minute run.
- G2 Durability: After `SIGKILL` during write, file remains valid JSON and is either pre- or post-state (never partial).
- G3 Logging: `.out/.err/.json` created with 0600; metadata includes `cmd`, `exit_code`, `duration_s`, and file paths; sampled logs show no unredacted secrets.
- G4 Timezone: All new timestamps ISO-8601 with zone; `days_since` matches manual calculation across month boundaries in PH tz.
- G5 Archival: `tasks_done.jsonl` entries contain required fields and obey retention policy.

### 6) Implementation Notes (Pointers to PoCs)
- Atomic IO (file+dir fsync, atomic replace, `flock`) — see Validation Report snippets `atomic_write_json`.
- Run logging with redaction and 0600 perms — see Validation Report `run_logged()`.
- PH timezone utilities using `zoneinfo` — see Validation Report `tz_utils.py` snippet.
- Concurrency stress test — see Validation Report stress test snippet.

### 7) Compliance Checklist
- Enforce 0600 files / 0700 directories for SoT and logs.
- Validate `MEMORY_STORAGE_ROOT` using `Path.resolve()`; disallow traversal outside allowed root.
- Document and test redaction filters; maintain denylist for common secret markers.
- Define log retention and rotation; document purge/archival rules.

### 8) Rollback/Recovery
- If lock contention or deadlocks exceed thresholds, revert to prior writers and disable enforcement via feature flag.
- If logging leaks detected, disable logging of stdout/stderr and retain metadata only until filters are corrected.
- If timezone normalization causes ordering regressions, fall back to previous sort key while patching inputs to aware timestamps.

### 9) Timeline & Ownership (high-level)
- Week 1: Phase 1 + tests (Owner: Core Platform)
- Week 2: Phase 2–3 (Owner: Core Platform, with Memory Tooling)
- Week 3: Phase 4–5 (Owner: Memory Tooling)
- Week 4: Phase 6–7, documentation, and CI policies (Owner: Core Platform)

### 10) References
- Action Plan: `frameworks/fwk-001-cursor-rules/Action_Plan.md`
- Summary Report: `frameworks/fwk-001-cursor-rules/examples/Summary_Report.md`
- Validation Report: `frameworks/fwk-001-cursor-rules/examples/Validation_Report.md`
- Python `os.replace`: `https://docs.python.org/3/library/os.html#os.replace`
- `flock(2)`: `https://man7.org/linux/man-pages/man2/flock.2.html`, `fcntl(2)`: `https://man7.org/linux/man-pages/man2/fcntl.2.html`
- PEP 615 `zoneinfo`: `https://peps.python.org/pep-0615/`

### 11) Success Criteria (Exit)
- All writers use atomic IO + lock.
- Only `cursor_memory_bridge.dump_markdown()` writes `current-session.md`.
- Canonical `cursor_state.json` under `memory-bank/` with optional mirror.
- All timestamps are aware and PH-tz; utilities integrated.
- `exec_substep` produces structured logs with redaction.
- Recall fallback works without embeddings.
- Completed tasks archived; no silent purges.
