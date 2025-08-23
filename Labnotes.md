# Lab Notes — Memory System Hardening

Date: (local) — please consider PH time context for timestamps.

## Scope
- Implement reliability and consistency improvements across memory + task subsystems.
- Phased rollout aligned with `frameworks/fwk-001-cursor-rules/examples/Final_Implementation_Plan.md`.

## Summary of Changes (by phase)

### Phase 1 — Atomic IO + Locking
- Added:
  - `atomic_io.py` — sidecar advisory locks (`flock`), atomic temp+replace, file/dir fsync, 0600 perms helpers.
- Refactored writers to atomic+locked JSON writes:
  - `todo_manager.py` → `_save()` now uses `with_json_lock` + `atomic_write_json`.
  - `auto_sync_manager.py` → `_update_cursor_state`, `_update_task_state`, `_update_task_interruption_state`, and active tasks cleanup now use atomic+locked writes; `current-session.md` writing deferred to bridge.
  - `task_state_manager.py` → `save_task_state()` uses `with_json_lock` + `atomic_write_json`; reads under shared lock.
  - `task_interruption_manager.py` → `save_state()` uses `with_json_lock` + `atomic_write_json`; loads under shared lock.

### Phase 3 — Cursor State Unification
- Updated `cursor_session_manager.py`:
  - Canonical path: `memory-bank/cursor_state.json`.
  - Ensures directory creation.
  - Mirrors to root `cursor_state.json` if present (compatibility), via atomic+locked write.

### Phase 4 — PH Timezone Normalization (ZoneInfo)
- Added `tz_utils.py` (Asia/Manila): `now_ph`, `now_ph_iso`, `parse_iso_aware`, `days_since`.
- Switched modules to PH-aware timestamps:
  - `todo_manager.py`: `_timestamp()` now `now_ph_iso()`; cleanup uses `parse_iso_aware` with PH-aware `now`.
  - `task_interruption_manager.py`: timestamps via `now_ph_iso()`.

### Phase 5 — Execution Run Logging
- Added `exec_logging.py`:
  - `run_logged(cmd)`: writes `.out`, `.err`, `.json` (0600 perms) under `memory-bank/logs/`, includes redaction for common secrets.
- Integrated into `todo_manager.py` → `exec_substep()` uses `run_logged` when `--run` is provided.

### Phase 6 — memory_cli Recall Fallback + Portability
- Updated `tools/memory/memory_cli.py`:
  - `MEMORY_STORAGE_ROOT` override for storage root.
  - Recall uses substring/tag fallback without requiring embeddings/FAISS; only loads model when semantic path is available.

### Phase 7 — Archival Policy (JSONL Append-only)
- Added `archive_tasks.py` — appends completed tasks to `memory-bank/queue-system/tasks_done.jsonl`.
- Updated `todo_manager.py` → `cleanup_completed_tasks()` now archives to JSONL and retains active list.

### Documentation
- Updated `frameworks/fwk-001-cursor-rules/DOCS/OVERVIEW.md` — end-to-end interaction mapping and Mermaid diagram.

## Tests & Results

### T1 — Concurrency Smoke Test (Phase 1)
- Command executed:
```bash
python3 - <<'PY'
import json, os, multiprocessing as mp, time
from atomic_io import safe_update_json
PATH = 'memory-bank/queue-system/tasks_active.json'

os.makedirs('memory-bank/queue-system', exist_ok=True)
if not os.path.exists(PATH):
    with open(PATH,'w') as f: f.write('[]')

def worker(i):
    def transform(obj):
        if not isinstance(obj, list):
            obj = []
        obj.append({"id": f"concurrency_{i}", "updated": time.time()})
        return obj
    safe_update_json(PATH, transform)

ps = [mp.Process(target=worker, args=(i,)) for i in range(16)]
[p.start() for p in ps]
[p.join() for p in ps]

data = json.load(open(PATH))
ids = {t.get('id') for t in data if isinstance(t, dict)}
print('count', len(data), 'unique', len(ids), 'ok', len(ids) >= 16)
PY
```
- Observed output:
```text
count 17 unique 17 ok True
```
- Verdict: PASS (no lost updates; all 16 parallel writes persisted).

### T2 — Single-writer `current-session.md` (Phase 2/3)
- Check: `auto_sync_manager.py` no longer writes the Markdown directly; it calls `cursor_memory_bridge.dump_markdown()`.
- Quick verify:
```bash
python3 cursor_memory_bridge.py --dump | cat
```
- Verdict: PASS (bridge-only writer enforced).

### T3 — Cursor State Path Unification (Phase 3)
- Verify canonical file exists and mirrors if root file present:
```bash
jq . memory-bank/cursor_state.json | head -n 50 | cat
```
- Verdict: PASS (canonical path active; mirroring logic present).

### T4 — Timezone Normalization (Phase 4)
- Verify helper:
```bash
python3 - <<'PY'
from tz_utils import now_ph_iso, parse_iso_aware
print('now_ph_iso:', now_ph_iso())
print('parse_iso_aware:', parse_iso_aware('2025-08-21T01:02:03Z'))
PY
```
- Verdict: PASS (aware ISO with +08:00).

### T5 — Exec Run Logging (Phase 5)
- How to test:
```bash
# Replace with valid task and phase index
python3 todo_manager.py exec <TASK_ID> K --run | cat
ls -l memory-bank/logs | cat
head -n 50 memory-bank/logs/run_*.json | cat
```
- Expected: `.out`, `.err`, `.json` created with 0600 perms; metadata includes `cmd`, `exit_code`, `duration_s`, `stdout`/`stderr` paths; sensitive strings redacted.
- Verdict: PENDING manual run (integration code in place).

### T6 — memory_cli Recall Fallback + Portability (Phase 6)
- How to test:
```bash
export MEMORY_STORAGE_ROOT="$PWD/memory-bank/storage/memory"
python3 tools/memory/memory_cli.py save "hello world" --tags demo
python3 tools/memory/memory_cli.py recall "hello" --topk 3 | cat
```
- Expected: Fallback recall prints JSON lines even without FAISS/embeddings; storage root under the env-specified path.
- Verdict: READY (manual test recommended).

### T7 — Archival JSONL (Phase 7)
- How to test:
```bash
python3 todo_manager.py cleanup | cat
wc -l memory-bank/queue-system/tasks_done.jsonl | cat
```
- Expected: Completed tasks appended to `tasks_done.jsonl`; active list retains non-completed tasks.
- Verdict: READY (functionality wired; content depends on current active tasks).

## Follow-ups / Next Steps
- Quantitative gates:
  - Lock acquisition p95 latency (< 50 ms @ 8 workers × 500 iterations) and 0 deadlocks — add dedicated stress test.
  - Crash durability (`SIGKILL` mid-write) → JSON remains valid as pre- or post-state.
- Redaction policy: expand patterns and add tests.
- Retention/rotation policy for `tasks_done.jsonl` and logs.
- CI checks to guard atomic IO usage and timezone-aware timestamps.

## File Inventory (changed/added)
- Added: `atomic_io.py`, `tz_utils.py`, `exec_logging.py`, `archive_tasks.py`.
- Modified: `todo_manager.py`, `auto_sync_manager.py`, `cursor_session_manager.py`, `task_state_manager.py`, `task_interruption_manager.py`, `tools/memory/memory_cli.py`.
- Docs: `frameworks/fwk-001-cursor-rules/DOCS/OVERVIEW.md` (diagram + mapping).
