# Overview

This framework defines a multi‑role, gate‑driven workflow for AI‑assisted development.

Core concepts
- Roles: product_owner_ai, planning_ai, codegen_ai, qa_ai, mlops_ai, documentation_ai, analyst_ai, memory_ai, observability_ai, auditor_ai, principal_engineer_ai, execution_orchestrator, prompt_factory_ai.
- Routing: commands (e.g., /backlog, /plan, /gen_code, /test, /deploy, /run_pipeline) are mapped to roles via rules_master_toggle.mdc.
- Gates (BLOCK semantics): planning, code_generation, quality_assurance, deployment, audit, verification, synthesis.
- Artifacts: Action_Plan.md → Summary_Report.md → Validation_Report.md → Final_Implementation_Plan.md.

Lifecycle (high-level)
1) Backlog and planning (/backlog → /plan)
2) Audit and validation (/audit → /peer_review)
3) Synthesis (/synthesize_plan → Final_Implementation_Plan.md)
4) Execute pipeline (/run_pipeline) with gates enforcing required inputs and blocking conditions.

Environment policy
- Dev (advisory): AI_ENFORCEMENT_MODE=solo (WARN)
- CI/Prod (strict): AI_ENFORCEMENT_MODE=team (BLOCK)

References
- system-prompt/rules_master_toggle.mdc — roles, triggers, routing
- system-prompt/execution_orchestrator.mdc — pipeline, gates, handoffs, states
- examples/* — artifact templates and examples


