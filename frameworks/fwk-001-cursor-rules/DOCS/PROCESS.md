# Process — Documenting and Tracking Changes

Principles
- Canonical policy lives in system-prompt/*. DOCS mirrors those files for easy consumption.
- Every policy change must update both the source (.mdc) and the mirror (DOCS) in the same PR.

When changing roles or routing
- Edit system-prompt/rules_master_toggle.mdc
- Update DOCS/ROLES_MATRIX.md; note changes in DOCS/CHANGELOG.md

When changing pipeline or gates
- Edit system-prompt/execution_orchestrator.mdc
- Update DOCS/PIPELINE_AND_GATES.md; note changes in CHANGELOG

When changing artifacts
- Update examples/* or project artifacts
- Reflect requirements in DOCS/ARTIFACTS.md; note changes in CHANGELOG

Status tracking
- After any change, update DOCS/STATUS.md (what is current, what is pending)

Enforcement
- Dev (advisory): export AI_ENFORCEMENT_MODE=solo
- CI/Prod (strict): export AI_ENFORCEMENT_MODE=team (BLOCK)
- Add CI guard to fail if not strict in CI

Commit hygiene
- One logical change per commit; include references to files/sections modified
- Keep messages concise: what changed, why, and impact on gates
