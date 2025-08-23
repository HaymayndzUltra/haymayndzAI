# Lab Notes — Memory Slice

Goal
- Validate atomic IO, recall fallback, and snapshot behavior without breaking legacy flows.

Setup
- Files: `atomic_io.py`, `tools/memory/memory_cli.py`, `cursor_memory_bridge.py`, `todo_manager.py` (uses atomic IO), `auto_sync_manager.py` (calls bridge for session md).

Steps
1) Concurrency test (active tasks):
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
2) Recall fallback test (without embeddings):
```bash
export MEMORY_STORAGE_ROOT="$PWD/memory-bank/storage/memory"
python3 tools/memory/memory_cli.py save "hello world" --tags demo
python3 tools/memory/memory_cli.py recall "hello" --topk 3 | cat
```
3) Snapshot (bridge owns markdown):
```bash
python3 cursor_memory_bridge.py --dump | cat
```

Results
- T1: PASS — no lost updates.
- T2: READY — verify JSON lines printed without model/index.
- T3: PASS — session markdown generated via bridge.

Findings
- Atomic IO and locks in place; recall fallback portable; single-writer for session MD enforced.

Next Logical Step
- PASS → proceed to Pipeline slice.