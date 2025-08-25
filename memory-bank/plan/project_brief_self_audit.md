# Project Brief: Comprehensive Self-Audit of the HaymayndzAI Framework

## Client Perspective
We are commissioning a comprehensive, end-to-end self-audit of the HaymayndzAI Framework. As an external client, our objective is to verify that the framework’s orchestration, role handoffs, gates, and memory subsystems operate cohesively, reliably, and safely across supported stacks.

## Mission Objectives
1) Analyze the framework’s own rules and capabilities and identify operational gaps, blind spots, and inconsistencies.
2) Validate gate behavior, role handoffs, and artifact generation across the full pipeline (backlog → plan → gen_code → test → deploy → observe), including audit/verification/synthesis phases.
3) Propose a robust, complete workflow with clear acceptance criteria, rollback steps, and traceable tasks.

## Source of Truth (Rules Directory)
- Primary rules directory (read-only reference): 
  - **Local environment:** `/home/haymayndz/HaymayndzAI/.cursor/rules/`
  - **AI workspace:** `/workspace/.cursor/rules/`
  - **Environment variable:** `$REPO_ROOT/.cursor/rules/` (recommended)
  - **Relative path:** `.cursor/rules/` (from project root)

## Required Artifacts (Deliverables)
- Summary_Report.md (audit findings; risks & alignments with evidence to rules/files)
- Validation_Report.md (principal engineer verdict; GO/NO-GO with rationale)
- Final_Implementation_Plan.md (only on GO; sequenced tasks with rollback and traceability)
- rule_attach_log.json (evidence of correct rule attachment across stacks)
- observability/alerts.yaml and observability/dashboards.mmd (lint/render cleanly)
- security_report.md (QA security checks integrated; High issues block)

## Scope
- End-to-end orchestration and gates enforcement
- Role routing and dependencies
- Memory bridge and storage layout; single-writer & atomic IO policies
- Docs generation and analysis collaboration flows

## Non-Goals
- Executing the audit now (this brief defines the work; execution to be triggered separately)
- Building application-specific features outside the framework itself

## Acceptance Criteria (Definition of Done)
- Risks are evidenced with file:line or section references to rules and code artifacts
- GO/NO-GO decision follows strict gating logic; synthesis only on GO
- Final_Implementation_Plan.md includes sources per task (Plan section / Risk ID / Validation section)
- Observability and security artifacts validate (YAML parses; Mermaid renders; High issues block)

## Constraints & Notes
- Treat the framework as a single addressed entity; the executing agent must resolve the correct handler and format
- Use environment-driven paths; avoid hardcoded absolutes in generated artifacts
- Maintain unbiased sessions for audit vs peer review

## Suggested Command Surface (for the executing agent)
- Begin with backlog/plan generation if missing; then draft Action_Plan.md
- Run audit to produce Summary_Report.md; then peer review to produce Validation_Report.md
- Only on GO, synthesize Final_Implementation_Plan.md

## Program: Framework Rules Migration & Enhancement (Client Scope)

- Goal: Migrate and enhance rules so per-stack guidance auto-attaches reliably, with no conflicts and measurable attach performance/coverage.
- In-Scope: `.cursor/frameworks/` consolidation; deconflict legacy `.cursor/test-rules/`; attach logging; coverage tests for React/Next, Vue/Nuxt, Angular, Svelte, Python(FastAPI/Django), PHP(Laravel), Node/Express, Go, Flutter, React Native.
- Out-of-Scope (this iteration): Java/Spring Boot, Rust, Unity, iOS/Swift, Shopify/WordPress (propose as P2).
- Artifacts:
  - `rule_attach_log.json` (per stack, with timestamps, mapping, and file markers)
  - Updated per-stack rule files with ≥20 actionable points (security, testing, performance)
  - Attach coverage tests (sample files per stack + expected attach map)
  - Observability configs: `observability/alerts.yaml`, `observability/dashboards.mmd`
  - `security_report.md` from QA checks
- Acceptance Criteria:
  - Attach coverage ≥ 1 sample per stack; 0 false positives for unrelated stacks
  - Attach latency P95 ≤ 200ms per check on local run
  - alwaysApply: false enforced; globs do not use generic `**/*` for matching; no conflicts with legacy rules
  - Security: High issues block at QA gate; Observability YAML parses and Mermaid renders
- Gates & Evidence:
  - Planning/Codegen/QA/Audit/Peer-review gates enforced
  - All findings cite file:line or section; attach evidence references to rules and logs
