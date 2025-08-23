## Memory Enhancement Plan (v1.0)

### Prioritized Enhancements
- **E-001: Normalize storage root and remove hardcoded paths**
  - **Why**: `tools/memory/pro_config.yaml` and `tools/memory/README.md` use absolute paths, hurting portability and violating env-first practice. Evidence: `storage.root` is absolute; README commands include absolute prefixes.
  - **Proposal**: Default `storage.root` to `memory-bank/storage/memory` (repo-local). Respect `MEMORY_STORAGE_ROOT` with `Path.resolve()`. Update docs and `framework_memory_bridge.mdc` command mappings to repo-relative forms. Add guard to disallow traversal outside allowed root when override is used.
  - **Acceptance**: Grep shows no hardcoded `/home/...` paths in config/docs. `echo $MEMORY_STORAGE_ROOT` drives all CLI operations. `Path.resolve()` applied and path stays under repo root.
  - **Risk**: Low (doc/config changes). Mitigation: environment override keeps backwards compatibility.
  - **Effort**: S

- **E-002: Enforce single-writer policy for `current-session.md`**
  - **Why**: `cursor_memory_bridge.py` is the canonical writer, but `memory_system/cli.py save` appends directly to the same file, risking drift under concurrency or future refactors.
  - **Proposal**: Keep bridge as sole snapshot writer. Move ad-hoc notes to `memory-bank/memory-notes.md` or provide `cursor_memory_bridge.append_note(...)` API that performs an append-only section, then triggers `dump_markdown()` for a fresh snapshot. Remove direct file writes elsewhere.
  - **Acceptance**: Grep shows only bridge writes to `current-session.md`. Notes go to `memory-notes.md` or via the new bridge API. Manual run of `cursor_memory_bridge.py --dump` always regenerates a consistent snapshot.
  - **Risk**: Medium (compat). Mitigation: keep a transitional mode where `memory_system/cli.py save` calls the new API.
  - **Effort**: M

- **E-003: Make all JSON updates atomic with sidecar locks**
  - **Why**: Some writers are non-atomic or missing locks. `archive_tasks.py` writes `tasks_active.json` without `atomic_write_json`; JSONL append operations (`tasks_done.jsonl`, KB JSONL) lack file locks.
  - **Proposal**: Use `with_json_lock + atomic_write_json` for JSON files and `with_file_lock(<path>.lock)` for JSONL appenders (both the source and the target). Add `atomic_io.append_jsonl_locked(path, obj)` that: acquires `<path>.lock`, opens in append binary, writes one line, flushes, fsyncs file and parent dir.
  - **Acceptance**: Multi-process stress (labnotes T1) passes repeatedly. No truncated JSON; no interleaved JSONL lines under 16-process concurrency.
  - **Risk**: Low. Mitigation: best-effort fsync; warn about network FS semantics.
  - **Effort**: M

- **E-004: Retrieval fallback behavior and clarity**
  - **Why**: Fallback search should not require embeddings/FAISS. Current behavior is correct; ensure it remains explicit and tested.
  - **Proposal**: Keep case-insensitive substring/tag fallback when index/model unavailable; add `--mode semantic|fallback|auto` flag to `recall` to force mode. Document complexity/case handling.
  - **Acceptance**: `save` then `recall` without embeddings prints JSON lines (as validated below). For `--mode semantic`, gracefully error if model/index missing.
  - **Risk**: Low.
  - **Effort**: S

- **E-005: Indexing lifecycle (batching + threshold switch)**
  - **Why**: `reindex` loads all entries at once; `batch_size` from config unused; `flatip_threshold` not enforced.
  - **Proposal**: Stream/batch encode and add vectors; enforce `flatip_threshold` to switch from `IndexFlatIP` to IVF/PQ; persist meta with id mapping. Add progress logging and elapsed timing.
  - **Acceptance**: On large KB, memory usage stays bounded; index build time and RPS reported; meta reflects chosen backend.
  - **Risk**: Medium. Mitigation: keep FlatIP default for small corpora; add `--force-flat`.
  - **Effort**: M

- **E-006: Rotation/archival policy for LTM (KB JSONL)**
  - **Why**: Config contains `rotation.ltm_max_mb`/`ltm_hot_days` but code does not rotate JSONL.
  - **Proposal**: On `save`, if KB exceeds size, rotate to timestamped `knowledge_base.YYYYMMDD.jsonl` (optionally gzip). Provide `recall` filter by hot window. Keep append-only semantics.
  - **Acceptance**: After synthetic growth, rotation triggers and new KB is created; recall still finds recent items; archival files preserved.
  - **Risk**: Low.
  - **Effort**: M

- **E-007: Redaction and logging hygiene**
  - **Why**: `exec_logging` redacts common patterns but coverage is narrow; outputs are not fsync'ed; some flows print raw content.
  - **Proposal**: Expand denylist (JWT, OAuth codes, email-like, private keys), support pluggable custom patterns, and fsync `.out/.err/.json`. Add `--redact` flag to `memory_cli recall` (default on) to sanitize printed text fields.
  - **Acceptance**: Sample runs show redacted outputs; file perms 0600 and dirs 0700; files durably persisted.
  - **Risk**: Low.
  - **Effort**: S

- **E-008: Observability & status reporting**
  - **Why**: Limited at-a-glance visibility.
  - **Proposal**: Add `memory_cli.py status` subcommand: show KB lines, last index ts/dim/backend, index file sizes, device used, recent snapshot tags. Emit structured JSON with `--json`.
  - **Acceptance**: Status prints expected fields and exits 0; `--json` produces valid JSON.
  - **Risk**: Low.
  - **Effort**: S

- **E-009: Device selection hardening**
  - **Why**: Handle faiss-cpu gracefully; avoid calling GPU APIs when gpu bindings absent.
  - **Proposal**: Feature-detect `faiss.get_num_gpus` via `hasattr`; prefer env `CUDA_VISIBLE_DEVICES`; log chosen device.
  - **Acceptance**: `reindex` works on CPU-only systems; no exception for missing GPU.
  - **Risk**: Low.
  - **Effort**: S

- **E-010: Safety rails for env/config**
  - **Why**: Prevent path traversal and cross-repo writes when `MEMORY_STORAGE_ROOT` is set.
  - **Proposal**: Validate that resolved root is within repo root (or an allowlist); refuse dangerous overrides with clear error; document policy.
  - **Acceptance**: Invalid overrides are rejected with actionable message.
  - **Risk**: Low.
  - **Effort**: S

### Risk Register
- **R-001 (HIGH)**: Competing writers for `current-session.md` may corrupt or drift snapshot under race.
  - **Mitigation**: E-002; bridge-only snapshot; notes via separate file or API.
- **R-002 (MEDIUM)**: Hardcoded absolute paths hinder portability and CI usage.
  - **Mitigation**: E-001; env-first, repo-relative defaults, docs cleanup.
- **R-003 (MEDIUM)**: JSON/JSONL races may interleave or truncate data.
  - **Mitigation**: E-003; locks for JSONL append; atomic JSON writes everywhere.
- **R-004 (LOW)**: Missing embeddings/FAISS breaks semantic path.
  - **Mitigation**: E-004; fallback mode and explicit `--mode`.
- **R-005 (MEDIUM)**: Logs may capture secrets; no rotation.
  - **Mitigation**: E-007; expand redaction; retention/rotation.
- **R-006 (LOW)**: GPU feature detection brittle across faiss builds.
  - **Mitigation**: E-009.
- **R-007 (LOW)**: Oversized KB slows recall.
  - **Mitigation**: E-006 rotation and hot-window filters.

### Compatibility Notes (Zero-Downtime)
- **Step 1**: Set `MEMORY_STORAGE_ROOT="$PWD/memory-bank/storage/memory"` in shells/CI. Keep current config until rollout completes.
- **Step 2**: Update `pro_config.yaml` default root to repo-local; do not remove env override. Commit docs using relative paths.
- **Step 3**: Replace direct writes to `current-session.md` with bridge API. For `memory_system/cli.py save`, switch to `memory-notes.md` or call `append_note()`.
- **Step 4**: Introduce `append_jsonl_locked` and refactor writers (`archive_tasks.py`, `memory_cli.append_jsonl`).
- **Step 5**: Deploy rotation for KB and logs. No data loss—old files remain readable.

### Validation Plan
- **Setup (portable root)**
```bash
export MEMORY_STORAGE_ROOT="$PWD/memory-bank/storage/memory"
```
- **V1: Fallback recall (no embeddings/index)**
```bash
python3 tools/memory/memory_cli.py save "audit: fallback recall ok" --tags audit demo
python3 tools/memory/memory_cli.py recall "audit" --topk 3 | cat
# Expect: JSON line(s) with the saved entry; no model/index required
```
- **V2: Snapshot via bridge**
```bash
python3 cursor_memory_bridge.py --dump | cat
# Expect: file updated at memory-bank/current-session.md
```
- **V3: Semantic index (optional; requires sentence-transformers + faiss)**
```bash
python3 -m pip install --break-system-packages sentence-transformers faiss-cpu  # or faiss-gpu on CUDA hosts
python3 tools/memory/memory_cli.py reindex
python3 tools/memory/memory_cli.py recall "audit" --topk 3 | cat
# Expect: semantic results; meta/index files present
```
- **V4: Concurrency write test (tasks_active.json)**
```bash
python3 - <<'PY'
import json, os, multiprocessing as mp, time
from atomic_io import safe_update_json
PATH = 'memory-bank/queue-system/tasks_active.json'
os.makedirs('memory-bank/queue-system', exist_ok=True)
if not os.path.exists(PATH):
    open(PATH,'w').write('[]')

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
print('ok', len(ids) >= 16)
PY
# Expect: ok True
```
- **V5: Log redaction**
```bash
python3 - <<'PY'
from exec_logging import run_logged
code, meta = run_logged('printf "AWS_SECRET_KEY=foo\nBearer abc.def.ghi\n"')
print(code, meta['stdout'])
PY
# Expect: redacted output; files 0600
```

### Decision Gate
- **PASS**: V1 and V2 are green; E-001 and E-003 implemented; no more direct writes to `current-session.md` detected by grep; optional V3 passes when deps installed.
- **FAIL**: Any data corruption under concurrency, missing portability override, or competing writers remain.

IMPORTANT NOTE: The bridge is the source of truth for the session snapshot. Treat the JSON files as SoT for automations and the markdown only as a human-readable view. Always prefer repo-local roots with env overrides for portability, and never silently purge—archive or rotate instead.