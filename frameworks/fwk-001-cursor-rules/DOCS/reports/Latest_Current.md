# Latest Current (last 3 days)

- Time window start: 2025-08-20
- Repo root: /home/haymayndz/HaymayndzAI

## Sources
- Git: frameworks/fwk-001-cursor-rules/DOCS/changes/git_changes.md
- Filesystem: frameworks/fwk-001-cursor-rules/DOCS/changes/fs_changes.md
- Labnotes: frameworks/fwk-001-cursor-rules/DOCS/changes/labnotes_changes.md
- Discrepancies: frameworks/fwk-001-cursor-rules/DOCS/changes/discrepancies.md

## Summary Snapshot
- Git commits found: 52
- Files touched (fs): 255
- Labnotes blocks: 73
# Latest Current (dry-run slice)

- Framework: fwk-001-cursor-rules
- Repo root: /workspace
- Progressive mode: OFF

## Gate Snapshot (names only)
- planning_gate
- code_generation_gate
- quality_assurance_gate
- deployment_gate
- audit_gate
- verification_gate
- synthesis_gate

## Routing Triggers (count)
- Triggers: 40

## Artifacts
- DOCS/changes/routing_baseline.json
- DOCS/changes/gates_baseline.json
- DOCS/changes/routing_override.yaml
- DOCS/changes/routing_effective.shadow.json


## Acceptance Gate Results
```json
{
  "routing_integrity": {
    "status": "FAIL",
    "details": [
      "Unknown role for trigger /toggle: rules_master_toggle"
    ]
  },
  "gates_parseable": {
    "status": "PASS",
    "details": []
  },
  "observability": {
    "status": "PASS",
    "details": []
  },
  "memory_integrity": {
    "status": "PASS",
    "details": []
  },
  "docs_updated": {
    "status": "PASS",
    "details": []
  }
}
```


## Acceptance Gate Results (after routing fix)
```json
{
  "routing_integrity": {
    "status": "PASS",
    "details": []
  },
  "gates_parseable": {
    "status": "PASS",
    "details": []
  },
  "observability": {
    "status": "PASS",
    "details": []
  },
  "memory_integrity": {
    "status": "PASS",
    "details": []
  },
  "docs_updated": {
    "status": "PASS",
    "details": []
  }
}
```


## Progressive ON (limited)
- Scope: /route only (no routing target changes)
- Acceptance: PASS (no regressions)


## Progressive Monitoring Snapshot (/route)
- Timestamp (UTC): 2025-08-23T12:36:37+00:00
- Status: WARN
- Progressive mode: True
- Allowlist: ['/route']
- Route target OK: False
- No routing drift: True
