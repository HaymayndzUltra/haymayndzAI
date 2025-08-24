## 1. Context Summary (type/intent detected)
- **Plan Title**: Action Plan — Memory System Hardening and Consistency
- **Type**: Operational
- **Intent**: Implement atomic, consistent, and portable memory/state handling across the repo, with single-writer enforcement, PH timezone normalization, structured execution logging, and archival policy.

## 2. Critical Risks (Conflicts with Codebase)
- **R-001 — Single-writer violation via direct writes to current-session.md in todo_manager**
  - **Evidence/Quote**: ```20:21:/workspace/frameworks/fwk-001-cursor-rules/Action_Plan.md```
  - **Codebase Conflict**: `tools/todo_manager.py` directly edits `memory-bank/current-session.md` during hard delete (lines 309-331), instead of delegating to `cursor_memory_bridge.dump_markdown()`.
  - **Severity**: High
  - **Affected Steps**: Phase 2; Exit criterion L64
  - **Downstream Impact**: Breaks single-writer policy and can cause race conditions/corruption during concurrent updates.

- **R-002 — Potential double-writing of cursor_state.json (no coordination with CursorSessionManager)**
  - **Evidence/Quote**: ```24:26:/workspace/frameworks/fwk-001-cursor-rules/Action_Plan.md```
  - **Codebase Conflict**: `src/repo/auto_sync_manager.py` writes `memory-bank/cursor_state.json` and mirrors root if present (lines 135-155); `tools/cursor_session_manager.py` independently autosaves to the same canonical file (lines 112-141) without detection/coordination.
  - **Severity**: Medium
  - **Affected Steps**: Phase 3; Exit criteria L63, L65
  - **Downstream Impact**: Interleaved writes and last-writer-wins inconsistencies.

- **R-003 — Timezone normalization incomplete (UTC/naive usage persists)**
  - **Evidence/Quote**: ```28:31:/workspace/frameworks/fwk-001-cursor-rules/Action_Plan.md```
  - **Codebase Conflict**:
    - `tools/cursor_memory_bridge.py` renders header with `datetime.utcnow()` (line 21) and prints "UTC" not `+08:00`.
    - `tools/cursor_session_manager.py` sets `last_activity` and `disconnected_at` via `datetime.utcnow().isoformat()` (lines 71, 152) producing naive/UTC timestamps.
  - **Severity**: Medium
  - **Affected Steps**: Phase 4; Exit criterion L66
  - **Downstream Impact**: Mixed timezones disrupt ordering, filtering, and auditability.

- **R-004 — Missing concurrency smoke test for multi-process updates**
  - **Evidence/Quote**: ```17:17:/workspace/frameworks/fwk-001-cursor-rules/Action_Plan.md```
  - **Codebase Conflict**: No test detected for concurrent writers to `memory-bank/queue-system/tasks_active.json`.
  - **Severity**: Medium
  - **Affected Steps**: Phase 1; Exit criterion L63
  - **Downstream Impact**: Unvalidated locking could allow regressions (truncation/corruption) under contention.

- **R-005 — Plan expects `locked` context; code provides `with_file_lock`/`with_json_lock`**
  - **Evidence/Quote**: ```15:15:/workspace/frameworks/fwk-001-cursor-rules/Action_Plan.md```
  - **Codebase Conflict**: `src/repo/atomic_io.py` exposes `with_file_lock` and `with_json_lock`, not a `locked` symbol. This breaks a literal API expectation.
  - **Severity**: Medium
  - **Affected Steps**: Phase 1
  - **Downstream Impact**: Implementers following the plan verbatim will not find a `locked` API; potential mis-implementation.

- **R-006 — Archival policy wording vs implementation (`tasks_done.json` vs `tasks_done.jsonl`)**
  - **Evidence/Quote**: ```41:42:/workspace/frameworks/fwk-001-cursor-rules/Action_Plan.md```
  - **Codebase Conflict**: `tools/archive_tasks.py` archives to `memory-bank/queue-system/tasks_done.jsonl` (line 14), not `tasks_done.json`.
  - **Severity**: Low
  - **Affected Steps**: Phase 7; Exit criterion L69
  - **Downstream Impact**: Path/format mismatch for downstream readers/documentation.

- **R-007 — Silent purges still occur for completed tasks**
  - **Evidence/Quote**: ```41:42:/workspace/frameworks/fwk-001-cursor-rules/Action_Plan.md```
  - **Codebase Conflict**: `tools/todo_manager.py` auto-purges old completed tasks on load via `_cleanup_outdated_tasks` (lines 62-83) without archiving first; contradicts "no silent purges" (Exit L69).
  - **Severity**: High
  - **Affected Steps**: Phase 7; Exit criterion L69
  - **Downstream Impact**: Data loss relative to desired archival-first policy.

- **R-008 — Advisory file locking missing in `cursor_session_manager` state writes**
  - **Evidence/Quote**: ```6:7:/workspace/frameworks/fwk-001-cursor-rules/Action_Plan.md```
  - **Codebase Conflict**: `tools/cursor_session_manager.py` uses temp+`os.replace` (lines 120-125) but not `with_json_lock`; plan calls for advisory locking to prevent concurrent truncation.
  - **Severity**: Medium
  - **Affected Steps**: Phase 1; Exit criterion L63
  - **Downstream Impact**: Races with other writers could bypass lock coordination.

- **R-009 — Recall CLI exists but was presumed absent; verify fallback behavior**
  - **Evidence/Quote**: ```36:39:/workspace/frameworks/fwk-001-cursor-rules/Action_Plan.md```
  - **Codebase Conflict**: Plan references `tools/memory/memory_cli.py` for recall fallback. File exists and implements substring/tag fallback when embeddings/index are unavailable (lines 154-165), satisfying the plan. Earlier repository scans missed it due to path filtering; ensure doc references align.
  - **Severity**: Low
  - **Affected Steps**: Phase 6; Exit criterion L68
  - **Downstream Impact**: Documentation mismatch risk rather than functional gap.

## 3. Confirmed Alignments (Matches with Codebase)
- **A-001 — Atomic IO utilities exist and are used by writers**
  - **Evidence/Quote**: ```15:16:/workspace/frameworks/fwk-001-cursor-rules/Action_Plan.md```
  - **Codebase Alignment**: `src/repo/atomic_io.py` provides `atomic_write_json`, `with_file_lock`, `with_json_lock`, `safe_update_json`. `tools/todo_manager.py` `_save` uses `with_json_lock` + `atomic_write_json` (lines 85-93). `src/repo/auto_sync_manager.py` uses the same for JSON updates (e.g., lines 147-155, 173-175, 187-188, 265-267).
  - **Rationale**: Reduces corruption risk and ensures durable writes.

- **A-002 — AutoSyncManager defers session note writes to memory bridge**
  - **Evidence/Quote**: ```20:21:/workspace/frameworks/fwk-001-cursor-rules/Action_Plan.md```
  - **Codebase Alignment**: `src/repo/auto_sync_manager.py` `_update_current_session()` calls `cursor_memory_bridge.dump_markdown()` (lines 217-219) instead of writing the markdown file directly.
  - **Rationale**: Implements single-writer policy via dedicated bridge.

- **A-003 — Cursor state canonical path and conditional mirror**
  - **Evidence/Quote**: ```24:25:/workspace/frameworks/fwk-001-cursor-rules/Action_Plan.md```
  - **Codebase Alignment**: `tools/cursor_session_manager.py` defaults to `memory-bank/cursor_state.json` (line 23) and mirrors to root only if the file exists (lines 136-141). `src/repo/auto_sync_manager.py` mirrors root only if present (lines 151-155).
  - **Rationale**: Maintains a single source of truth while preserving backward compatibility.

- **A-004 — PH timezone helpers implemented and partially adopted**
  - **Evidence/Quote**: ```28:31:/workspace/frameworks/fwk-001-cursor-rules/Action_Plan.md```
  - **Codebase Alignment**: `src/repo/tz_utils.py` provides `now_ph_iso`, `parse_iso_aware`, and `days_since`. `tools/todo_manager.py` uses these for timestamps and cleanup logic (e.g., lines 68-76, 106-109).
  - **Rationale**: Establishes consistent timezone-aware operations in core flows.

- **A-005 — Structured run logging for exec_substep**
  - **Evidence/Quote**: ```33:35:/workspace/frameworks/fwk-001-cursor-rules/Action_Plan.md```
  - **Codebase Alignment**: `src/repo/exec_logging.py` offers `run_logged()` producing `.out`, `.err`, and `.json` files under `memory-bank/logs/`. `tools/todo_manager.py` `exec_substep()` integrates this (lines 631-645).
  - **Rationale**: Enables reproducible executions with redacted logs and timing metadata.

- **A-006 — Archival helper integrated into cleanup flow**
  - **Evidence/Quote**: ```41:42:/workspace/frameworks/fwk-001-cursor-rules/Action_Plan.md```
  - **Codebase Alignment**: `tools/archive_tasks.py` exists and `tools/todo_manager.py` `cleanup_completed_tasks()` calls `archive_completed()` (lines 359-368).
  - **Rationale**: Provides archival mechanism instead of hard deletion.

- **A-007 — Recall fallback without embeddings is implemented**
  - **Evidence/Quote**: ```36:39:/workspace/frameworks/fwk-001-cursor-rules/Action_Plan.md```
  - **Codebase Alignment**: `tools/memory/memory_cli.py` `cmd_recall` falls back to substring/tag search when FAISS/model/index are unavailable (lines 154-165).
  - **Rationale**: Meets portability goal for recall.

## 4. Potential Blind Spots
- **B-001 — Limited secret redaction in execution logs**
  - **Why it matters**: Current regexes in `exec_logging.py` may miss other sensitive patterns (env var variants, JSON-embedded secrets).
- **B-002 — Direct writes to `memory_store.json` and `current-session.md` from `memory_system/cli.py save`**
  - **Why it matters**: Bypasses locking and single-writer model outside of the core writers.
- **B-003 — Content of markdown snapshot not sourced from `_update_current_session()`**
  - **Why it matters**: `AutoSyncManager` builds `session_content` but ultimately defers to the bridge, which builds independently; potential drift in intended content.

## 5. Assumptions (explicit/implicit) & fragility
- **A-001 (Explicit)**: Linux with flock support
  - **Fragility**: Medium — `fcntl` absence downgrades locks to no-ops; tests missing.
- **A-002 (Explicit)**: Python 3.10+
  - **Fragility**: Low — Code uses 3.10 features (PEP 604 unions), present in repo.
- **A-003 (Implicit)**: No other processes write SoT files
  - **Fragility**: High — Multiple in-repo writers already target the same SoT; external writers would exacerbate races.

## 6. Ambiguities & Measurement Gaps
- **M-001**: Criteria for "avoid double-writing when CursorSessionManager is active" not operationalized (no detection/lock-ownership metric).
- **M-002**: "All timestamps stored/printed with +08:00 offset" — extent (logs, markdown headers, JSON state) not clearly bounded.

## 7. Consistency Issues (within plan & across refs)
- Plan references `tools/memory/memory_cli.py` for recall; confirmed present and aligned. Some docs refer to other CLIs (`memory_system/cli.py`).
- Archival filename `.json` vs implemented `.jsonl` differs.

## 8. Compliance/Feasibility/Timeline/Scope findings
- **Compliance**: Basic log redaction present; no explicit data retention/privacy policy observed.
- **Feasibility**: Many foundations already implemented (atomic IO, exec logging, tz utils); gaps are constrained and actionable.
- **Timeline/Ordering**: Atomic IO and single-writer largely in place; remaining items involve refactors and test coverage.
- **Scope**: Plan scope touches multiple writers; additional flows (e.g., `memory_system/cli.py save`) write outside the intended guardrails.

## 9. Traceability Map (Risk & Alignment IDs → Plan refs)
- R-001 → ```20:21:/workspace/frameworks/fwk-001-cursor-rules/Action_Plan.md```
- R-002 → ```24:26:/workspace/frameworks/fwk-001-cursor-rules/Action_Plan.md```
- R-003 → ```28:31:/workspace/frameworks/fwk-001-cursor-rules/Action_Plan.md```
- R-004 → ```17:17:/workspace/frameworks/fwk-001-cursor-rules/Action_Plan.md```
- R-005 → ```15:15:/workspace/frameworks/fwk-001-cursor-rules/Action_Plan.md```
- R-006 → ```41:42:/workspace/frameworks/fwk-001-cursor-rules/Action_Plan.md```
- R-007 → ```41:42:/workspace/frameworks/fwk-001-cursor-rules/Action_Plan.md```
- R-008 → ```6:7:/workspace/frameworks/fwk-001-cursor-rules/Action_Plan.md```
- R-009 → ```36:39:/workspace/frameworks/fwk-001-cursor-rules/Action_Plan.md```
- A-001 → ```15:16:/workspace/frameworks/fwk-001-cursor-rules/Action_Plan.md```
- A-002 → ```20:21:/workspace/frameworks/fwk-001-cursor-rules/Action_Plan.md```
- A-003 → ```24:25:/workspace/frameworks/fwk-001-cursor-rules/Action_Plan.md```
- A-004 → ```28:31:/workspace/frameworks/fwk-001-cursor-rules/Action_Plan.md```
- A-005 → ```33:35:/workspace/frameworks/fwk-001-cursor-rules/Action_Plan.md```
- A-006 → ```41:42:/workspace/frameworks/fwk-001-cursor-rules/Action_Plan.md```
- A-007 → ```36:39:/workspace/frameworks/fwk-001-cursor-rules/Action_Plan.md```

## 10. Verdict
- Risks detected. See sections above.
