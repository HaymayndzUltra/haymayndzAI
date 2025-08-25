## Folder: /frameworks

Purpose: Houses framework packages; currently includes `fwk-001-cursor-rules` (a comprehensive Cursor multi-agent framework).

### /frameworks/fwk-001-cursor-rules
- README.md, QUICK_START.md: How to enable roles, run pipelines, and customize inputs.
- SYSTEM_FOLDER_TREE.md, ACCURATE_FOLDER_TREE.md: Structure maps.
- contracts/, schemas/: Contracts and schema validations.
- system-prompt/: Core role prompts (product_owner_ai, planning_ai, codegen_ai, qa_ai, documentation_ai, memory_ai, mlops_ai, observability_ai, prompt_factory_ai). Optional roles under `OPTIONAL/`.
- security/: Access policies (`access_policies.md`, `acl.json`), validation utilities (`validate_security_config.py`).
- routing/: Command routing artifacts.
- governance/: Ownership matrix and acceptance checklists.
- sync/: Concurrency, lease design, sync docs.
- observability/: Dashboards, alerts definitions.
- tests/: Pytest config, unit tests for schema validation.
- promotion/, hydration/, examples/: Supporting materials for adoption and hydration.

Integration Notes:
- This framework aligns with `/.cursor/rules` roles and extends with governance and security.
- Use QUICK_START.md to quickly activate a minimal pipeline, then opt-in advanced modules.