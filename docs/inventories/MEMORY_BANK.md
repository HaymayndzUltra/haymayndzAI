## Folder: /memory-bank

Purpose: Centralized store for session state, plans, project brain, queues, and persisted knowledge.

Top files:
- current-session.md: Active session notes.
- cursor_state.json: Cursor framework session state snapshot.
- task_state.json, task_interruption_state.json: Execution state.

Subfolders:
- architecture-plans/: Plans, prompts, and implementation artifacts.
- plan/: Planning materials.
- project-brain/: Core project context and documentation.
- queue-system/: Task queues and orchestration state.
- storage/: Backing store for memory-bank data.

Integration Notes:
- Read by `framework_memory_bridge.mdc` to align frameworks with existing memory and tasks.
- Used alongside `/storage/memory` KB for retrieval and learning signals.