## Folder: /storage/memory

Purpose: Persisted AI memory store and vector index for project knowledge.

Files:
- context_snapshot.yaml: Recent context snapshot metadata.
- knowledge_base.jsonl: Append-only knowledge entries.
- kb.index.faiss: FAISS vector index for retrieval.
- kb.meta.json: Index metadata.

Integration Notes:
- Produced/consumed by `/memory_system` and referenced by `memory_ai.mdc`.
- Bridge syncs patterns and attach logs for observability and recall.