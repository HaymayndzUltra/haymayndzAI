## Decision Guide: Integration vs. New Repo

Use these inventories to decide:

- /.cursor/rules (universal) + /.cursor/test (framework):
  - If you need Cursor-native orchestration and auto-attach by stack → KEEP and refine globs/descriptions.
  - If you want a clean separation per client → mirror subsets into a new repo as a rules package.

- /frameworks/fwk-001-cursor-rules:
  - Comprehensive; includes governance/security/tests.
  - If adopting full process (audit → verify → synthesize) → INTEGRATE as submodule.
  - If you only need prompts → extract `system-prompt/` into your `.cursor/rules` and keep references to docs.
  - Templates: see `/.cursor/templates/CLIENT_ONBOARDING_CHECKLIST.md`, `/.cursor/templates/QA_WORKFLOW_TEMPLATE.md`.

- /memory_system + /memory-bank + /storage/memory:
  - If you need learning/retrieval across projects → INTEGRATE all three; ensure `kb.index.faiss` lifecycle.
  - If per-project isolation is required → create project-scoped storage roots; keep bridge mappings.

- /src/repo and /tools:
  - If orchestration scripts are shared infra → KEEP centralized.
  - If you plan to publish SDK-like utilities → SPIN OUT `/src/repo` + selected `/tools` into a Python package.

Next actions:
- Start with `FRAMEWORKS.md` and `CURSOR_RULES.md` to pick the orchestration layer.
- Decide storage policy (shared vs per-project) from `STORAGE_MEMORY.md`.
- If going multi-repo: create a template repo containing `.cursor/rules`, minimal `/tools`, and `memory` schema.