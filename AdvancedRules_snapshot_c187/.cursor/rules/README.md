# .cursor/rules/

- Purpose: Rule system for orchestrators, roles, domains, kits, and templates.

## Layout
- roles/: machine-consumable role rules (no non-empty `globs`, not `alwaysApply: true`)
- orchestrator/: high-level coordination docs
- domains/: technology stacks and utilities
- kits/: prestart and upwork kits
- indexes/, advanced/, templates/: supporting rules

## Governance
- Validate role policies:
```bash
python3 tools/rules/validate.py
```