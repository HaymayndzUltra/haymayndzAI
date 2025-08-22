# Consolidated Analysis Master Report

Repo: /home/haymayndz/HaymayndzAI
Generated: summary of VERIFICATION/* at merge time

## Status Summary

| Vertical       | Status | Findings Path                                 | Report Path                           |
|----------------|--------|-----------------------------------------------|----------------------------------------|
| orchestrator   | WARN   | VERIFICATION/orchestrator/findings.json       | VERIFICATION/orchestrator/report.md    |
| qa_gate        | WARN   | VERIFICATION/qa_gate/findings.json            | VERIFICATION/qa_gate/report.md         |
| routing        | WARN   | VERIFICATION/routing/findings.json            | VERIFICATION/routing/report.md         |
| memory         | WARN   | VERIFICATION/memory/findings.json             | VERIFICATION/memory/report.md          |
| docs_analyst   | WARN   | VERIFICATION/docs_analyst/findings.json       | VERIFICATION/docs_analyst/report.md    |
| deploy_obs     | WARN   | VERIFICATION/deploy_obs/findings.json         | VERIFICATION/deploy_obs/report.md      |

Note: Status is (n/a) where the findings.json does not yet set a PASS/WARN/FAIL status.

## Duplicates/Conflicts Scan

- Duplicates: none detected by collect_analysis.py
- Conflicts: none detected by collect_analysis.py

## Next Steps

1. Set each findings.json "status" to one of: PASS | WARN | FAIL
2. Update each report.md Status accordingly and link to concrete evidence
3. Raise follow-up tasks for any WARN/FAIL with concern tags from findings


