# Lab Notes — Pipeline Slice

Goal
- Validate execution logging, archival behavior, and gate checks in the execution flow.

Setup
- Files: `todo_manager.py`, `exec_logging.py`, `archive_tasks.py`, `plan_next.py`.
- Pre-req: At least one task with a phase that has a fenced block of commands.

Steps
1) Exec preview then run (produces logs):
```bash
# Replace with actual task id and phase index K
python3 todo_manager.py exec <TASK_ID> K | cat
python3 todo_manager.py exec <TASK_ID> K --run | cat
ls -l memory-bank/logs | cat
head -n 50 memory-bank/logs/run_*.json | cat
```
2) Archival: mark a task completed then cleanup:
```bash
# After completing todos, or manually set status via set_task_status then
python3 todo_manager.py cleanup | cat
wc -l memory-bank/queue-system/tasks_done.jsonl | cat
```
3) Gate check (Deep Analysis):
```bash
python3 plan_next.py --gate --task-id memory_system_canonicalization_actionable_20250820 | cat
```

Results
- L1 (logging): EXPECT PASS — `.out/.err/.json` created with 0600 perms; redaction applied.
- L2 (archival): EXPECT PASS — completed tasks appended to JSONL; active list retains others.
- L3 (gate): EXPECT PASS/WARN — depending on analysis state.

Findings
- Logging structured and file-perms enforced; archival is append-only; gate integration is intact.

Next Logical Step
- If all PASS, flip slice to new pipeline behavior; otherwise, fix failing step before proceed.
