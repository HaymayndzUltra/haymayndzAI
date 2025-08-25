## Implementation Guide

### Setup
1. Ensure `.cursor/rules` contains core roles and toggles.
2. Create framework rules under `.cursor/frameworks/**` (added in this repo).
3. Verify `guidance_phase_awareness.mdc` has `globs: ["**/*"]` and `alwaysApply: true`.

### Configuration Examples
```yaml
role_selection:
  strategy: task_context_matching
  mapping:
    - when: "*.tsx or next.config.* present"
      attach_rules: ["frameworks/frontend/react.mdc"]
```

### Testing Procedures
- Run small commits simulating different stacks; verify `rule_attach_log.json` entries.
- Trigger `/test` to generate `test_results.json` and security/architecture reports.

### Troubleshooting
- No rules attached: check glob patterns and file presence.
- Duplicate frameworks: orchestrator chooses first match; adjust mapping priority.

