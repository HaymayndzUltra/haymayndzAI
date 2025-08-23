# Memory Tools (Pro)

## Install
```bash
pip install -r /workspace/tools/memory/requirements.txt
```

## Config
- Edit `/workspace/tools/memory/pro_config.yaml` if needed.
- Device auto-selects GPU (cuda) if available, else CPU.

## Commands
```bash
# Save a fact/decision
python3 /workspace/tools/memory/memory_cli.py save "Payment provider: PayPal" --type fact --tags project:default payments

# Recall by text/tag (semantic if index exists, else substring)
python3 /workspace/tools/memory/memory_cli.py recall "payments" --topk 5

# Build or rebuild index (after many new entries)
python3 /workspace/tools/memory/memory_cli.py reindex

# Snapshot current state (summary/open questions/next steps)
python3 /workspace/tools/memory/memory_cli.py snapshot --summary "Week 1 wrap-up" --open "tax config" --next "connect DB" --tags always_hot
```

## Storage Layout
- Root: `/workspace/storage/memory`
  - `knowledge_base.jsonl`: append-only entries
  - `kb.index.faiss`: FAISS index (GPU/CPU)
  - `kb.meta.json`: metadata (ids, dim)
  - `decision_log.md`: human-readable decisions
  - `context_snapshot.yaml`: periodic snapshot

## Tips
- Use `--tags` to namespace (e.g., `project:cafe`, `scope:payments`).
- Run `reindex` after many new saves to speed up semantic recall.
- Rotate/backup the storage folder per your policy.