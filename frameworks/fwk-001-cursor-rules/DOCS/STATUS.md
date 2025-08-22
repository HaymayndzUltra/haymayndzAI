# Status

Policy mode
- Dev (advisory): AI_ENFORCEMENT_MODE=solo (WARN)
- CI/Prod (strict): AI_ENFORCEMENT_MODE=team (BLOCK) — default and required in CI

Current
- Legacy Cursor rules archived: legacy/.cursor-rules-archived
- Canonical policies: frameworks/fwk-001-cursor-rules/system-prompt/*
- Gates: BLOCK semantics per execution_orchestrator.mdc
- Examples present for all required artifacts

Open items (project-specific)
- Fill project goals and constraints into role INPUT contracts
- Confirm required_inputs per gate match project artifacts
- Decide optional roles to enable (security_ai, data_ai, etc.)

Checklists
- [ ] Roles customized
- [ ] Pipeline gates tailored
- [ ] Artifacts authored and linked
- [ ] CI guard for AI_ENFORCEMENT_MODE=team
