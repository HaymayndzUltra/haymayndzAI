# Roles Matrix

Source: system-prompt/rules_master_toggle.mdc

Core roles
- product_owner_ai — triggers: /backlog, /prioritize, /refine — deps: []
- planning_ai — triggers: /plan, /architect, /estimate — deps: [product_owner_ai]
- codegen_ai — triggers: /gen_code, /implement, /refactor — deps: [planning_ai]
- qa_ai — triggers: /test, /review, /validate — deps: [codegen_ai]
- mlops_ai — triggers: /deploy, /rollback, /scale — deps: [qa_ai]

Support roles
- documentation_ai — triggers: /docs, /update_docs, /validate_docs — deps: [codegen_ai]
- analyst_ai — triggers: /review, /analyze, /benchmark — deps: []
- memory_ai — triggers: /snapshot, /recall, /learn — deps: []
- observability_ai — triggers: /observe, /alert, /health — deps: [mlops_ai]

Orchestration
- execution_orchestrator — triggers: /run_pipeline, /status, /halt — deps: []
- prompt_factory_ai — triggers: /new_framework, /extend_framework, /template — deps: []
- auditor_ai — triggers: /audit — deps: [planning_ai]
- principal_engineer_ai — triggers: /peer_review, /synthesize_plan — deps: [auditor_ai]

Routing highlights
- /plan → planning_ai
- /gen_code → codegen_ai
- /test → qa_ai
- /deploy → mlops_ai
- /audit → auditor_ai
- /peer_review, /synthesize_plan → principal_engineer_ai
- /run_pipeline → execution_orchestrator

---

Canonical repo paths and references
- Canonical roles matrix doc (this file): `frameworks/fwk-001-cursor-rules/DOCS/ROLES_MATRIX.md`
- Harvested system-prompt copy: `frameworks/fwk-001-cursor-rules/DOCS/harvested/selection_20250824_090835/fwk-001-cursor-rules/system-prompt/rules_master_toggle.mdc`
- Framework rule: `frameworks/fwk-001-cursor-rules/.cursor/rules/principal_engineer_ai.mdc` (validation mode)
- Routing changes directory: `frameworks/fwk-001-cursor-rules/DOCS/changes/`
