## Folder: /tools

Purpose: Orchestration, analysis, and memory tooling used by the AI system.

Key scripts:
- workflow_memory_intelligence_fixed.py: Main workflow intelligence (1950 lines).
- task_command_center.py: Task command center operations.
- todo_manager.py: TODO/task management.
- analyzer.py, analysis_advanced_check.py: Analysis and validation utilities.
- cursor_session_manager.py, cursor_memory_bridge.py: Cursor session and memory bridging.
- setup_memory_mcp.py: MCP setup.
- std_mdc.py: Standardizes `.mdc` files with frontmatter.
- organize_root_python.sh: Repo organization helper.
- rule_attach_detector.py: Scans repo for stack markers and writes `rule_attach_log.json`.
- hydration_selector.py: Promotes matching `.mdc` from `.cursor/test-rules` to `.cursor/rules`.
- mdc_linter.py: Validates and auto-fixes `.mdc` frontmatter.

### Auto-Attach Pipeline (Detector → Selector → Linter)
Run from repo root:
```bash
python3 tools/rule_attach_detector.py --output rule_attach_log.json
python3 tools/hydration_selector.py --attach-log rule_attach_log.json --source .cursor/test-rules --dest .cursor/rules
python3 tools/mdc_linter.py --paths .cursor/rules .cursor/test-rules --write
```

Subfolder:
- memory/: Auxiliary memory utilities.

Integration Notes:
- Invoked by framework bridge and orchestrator for end-to-end flows.