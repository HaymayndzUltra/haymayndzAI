import json, os, tempfile, fcntl, time
from typing import Dict, Any, List

INDEX_PATH = os.path.join(os.path.dirname(__file__), "artifacts_index.json")

def _atomic_replace_file(target_path: str, content_str: str) -> None:
    directory = os.path.dirname(target_path) or "."
    fd, tmp = tempfile.mkstemp(prefix=".idx.", dir=directory)
    try:
        with os.fdopen(fd, "w") as f:
            f.write(content_str)
            f.flush(); os.fsync(f.fileno())
        dir_fd = os.open(directory, os.O_DIRECTORY)
        try:
            os.replace(tmp, target_path)
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)

def recover_index(path: str = INDEX_PATH) -> bool:
    """Recover from journal if present. Returns True if recovery happened."""
    lock_path = path + ".lock"
    journal_path = path + ".journal"
    if not os.path.exists(journal_path) or os.path.getsize(journal_path) == 0:
        return False
    with open(lock_path, "w") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        data = open(journal_path, "r", encoding="utf-8").read()
        _atomic_replace_file(path, data)
        try:
            os.unlink(journal_path)
        except FileNotFoundError:
            pass
    return True

def write_atomic_json(path: str, data: Dict[str, Any]) -> None:
    """Write with single-writer lock, journal, and atomic replace."""
    directory = os.path.dirname(path) or "."
    lock_path = path + ".lock"
    journal_path = path + ".journal"
    with open(lock_path, "w") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        # Write journal (intent) first
        with open(journal_path, "w", encoding="utf-8") as jf:
            json.dump(data, jf, separators=(",", ":"), sort_keys=True)
            jf.flush(); os.fsync(jf.fileno())
        # Commit to index atomically
        content_str = json.dumps(data, separators=(",", ":"), sort_keys=True)
        _atomic_replace_file(path, content_str)
        # Remove journal to mark commit complete
        try:
            os.unlink(journal_path)
        except FileNotFoundError:
            pass

def load_index(path: str = INDEX_PATH) -> Dict[str, Any]:
    if not os.path.exists(path):
        return {"version": 1, "artifacts": []}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def upsert_entry(entry: Dict[str, Any], path: str = INDEX_PATH) -> None:
    idx = load_index(path)
    artifacts: List[Dict[str, Any]] = idx.get("artifacts", [])
    artifacts = [a for a in artifacts if not (a.get("id") == entry.get("id") and a.get("version") == entry.get("version"))]
    entry = {**entry, "updatedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    artifacts.append(entry)
    idx["artifacts"] = artifacts
    write_atomic_json(path, idx)

if __name__ == "__main__":
    # Attempt recovery if needed
    recovered = recover_index(INDEX_PATH)
    if recovered:
        print("Recovered index from journal.")
    # Seed with example artifacts from sidecars
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "examples"))
    names = [
        "Action_Plan.md.sidecar.json",
        "Summary_Report.md.sidecar.json",
        "Validation_Report.md.sidecar.json",
        "Final_Implementation_Plan.md.sidecar.json",
    ]
    for n in names:
        p = os.path.join(base, n)
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                upsert_entry(json.load(f))
    print(f"Index written to {INDEX_PATH}")


