# Lab Notes — Router Slice

Goal
- Validate role routing and gate toggles without modifying legacy execution.

Setup
- Files: `frameworks/fwk-001-cursor-rules/system-prompt/{rules_master_toggle.mdc,execution_orchestrator.mdc}`
- Expect `enabled: true` for auditor/principal_engineer; audit/verification/synthesis gates set to true.

Steps
1) Inspect toggles:
```bash
sed -n '70,120p' frameworks/fwk-001-cursor-rules/system-prompt/rules_master_toggle.mdc | cat
sed -n '70,110p' frameworks/fwk-001-cursor-rules/system-prompt/execution_orchestrator.mdc | cat
```
2) Dry-run plan/gate:
```bash
python3 plan_next.py | cat
python3 plan_next.py --gate --task-id memory_system_canonicalization_actionable_20250820 | cat
```

Results
- routing matrix present; roles enabled; gates enabled (audit/verification/synthesis).
- plan_next.py outputs next phase and gate status.

Findings
- Router configuration is consistent; gates are set to enabled in orchestrator.

Next Logical Step
- PASS → proceed to Memory slice.
