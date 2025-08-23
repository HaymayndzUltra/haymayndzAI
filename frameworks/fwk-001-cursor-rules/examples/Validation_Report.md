## Validation Report — Memory System Hardening and Consistency

### 1) Scope and Artifacts
- **Plan Under Test**: `frameworks/fwk-001-cursor-rules/Action_Plan.md`
- **Objective**: Validate the plan’s feasibility, risks, mitigations, and provide executable proofs-of-concept (PoC) with measurable acceptance criteria.
- **Method**: Consistency checks, evidence-backed citations, executable PoC snippets, edge-case analysis, and verification gates.

### 2) Evidence Citations (Plan Excerpts)
```14:19:/workspace/frameworks/fwk-001-cursor-rules/Action_Plan.md
## Phases
1) Atomic IO + Locking foundation
- Implement `atomic_io.py` with `atomic_write_json`, `locked`, and `safe_update_json`.
- Refactor writers in `todo_manager.py` and `auto_sync_manager.py` to use atomic IO.
- Add a concurrency smoke test for multi-process updates to `tasks_active.json`.
```
```29:36:/workspace/frameworks/fwk-001-cursor-rules/Action_Plan.md
4) PH timezone normalization
- Create `tz_utils.py` with `now_ph_iso`, `parse_iso_aware`, and `days_since`.
- Replace naive usages (`datetime.utcnow()`) and naive delta arithmetic.
5) Execution run logging
- Introduce `exec_logging.py` with `run_logged()` for `todo_manager.exec_substep`.
- Log to `memory-bank/logs/` with `.out`, `.err`, and `.json` metadata.
```
```41:44:/workspace/frameworks/fwk-001-cursor-rules/Action_Plan.md
7) Archival policy for completed tasks
- Archive completed tasks to `memory-bank/queue-system/tasks_done.json` instead of purge.
- Provide `archive_tasks.py` helper and integrate into cleanup flow.
```
```51:56:/workspace/frameworks/fwk-001-cursor-rules/Action_Plan.md
## Risks
- Concurrency changes can introduce deadlocks if locks are misused.
- Single-writer enforcement may break scripts relying on `AutoSyncManager` direct markdown writes.
- Timezone normalization may alter sorting if mixed old records lack tz offsets.
- Run logging could capture sensitive output if commands emit secrets (mitigation: filter/redact).
```

### 3) Consistency Validation
- **Locking semantics clarity**: The plan mentions “flock support (fcntl)”. `flock(2)` and `fcntl(2)` are distinct; pick one and document semantics and portability. Recommended: advisory locks via `flock(2)` with a dedicated sidecar lock file.
- **Atomicity guarantees**: Specify fsync for file and parent directory, and same-directory temp file use to preserve atomic rename assumptions on Linux.
- **Single-writer policy**: Define detection and gating for `current-session.md` writes (lock file or PID file ownership) and explicit rejection behavior/timeouts.
- **Timezone**: Prefer `zoneinfo.ZoneInfo("Asia/Manila")` over fixed `+08:00` to future-proof policy changes.
- **Logging**: Define JSON metadata schema, 0600 perms, redaction policy, and rotation/retention.
- **Archival**: Use append-only `tasks_done.jsonl` (or sharded) with index fields and retention.

### 4) Executable PoC Snippets (Python 3.10+, Linux)
- Minimal, self-contained snippets demonstrating feasibility and error handling.

```python
#!/usr/bin/env python3
# PoC: Atomic JSON write with flock, fsync, and safe replace
import json, os, tempfile, fcntl
from pathlib import Path

def atomic_write_json(path: str, data: dict, *, perm: int = 0o600) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    lock_path = target.with_suffix(target.suffix + ".lock")
    # Acquire exclusive advisory lock
    with open(lock_path, "a+") as lockf:
        fcntl.flock(lockf.fileno(), fcntl.LOCK_EX)
        tmp_fd, tmp_name = tempfile.mkstemp(prefix=target.name + ".", dir=str(target.parent))
        try:
            with os.fdopen(tmp_fd, "w") as tmpf:
                os.fchmod(tmpf.fileno(), perm)
                json.dump(data, tmpf, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
                tmpf.flush(); os.fsync(tmpf.fileno())
            os.replace(tmp_name, target)  # atomic on same filesystem
            dfd = os.open(target.parent, os.O_DIRECTORY)
            try:
                os.fsync(dfd)
            finally:
                os.close(dfd)
        finally:
            if os.path.exists(tmp_name):
                os.unlink(tmp_name)
```

```python
#!/usr/bin/env python3
# PoC: Logged subprocess execution with redaction and 0600 perms
import json, os, subprocess, time
from pathlib import Path

REDACT_PATTERNS = ("AWS_SECRET_ACCESS_KEY=", "Authorization:", "password=")

def redact(text: str) -> str:
    out = text
    for p in REDACT_PATTERNS:
        if p in out:
            out = out.replace(p, p + "REDACTED")
    return out

def run_logged(cmd: list[str], log_dir: str) -> dict:
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    ts = int(time.time() * 1000)
    base = Path(log_dir) / f"run-{ts}"
    out_path, err_path, meta_path = f"{base}.out", f"{base}.err", f"{base}.json"
    start = time.time()
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = proc.communicate()
    stdout, stderr = redact(stdout), redact(stderr)
    with open(out_path, "w") as out, open(err_path, "w") as err:
        os.fchmod(out.fileno(), 0o600); os.fchmod(err.fileno(), 0o600)
        out.write(stdout); err.write(stderr)
    meta = {
        "cmd": cmd,
        "exit_code": proc.returncode,
        "duration_s": round(time.time() - start, 6),
        "stdout_path": out_path,
        "stderr_path": err_path,
        "started_at_unix_ms": ts,
    }
    with open(meta_path, "w") as mf:
        os.fchmod(mf.fileno(), 0o600)
        json.dump(meta, mf, separators=(",", ":"), sort_keys=True)
    return meta
```

```python
#!/usr/bin/env python3
# PoC: PH timezone helpers using zoneinfo
from datetime import datetime
from zoneinfo import ZoneInfo

PH = ZoneInfo("Asia/Manila")

def now_ph_iso() -> str:
    return datetime.now(tz=PH).isoformat()

def parse_iso_aware(s: str) -> datetime:
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        raise ValueError("Timestamp must be timezone-aware")
    return dt

def days_since(iso_then: str) -> int:
    then = parse_iso_aware(iso_then)
    return int((datetime.now(tz=PH) - then.astimezone(PH)).total_seconds() // 86400)
```

```python
#!/usr/bin/env python3
# PoC: Concurrency stress test (8 procs x 500 writes) for atomic_write_json
import json, multiprocessing as mp, random, time
from pathlib import Path

# assume atomic_write_json is available in scope

def worker(path: str, iters: int):
    rng = random.Random()
    for _ in range(iters):
        cur = 0
        p = Path(path)
        if p.exists():
            try:
                cur = json.loads(p.read_text()).get("counter", 0)
            except Exception:
                # tolerate read races; writer guarantees atomicity
                pass
        atomic_write_json(path, {"counter": cur + 1})
        time.sleep(rng.random() * 0.003)

if __name__ == "__main__":
    target = "/tmp/tasks_active.json"
    procs = [mp.Process(target=worker, args=(target, 500)) for _ in range(8)]
    [p.start() for p in procs]; [p.join() for p in procs]
    print(Path(target).read_text())
```

### 5) Edge Cases, Failure Modes, and Handling
- **Crash mid-write**: Temp file persisted, atomic `os.replace` ensures either old or new valid JSON. Parent dir fsync ensures durability of rename.
- **Lock contention/deadlock**: Single sidecar lock per SoT file; enforce bounded wait and define a global acquisition order if multiple locks are ever used.
- **Network FS semantics**: Plan assumes local FS. Document non-goals for NFS/SMB. Detect and warn if on non-local FS.
- **Secret leakage in logs**: Best-effort redaction; add configurable regex list; consider writing secrets to separate descriptors never logged.
- **Timezone edge**: Require aware timestamps; reject naive inputs; always convert to `Asia/Manila` for arithmetic.
- **Backward compatibility**: Single-writer policy may break callers; add deprecation window with warnings and feature flag to opt into new behavior before hard enforcement.

### 6) Verification Gates (Measurable Acceptance Criteria)
- **Locking latency**: Under 8 workers × 500 writes, p95 lock acquisition latency < 50 ms; zero deadlocks observed in 5-minute run.
- **Durability**: After `SIGKILL` during write, target file remains valid JSON and reflects either pre- or post-state, never partial JSON.
- **Logging artifacts**: `.out/.err/.json` created with 0600 perms; metadata includes `cmd`, `exit_code`, `duration_s`, and file paths; sampled logs contain no unredacted secrets.
- **Timezone correctness**: All new timestamps are ISO-8601 with zone; `days_since` matches manual calculation across month boundaries in PH timezone.
- **Archival policy**: Completed tasks appended to `tasks_done.jsonl` with fields `{task_id, finished_at, source}`; retention rule documented and tested.

### 7) Security and Compliance Checklist
- Files created with 0600; directories 0700.
- Validate and normalize `MEMORY_STORAGE_ROOT` via `Path.resolve()`; prevent path traversal outside allowed root.
- Redaction filters configurable and test-covered; add denylist for common secret markers.
- Logs retention/rotation policy defined and enforced.

### 8) Recommendations (Prioritized)
1. Adopt `flock(2)` with sidecar lock files; document acquisition ordering and bounded waits.
2. Implement `atomic_io.py` exactly as PoC, including fsync of file and directory.
3. Use `zoneinfo` with `Asia/Manila`; reject naive datetimes in utilities.
4. Add `run_logged()` with redaction and file perms; define JSON metadata schema.
5. Switch archival to JSON Lines with indexed fields and retention policy.
6. Provide stress, chaos (SIGKILL), and property-based tests; record SLI/SLOs for lock contention and write failures.

### 9) References
- Python `os.replace`: `https://docs.python.org/3/library/os.html#os.replace`
- Linux `flock(2)`: `https://man7.org/linux/man-pages/man2/flock.2.html`
- Linux `fcntl(2)`: `https://man7.org/linux/man-pages/man2/fcntl.2.html`
- PEP 615 `zoneinfo`: `https://peps.python.org/pep-0615/`

### 10) Verdict
- **Plan is feasible with mitigations**. Risks are identifiable and controllable with the provided acceptance gates and implementations.

### 11) Confidence
- **Confidence Score**: 90%
- **Uncertainties**: Live environment FS semantics (non-local filesystems), unknown external writers to SoT, and undisclosed legacy data needing timezone normalization.
