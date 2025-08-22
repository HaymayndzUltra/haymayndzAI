# framework_memory_bridge

## Purpose
Bridges the fwk-001 role-based framework with an existing memory-bank system while preserving current workflows.

## How It Works
- Maps framework triggers to commands in the existing system (e.g., `/gen_code` → `python3 workflow_memory_intelligence_fixed.py execute`).
- Synchronizes state bidirectionally via defined sync rules (framework todos → `tasks_active.json`, role outputs → `project-brain/`, logs → `logs/`; and memory state back into role contexts).
- Conflict resolution favors the existing system while allowing framework enhancements.
- Interaction verbs: BRIDGE, SYNC, HYBRID, CONTEXT.

## How to Use It
- Commands:
  - `/bridge_sync`: synchronize framework with the memory system
  - `/hybrid_execute <command>`: run using both systems where beneficial
  - `/memory_context`: load existing context into framework roles

## Example Usage
```bash
/bridge_sync
/hybrid_execute /gen_code
/memory_context
```

## Dependencies
- Integrates with existing CLI and files:
  - `tasks_active.json`, `cursor_state.json`, `current-session.md`
  - `workflow_memory_intelligence_fixed.py`, `todo_manager.py`, `task_command_center.py`