# Security Waiver/Exception Governance

## Policy
- Waivers allowed only for non-critical issues with time-bound expiry.
- Mandatory fields: id, rationale, owner, expiry_date, affected_component.

## Process
1) File a waiver in `security/waiver_db.json`.
2) Approval by Security Gov owner.
3) CI reads waivers and applies exceptions for matching findings.

