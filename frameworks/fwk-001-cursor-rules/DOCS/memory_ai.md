# memory_ai

## Purpose
Preserves and serves project knowledge and decisions across sessions.

## How It Works
- Consumes session logs, project artifacts, decision records, and knowledge updates.
- Produces `knowledge_base.json`, `decision_log.md`, and `context_snapshot.yaml`.
- Success requires durable storage with accurate indexing and retrieval.
- Single-writer policy: owns `knowledge_base.json`.

## How to Use It
- Commands:
  - `/snapshot`: create project state backup
  - `/recall <query>`: retrieve historical context
  - `/learn <insight>`: store new knowledge
- Allowed verbs: STORE, RETRIEVE, SNAPSHOT, LEARN.

## Example Usage
```bash
/snapshot
/recall "rollback strategy"
/learn "Adopt feature flags for risky changes"
```

## Dependencies
- Syncs with `framework_memory_bridge` when integrated with external memory systems.