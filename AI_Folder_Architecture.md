AI Development System - Folder Architecture

Overview
This architecture separates universal AI agent behavior from technology-specific knowledge and project-scoped rules to enable precise, context-aware assistance. The system combines global orchestration (agents and guidance) with framework intelligence (React, Python, PHP, etc.) and can grow into a richer knowledge base via the proposed frameworks directory.

Folder Hierarchy & Purposes
### /workspace/.cursor/rules/ - AI Role System
Purpose: Core AI agent definitions and orchestration logic.
Contains: Specialized AI roles for analysis, code generation, QA, security; universal orchestrators and guidance.
Integration: Invoked across all frameworks via `execution_orchestrator.mdc`; shares memory via `memory_ai.mdc` and global guidance via `guidance_*.mdc`.
Auto-Apply: Universal rules use alwaysApply: true (e.g., orchestrator, memory, master toggle, guidance); role files are usually alwaysApply: false and activated by intent.

#### Individual Files:
- analyst_ai.mdc: Analysis and diagnostics role; activated when analysis, audit, or assessment is requested; consumes framework context but remains tech-agnostic.
- codegen_ai.mdc: Code synthesis and refactoring role; triggered when implementation or code edits are requested; respects project conventions and framework rules.
- qa_ai.mdc: Test generation and verification role; activated during validation, CI hints, or when asked to write tests.
- security_ai.mdc: Security review and threat modeling role; engaged explicitly or when security-related tasks are detected.
- execution_orchestrator.mdc: Universal orchestration for multi-step flows, handoffs between roles, and phased execution.
- memory_ai.mdc: Universal long/short-term memory bridge to carry key decisions and constraints across steps.
- guidance_*.mdc: Universal behavioral guardrails and operating principles applied globally.

### /workspace/.cursor/test/ - Framework Rules
Purpose: Technology-specific rule collection used to guide best practices, patterns, and guardrails per stack.
Contains: 100+ framework rules (e.g., React/Next.js, Python/Django, PHP/Laravel, Flutter/Dart, Go, Rust, etc.).
Integration: Auto-attached through globs on file types (e.g., `**/*.tsx`, `**/*.py`, `**/*.php`) and config files (e.g., `package.json`, `pyproject.toml`). These rules inform the AI roles with stack-specific conventions.
Auto-Apply: Context-specific (alwaysApply: false). Rules are attached when matching files are in focus or referenced.

Examples:
- rules-test-001-chrome-extension.mdc: Patterns and APIs for Chrome extensions; applies when extension manifests or JS files are present.
- rules-test-003-reactjs-nextjs.mdc: Component patterns, routing, data fetching, and performance guidance for React/Next.js; globs over TSX/JSX and Next config files.
- rules-test-026-python-django.mdc: Django project structure, apps, models, migrations, and settings patterns; globs over `**/*.py`, `requirements.txt`, and `pyproject.toml`.
- [100+ other framework rules]: Categorized by frontend (React/Vue/Svelte/Remix), backend (Node/Go/Rust/Python/PHP/Ruby/Java), mobile (React Native/Flutter), and database (SQL/Prisma/Postgres).

### /workspace/.cursor/frameworks/ - Framework Intelligence (Proposed)
Purpose: Curated, hierarchical knowledge base for technologies; enables deeper examples, cookbook-style snippets, and domain conventions separate from raw rules.
Contains: Organized subfolders by domain and framework with reference docs, examples, and supplementary rules.
Integration: Attached via targeted globs per framework; referenced by AI roles for richer, example-driven guidance without bloating base rules.
Auto-Apply: Context-driven; subfolders define precise globs for activation.

Proposed Structure
frameworks/
├── frontend/
│  ├── react-nextjs/        # Integration: TSX/JSX components, Next config; SSR/ISR patterns
│  ├── vue-nuxt/            # Integration: .vue files, Nuxt config; routing/layout patterns
│  └── angular/             # Integration: Angular workspaces, TS config; module/component patterns
├── backend/
│  ├── nodejs/              # Integration: Node services, Fastify/Express; env/config patterns
│  ├── python/              # Integration: FastAPI/Flask/Django; dependencies, structure, testing
│  └── php/                 # Integration: Laravel/WordPress; artisan/composer patterns
└── mobile/
   ├── react-native/        # Integration: Expo/bare RN; app.json, metro config, native modules
   └── flutter/             # Integration: Dart, pubspec; widget patterns, platform channels

Integration Matrix
- Orchestration: `.cursor/rules/execution_orchestrator.mdc` coordinates role activation and phase transitions (plan → code → test → review).
- Memory: `.cursor/rules/memory_ai.mdc` persists key constraints across folders; avoids repetition and maintains decisions.
- Framework Detection: `.cursor/test/*` rules auto-attach via globs that match active files and configs (e.g., TSX, pyproject, composer.json).
- Security: `.cursor/rules/security_ai.mdc` plus security-focused framework rules enforce secure defaults; works with `qa_ai.mdc` for verification.
- Domain Knowledge: Proposed `frameworks/*` folders store examples and conventions; globs keep attachment targeted to relevant workspaces.

Auto-Attachment Strategy
- Universal rules: `globs: ["**/*"]`, `alwaysApply: true`.
- Role rules: `globs: ["**/*"]`, `alwaysApply: false`; invoked when requested or inferred by task intent.
- Framework rules: specific globs by technology (e.g., React: `**/*.tsx`, `**/*.jsx`, `package.json`; Python: `**/*.py`, `requirements.txt`).

Usage Context
- When working in React/Next.js files, React rules attach to guide component patterns, routing, and performance.
- During planning or audits, `analyst_ai.mdc` activates to evaluate risks/assumptions and system design.
- During implementation, `codegen_ai.mdc` uses framework rules to generate idiomatic, testable code.
- During validation, `qa_ai.mdc` leverages framework conventions to propose tests and verify behavior.
- Security-sensitive tasks trigger `security_ai.mdc` alongside framework checks.

Migration Strategy
1) Normalize all `.mdc` files with YAML frontmatter (description, globs, alwaysApply) and remove filename comments.
2) Keep universal rules in `.cursor/rules` with `alwaysApply: true` where appropriate; role rules default to `false`.
3) Keep framework rules in `.cursor/test` with technology-specific globs.
4) Gradually promote curated examples and domain knowledge into the proposed `frameworks/` tree; define precise globs to avoid over-attachment.

