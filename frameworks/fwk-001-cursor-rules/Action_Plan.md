# Action Plan — Memory System Hardening and Consistency

## Type
Operational

## Objectives
- Establish single sources of truth (SoT) for session and queue state.
- Prevent data corruption through atomic writes and advisory file locking.
- Normalize time handling to PH timezone (+08:00) with aware ISO timestamps.
- Enforce single-writer policy for `current-session.md` via `cursor_memory_bridge.dump_markdown()`.
- Add structured run logging for `todo_manager.exec_substep` (stdout/stderr paths, timings, exit codes).
- Improve portability (no hardcoded absolute paths) and graceful logging fallback.

## Phases
1) Atomic IO + Locking foundation
- Implement `atomic_io.py` with `atomic_write_json`, `locked`, and `safe_update_json`.
- Refactor writers in `todo_manager.py` and `auto_sync_manager.py` to use atomic IO.
- Add a concurrency smoke test for multi-process updates to `tasks_active.json`.

2) Single-writer enforcement for current-session.md
- Remove direct writes in `AutoSyncManager` to `current-session.md`.
- Call `cursor_memory_bridge.dump_markdown()` after successful syncs.

3) Cursor state unification
- Set canonical path to `memory-bank/cursor_state.json`.
- Mirror to root `cursor_state.json` only if file exists.
- Avoid double-writing when `CursorSessionManager` is active.

4) PH timezone normalization
- Create `tz_utils.py` with `now_ph_iso`, `parse_iso_aware`, and `days_since`.
- Replace naive usages (`datetime.utcnow()`) and naive delta arithmetic.

5) Execution run logging
- Introduce `exec_logging.py` with `run_logged()` for `todo_manager.exec_substep`.
- Log to `memory-bank/logs/` with `.out`, `.err`, and `.json` metadata.

6) Memory CLI recall fallback + config portability
- Modify recall to not require embeddings when using substring/tag fallback.
- Add `MEMORY_STORAGE_ROOT` env override; default to repo-local storage path.

7) Archival policy for completed tasks
- Archive completed tasks to `memory-bank/queue-system/tasks_done.json` instead of purge.
- Provide `archive_tasks.py` helper and integrate into cleanup flow.

## Assumptions
- Linux environment with flock support (fcntl).
- Python 3.10+ available across tooling.
- No other external process writes to SoT files except these modules.
- Acceptable to add small utility modules (`atomic_io.py`, `tz_utils.py`, etc.).

## Risks
- Concurrency changes can introduce deadlocks if locks are misused.
- Single-writer enforcement may break scripts relying on `AutoSyncManager` direct markdown writes.
- Timezone normalization may alter sorting if mixed old records lack tz offsets.
- Run logging could capture sensitive output if commands emit secrets (mitigation: filter/redact).

## References
- Python `os.replace` (atomic rename): https://docs.python.org/3/library/os.html#os.replace
- File locking (`fcntl`): https://man7.org/linux/man-pages/man2/flock.2.html
- ISO 8601 and timezone-aware datetimes: https://docs.python.org/3/library/datetime.html
- Repository files: `todo_manager.py`, `auto_sync_manager.py`, `cursor_session_manager.py`, `cursor_memory_bridge.py`, `tools/memory/memory_cli.py`

## Exit Criteria
- All writers to SoT use atomic IO and locks.
- Only `cursor_memory_bridge.dump_markdown()` writes `current-session.md`.
- `cursor_state.json` unified under `memory-bank/` with optional mirror.
- All timestamps stored/printed with `+08:00` offset.
- `exec_substep` produces structured logs per command.
- `memory_cli recall` works without embeddings installed.
- Completed tasks archived; no silent purges.
