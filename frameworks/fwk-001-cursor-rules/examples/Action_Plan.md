Phase 1: Foundational Integrity Testing
Command Surface Sanity
Purpose: Verify that all routed commands exist and map to the correct roles.
Specific Items to Test: /backlog, /prioritize, /refine, /plan, /architect, /estimate, /gen_code, /implement, /refactor, /test, /review, /validate, /deploy, /rollback, /scale, /docs, /update_docs, /validate_docs, /analyze, /benchmark, /snapshot, /recall, /learn, /observe, /alert, /health, /run_pipeline, /status, /halt, /new_framework, /extend_framework, /template, /toggle, /route, /design_schema, /create_migration, /optimize_queries, /security_scan, /threat_model, /compliance_check, /planner_mode.
Expected Outcome: Command-to-role mapping equals system-prompt/rules_master_toggle.mdc matrix; DOCS/changes/routing_effective.shadow.json aligns with baseline; conflicts report is empty.
Role Activation Matrix Integrity
Purpose: Ensure roles toggling and dependencies behave as defined.
Specific Items to Test: Enabling/disabling roles via /toggle, ordering of priorities, dependency enforcement for planning_ai → codegen_ai → qa_ai → mlops_ai; optional roles default disabled behavior.
Expected Outcome: roles_status.json reflects toggles; dependent commands fail gracefully when prerequisites disabled; re-enable restores behavior.
Schema Conformance: Artifact Sidecar
Purpose: Guarantee artifacts adhere to schemas/artifact.schema.json.
Specific Items to Test: Required fields, types, regex patterns, enum values; file readability/encoding/size bounds; validation performance.
Expected Outcome: Valid examples pass; invalid examples fail with actionable errors; perf thresholds met (<2ms avg synthetic; <5ms avg real).
Routing Files and Utilities
Purpose: Validate artifact routing and conflict detection.
Specific Items to Test: routing/resolve_artifact_path.py deterministic pathing; check_routing_conflicts.py report and exit code; artifact_routing.json shape.
Expected Outcome: Correct path resolution for each artifact type; conflicts report shows “No conflicts detected”; non-existent type raises KeyError.
Configuration Baseline and Hydration
Purpose: Validate hydration selector and rules.
Specific Items to Test: hydration/hydration_selector.py, hydration_tests.yaml, run_hydration_tests.py.
Expected Outcome: All hydration tests pass; selector chooses correct config by scenario.
Observability Config Static Checks
Purpose: Ensure dashboards, alerts, and audit logs are syntactically valid.
Specific Items to Test: observability/alerts.yaml, dashboards.mmd, audit_logs.md format.
Expected Outcome: YAML parses; Mermaid renders; no broken anchors.
Security Configuration Validation
Purpose: Confirm security policies are valid and enforceable.
Specific Items to Test: security/validate_security_config.py against security/acl.json and security/access_policies.md.
Expected Outcome: Validator returns success; violations produce clear, line-localized errors.
Phase 2: Workflow and Integration Testing
Core Sequential Workflow: Requirements to QA
Purpose: Validate end-to-end handoffs and gate checks up to QA.
Specific Items to Test: /backlog → /plan → /gen_code → /test; ensure creation of product_backlog.yaml, technical_plan.md, task_breakdown.yaml, test_results.json; planning gate must pass before code generation.
Expected Outcome: Artifacts are generated in correct locations; gate validations per execution_orchestrator.mdc succeed; handoff_log contains expected transitions.
Extended Pipeline: Audit, Validation, and Synthesis
Purpose: Verify newly added phases and gates.
Specific Items to Test: /audit produces Summary_Report.md; /peer_review produces Validation_Report.md; synthesis yields Final_Implementation_Plan.md.
Expected Outcome: Audit, verification, and synthesis gates pass with required inputs; blocking conditions enforced; failure scenarios re-route appropriately.
Deployment and Observability
Purpose: Validate deployment gate and post-deploy observability.
Specific Items to Test: /deploy produces deployment_manifest.yaml; /observe, /health, /alert operations; monitoring artifacts creation.
Expected Outcome: Deployment gate passes; health checks succeed; monitoring artifacts are created and valid.
Documentation and Analyst Collaboration
Purpose: Confirm doc generation and analysis workflows.
Specific Items to Test: /docs, /update_docs, /validate_docs; /review, /analyze, /benchmark interactions.
Expected Outcome: Documentation artifacts generated and validated; analysis produces expected reports without breaking main pipeline.
Memory Bridge Integration
Purpose: Validate framework_memory_bridge mappings into tools/memory.
Specific Items to Test: /snapshot, /recall, /learn mapping and execution; bridge_sync synchronization to memory-bank/queue-system files; environment variable MEMORY_STORAGE_ROOT handling.
Expected Outcome: Memory CLI commands execute; storage layout correct; sync reports produced; no divergence between systems.
Sync and Promotion Flows
Purpose: Validate artifact index, concurrency, and promotion snapshotting.
Specific Items to Test: sync/index_writer.py and enhanced_index_writer.py CRUD and lock handling; promotion/snapshot_cli.py and promotion_rules.mdc.
Expected Outcome: No deadlocks; index updates are atomic; snapshots created and restorable.
Phase 3: Robustness and Advanced Capabilities Testing
Error Handling and Recovery Paths
Purpose: Exercise orchestrator error matrix.
Specific Items to Test: Gate failures, role timeouts, critical errors, dependency failures, audit failures, verification conflicts, synthesis incomplete; /halt, /resume.
Expected Outcome: States transition to BLOCKED/HALT as defined; backoff/retry policies honored; alerts emitted; rollback triggered when configured.
Routing Overrides and Progressive Mode
Purpose: Validate DOCS/changes/routing_override.yaml and effective routing shadow.
Specific Items to Test: Apply overrides for a subset (/route, /status, /health, /observe, /alert, /benchmark, /analyze, /review, /validate_docs); ensure .bak rollback works.
Expected Outcome: Effective routing updates match override; rollback restores baseline; conflicts report remains clean.
Performance and Concurrency
Purpose: Validate performance SLAs and concurrent operations.
Specific Items to Test: Pytest durations; coverage thresholds; sync/test_concurrency.py scenarios; promotion snapshot throughput.
Expected Outcome: Coverage ≥ 80%; top 10 durations under thresholds; concurrency tests pass; no race conditions or file lock contention.
Security Posture Tests
Purpose: Ensure security gates and scanners integrate safely.
Specific Items to Test: /security_scan, /threat_model, /compliance_check; Bandit/Safety runs; access policy checks.
Expected Outcome: No high/critical issues; violations block pipelines with clear guidance.
Planner-first Mode and Toggles
Purpose: Validate safety features of planner-first.
Specific Items to Test: /planner_mode on|off, confirmation requirements, restricted actions without confirmation.
Expected Outcome: In planner-first mode, actions require explicit confirmation; logs record confirmations; turning off restores default behavior.
Disaster Recovery and Rollback Rehearsal
Purpose: Validate rollback playbook and rehearsal utilities.
Specific Items to Test: promotion/rollback_rehearsal.py; promotion/rollback_playbook.md checklists.
Expected Outcome: Simulated rollback succeeds; all artifacts restored; health checks pass post-rollback.
Notes and Gaps Addressed vs Draft:
Added many commands missing from the draft (e.g., /prioritize, /refine, /architect, /estimate, /implement, /refactor, /rollback, /scale, /update_docs, /validate_docs, /analyze, /benchmark, /health, /new_framework, /extend_framework, /template, /design_schema, /create_migration, /optimize_queries, /security_scan, /threat_model, /compliance_check, /planner_mode, /halt, /resume).
Included Audit/Verification/Synthesis phases and gate enforcement.
Covered memory bridge integration with tools/memory.
Added routing overrides testing, hydration, sync/promotion, security validations, and concurrency.
Explicit artifacts and pathing validation, including schema conformance and routing utilities.
Performance thresholds and coverage requirements per pytest.ini.