# Security Report

## Summary
- High: 0
- Medium: 2
- Low: 0

## Dependency Audit (stub)
- N/A (lockfile not found or audit tool not integrated in baseline)

## Findings
- [MEDIUM] Possible SQL query string concatenation — /workspace/scripts/advanced_rule_integrator.py:513 — f"selection_{ts}",
- [MEDIUM] Possible SQL query string concatenation — /workspace/tools/security_scan.py:45 — ("MEDIUM", r"(SELECT\s+.*\+\s*\w+|f\"SELECT.*\{|format\(.*SELECT|\%s.*SELECT)", "Possible SQL query string concatenation"),
