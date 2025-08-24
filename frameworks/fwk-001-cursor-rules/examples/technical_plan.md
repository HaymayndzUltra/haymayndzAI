## Technical Plan — Governance/Config Artifacts Integration

### 1) Goals and Non‑Goals
- Goals:
  - Establish uniform artifact metadata schema (ids, versions, status) for all framework artifacts.
  - Add deterministic artifact routing distinct from command routing with conflict detection.
  - Implement a crash‑safe, single‑writer `artifacts_index.json` with atomic writes and journaled recovery.
  - Define deterministic hydration precedence with explicit tie‑breakers.
  - Enforce per‑framework contract for allowed artifacts and gate checks.
  - Govern promotions with signed snapshots, retention, and rollback triggers.
- Non‑Goals (Phase‑1): Cross‑repo rollouts; org‑wide tooling standardization beyond fwk‑001.

### 2) Architecture Overview
- Components:
  - Schema Validator: validates artifact frontmatter/sidecar against schema.
  - Artifact Router: resolves artifact → canonical path via routing map; detects conflicts vs `routing_matrix.json` (command routing).
  - Index Writer: maintains `artifacts_index.json` with lockfile + temp file + fsync + atomic rename; journal for recovery.
  - Hydration Engine: selects inputs based on precedence (approved > latest non‑draft > solo) with deterministic tie‑breakers.
  - Framework Contract Enforcer: validates allowed artifact set and required states per framework.
  - Promotion Manager: creates signed snapshots; enforces retention and rollback playbooks.

### 3) Data Schemas
- Frontmatter (YAML/JSON sidecar) minimal schema (excerpt):
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "FrameworkArtifact",
  "type": "object",
  "required": ["id", "version", "status", "framework", "kind"],
  "properties": {
    "id": {"type": "string", "pattern": "^[A-Za-z0-9_.-]+$"},
    "version": {"type": "string"},
    "status": {"type": "string", "enum": ["draft", "review", "approved"]},
    "framework": {"type": "string"},
    "kind": {"type": "string"},
    "checksum": {"type": "string"},
    "created_at": {"type": "string", "format": "date-time"},
    "updated_at": {"type": "string", "format": "date-time"}
  }
}
```

### 4) Algorithms (Executable PoC snippets)
- Atomic, single‑writer JSON index with fsync + rename:
```python
import json, os, tempfile, fcntl

def write_atomic_json(path: str, data: dict) -> None:
    directory = os.path.dirname(path) or "."
    lock_path = path + ".lock"
    # Acquire exclusive lock
    with open(lock_path, "w") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        # Write to temp file in same dir
        fd, tmp = tempfile.mkstemp(prefix=".idx.", dir=directory)
        try:
            with os.fdopen(fd, "w") as f:
                json.dump(data, f, separators=(",", ":"), sort_keys=True)
                f.flush(); os.fsync(f.fileno())
            # Durability of directory entry before rename
            dir_fd = os.open(directory, os.O_DIRECTORY)
            try:
                os.replace(tmp, path)
                os.fsync(dir_fd)
            finally:
                os.close(dir_fd)
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)
```

- Deterministic hydration selection with explicit tie‑breakers:
```python
from typing import List, Dict

def select_inputs(candidates: List[Dict]) -> Dict:
    # candidates: [{status, commit_time, path, approved(bool)}]
    ranked = sorted(
        candidates,
        key=lambda c: (
            0 if c.get("status") == "approved" else 1,
            0 if c.get("status") == "review" else 1,
            0 if c.get("status") == "draft" else 1,
            -int(c.get("commit_time", 0)),  # newer first
            c.get("path", "")
        )
    )
    return ranked[0] if ranked else {}
```

### 5) Interfaces
- Artifact routing map: `artifact_routing.mdc` (artifact kinds → canonical dirs); validation detects drift vs `routing_matrix.json`.
- Index API (Python/CLI): `index add|update|rebuild|verify` uses `write_atomic_json` and emits checksums.
- Hydration API: `hydrate --framework <fwk> --stage <gate> --deterministic` returns chosen inputs and audit log of decisions.

### 6) Rollout & Phasing
- Phase 0: Owners/estimates/acceptance (aligns to T‑12).
- Phase 1: Schema + Routing (T‑01, T‑02).
- Phase 2: Index + Hydration (T‑03, T‑04).
- Phase 3: Contract + Promotion (T‑05, T‑06).
- Phase 4: Migration + Tests + Security (T‑07, T‑08, T‑09).
- Phase 5: Hardening + Observability (T‑10, T‑11).

### 7) Risks & Mitigations (selected)
- Integrity/Concurrency (R‑002): lock + fsync + rename + recovery journal; simulate crashes in CI.
- Non‑determinism (R‑004): explicit tie‑breakers; CI check that repeated runs select identical inputs.
- Routing Drift (R‑003): diff artifact routing vs command routing; block on conflicts.
- Governance gaps (R‑006): enforce RACI and acceptance in gate checks.

### 8) Acceptance Criteria
- Rebuilding index after simulated crash yields identical `artifacts_index.json`.
- Hydration produces identical outputs across 3+ runs given same inputs.
- All artifact files validate against schema; routing has 0 conflicts.
- Snapshots are signed and verifiable; rollback playbooks pass rehearsal.

References: Action_Plan L1–L6; Summary_Report R‑001..R‑006, B‑001..B‑005; Validation_Report (CONFIRM R‑001..R‑006)


