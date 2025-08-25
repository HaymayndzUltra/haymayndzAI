## Commands Demo — Role Triggers Reference

### Planning
```
/plan {"source":"memory-bank/plan/product_backlog.yaml"}
/plan --action-plan {"source":"memory-bank/plan/product_backlog.yaml"}
/architect {"feature":"auth"}
/estimate {"task":"BL-005"}
```

### Audit & Validation
```
/audit {"source":"memory-bank/plan/Action_Plan.md","context":["memory-bank/plan/technical_plan.md","memory-bank/plan/task_breakdown.yaml"],"outputs":{"report":"memory-bank/plan/Summary_Report.md"}}
/peer_review {"source":"memory-bank/plan/Summary_Report.md","plan":"memory-bank/plan/Action_Plan.md","outputs":{"report":"memory-bank/plan/Validation_Report.md"}}
/synthesize_plan {"source":"memory-bank/plan/Action_Plan.md","audit":"memory-bank/plan/Summary_Report.md","validation":"memory-bank/plan/Validation_Report.md","outputs":{"plan":"memory-bank/plan/Final_Implementation_Plan.md"}}
```

### Codegen & QA
```
/gen_code
/test {"phase":"security","outputs":{"report":"security_report.md"}}
/review {"component":"api"}
/validate {"feature":"BL-006"}
```

### Security & Observability
```
/security_scan
/threat_model {"component":"auth"}
/compliance_check
/observe
/alert {"condition":"HighErrorRate"}
/health
```

### Memory & Data
```
/snapshot {"summary":"Sprint wrap"}
/recall {"query":"decision"}
/learn {"insight":"Attach latency tuning"}
/design_schema
/create_migration
/optimize_queries
```

### Orchestration & Others
```
/run_pipeline
/status
/halt
/resume
/toggle codegen_ai on
/route /gen_code
/lint_prompts
/check_style {"file":".cursor/rules/codegen_ai.mdc"}
/suggest_improvements
/new_framework backend/java
/extend_framework mobile/ios
/template planning_ai
/mem_audit repo
/planner_mode on
/bridge_sync
/hybrid_execute /gen_code
/memory_context
/docs
/update_docs {"component":"orchestrator"}
/validate_docs
```

