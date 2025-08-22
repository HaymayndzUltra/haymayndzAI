# Pipeline and Gates

Source: system-prompt/execution_orchestrator.mdc

Pipeline (simplified)
- product_owner_ai → planning_ai → auditor_ai → principal_engineer_ai → codegen_ai → qa_ai → mlops_ai → observability_ai
- documentation_ai, analyst_ai can operate in parallel where applicable.

Gates (BLOCK semantics)
- planning_gate
  - required_inputs: product_backlog.yaml
  - blocking: missing_requirements, invalid_architecture
- code_generation_gate
  - required_inputs: technical_plan.md, task_breakdown.yaml
  - blocking: compilation_errors, missing_tests
- quality_assurance_gate
  - required_inputs: source_code, acceptance_criteria.json
  - blocking: test_failures, security_issues, performance_degradation
  - exit_criteria: PASS
- deployment_gate
  - required_inputs: validated_code, deployment_config
  - blocking: failed_health_checks, missing_monitoring
- audit_gate
  - required_inputs: technical_plan.md, Action_Plan.md
  - output: Summary_Report.md
  - blocking: missing_Summary_Report, untraceable_findings, ambiguous_verdict
- verification_gate
  - required_inputs: Action_Plan.md, Summary_Report.md
  - output: Validation_Report.md
  - blocking: missing_Validation_Report, unresolved_contested_findings
- synthesis_gate
  - required_inputs: Action_Plan.md, Summary_Report.md, Validation_Report.md
  - output: Final_Implementation_Plan.md
  - blocking: missing_Final_Implementation_Plan, missing_traceability, no_rollback_for_high_risk

States
- IDLE, PLANNING, DEVELOPMENT, TESTING, DEPLOYMENT, MONITORING, BLOCKED, ROLLBACK, AUDIT, VALIDATION, SYNTHESIS

Error handling (selected)
- gate_failure: BLOCK
- critical_error: HALT_PIPELINE (rollback=true)
- verification_conflict: ESCALATE
