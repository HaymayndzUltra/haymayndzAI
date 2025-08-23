# Migration Playbook — Strangler Pattern Workflow

Protocol:
1. Test slices one-by-one (router, memory, core pipeline, etc.).
2. Use Lab Notes format for each slice: Goal, Setup, Steps, Results, Findings, Next Logical Step.
3. Do not proceed to next slice unless current slice is PASS.
4. Flip traffic to the new code for a slice only when stable.
5. Legacy modules remain; deprecate only after migration completion.

## Slices
- Router: roles/commands routing (`rules_master_toggle.mdc`, `execution_orchestrator.mdc`).
- Memory: atomic IO, recall fallback, snapshot/sync (`atomic_io.py`, `tools/memory/memory_cli.py`, `cursor_memory_bridge.py`).
- Pipeline: exec logging, archival, gates (`todo_manager.py`, `exec_logging.py`, `archive_tasks.py`).

## Lab Notes Index
- See `labnotes/router.md`
- See `labnotes/memory.md`
- See `labnotes/pipeline.md`