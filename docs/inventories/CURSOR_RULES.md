## Folder: /.cursor/rules

Purpose: Cursor project rules defining multi-agent roles, orchestration, guidance, and memory integration. These `.mdc` files are read by Cursor to scope behavior.

Key files:
- execution_orchestrator.mdc: Orchestrates pipeline, gates, handoffs, and rule loading.
- rules_master_toggle.mdc: Role activation matrix and command routing.
- guidance_next_steps.mdc, guidance_phase_awareness.mdc, guidance_command_suggester.mdc: Universal guidance and phase-aware steps.
- memory_ai.mdc, framework_memory_bridge.mdc, memory_enhancement_auditor.mdc: Knowledge capture, bridging, and audit of memory rules.
- Core roles: product_owner_ai.mdc, planning_ai.mdc, codegen_ai.mdc, qa_ai.mdc, documentation_ai.mdc, security_ai.mdc, mlops_ai.mdc, observability_ai.mdc, analyst_ai.mdc, principal_engineer_ai.mdc, planner_moderator_ai.mdc, prompt_factory_ai.mdc, prompt_linter_ai.mdc, data_ai.mdc.

Notes:
- All files standardized with frontmatter (description, globs, alwaysApply).
- Intended to be universal; framework specifics live under `/.cursor/frameworks` and `/.cursor/test`.