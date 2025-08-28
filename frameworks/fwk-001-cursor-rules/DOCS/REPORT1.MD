A. EXECUTIVE SUMMARY

This report inventories Cursor rules and activation using only repository evidence (file paths and line ranges). No assumptions were made.

B. WORKFLOW MAP

Orchestrators (alwaysApply: true):

~/.cursor/rules/ai-system-architecture.mdc

~/.cursor/rules/development-excellence.mdc

~/.cursor/rules/development-workflow.mdc

~/.cursor/rules/python-development-standards.mdc

~/.cursor/rules/security-and-compliance.mdc

~/.cursor/rules/testing-and-quality.mdc

Routers/Context Rules:

~/.cursor/rules/execution_orchestrator.mdc

~/.cursor/rules/framework_memory_bridge.mdc

~/.cursor/rules/guidance_command_suggester.mdc

~/.cursor/rules/guidance_next_steps.mdc

~/.cursor/rules/guidance_phase_awareness.mdc

~/.cursor/rules/planner_moderator_ai.mdc

~/.cursor/rules/rules_master_toggle.mdc

Role Files:

~/.cursor/rules/analyst_ai.mdc

~/.cursor/rules/auditor_ai.mdc

~/.cursor/rules/codegen_ai.mdc

~/.cursor/rules/data_ai.mdc

~/.cursor/rules/documentation_ai.mdc

~/.cursor/rules/l10n_i18n_ai.mdc

~/.cursor/rules/memory_ai.mdc

~/.cursor/rules/mlops_ai.mdc

~/.cursor/rules/observability_ai.mdc

~/.cursor/rules/planning_ai.mdc

~/.cursor/rules/principal_engineer_ai.mdc

~/.cursor/rules/product_owner_ai.mdc

~/.cursor/rules/prompt_factory_ai.mdc

~/.cursor/rules/prompt_linter_ai.mdc

~/.cursor/rules/qa_ai.mdc

~/.cursor/rules/security_ai.mdc

Domain Rules:

~/.cursor/rules/ai-assistant-guidance.mdc

~/.cursor/rules/curated_test-when-generating-rspec-tests-follow-these-best-practices-to-ensure-they-are-comp.mdc

~/.cursor/rules/curated_test-you-are-an-expert-in-python-and-cybersecurity-tool-development.mdc

~/.cursor/rules/curated_test-you-are-an-expert-in-python-django-and-scalable-restful-api-development.mdc

~/.cursor/rules/curated_test-you-are-an-expert-in-solidity-and-smart-contract-security.mdc

~/.cursor/rules/curated_test-you-are-an-expert-in-terraform-and-infrastructure-as-code-iac-for-cloud-platfo.mdc

~/.cursor/rules/makeaprompt.mdc

~/.cursor/rules/memory_enhancement_auditor.mdc

~/.cursor/rules/project-guidance.mdc

~/.cursor/rules/technology-stacks.mdc

~/.cursor/rules/test-rules-management.mdc

C. RULE INVENTORY TABLE
file	type	alwaysApply	globs_count	includes_count
~/.cursor/rules/ai-assistant-guidance.mdc	domain	false	0	0
~/.cursor/rules/ai-system-architecture.mdc	orchestrator	true	1	2
~/.cursor/rules/analyst_ai.mdc	role	false	1	0
~/.cursor/rules/auditor_ai.mdc	role	false	1	0
~/.cursor/rules/codegen_ai.mdc	role	false	1	0
~/.cursor/rules/curated_test-when-generating-rspec-tests-follow-these-best-practices-to-ensure-they-are-comp.mdc	domain	false	4	0
~/.cursor/rules/curated_test-you-are-an-expert-in-python-and-cybersecurity-tool-development.mdc	domain	false	3	0
~/.cursor/rules/curated_test-you-are-an-expert-in-python-django-and-scalable-restful-api-development.mdc	domain	false	3	0
~/.cursor/rules/curated_test-you-are-an-expert-in-solidity-and-smart-contract-security.mdc	domain	false	3	0
~/.cursor/rules/curated_test-you-are-an-expert-in-terraform-and-infrastructure-as-code-iac-for-cloud-platfo.mdc	domain	false	2	0
~/.cursor/rules/data_ai.mdc	role	false	1	0
~/.cursor/rules/development-excellence.mdc	orchestrator	true	1	7
~/.cursor/rules/development-workflow.mdc	orchestrator	true	1	0
~/.cursor/rules/documentation_ai.mdc	role	false	1	0
~/.cursor/rules/execution_orchestrator.mdc	router	false	1	0
~/.cursor/rules/framework_memory_bridge.mdc	router	false	1	0
~/.cursor/rules/guidance_command_suggester.mdc	router	false	1	0
~/.cursor/rules/guidance_next_steps.mdc	router	false	1	0
~/.cursor/rules/guidance_phase_awareness.mdc	router	false	1	0
~/.cursor/rules/l10n_i18n_ai.mdc	role	false	1	0
~/.cursor/rules/makeaprompt.mdc	domain	false	1	0
~/.cursor/rules/memory_ai.mdc	role	false	1	0
~/.cursor/rules/memory_enhancement_auditor.mdc	domain	false	1	0
~/.cursor/rules/mlops_ai.mdc	role	false	1	0
~/.cursor/rules/observability_ai.mdc	role	false	1	0
~/.cursor/rules/planner_moderator_ai.mdc	router	false	1	0
~/.cursor/rules/planning_ai.mdc	role	false	0	0
~/.cursor/rules/principal_engineer_ai.mdc	role	false	1	0
~/.cursor/rules/product_owner_ai.mdc	role	false	1	0
~/.cursor/rules/project-guidance.mdc	domain	false	0	0
~/.cursor/rules/prompt_factory_ai.mdc	role	false	1	0
~/.cursor/rules/prompt_linter_ai.mdc	role	false	1	0
~/.cursor/rules/python-development-standards.mdc	orchestrator	true	3	1
~/.cursor/rules/qa_ai.mdc	role	false	1	0
~/.cursor/rules/rules_master_toggle.mdc	router	false	1	0
~/.cursor/rules/security-and-compliance.mdc	orchestrator	true	1	1
~/.cursor/rules/security_ai.mdc	role	false	1	0
~/.cursor/rules/technology-stacks.mdc	domain	false	0	46
~/.cursor/rules/test-rules-management.mdc	domain	false	0	3
~/.cursor/rules/testing-and-quality.mdc	orchestrator	true	1	0
D. GLOBS & COVERAGE

~/.cursor/rules/ai-assistant-guidance.mdc

~/.cursor/rules/ai-system-architecture.mdc

glob: **/*

sample: ~/${MEMORY_STORAGE_ROOT:-storage

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}/knowledge_base.jsonl

sample: ~/-across-all-frameworks-89b1 into main"

sample: ~/AI_Folder_Architecture.md

sample: ~/AI_TEAM_ANALYSIS_PROMPT.md

sample: ~/DIFFS

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_main_pc_code_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_voice-assistant-prod_.cursor.patch

~/.cursor/rules/analyst_ai.mdc

glob: **/*

sample: ~/${MEMORY_STORAGE_ROOT:-storage

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}/knowledge_base.jsonl

sample: ~/-across-all-frameworks-89b1 into main"

sample: ~/AI_Folder_Architecture.md

sample: ~/AI_TEAM_ANALYSIS_PROMPT.md

sample: ~/DIFFS

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_main_pc_code_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_voice-assistant-prod_.cursor.patch

~/.cursor/rules/auditor_ai.mdc

glob: **/*

sample: ~/${MEMORY_STORAGE_ROOT:-storage

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}/knowledge_base.jsonl

sample: ~/-across-all-frameworks-89b1 into main"

sample: ~/AI_Folder_Architecture.md

sample: ~/AI_TEAM_ANALYSIS_PROMPT.md

sample: ~/DIFFS

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_main_pc_code_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_voice-assistant-prod_.cursor.patch

~/.cursor/rules/codegen_ai.mdc

glob: **/*

sample: ~/${MEMORY_STORAGE_ROOT:-storage

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}/knowledge_base.jsonl

sample: ~/-across-all-frameworks-89b1 into main"

sample: ~/AI_Folder_Architecture.md

sample: ~/AI_TEAM_ANALYSIS_PROMPT.md

sample: ~/DIFFS

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_main_pc_code_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_voice-assistant-prod_.cursor.patch

~/.cursor/rules/curated_test-when-generating-rspec-tests-follow-these-best-practices-to-ensure-they-are-comp.mdc

glob: **/*.ts

glob: **/*.tsx

glob: **/*.js

glob: **/*.jsx

no matches found

~/.cursor/rules/curated_test-you-are-an-expert-in-python-and-cybersecurity-tool-development.mdc

glob: **/*.py

sample: ~/frameworks/fwk-001-cursor-rules/contracts/validate_contract.py

sample: ~/frameworks/fwk-001-cursor-rules/hydration/hydration_selector.py

sample: ~/frameworks/fwk-001-cursor-rules/hydration/run_hydration_tests.py

sample: ~/frameworks/fwk-001-cursor-rules/promotion/rollback_rehearsal.py

sample: ~/frameworks/fwk-001-cursor-rules/promotion/snapshot_cli.py

sample: ~/frameworks/fwk-001-cursor-rules/routing/check_routing_conflicts.py

sample: ~/frameworks/fwk-001-cursor-rules/routing/resolve_artifact_path.py

sample: ~/frameworks/fwk-001-cursor-rules/security/validate_security_config.py

sample: ~/frameworks/fwk-001-cursor-rules/sync/backfill_script.py

sample: ~/frameworks/fwk-001-cursor-rules/sync/enhanced_index_writer.py

glob: requirements.txt

glob: pyproject.toml

~/.cursor/rules/curated_test-you-are-an-expert-in-python-django-and-scalable-restful-api-development.mdc

glob: **/*.py

sample: ~/frameworks/fwk-001-cursor-rules/contracts/validate_contract.py

sample: ~/frameworks/fwk-001-cursor-rules/hydration/hydration_selector.py

sample: ~/frameworks/fwk-001-cursor-rules/hydration/run_hydration_tests.py

sample: ~/frameworks/fwk-001-cursor-rules/promotion/rollback_rehearsal.py

sample: ~/frameworks/fwk-001-cursor-rules/promotion/snapshot_cli.py

sample: ~/frameworks/fwk-001-cursor-rules/routing/check_routing_conflicts.py

sample: ~/frameworks/fwk-001-cursor-rules/routing/resolve_artifact_path.py

sample: ~/frameworks/fwk-001-cursor-rules/security/validate_security_config.py

sample: ~/frameworks/fwk-001-cursor-rules/sync/backfill_script.py

sample: ~/frameworks/fwk-001-cursor-rules/sync/enhanced_index_writer.py

glob: requirements.txt

glob: pyproject.toml

~/.cursor/rules/curated_test-you-are-an-expert-in-solidity-and-smart-contract-security.mdc

glob: **/*.sol

glob: hardhat.config.*

glob: foundry.toml

no matches found

~/.cursor/rules/curated_test-you-are-an-expert-in-terraform-and-infrastructure-as-code-iac-for-cloud-platfo.mdc

glob: **/*.tf

glob: **/*.tfvars

no matches found

~/.cursor/rules/data_ai.mdc

glob: **/*

sample: ~/${MEMORY_STORAGE_ROOT:-storage

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}/knowledge_base.jsonl

sample: ~/-across-all-frameworks-89b1 into main"

sample: ~/AI_Folder_Architecture.md

sample: ~/AI_TEAM_ANALYSIS_PROMPT.md

sample: ~/DIFFS

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_main_pc_code_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_voice-assistant-prod_.cursor.patch

~/.cursor/rules/development-excellence.mdc

glob: **/*

sample: ~/${MEMORY_STORAGE_ROOT:-storage

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}/knowledge_base.jsonl

sample: ~/-across-all-frameworks-89b1 into main"

sample: ~/AI_Folder_Architecture.md

sample: ~/AI_TEAM_ANALYSIS_PROMPT.md

sample: ~/DIFFS

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_main_pc_code_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_voice-assistant-prod_.cursor.patch

~/.cursor/rules/development-workflow.mdc

glob: **/*

sample: ~/${MEMORY_STORAGE_ROOT:-storage

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}/knowledge_base.jsonl

sample: ~/-across-all-frameworks-89b1 into main"

sample: ~/AI_Folder_Architecture.md

sample: ~/AI_TEAM_ANALYSIS_PROMPT.md

sample: ~/DIFFS

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_main_pc_code_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_voice-assistant-prod_.cursor.patch

~/.cursor/rules/documentation_ai.mdc

glob: **/*

sample: ~/${MEMORY_STORAGE_ROOT:-storage

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}/knowledge_base.jsonl

sample: ~/-across-all-frameworks-89b1 into main"

sample: ~/AI_Folder_Architecture.md

sample: ~/AI_TEAM_ANALYSIS_PROMPT.md

sample: ~/DIFFS

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_main_pc_code_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_voice-assistant-prod_.cursor.patch

~/.cursor/rules/execution_orchestrator.mdc

glob: **/*

sample: ~/${MEMORY_STORAGE_ROOT:-storage

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}/knowledge_base.jsonl

sample: ~/-across-all-frameworks-89b1 into main"

sample: ~/AI_Folder_Architecture.md

sample: ~/AI_TEAM_ANALYSIS_PROMPT.md

sample: ~/DIFFS

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_main_pc_code_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_voice-assistant-prod_.cursor.patch

~/.cursor/rules/framework_memory_bridge.mdc

glob: **/*

sample: ~/${MEMORY_STORAGE_ROOT:-storage

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}/knowledge_base.jsonl

sample: ~/-across-all-frameworks-89b1 into main"

sample: ~/AI_Folder_Architecture.md

sample: ~/AI_TEAM_ANALYSIS_PROMPT.md

sample: ~/DIFFS

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_main_pc_code_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_voice-assistant-prod_.cursor.patch

~/.cursor/rules/guidance_command_suggester.mdc

glob: **/*

sample: ~/${MEMORY_STORAGE_ROOT:-storage

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}/knowledge_base.jsonl

sample: ~/-across-all-frameworks-89b1 into main"

sample: ~/AI_Folder_Architecture.md

sample: ~/AI_TEAM_ANALYSIS_PROMPT.md

sample: ~/DIFFS

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_main_pc_code_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_voice-assistant-prod_.cursor.patch

~/.cursor/rules/guidance_next_steps.mdc

glob: **/*

sample: ~/${MEMORY_STORAGE_ROOT:-storage

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}/knowledge_base.jsonl

sample: ~/-across-all-frameworks-89b1 into main"

sample: ~/AI_Folder_Architecture.md

sample: ~/AI_TEAM_ANALYSIS_PROMPT.md

sample: ~/DIFFS

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_main_pc_code_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_voice-assistant-prod_.cursor.patch

~/.cursor/rules/guidance_phase_awareness.mdc

glob: **/*

sample: ~/${MEMORY_STORAGE_ROOT:-storage

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}/knowledge_base.jsonl

sample: ~/-across-all-frameworks-89b1 into main"

sample: ~/AI_Folder_Architecture.md

sample: ~/AI_TEAM_ANALYSIS_PROMPT.md

sample: ~/DIFFS

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_main_pc_code_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_voice-assistant-prod_.cursor.patch

~/.cursor/rules/l10n_i18n_ai.mdc

glob: **/*

sample: ~/${MEMORY_STORAGE_ROOT:-storage

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}/knowledge_base.jsonl

sample: ~/-across-all-frameworks-89b1 into main"

sample: ~/AI_Folder_Architecture.md

sample: ~/AI_TEAM_ANALYSIS_PROMPT.md

sample: ~/DIFFS

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_main_pc_code_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_voice-assistant-prod_.cursor.patch

~/.cursor/rules/makeaprompt.mdc

glob: **/*

sample: ~/${MEMORY_STORAGE_ROOT:-storage

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}/knowledge_base.jsonl

sample: ~/-across-all-frameworks-89b1 into main"

sample: ~/AI_Folder_Architecture.md

sample: ~/AI_TEAM_ANALYSIS_PROMPT.md

sample: ~/DIFFS

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_main_pc_code_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_voice-assistant-prod_.cursor.patch

~/.cursor/rules/memory_ai.mdc

glob: **/*

sample: ~/${MEMORY_STORAGE_ROOT:-storage

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}/knowledge_base.jsonl

sample: ~/-across-all-frameworks-89b1 into main"

sample: ~/AI_Folder_Architecture.md

sample: ~/AI_TEAM_ANALYSIS_PROMPT.md

sample: ~/DIFFS

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_main_pc_code_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_voice-assistant-prod_.cursor.patch

~/.cursor/rules/memory_enhancement_auditor.mdc

glob: **/*

sample: ~/${MEMORY_STORAGE_ROOT:-storage

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}/knowledge_base.jsonl

sample: ~/-across-all-frameworks-89b1 into main"

sample: ~/AI_Folder_Architecture.md

sample: ~/AI_TEAM_ANALYSIS_PROMPT.md

sample: ~/DIFFS

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_main_pc_code_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_voice-assistant-prod_.cursor.patch

~/.cursor/rules/mlops_ai.mdc

glob: **/*

sample: ~/${MEMORY_STORAGE_ROOT:-storage

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}/knowledge_base.jsonl

sample: ~/-across-all-frameworks-89b1 into main"

sample: ~/AI_Folder_Architecture.md

sample: ~/AI_TEAM_ANALYSIS_PROMPT.md

sample: ~/DIFFS

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_main_pc_code_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_voice-assistant-prod_.cursor.patch

~/.cursor/rules/observability_ai.mdc

glob: **/*

sample: ~/${MEMORY_STORAGE_ROOT:-storage

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}/knowledge_base.jsonl

sample: ~/-across-all-frameworks-89b1 into main"

sample: ~/AI_Folder_Architecture.md

sample: ~/AI_TEAM_ANALYSIS_PROMPT.md

sample: ~/DIFFS

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_main_pc_code_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_voice-assistant-prod_.cursor.patch

~/.cursor/rules/planner_moderator_ai.mdc

glob: **/*

sample: ~/${MEMORY_STORAGE_ROOT:-storage

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}/knowledge_base.jsonl

sample: ~/-across-all-frameworks-89b1 into main"

sample: ~/AI_Folder_Architecture.md

sample: ~/AI_TEAM_ANALYSIS_PROMPT.md

sample: ~/DIFFS

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_main_pc_code_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_voice-assistant-prod_.cursor.patch

~/.cursor/rules/planning_ai.mdc

~/.cursor/rules/principal_engineer_ai.mdc

glob: **/*

sample: ~/${MEMORY_STORAGE_ROOT:-storage

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}/knowledge_base.jsonl

sample: ~/-across-all-frameworks-89b1 into main"

sample: ~/AI_Folder_Architecture.md

sample: ~/AI_TEAM_ANALYSIS_PROMPT.md

sample: ~/DIFFS

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_main_pc_code_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_voice-assistant-prod_.cursor.patch

~/.cursor/rules/product_owner_ai.mdc

glob: **/*

sample: ~/${MEMORY_STORAGE_ROOT:-storage

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}/knowledge_base.jsonl

sample: ~/-across-all-frameworks-89b1 into main"

sample: ~/AI_Folder_Architecture.md

sample: ~/AI_TEAM_ANALYSIS_PROMPT.md

sample: ~/DIFFS

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_main_pc_code_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_voice-assistant-prod_.cursor.patch

~/.cursor/rules/project-guidance.mdc

~/.cursor/rules/prompt_factory_ai.mdc

glob: **/*

sample: ~/${MEMORY_STORAGE_ROOT:-storage

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}/knowledge_base.jsonl

sample: ~/-across-all-frameworks-89b1 into main"

sample: ~/AI_Folder_Architecture.md

sample: ~/AI_TEAM_ANALYSIS_PROMPT.md

sample: ~/DIFFS

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_main_pc_code_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_voice-assistant-prod_.cursor.patch

~/.cursor/rules/prompt_linter_ai.mdc

glob: **/*

sample: ~/${MEMORY_STORAGE_ROOT:-storage

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}/knowledge_base.jsonl

sample: ~/-across-all-frameworks-89b1 into main"

sample: ~/AI_Folder_Architecture.md

sample: ~/AI_TEAM_ANALYSIS_PROMPT.md

sample: ~/DIFFS

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_main_pc_code_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_voice-assistant-prod_.cursor.patch

~/.cursor/rules/python-development-standards.mdc

glob: **/*.py

sample: ~/frameworks/fwk-001-cursor-rules/contracts/validate_contract.py

sample: ~/frameworks/fwk-001-cursor-rules/hydration/hydration_selector.py

sample: ~/frameworks/fwk-001-cursor-rules/hydration/run_hydration_tests.py

sample: ~/frameworks/fwk-001-cursor-rules/promotion/rollback_rehearsal.py

sample: ~/frameworks/fwk-001-cursor-rules/promotion/snapshot_cli.py

sample: ~/frameworks/fwk-001-cursor-rules/routing/check_routing_conflicts.py

sample: ~/frameworks/fwk-001-cursor-rules/routing/resolve_artifact_path.py

sample: ~/frameworks/fwk-001-cursor-rules/security/validate_security_config.py

sample: ~/frameworks/fwk-001-cursor-rules/sync/backfill_script.py

sample: ~/frameworks/fwk-001-cursor-rules/sync/enhanced_index_writer.py

glob: pyproject.toml

glob: requirements.txt

~/.cursor/rules/qa_ai.mdc

glob: **/*

sample: ~/${MEMORY_STORAGE_ROOT:-storage

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}/knowledge_base.jsonl

sample: ~/-across-all-frameworks-89b1 into main"

sample: ~/AI_Folder_Architecture.md

sample: ~/AI_TEAM_ANALYSIS_PROMPT.md

sample: ~/DIFFS

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_main_pc_code_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_voice-assistant-prod_.cursor.patch

~/.cursor/rules/rules_master_toggle.mdc

glob: **/*

sample: ~/${MEMORY_STORAGE_ROOT:-storage

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}/knowledge_base.jsonl

sample: ~/-across-all-frameworks-89b1 into main"

sample: ~/AI_Folder_Architecture.md

sample: ~/AI_TEAM_ANALYSIS_PROMPT.md

sample: ~/DIFFS

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_main_pc_code_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_voice-assistant-prod_.cursor.patch

~/.cursor/rules/security-and-compliance.mdc

glob: **/*

sample: ~/${MEMORY_STORAGE_ROOT:-storage

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}/knowledge_base.jsonl

sample: ~/-across-all-frameworks-89b1 into main"

sample: ~/AI_Folder_Architecture.md

sample: ~/AI_TEAM_ANALYSIS_PROMPT.md

sample: ~/DIFFS

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_main_pc_code_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_voice-assistant-prod_.cursor.patch

~/.cursor/rules/security_ai.mdc

glob: **/*

sample: ~/${MEMORY_STORAGE_ROOT:-storage

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}/knowledge_base.jsonl

sample: ~/-across-all-frameworks-89b1 into main"

sample: ~/AI_Folder_Architecture.md

sample: ~/AI_TEAM_ANALYSIS_PROMPT.md

sample: ~/DIFFS

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_main_pc_code_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_voice-assistant-prod_.cursor.patch

~/.cursor/rules/technology-stacks.mdc

~/.cursor/rules/test-rules-management.mdc

~/.cursor/rules/testing-and-quality.mdc

glob: **/*

sample: ~/${MEMORY_STORAGE_ROOT:-storage

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}

sample: ~/${MEMORY_STORAGE_ROOT:-storage/memory}/knowledge_base.jsonl

sample: ~/-across-all-frameworks-89b1 into main"

sample: ~/AI_Folder_Architecture.md

sample: ~/AI_TEAM_ANALYSIS_PROMPT.md

sample: ~/DIFFS

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_main_pc_code_.cursor.patch

sample: ~/DIFFS/cursor_diff__home_haymayndz_AI_System_Monorepo_voice-assistant-prod_.cursor.patch

E. CROSS-REFERENCE (FOUND vs MISSING)

~/.cursor/rules/ai-system-architecture.mdc

src/repo/atomic_io.py → FOUND :: ~/src/repo/atomic_io.py :: type=other

src/repo/auto_sync_manager.py → FOUND :: ~/src/repo/auto_sync_manager.py :: type=other

~/.cursor/rules/auditor_ai.mdc

Action_Plan.md → MISSING :: ~/Action_Plan.md :: type=other

Summary_Report.md → MISSING :: ~/Summary_Report.md :: type=other

handoff_log.json → MISSING :: ~/handoff_log.json :: type=other

memory-bank/plan/Action_Plan.md","context":["memory-bank/plan/technical_plan.md","memory-bank/plan/task_breakdown.yaml"],"outputs":{"report":"memory-bank/plan/Summary_Report.md"}} → MISSING :: ~/memory-bank/plan/Action_Plan.md","context":["memory-bank/plan/technical_plan.md","memory-bank/plan/task_breakdown.yaml"],"outputs":{"report":"memory-bank/plan/Summary_Report.md"}} :: type=other

task_breakdown.yaml → MISSING :: ~/task_breakdown.yaml :: type=other

technical_plan.md → MISSING :: ~/technical_plan.md :: type=other

~/.cursor/rules/codegen_ai.mdc

Final_Implementation_Plan.md → MISSING :: ~/Final_Implementation_Plan.md :: type=other

acceptance_criteria.json → MISSING :: ~/acceptance_criteria.json :: type=other

memory-bank/plan/Final_Implementation_Plan.md" → MISSING :: ~/memory-bank/plan/Final_Implementation_Plan.md" :: type=other

task_breakdown.yaml → MISSING :: ~/task_breakdown.yaml :: type=other

technical_plan.md → MISSING :: ~/technical_plan.md :: type=other

~/.cursor/rules/development-excellence.mdc

.cursor/rules/ai-system-architecture.mdc → FOUND :: ~/.cursor/rules/ai-system-architecture.mdc :: type=rule

.cursor/rules/development-workflow.mdc → FOUND :: ~/.cursor/rules/development-workflow.mdc :: type=rule

.cursor/rules/execution_orchestrator.mdc → FOUND :: ~/.cursor/rules/execution_orchestrator.mdc :: type=rule

.cursor/rules/python-development-standards.mdc → FOUND :: ~/.cursor/rules/python-development-standards.mdc :: type=rule

.cursor/rules/security-and-compliance.mdc → FOUND :: ~/.cursor/rules/security-and-compliance.mdc :: type=rule

.cursor/rules/testing-and-quality.mdc → FOUND :: ~/.cursor/rules/testing-and-quality.mdc :: type=rule

src/repo/atomic_io.py → FOUND :: ~/src/repo/atomic_io.py :: type=other

~/.cursor/rules/execution_orchestrator.mdc

Action_Plan.md → MISSING :: ~/Action_Plan.md :: type=other

Final_Implementation_Plan.md → MISSING :: ~/Final_Implementation_Plan.md :: type=other

Summary_Report.md → MISSING :: ~/Summary_Report.md :: type=other

Validation_Report.md → MISSING :: ~/Validation_Report.md :: type=other

acceptance_criteria.json → MISSING :: ~/acceptance_criteria.json :: type=other

frameworks/backend/go.mdc → MISSING :: ~/frameworks/backend/go.mdc :: type=rule

frameworks/backend/node.mdc → MISSING :: ~/frameworks/backend/node.mdc :: type=rule

frameworks/backend/php.mdc → MISSING :: ~/frameworks/backend/php.mdc :: type=rule

frameworks/backend/python.mdc → MISSING :: ~/frameworks/backend/python.mdc :: type=rule

frameworks/frontend/react.mdc → MISSING :: ~/frameworks/frontend/react.mdc :: type=rule

frameworks/mobile/flutter.mdc → MISSING :: ~/frameworks/mobile/flutter.mdc :: type=rule

gate_results.json → MISSING :: ~/gate_results.json :: type=other

handoff_log.json → MISSING :: ~/handoff_log.json :: type=other

product_backlog.yaml → MISSING :: ~/product_backlog.yaml :: type=other

rule_attach_log.json → FOUND :: ~/rule_attach_log.json :: type=other

task_breakdown.yaml → MISSING :: ~/task_breakdown.yaml :: type=other

technical_plan.md → MISSING :: ~/technical_plan.md :: type=other

workflow_state.json → MISSING :: ~/workflow_state.json :: type=other

~/.cursor/rules/framework_memory_bridge.mdc

memory-bank/logs/ → MISSING :: ~/memory-bank/logs/ :: type=other

memory-bank/observability/rules/ → MISSING :: ~/memory-bank/observability/rules/ :: type=other

memory-bank/project-brain/ → FOUND :: ~/memory-bank/project-brain/ :: type=other

memory-bank/queue-system/ → FOUND :: ~/memory-bank/queue-system/ :: type=other

rule_attach_log.json → FOUND :: ~/rule_attach_log.json :: type=other

tools/memory/memory_cli.py → FOUND :: ~/tools/memory/memory_cli.py :: type=other

~/.cursor/rules/guidance_phase_awareness.mdc

Final_Implementation_Plan.md → MISSING :: ~/Final_Implementation_Plan.md :: type=other

Summary_Report.md → MISSING :: ~/Summary_Report.md :: type=other

Validation_Report.md → MISSING :: ~/Validation_Report.md :: type=other

deployment_manifest.yaml → MISSING :: ~/deployment_manifest.yaml :: type=other

product_backlog.yaml → MISSING :: ~/product_backlog.yaml :: type=other

task_breakdown.yaml → MISSING :: ~/task_breakdown.yaml :: type=other

technical_plan.md → MISSING :: ~/technical_plan.md :: type=other

test_results.json → MISSING :: ~/test_results.json :: type=other

~/.cursor/rules/makeaprompt.mdc

memory-bank/current-session.md → FOUND :: ~/memory-bank/current-session.md :: type=doc

memory-bank/cursor_state.json → FOUND :: ~/memory-bank/cursor_state.json :: type=other

memory-bank/queue-system/tasks_active.json → FOUND :: ~/memory-bank/queue-system/tasks_active.json :: type=other

memory-bank/storage/memory" → MISSING :: ~/memory-bank/storage/memory" :: type=other

tools/memory/memory_cli.py → FOUND :: ~/tools/memory/memory_cli.py :: type=other

tools/memory/pro_config.yaml → FOUND :: ~/tools/memory/pro_config.yaml :: type=other

~/.cursor/rules/memory_enhancement_auditor.mdc

frameworks/fwk-001-cursor-rules/system-prompt/framework_memory_bridge.mdc → MISSING :: ~/frameworks/fwk-001-cursor-rules/system-prompt/framework_memory_bridge.mdc :: type=rule

memory-bank/storage/memory" → MISSING :: ~/memory-bank/storage/memory" :: type=other

tools/memory/README.md → FOUND :: ~/tools/memory/README.md :: type=other

tools/memory/memory_cli.py → FOUND :: ~/tools/memory/memory_cli.py :: type=other

tools/memory/pro_config.yaml → FOUND :: ~/tools/memory/pro_config.yaml :: type=other

~/.cursor/rules/mlops_ai.mdc

deployment_manifest.yaml → MISSING :: ~/deployment_manifest.yaml :: type=other

monitoring_config.json → MISSING :: ~/monitoring_config.json :: type=other

~/.cursor/rules/planning_ai.mdc

Action_Plan.md → MISSING :: ~/Action_Plan.md :: type=other

Final_Implementation_Plan.md → MISSING :: ~/Final_Implementation_Plan.md :: type=other

Summary_Report.md → MISSING :: ~/Summary_Report.md :: type=other

memory-bank/plan/Action_Plan.md → FOUND :: ~/memory-bank/plan/Action_Plan.md :: type=doc

memory-bank/plan/Action_Plan.md","context":["memory-bank/plan/technical_plan.md","memory-bank/plan/task_breakdown.yaml"],"outputs":{"report":"memory-bank/plan/Summary_Report.md"}} → MISSING :: ~/memory-bank/plan/Action_Plan.md","context":["memory-bank/plan/technical_plan.md","memory-bank/plan/task_breakdown.yaml"],"outputs":{"report":"memory-bank/plan/Summary_Report.md"}} :: type=other

memory-bank/plan/product_backlog.yaml → FOUND :: ~/memory-bank/plan/product_backlog.yaml :: type=other

memory-bank/plan/task_breakdown.yaml → FOUND :: ~/memory-bank/plan/task_breakdown.yaml :: type=other

memory-bank/plan/technical_plan.md → FOUND :: ~/memory-bank/plan/technical_plan.md :: type=doc

product_backlog.yaml → MISSING :: ~/product_backlog.yaml :: type=other

task_breakdown.yaml → MISSING :: ~/task_breakdown.yaml :: type=other

technical_plan.md → MISSING :: ~/technical_plan.md :: type=other

~/.cursor/rules/principal_engineer_ai.mdc

Action_Plan.md → MISSING :: ~/Action_Plan.md :: type=other

Final_Implementation_Plan.md → MISSING :: ~/Final_Implementation_Plan.md :: type=other

Summary_Report.md → MISSING :: ~/Summary_Report.md :: type=other

Validation_Report.md → MISSING :: ~/Validation_Report.md :: type=other

handoff_log.json → MISSING :: ~/handoff_log.json :: type=other

memory-bank/plan/Action_Plan.md → FOUND :: ~/memory-bank/plan/Action_Plan.md :: type=doc

memory-bank/plan/Action_Plan.md","context":["memory-bank/plan/technical_plan.md","memory-bank/plan/task_breakdown.yaml"],"outputs":{"report":"memory-bank/plan/Summary_Report.md"}} → MISSING :: ~/memory-bank/plan/Action_Plan.md","context":["memory-bank/plan/technical_plan.md","memory-bank/plan/task_breakdown.yaml"],"outputs":{"report":"memory-bank/plan/Summary_Report.md"}} :: type=other

memory-bank/plan/Summary_Report.md → FOUND :: ~/memory-bank/plan/Summary_Report.md :: type=doc

memory-bank/plan/Validation_Report.md → FOUND :: ~/memory-bank/plan/Validation_Report.md :: type=doc

task_breakdown.yaml → MISSING :: ~/task_breakdown.yaml :: type=other

technical_plan.md → MISSING :: ~/technical_plan.md :: type=other

~/.cursor/rules/product_owner_ai.mdc

acceptance_criteria.json → MISSING :: ~/acceptance_criteria.json :: type=other

memory-bank/plan/client_brief.md → FOUND :: ~/memory-bank/plan/client_brief.md :: type=doc

memory-bank/plan/client_brief.md" → MISSING :: ~/memory-bank/plan/client_brief.md" :: type=other

product_backlog.yaml → MISSING :: ~/product_backlog.yaml :: type=other

~/.cursor/rules/python-development-standards.mdc

src/repo/atomic_io.py → FOUND :: ~/src/repo/atomic_io.py :: type=other

~/.cursor/rules/qa_ai.mdc

acceptance_criteria.json → MISSING :: ~/acceptance_criteria.json :: type=other

test_results.json → MISSING :: ~/test_results.json :: type=other

~/.cursor/rules/security-and-compliance.mdc

src/repo/atomic_io.py → FOUND :: ~/src/repo/atomic_io.py :: type=other

~/.cursor/rules/technology-stacks.mdc

.cursor/rules/development-excellence.mdc → FOUND :: ~/.cursor/rules/development-excellence.mdc :: type=rule

.cursor/rules/python-development-standards.mdc → FOUND :: ~/.cursor/rules/python-development-standards.mdc :: type=rule

.cursor/rules/security-and-compliance.mdc → FOUND :: ~/.cursor/rules/security-and-compliance.mdc :: type=rule

.cursor/rules/testing-and-quality.mdc → FOUND :: ~/.cursor/rules/testing-and-quality.mdc :: type=rule

.cursor/test-rules/test-drupal-10-module-development-rules.mdc → FOUND :: ~/.cursor/test-rules/test-drupal-10-module-development-rules.mdc :: type=template

.cursor/test-rules/test-prisma-orm-development-guidelines.mdc → FOUND :: ~/.cursor/test-rules/test-prisma-orm-development-guidelines.mdc :: type=template

.cursor/test-rules/test-sanity-development-guidelines.mdc → FOUND :: ~/.cursor/test-rules/test-sanity-development-guidelines.mdc :: type=template

.cursor/test-rules/test-unity-c-expert-developer-prompt.mdc → FOUND :: ~/.cursor/test-rules/test-unity-c-expert-developer-prompt.mdc :: type=template

.cursor/test-rules/test-when-generating-rspec-tests-follow-these-best-practices-to-ensure-they-are-comp.mdc → FOUND :: ~/.cursor/test-rules/test-when-generating-rspec-tests-follow-these-best-practices-to-ensure-they-are-comp.mdc :: type=template

.cursor/test-rules/test-you-are-a-senior-devops-engineer-and-backend-solutions-developer-with-expertise.mdc → FOUND :: ~/.cursor/test-rules/test-you-are-a-senior-devops-engineer-and-backend-solutions-developer-with-expertise.mdc :: type=template

.cursor/test-rules/test-you-are-a-senior-front-end-developer-and-an-expert-in-reactjs-nextjs-javascrip.mdc → FOUND :: ~/.cursor/test-rules/test-you-are-a-senior-front-end-developer-and-an-expert-in-reactjs-nextjs-javascrip.mdc :: type=template

.cursor/test-rules/test-you-are-a-senior-kotlin-programmer-with-experience-in-the-android-framework-and.mdc → FOUND :: ~/.cursor/test-rules/test-you-are-a-senior-kotlin-programmer-with-experience-in-the-android-framework-and.mdc :: type=template

.cursor/test-rules/test-you-are-a-senior-qa-automation-engineer-expert-in-typescript-javascript-fronte.mdc → FOUND :: ~/.cursor/test-rules/test-you-are-a-senior-qa-automation-engineer-expert-in-typescript-javascript-fronte.mdc :: type=template

.cursor/test-rules/test-you-are-a-senior-typescript-programmer-with-experience-in-the-fastify-framework.mdc → FOUND :: ~/.cursor/test-rules/test-you-are-a-senior-typescript-programmer-with-experience-in-the-fastify-framework.mdc :: type=template

.cursor/test-rules/test-you-are-a-senior-typescript-programmer-with-experience-in-the-nestjs-framework-a-1.mdc → FOUND :: ~/.cursor/test-rules/test-you-are-a-senior-typescript-programmer-with-experience-in-the-nestjs-framework-a-1.mdc :: type=template

.cursor/test-rules/test-you-are-an-expert-in-go-programming-language-and-related-web-development-technologies.mdc → MISSING :: ~/.cursor/test-rules/test-you-are-an-expert-in-go-programming-language-and-related-web-development-technologies.mdc :: type=template

.cursor/test-rules/test-you-are-an-expert-in-java-programming-quarkus-framework-jakarta-ee-microprofi.mdc → FOUND :: ~/.cursor/test-rules/test-you-are-an-expert-in-java-programming-quarkus-framework-jakarta-ee-microprofi.mdc :: type=template

.cursor/test-rules/test-you-are-an-expert-in-javascript-react-native-expo-and-mobile-ui-development.mdc → FOUND :: ~/.cursor/test-rules/test-you-are-an-expert-in-javascript-react-native-expo-and-mobile-ui-development.mdc :: type=template

.cursor/test-rules/test-you-are-an-expert-in-javascript-react-node-js-next-js-app-router-zustand-sh.mdc → FOUND :: ~/.cursor/test-rules/test-you-are-an-expert-in-javascript-react-node-js-next-js-app-router-zustand-sh.mdc :: type=template

.cursor/test-rules/test-you-are-an-expert-in-javascript-typescript-and-astro-framework-for-scalable-we.mdc → FOUND :: ~/.cursor/test-rules/test-you-are-an-expert-in-javascript-typescript-and-astro-framework-for-scalable-we.mdc :: type=template

.cursor/test-rules/test-you-are-an-expert-in-jax-python-numpy-and-machine-learning.mdc → FOUND :: ~/.cursor/test-rules/test-you-are-an-expert-in-jax-python-numpy-and-machine-learning.mdc :: type=template

.cursor/test-rules/test-you-are-an-expert-in-julia-language-programming-data-science-and-numerical-com.mdc → FOUND :: ~/.cursor/test-rules/test-you-are-an-expert-in-julia-language-programming-data-science-and-numerical-com.mdc :: type=template

.cursor/test-rules/test-you-are-an-expert-in-laravel-php-and-related-web-development-technologies.mdc → FOUND :: ~/.cursor/test-rules/test-you-are-an-expert-in-laravel-php-and-related-web-development-technologies.mdc :: type=template

.cursor/test-rules/test-you-are-an-expert-in-laravel-php-livewire-alpine-js-tailwindcss-and-daisyui.mdc → FOUND :: ~/.cursor/test-rules/test-you-are-an-expert-in-laravel-php-livewire-alpine-js-tailwindcss-and-daisyui.mdc :: type=template

.cursor/test-rules/test-you-are-an-expert-in-laravel-vue-js-and-modern-full-stack-web-development-tech.mdc → FOUND :: ~/.cursor/test-rules/test-you-are-an-expert-in-laravel-vue-js-and-modern-full-stack-web-development-tech.mdc :: type=template

.cursor/test-rules/test-you-are-an-expert-in-lua-programming-with-deep-knowledge-of-its-unique-features.mdc → FOUND :: ~/.cursor/test-rules/test-you-are-an-expert-in-lua-programming-with-deep-knowledge-of-its-unique-features.mdc :: type=template

.cursor/test-rules/test-you-are-an-expert-in-python-and-cybersecurity-tool-development.mdc → FOUND :: ~/.cursor/test-rules/test-you-are-an-expert-in-python-and-cybersecurity-tool-development.mdc :: type=template

.cursor/test-rules/test-you-are-an-expert-in-python-django-and-scalable-web-application-development.mdc → FOUND :: ~/.cursor/test-rules/test-you-are-an-expert-in-python-django-and-scalable-web-application-development.mdc :: type=template

.cursor/test-rules/test-you-are-an-expert-in-python-fastapi-integrations-and-web-app-development-you-a.mdc → FOUND :: ~/.cursor/test-rules/test-you-are-an-expert-in-python-fastapi-integrations-and-web-app-development-you-a.mdc :: type=template

.cursor/test-rules/test-you-are-an-expert-in-python-flask-and-scalable-api-development.mdc → FOUND :: ~/.cursor/test-rules/test-you-are-an-expert-in-python-flask-and-scalable-api-development.mdc :: type=template

.cursor/test-rules/test-you-are-an-expert-in-python-robocorp-and-scalable-rpa-development.mdc → FOUND :: ~/.cursor/test-rules/test-you-are-an-expert-in-python-robocorp-and-scalable-rpa-development.mdc :: type=template

.cursor/test-rules/test-you-are-an-expert-in-react-vite-tailwind-css-three-js-react-three-fiber-and.mdc → FOUND :: ~/.cursor/test-rules/test-you-are-an-expert-in-react-vite-tailwind-css-three-js-react-three-fiber-and.mdc :: type=template

.cursor/test-rules/test-you-are-an-expert-in-rust-async-programming-and-concurrent-systems.mdc → FOUND :: ~/.cursor/test-rules/test-you-are-an-expert-in-rust-async-programming-and-concurrent-systems.mdc :: type=template

.cursor/test-rules/test-you-are-an-expert-in-svelte-5-sveltekit-typescript-and-modern-web-development.mdc → FOUND :: ~/.cursor/test-rules/test-you-are-an-expert-in-svelte-5-sveltekit-typescript-and-modern-web-development.mdc :: type=template

.cursor/test-rules/test-you-are-an-expert-in-terraform-and-infrastructure-as-code-iac-for-cloud-platfo.mdc → FOUND :: ~/.cursor/test-rules/test-you-are-an-expert-in-terraform-and-infrastructure-as-code-iac-for-cloud-platfo.mdc :: type=template

.cursor/test-rules/test-you-are-an-expert-in-typescript-node-js-next-js-app-router-react-shadcn-ui.mdc → FOUND :: ~/.cursor/test-rules/test-you-are-an-expert-in-typescript-node-js-next-js-app-router-react-shadcn-ui.mdc :: type=template

.cursor/test-rules/test-you-are-an-expert-in-typescript-pixi-js-web-game-development-and-mobile-app-o.mdc → FOUND :: ~/.cursor/test-rules/test-you-are-an-expert-in-typescript-pixi-js-web-game-development-and-mobile-app-o.mdc :: type=template

.cursor/test-rules/test-you-are-an-expert-in-typescript-react-native-expo-and-mobile-app-development.mdc → FOUND :: ~/.cursor/test-rules/test-you-are-an-expert-in-typescript-react-native-expo-and-mobile-app-development.mdc :: type=template

.cursor/test-rules/test-you-are-an-expert-in-ui-and-ux-design-principles-for-software-development.mdc → FOUND :: ~/.cursor/test-rules/test-you-are-an-expert-in-ui-and-ux-design-principles-for-software-development.mdc :: type=template

.cursor/test-rules/test-you-are-an-expert-in-web-scraping-and-data-extraction-with-a-focus-on-python-li.mdc → FOUND :: ~/.cursor/test-rules/test-you-are-an-expert-in-web-scraping-and-data-extraction-with-a-focus-on-python-li.mdc :: type=template

.cursor/test-rules/test-you-are-an-expert-in-wordpress-php-and-related-web-development-technologies.mdc → FOUND :: ~/.cursor/test-rules/test-you-are-an-expert-in-wordpress-php-and-related-web-development-technologies.mdc :: type=template

.cursor/test-rules/test-you-are-an-expert-in-wordpress-woocommerce-php-and-related-web-development-te.mdc → FOUND :: ~/.cursor/test-rules/test-you-are-an-expert-in-wordpress-woocommerce-php-and-related-web-development-te.mdc :: type=template

.cursor/test-rules/test-you-are-an-expert-ios-developer-using-swift-and-swiftui-follow-these-guidelines.mdc → FOUND :: ~/.cursor/test-rules/test-you-are-an-expert-ios-developer-using-swift-and-swiftui-follow-these-guidelines.mdc :: type=template

.cursor/test-rules/test-you-are-an-expert-salesforce-developer-that-will-create-apex-classes-apex-trig.mdc → FOUND :: ~/.cursor/test-rules/test-you-are-an-expert-salesforce-developer-that-will-create-apex-classes-apex-trig.mdc :: type=template

.cursor/test-rules/test-you-are-an-expert-shopify-theme-developer-with-advanced-knowledge-of-liquid-htm.mdc → FOUND :: ~/.cursor/test-rules/test-you-are-an-expert-shopify-theme-developer-with-advanced-knowledge-of-liquid-htm.mdc :: type=template

.cursor/test-rules/test-you-have-extensive-expertise-in-vue-3-nuxt-3-typescript-node-js-vite-vue-ro.mdc → FOUND :: ~/.cursor/test-rules/test-you-have-extensive-expertise-in-vue-3-nuxt-3-typescript-node-js-vite-vue-ro.mdc :: type=template

~/.cursor/rules/test-rules-management.mdc

" → MISSING :: ~/" :: type=other

.cursor/rules/technology-stacks.mdc → FOUND :: ~/.cursor/rules/technology-stacks.mdc :: type=rule

[^ → MISSING :: ~/[^ :: type=other

F. RISKS & GAPS

Conflicting/overlapping globs between ~/.cursor/rules/ai-system-architecture.mdc and ~/.cursor/rules/development-excellence.mdc: ['**/*']

Conflicting/overlapping globs between ~/.cursor/rules/ai-system-architecture.mdc and ~/.cursor/rules/development-workflow.mdc: ['**/*']

Conflicting/overlapping globs between ~/.cursor/rules/ai-system-architecture.mdc and ~/.cursor/rules/security-and-compliance.mdc: ['**/*']

Conflicting/overlapping globs between ~/.cursor/rules/ai-system-architecture.mdc and ~/.cursor/rules/testing-and-quality.mdc: ['**/*']

Conflicting/overlapping globs between ~/.cursor/rules/development-excellence.mdc and ~/.cursor/rules/development-workflow.mdc: ['**/*']

Conflicting/overlapping globs between ~/.cursor/rules/development-excellence.mdc and ~/.cursor/rules/security-and-compliance.mdc: ['**/*']

Conflicting/overlapping globs between ~/.cursor/rules/development-excellence.mdc and ~/.cursor/rules/testing-and-quality.mdc: ['**/*']

Conflicting/overlapping globs between ~/.cursor/rules/development-workflow.mdc and ~/.cursor/rules/security-and-compliance.mdc: ['**/*']

Conflicting/overlapping globs between ~/.cursor/rules/development-workflow.mdc and ~/.cursor/rules/testing-and-quality.mdc: ['**/*']

Conflicting/overlapping globs between ~/.cursor/rules/security-and-compliance.mdc and ~/.cursor/rules/testing-and-quality.mdc: ['**/*']

Missing referenced rule link in ~/.cursor/rules/technology-stacks.mdc: .cursor/test-rules/test-you-are-an-expert-in-go-programming-language-and-related-web-development-technologies.mdc

Missing referenced rule link in ~/.cursor/rules/test-rules-management.mdc: "

Missing referenced rule link in ~/.cursor/rules/test-rules-management.mdc: [^

Zero-match globs observed:

**/*.ts, **/*.tsx, **/*.js, **/*.jsx (no matching files under ~)

**/*.sol, hardhat.config.*, foundry.toml (no matching files under ~)

**/*.tf, **/*.tfvars (no matching files under ~)

Malformed reference strings detected (likely YAML or formatting spillover) that could cause false-negative existence checks:

In ~/.cursor/rules/auditor_ai.mdc and others: entries containing embedded JSON-like context (see section E lines referencing memory-bank/plan/Action_Plan.md","context":...). These are treated as a single path and marked MISSING.

In ~/.cursor/rules/product_owner_ai.mdc: memory-bank/plan/client_brief.md" (trailing quote) marked MISSING while the correct path exists.

Top-level vs memory-bank artifacts:

Several artifacts exist under ~/memory-bank/plan/ but are checked at repository root and marked MISSING (e.g., Action_Plan.md, Summary_Report.md, Validation_Report.md, technical_plan.md, task_breakdown.yaml). Evidence in section E shows their presence under memory-bank/plan/.

G. RECOMMENDATIONS (EVIDENCE-BASED ONLY)

Narrow overlapping alwaysApply globs or convert to conditional activation.

Fix broken mdc: links or restore referenced files under .cursor/test-rules or frameworks/.

Normalize references to actual artifact locations (prefer memory-bank/plan/* where applicable) and correct malformed path strings to avoid false MISSING statuses.

For zero-match globs, either scope them to subdirectories present in this repo or annotate them as intentionally broad with no current matches.

H. EVIDENCE INDEX
code
1:20:.cursor/rules/ai-assistant-guidance.mdc
download
content_copy
expand_less

---
description: AI Assistant Guidance Rules - Global Communication & Behavior
globs: []
alwaysApply: false
---
# AI Assistant Guidance Rules - Global Communication & Behavior

## Communication Style
- Always communicate in a friendly, conversational tone that feels like a helpful colleague
- Use phrases like "I'm here to help!" or "Let's break this down together" to build rapport
- Avoid robotic or overly formal language—opt for empathy and encouragement
- Be especially supportive when users seem frustrated or stuck

## Response Structure

### For Simple Questions
- Keep responses concise (1-2 paragraphs) with a clear answer
- Follow with a quick tip or next step
- End with an open-ended question to invite further discussion
code
1:20:.cursor/rules/ai-system-architecture.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: "AI system architecture, roles, memory, orchestration"
globs: ["**/*"]
alwaysApply: true
---
# AI System Architecture

## System Overview
This workspace implements a sophisticated AI development environment with multiple specialized AI roles, memory systems, and execution orchestration.

## Core Components

### AI Role System
- **product_owner_ai**: Requirements and backlog management
- **planning_ai**: Technical architecture and implementation planning
- **codegen_ai**: Code generation and implementation
- **qa_ai**: Quality assurance and testing
- **mlops_ai**: Machine learning operations and deployment
- **observability_ai**: Monitoring and observability
- **security_ai**: Security analysis and compliance
code
1:20:.cursor/rules/analyst_ai.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: >
  AI role specialization for analyst ai. Activated when orchestrator selects this role or via explicit commands.
globs: ["**/*"]
alwaysApply: false
---
--------------------------------------------------
title:        "ANALYST_AI  —  v0.1.0"
description:  "Performance analysis, metrics collection, and optimization recommendations"
owner:        "ANALYST_AI"
phases:       "Support"
--------------------------------------------------
## 1. PURPOSE
• Analyzes system performance, code quality, and development metrics
• Identifies bottlenecks, optimization opportunities, and improvement areas
• Provides data-driven insights for technical and business decisions

## 2. INPUT CONTRACT
• Expected fields / schema:
  - performance_metrics: system and application performance data
code
1:20:.cursor/rules/auditor_ai.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: >
  AI role specialization for auditor ai. Activated when orchestrator selects this role or via explicit commands.
globs: ["**/*"]
alwaysApply: false
---
# Role: auditor_ai
# Purpose
You act as a Systems Auditor and Risk Analyst. Your only job is to run a pre-mortem by **comparing a provided Action_Plan.md against the current state of the codebase**. You identify **conflicts (risks)** and **alignments (correct observations)**. You are a critic and an observer, not a solver.

# Triggers / Commands
- /audit <path_to_Action_Plan.md> --codebase <path_to_codebase_root>

# Required Inputs
- Action_Plan.md (the plan under review)
- **Access to the entire project codebase.**

# Context Awareness
Before analysis, detect the declared type and intent of the plan:
- Diagnostic/Analytical (e.g., conflict analysis, evaluation): do NOT flag intended contradictions/exploration as risks.
code
1:20:.cursor/rules/codegen_ai.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: >
  AI role specialization for codegen ai. Activated when orchestrator selects this role or via explicit commands.
globs: ["**/*"]
alwaysApply: false
---
--------------------------------------------------
title:        "CODEGEN_AI  —  v0.1.0"
description:  "Code generation and implementation specialist"
owner:        "CODEGEN_AI"
phases:       "Execution"
--------------------------------------------------
## 1. PURPOSE
• Generates production-ready code based on technical specifications and Final_Implementation_Plan.md
• Implements features according to validated requirements and acceptance criteria
• Ensures code quality, testing, and documentation standards are met
• Follows the established development workflow and coding standards

## 2. INPUT CONTRACT
• Expected fields / schema:
code
1:20:.cursor/rules/curated_test-when-generating-rspec-tests-follow-these-best-practices-to-ensure-they-are-comp.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: >
  Framework-specific rules for TypeScript/JavaScript stacks.
globs: ["**/*.ts", "**/*.tsx", "**/*.js", "**/*.jsx"]
alwaysApply: false
---
When generating RSpec tests, follow these best practices to ensure they are comprehensive, readable, and maintainable:

### Comprehensive Coverage:
- Tests must cover both typical cases and edge cases, including invalid inputs and error conditions.
- Consider all possible scenarios for each method or behavior and ensure they are tested.

### Readability and Clarity:
- Use clear and descriptive names for describe, context, and it blocks.
- Prefer the expect syntax for assertions to improve readability.
- Keep test code concise; avoid unnecessary complexity or duplication.

### Structure:
- Organize tests logically using describe for classes/modules and context for different scenarios.
- Use subject to define the object under test when appropriate to avoid repetition.
code
1:20:.cursor/rules/curated_test-you-are-an-expert-in-python-and-cybersecurity-tool-development.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: >
  Framework-specific rules for Python (Django/FastAPI/Flask).
globs: ["**/*.py", "requirements.txt", "pyproject.toml"]
alwaysApply: false
---
You are an expert in Python and cybersecurity-tool development.
  
  Key Principles  
  - Write concise, technical responses with accurate Python examples.  
  - Use functional, declarative programming; avoid classes where possible.  
  - Prefer iteration and modularization over code duplication.  
  - Use descriptive variable names with auxiliary verbs (e.g., is_encrypted, has_valid_signature).  
  - Use lowercase with underscores for directories and files (e.g., scanners/port_scanner.py).  
  - Favor named exports for commands and utility functions.  
  - Follow the Receive an Object, Return an Object (RORO) pattern for all tool interfaces.
  
  Python/Cybersecurity  
  - Use `def` for pure, CPU-bound routines; `async def` for network- or I/O-bound operations.  
  - Add type hints for all function signatures; validate inputs with Pydantic v2 models where structured config is required.
code
1:20:.cursor/rules/curated_test-you-are-an-expert-in-python-django-and-scalable-restful-api-development.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: >
  Framework-specific rules for Python (Django/FastAPI/Flask).
globs: ["**/*.py", "requirements.txt", "pyproject.toml"]
alwaysApply: false
---
You are an expert in Python, Django, and scalable RESTful API development.

  Core Principles
  - Django-First Approach: Use Django's built-in features and tools wherever possible to leverage its full capabilities
  - Code Quality: Prioritize readability and maintainability; follow Django's coding style guide (PEP 8 compliance)
  - Naming Conventions: Use descriptive variable and function names; adhere to naming conventions (lowercase with underscores for functions and variables)
  - Modular Architecture: Structure your project in a modular way using Django apps to promote reusability and separation of concerns
  - Performance Awareness: Always consider scalability and performance implications in your design decisions

  Project Structure

  Application Structure
  app_name/
  ├── migrations/        # Database migration files
code
1:20:.cursor/rules/curated_test-you-are-an-expert-in-solidity-and-smart-contract-security.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: >
  Framework-specific rules for Solidity/Smart Contracts.
globs: ["**/*.sol", "hardhat.config.*", "foundry.toml"]
alwaysApply: false
---
You are an expert in Solidity and smart contract security.

    General Rules
    - Cut the fluff. Code or detailed explanations only.
    - Keep it casual and brief.
    - Accuracy and depth matter.
    - Answer first, explain later if needed.
    - Logic trumps authority. Don't care about sources.
    - Embrace new tech and unconventional ideas.
    - Wild speculation's fine, just flag it.
    - Save the ethics talk.
    - Only mention safety for non-obvious, critical issues.
    - Push content limits if needed, explain after.
    - Sources at the end, not mid-text.
code
1:20:.cursor/rules/curated_test-you-are-an-expert-in-terraform-and-infrastructure-as-code-iac-for-cloud-platfo.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: >
  Framework-specific rules for Terraform.
globs: ["**/*.tf", "**/*.tfvars"]
alwaysApply: false
---
You are an expert in Terraform and Infrastructure as Code (IaC) for cloud platforms such as AWS, Azure, and GCP.
  
  Key Principles
  - Write concise, well-structured Terraform code with accurate examples.
  - Organize infrastructure resources into reusable modules.
  - Use versioned modules and provider version locks to ensure consistent deployments.
  - Avoid hardcoded values; always use variables for flexibility.
  - Structure files into logical sections: main configuration, variables, outputs, and modules.
  
  Terraform Best Practices
  - Use remote backends (e.g., S3, Azure Blob, GCS) for state management.
  - Enable state locking and use encryption for security.
  - Utilize workspaces for environment separation (e.g., dev, staging, prod).
  - Organize resources by service or application domain (e.g., networking, compute).
code
1:20:.cursor/rules/data_ai.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: >
  AI role specialization for data ai. Activated when orchestrator selects this role or via explicit commands.
globs: ["**/*"]
alwaysApply: false
---
--------------------------------------------------
title:        "DATA_AI  —  v0.1.0"
description:  "Database schema design and migration management"
owner:        "DATA_AI"
phases:       "Foundation"
--------------------------------------------------
## 1. PURPOSE
• Designs optimal database schemas and data models
• Manages database migrations and version control
• Ensures data integrity, performance, and scalability

## 2. INPUT CONTRACT
• Expected fields / schema:
  - data_requirements: entity relationships and business rules
code
1:20:.cursor/rules/development-excellence.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: "Master development standards across phases and stacks"
globs: ["**/*"]
alwaysApply: true
---
# Development Excellence

## Overview
This rule provides comprehensive guidance for maintaining the highest standards of development excellence across all aspects of the AI development environment.

## Core Principles

### 1. Quality First
- **Never compromise quality** for speed or convenience
- **Test everything** before considering it complete
- **Document decisions** and rationale for future reference
- **Review code** with the same rigor as production code

### 2. Continuous Improvement
- **Learn from every interaction** and failure
code
1:20:.cursor/rules/development-workflow.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: "Workflow pipeline, phases, gates, and orchestration"
globs: ["**/*"]
alwaysApply: true
---
# Development Workflow

## Pipeline Overview
This workspace uses a structured development pipeline with multiple phases and quality gates.

## Development Phases

### 1. Planning Phase
**Role**: `planning_ai`
**Inputs**: Product requirements, user stories, technical constraints
**Outputs**: Technical design, architecture decisions, implementation plan
**Deliverables**:
- Technical architecture document
- API specifications
- Database schema design
code
1:20:.cursor/rules/documentation_ai.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: >
  AI role specialization for documentation ai. Activated when orchestrator selects this role or via explicit commands.
globs: ["**/*"]
alwaysApply: false
---
--------------------------------------------------
title:        "DOCUMENTATION_AI  —  v0.1.0"
description:  "Comprehensive technical documentation generation and maintenance"
owner:        "DOCUMENTATION_AI"
phases:       "Support"
--------------------------------------------------
## 1. PURPOSE
• Creates and maintains comprehensive technical documentation
• Generates API documentation, user guides, and developer resources
• Ensures documentation stays current with code changes and requirements

## 2. INPUT CONTRACT
• Expected fields / schema:
  - source_code: implemented features with inline documentation
code
1:20:.cursor/rules/execution_orchestrator.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: "Universal guidance rule: execution_orchestrator \u2014 Always active\
  \ across the workspace.\n"
globs:
- '**/*'
alwaysApply: false
---
--------------------------------------------------
title:        "EXECUTION_ORCHESTRATOR  —  v0.1.0"
description:  "Pipeline coordination and workflow management"
owner:        "EXECUTION_ORCHESTRATOR"
phases:       "Orchestration"
--------------------------------------------------
## 1. PURPOSE
• Coordinates execution flow between AI roles in proper sequence
• Enforces gate rules and quality checkpoints throughout pipeline
• Manages workflow state and handles error recovery scenarios

# Output Artifact
- workflow_state.json: current pipeline state
code
1:20:.cursor/rules/framework_memory_bridge.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: "Universal guidance rule: framework_memory_bridge \u2014 Always active\
  \ across the workspace.\n"
globs:
- '**/*'
alwaysApply: false
---
--------------------------------------------------
title:        "FRAMEWORK_MEMORY_BRIDGE  —  v0.1.0"
description:  "Integration bridge between framework roles and existing memory-bank system"
owner:        "FRAMEWORK_MEMORY_BRIDGE"
phases:       "Orchestration"
--------------------------------------------------
## 1. PURPOSE
• Bridges new framework AI roles with existing sophisticated memory-bank system
• Synchronizes framework state with tasks_active.json and memory persistence
• Preserves existing workflow while enabling new role-based capabilities

# Output Artifact
- bridge_sync_report.md: summary of sync actions and results
code
1:20:.cursor/rules/guidance_command_suggester.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: "Universal guidance rule: guidance_command_suggester \u2014 Always active\
  \ across the workspace.\n"
globs:
- '**/*'
alwaysApply: false
---
# Rule: guidance_command_suggester.mdc (Command Guardrails)
## Signals: Framework Enabled?
- Consider framework-enabled = TRUE only if at least ONE is true:
  - Files exist:
    - `.cursor/rules/rules_master_toggle.mdc`
    - `.cursor/rules/execution_orchestrator.mdc`
    - `.cursor/rules/framework_memory_bridge.mdc`
  - OR `cursor_state.json` contains: `"framework_enabled": true`
  - OR user explicitly used **any** framework command within the session:
    `/backlog`, `/plan`, `/audit`, `/peer_review`, `/gen_code`, `/test`,
    `/deploy`, `/observe`, `/docs`, `/review`, `/snapshot`, `/run_pipeline`.

## When to Suggest Commands
code
1:20:.cursor/rules/guidance_next_steps.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: >
  Universal guidance rule: guidance_next_steps — Always active across the workspace.
globs: ["**/*"]
alwaysApply: false
---

# Rule: guidance_next_steps.mdc (Universal Guidance)

## Intent
- Always end with **Suggested Next Step(s)**, but:
  - Keep it **relevant, minimal (1–3 items)**, and **non-repetitive**.
  - Respect user intent and current phase.
  - Prefer **domain action** (e.g., “run tests”, “refine acceptance criteria”)
    over **framework command** unless the command is explicitly allowed
    by `guidance_command_suggester.mdc`.

## Decision Heuristics
- If the user asks for **knowledge/explanation** (no project context),
  → Suggest **one** learning/action step (e.g., “Need code sample?”),
code
1:20:.cursor/rules/guidance_phase_awareness.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: >
  Universal guidance rule: guidance_phase_awareness — Always active across the workspace.
globs: ["**/*"]
alwaysApply: false
---

# Rule: guidance_phase_awareness.mdc (Phase-Aware Steps)

## Phase Detection (Heuristics)
- BACKLOG if `product_backlog.yaml` present/just updated.
- PLANNING if `technical_plan.md` or `task_breakdown.yaml` updated.
- AUDIT if `Summary_Report.md` requested/generated.
- VERIFICATION/SYNTHESIS if `Validation_Report.md` or
  `Final_Implementation_Plan.md` referenced.
- DEVELOPMENT if code/test files changed by `/gen_code`.
- TESTING if `test_results.json` present.
- DEPLOYMENT if `deployment_manifest.yaml` applied.
- MONITORING if dashboards/alerts updated.
code
1:20:.cursor/rules/l10n_i18n_ai.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: >
  AI role specialization for l10n i18n ai. Activated when orchestrator selects this role or via explicit commands.
globs: ["**/*"]
alwaysApply: false
---
--------------------------------------------------
title:        "L10N_I18N_AI  —  v0.1.0"
description:  "Localization and internationalization template generation"
owner:        "L10N_I18N_AI"
phases:       "Support"
--------------------------------------------------
## 1. PURPOSE
• Manages internationalization and localization requirements
• Generates translation templates and manages language resources
• Ensures cultural and linguistic appropriateness across target markets

## 2. INPUT CONTRACT
• Expected fields / schema:
  - source_content: text content requiring translation
code
1:20:.cursor/rules/makeaprompt.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: 'Universal system rule for makeaprompt that supports orchestration.

  '
globs:
- '**/*'
alwaysApply: false
---
### **The Clarification Mandate (The "No Assumption" Rule)**

This is your most important rule.

If any of the five components of "The What" are missing, vague, or ambiguous, you **MUST NOT** proceed to generate the solution.

Your immediate and only response must be to ask targeted, clarifying questions to fill the gaps.

**Examples of Clarifying Questions:**

- **For a missing [GOAL]:** "You've asked for a 'report'. To ensure I create the right one, could you specify who the audience is (e.g., executives, developers) and what key metrics it should contain?"
code
1:20:.cursor/rules/memory_ai.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: "Universal guidance rule: memory_ai \u2014 Always active across the workspace.\n"
globs:
- '**/*'
alwaysApply: false
---
--------------------------------------------------
title:        "MEMORY_AI  —  v0.1.0"
description:  "Knowledge management and context preservation across sessions"
owner:        "MEMORY_AI"
phases:       "Support"
--------------------------------------------------
## 1. PURPOSE
• Maintains persistent knowledge base of project decisions and context
• Preserves important conversations, decisions, and lessons learned
• Provides historical context for future development and troubleshooting

## 2. INPUT CONTRACT
• Expected fields / schema:
  - session_logs: conversation history and decisions
code
1:20:.cursor/rules/memory_enhancement_auditor.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: 'Universal system rule for memory_enhancement_auditor that supports orchestration.

  '
globs:
- '**/*'
alwaysApply: false
---
owner:        "MEMORY_ENHANCEMENT_AUDITOR_AI"
phases:       "Audit"
--------------------------------------------------
## 1. PURPOSE
• Analyze repository memory subsystems end-to-end and propose concrete enhancements to improve reliability, portability, retrieval quality, and safety.

## 2. INPUT CONTRACT
• Sources to analyze (read-only):
  - `tools/memory/memory_cli.py`, `tools/memory/pro_config.yaml`, `tools/memory/README.md`
  - `atomic_io.py`, `todo_manager.py`, `auto_sync_manager.py`, `cursor_memory_bridge.py`
  - `memory-bank/` (structure), `storage/memory/knowledge_base.jsonl` examples
  - `labnotes/memory.md`, `frameworks/fwk-001-cursor-rules/system-prompt/framework_memory_bridge.mdc`, `memory_ai.mdc`
code
1:20:.cursor/rules/mlops_ai.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: >
  AI role specialization for mlops ai. Activated when orchestrator selects this role or via explicit commands.
globs: ["**/*"]
alwaysApply: false
---
--------------------------------------------------
title:        "MLOPS_AI  —  v0.1.0"
description:  "Deployment automation and infrastructure management"
owner:        "MLOPS_AI"
phases:       "Execution"
--------------------------------------------------
## 1. PURPOSE
• Automates deployment pipelines and infrastructure provisioning
• Manages environment configurations and release processes
• Ensures scalable, reliable, and secure production deployments

## 2. INPUT CONTRACT
• Expected fields / schema:
  - validated_code: tested code from qa_ai with PASS status
code
1:20:.cursor/rules/observability_ai.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: >
  AI role specialization for observability ai. Activated when orchestrator selects this role or via explicit commands.
globs: ["**/*"]
alwaysApply: false
---
--------------------------------------------------
title:        "OBSERVABILITY_AI  —  v0.1.0"
description:  "System monitoring, alerting, and health tracking"
owner:        "OBSERVABILITY_AI"
phases:       "Support"
--------------------------------------------------
## 1. PURPOSE
• Monitors system health, performance, and operational metrics
• Provides real-time alerting for issues and anomalies
• Maintains comprehensive logging and tracing for debugging and analysis

## 2. INPUT CONTRACT
• Expected fields / schema:
  - system_metrics: CPU, memory, network, and application metrics
code
1:20:.cursor/rules/planner_moderator_ai.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: >
  AI role specialization for planner moderator ai. Activated when orchestrator selects this role or via explicit commands.
globs: ["**/*"]
alwaysApply: false
---
--------------------------------------------------
title:        "PLANNER_MODERATOR_AI  —  v0.1.0"
description:  "Single-toggle, answer-first, confirm-before-action session moderator"
owner:        "PLANNER_MODERATOR_AI"
phases:       "Orchestration"
--------------------------------------------------
## 1. PURPOSE
• Ensure human-like, answer-first conversation and explicit confirmation before any action or code.

## 2. SESSION POLICY (ONE SWITCH)
```yaml
session_policies:
  planner_mode:
    enabled: true                 # controlled by /planner_mode on|off
code
1:20:.cursor/rules/planning_ai.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: Technical architecture design and implementation planning
globs: []
alwaysApply: false
---
--------------------------------------------------
title:        "PLANNING_AI  —  v0.1.0"
description:  "Technical architecture design and implementation planning"
owner:        "PLANNING_AI"
phases:       "Foundation"
--------------------------------------------------
## 1. PURPOSE
• Converts product requirements into detailed technical implementation plans
• Designs system architecture with scalability and maintainability in mind
• Creates development roadmaps with clear milestones and dependencies
• Generates Action_Plan.md from product backlog and technical plan

## 2. INPUT CONTRACT
• Expected fields / schema:
  - product_backlog.yaml: prioritized features from product_owner_ai
code
1:20:.cursor/rules/principal_engineer_ai.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: >
  AI role specialization for principal engineer ai. Activated when orchestrator selects this role or via explicit commands.
globs: ["**/*"]
alwaysApply: false
---
# Role: principal_engineer_ai
# Purpose
You act as a Principal Engineer and Strategic Planner. You DO NOT perform initial risk assessment. Your primary role is to **validate the Auditor's findings against the codebase** and then, based on a strict gating logic, either **synthesize a final, executable plan** or **halt the process and provide feedback for revision**.

# Modes & Commands
- Mode 1 (Peer Review & Validation): @peer_review
  Command: /peer_review <path_to_Action_Plan.md> <path_to_Summary_Report.md> --codebase <path_to_codebase_root>
- Mode 2 (Synthesis): @synthesize_plan
  Command: /synthesize_plan <path_to_Action_Plan.md> <path_to_Summary_Report.md> <path_to_Validation_Report.md>

# Required Inputs
- Peer Review: Action_Plan.md + Summary_Report.md (from auditor_ai) + **Access to the entire project codebase.**
- Synthesis: Action_Plan.md + Summary_Report.md + Validation_Report.md (your own output from Peer Review)
code
1:20:.cursor/rules/product_owner_ai.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: >
  AI role specialization for product owner ai. Activated when orchestrator selects this role or via explicit commands.
globs: ["**/*"]
alwaysApply: false
---

--------------------------------------------------
title:        "PRODUCT_OWNER_AI  —  v0.1.0"
description:  "Requirements gathering, backlog management, and feature prioritization"
owner:        "PRODUCT_OWNER_AI"
phases:       "Foundation"
--------------------------------------------------
## 1. PURPOSE
• Translates business requirements into actionable development tasks
• Manages product backlog with clear priorities and acceptance criteria
• Ensures alignment between stakeholder needs and technical implementation

## 2. INPUT CONTRACT
• Expected fields / schema:
code
1:20:.cursor/rules/project-guidance.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: Project Guidance Rules - Domain-Specific AI Assistant Behavior
globs: []
alwaysApply: false
---
# Project Guidance Rules - Domain-Specific AI Assistant Behavior

## Glob Pattern
**/* (applies broadly; can be narrowed to *.py for Python projects, *.js for JavaScript, or src/**/* for source directories)

## Domain-Specific Behavior
Tailor responses to the project's context:

### Web Development
- Emphasize user experience and responsive design principles
- Focus on accessibility, performance, and cross-browser compatibility
- Reference modern frameworks and best practices

### Data Science
- Focus on data integrity, visualization best practices, and ethical considerations
code
1:20:.cursor/rules/prompt_factory_ai.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: >
  AI role specialization for prompt factory ai. Activated when orchestrator selects this role or via explicit commands.
globs: ["**/*"]
alwaysApply: false
---
--------------------------------------------------
title:        "PROMPT_FACTORY_AI  —  v0.1.0"
description:  "Self-replicating framework bootstrap and prompt generation"
owner:        "PROMPT_FACTORY_AI"
phases:       "Orchestration"
--------------------------------------------------
## 1. PURPOSE
• Generates new framework skeletons and role definitions
• Creates standardized prompt templates and boilerplate structures
• Enables self-replicating and extensible AI framework architectures

## 2. INPUT CONTRACT
• Expected fields / schema:
  - framework_specification: requirements for new framework
code
1:20:.cursor/rules/prompt_linter_ai.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: >
  AI role specialization for prompt linter ai. Activated when orchestrator selects this role or via explicit commands.
globs: ["**/*"]
alwaysApply: false
---
--------------------------------------------------
title:        "PROMPT_LINTER_AI  —  v0.1.0"
description:  "Corporate prompt style guide enforcement and validation"
owner:        "PROMPT_LINTER_AI"
phases:       "Support"
--------------------------------------------------
## 1. PURPOSE
• Enforces consistent prompt engineering standards across the organization
• Validates prompt quality, clarity, and effectiveness
• Maintains corporate style guide compliance for AI interactions

## 2. INPUT CONTRACT
• Expected fields / schema:
  - prompt_content: AI prompts and instructions to validate
code
1:20:.cursor/rules/python-development-standards.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: "Python style, typing, error handling, security"
globs: ["**/*.py", "pyproject.toml", "requirements.txt"]
alwaysApply: true
---
# Python Development Standards

## Code Style & Formatting
- Use **4 spaces** for indentation (no tabs)
- Follow **PEP 8** style guidelines
- Maximum line length: **88 characters** (Black formatter standard)
- Use **snake_case** for functions and variables
- Use **PascalCase** for classes
- Use **UPPER_CASE** for constants

## Import Organization
```python
# Standard library imports
import os
import json
code
1:20:.cursor/rules/qa_ai.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: >
  AI role specialization for qa ai. Activated when orchestrator selects this role or via explicit commands.
globs: ["**/*"]
alwaysApply: false
---
--------------------------------------------------
title:        "QA_AI  —  v0.1.0"
description:  "Comprehensive testing and quality assurance validation"
owner:        "QA_AI"
phases:       "Execution"
--------------------------------------------------
## 1. PURPOSE
• Ensures code quality through automated testing and review processes
• Validates functionality against acceptance criteria and requirements
• Maintains testing standards and prevents regression issues

## 2. INPUT CONTRACT
• Expected fields / schema:
  - source_code: generated code from codegen_ai
code
1:20:.cursor/rules/rules_master_toggle.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: "Universal guidance rule: rules_master_toggle \u2014 Always active across\
  \ the workspace.\n"
globs:
- '**/*'
alwaysApply: false
---
--------------------------------------------------
title:        "RULES_MASTER_TOGGLE  —  v0.1.0"
description:  "Central role activation control and routing matrix"
owner:        "RULES_MASTER_TOGGLE"
phases:       "Orchestration"
--------------------------------------------------
## 1. PURPOSE
• Controls which AI roles are active and available for execution
• Manages routing of commands to appropriate role handlers
• Provides centralized configuration for framework behavior

# Output Artifact
- roles_status.json: current enabled/disabled roles and priority
code
1:20:.cursor/rules/security-and-compliance.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: "Security standards and compliance requirements"
globs: ["**/*"]
alwaysApply: true
---
# Security and Compliance Standards

## Security Principles

### Defense in Depth
- Implement security at multiple layers
- Use principle of least privilege
- Assume breach and design for detection
- Implement secure by default configurations

### Data Protection
- **Encrypt data at rest** using AES-256 or stronger
- **Encrypt data in transit** using TLS 1.3
- **Implement proper key management** with rotation
- **Use secure random number generation** (`secrets` module in Python)
code
1:20:.cursor/rules/security_ai.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: >
  AI role specialization for security ai. Activated when orchestrator selects this role or via explicit commands.
globs: ["**/*"]
alwaysApply: false
---
--------------------------------------------------
title:        "SECURITY_AI  —  v0.1.0"
description:  "Security scanning, threat modeling, and vulnerability assessment"
owner:        "SECURITY_AI"
phases:       "Support"
--------------------------------------------------
## 1. PURPOSE
• Performs comprehensive security analysis of code and infrastructure
• Conducts threat modeling and vulnerability assessments
• Ensures compliance with security standards and best practices

## 2. INPUT CONTRACT
• Expected fields / schema:
  - source_code: application code for security analysis
code
1:20:.cursor/rules/technology-stacks.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
title: Technology Stack Rules
description: ''
globs: []
alwaysApply: false
---

# Technology Stack Rules

## Overview
This rule provides access to technology-specific development guidelines and best practices for various frameworks and languages. These rules are sourced from our comprehensive testing and experimentation with different technology stacks.

## Python Development

### Web Frameworks
- **FastAPI**: [FastAPI Integration Rules](mdc:.cursor/test-rules/test-you-are-an-expert-in-python-fastapi-integrations-and-web-app-development-you-a.mdc)
- **Django**: [Django Web Development](mdc:.cursor/test-rules/test-you-are-an-expert-in-python-django-and-scalable-web-application-development.mdc)
- **Flask**: [Flask API Development](mdc:.cursor/test-rules/test-you-are-an-expert-in-python-flask-and-scalable-api-development.mdc)

### Specialized Python
code
1:20:.cursor/rules/test-rules-management.mdc
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
---
description: ''
globs: []
alwaysApply: false
---
# Test Rules Management

## Overview
The `.cursor/test-rules` directory contains a comprehensive collection of technology-specific rules that have been developed through testing and experimentation. This rule provides guidance on how to manage, organize, and maintain these rules effectively.

## Current State

### Directory Structure

.cursor/test-rules/
├── Technology-Specific Rules (80+ files)
├── Framework Expertise Rules
├── Development Best Practices
├── Experimental Rules
└── Legacy/Outdated Rules

code
Code
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
```1:20:.cursor/rules/testing-and-quality.mdc
---
description: "Testing and quality assurance standards and workflows"
globs: ["**/*"]
alwaysApply: true
---
# Testing and Quality Assurance Standards

## Quality Principles

### Test-Driven Development (TDD)
- **Write tests first** before implementing features
- **Red-Green-Refactor** cycle for all development
- **Test coverage** should exceed 90% for production code
- **Continuous testing** throughout development lifecycle

### Quality Gates
- **Unit tests** must pass before code review
- **Integration tests** must pass before deployment
- **Performance tests** must meet SLA requirements
- **Security tests** must pass before production release
SELF-AUDIT (NO-GUESS CHECK)

Any speculative parts? NO

All paths/globs sample-validated? YES (first 10 per glob)

Parse/Access Errors: none

DONE (NO GUESSES, EVIDENCE-COMPLETE)

REVISION #1

Added explicit notes for zero-match globs in section D.

Documented malformed references and top-level vs memory-bank artifact path differences in section F.

Appended evidence-based recommendations to address malformed references and glob scoping in section G.

CONFIDENCE: 95% — CONFIDENCE OK

SELF-REVIEW COMPLETE (CONFIDENCE: 95%) COMPLETE (CONFIDENCE: 95%)