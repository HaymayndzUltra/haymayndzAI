# Artifacts

Required by gates and roles.

Action_Plan.md (input to auditor_ai)
- Sections: Objectives, Phases, Assumptions, Risks, References
- Type: Diagnostic or Operational (declare explicitly)

Summary_Report.md (output of auditor_ai)
- Sections: Context Summary, Critical Risks (R-###), Blind Spots, Assumptions, Ambiguities, Consistency Issues, Compliance/Feasibility/Timeline/Scope, Traceability, Verdict
- Requirements: exact citations/traceability for each claim

Validation_Report.md (output of principal_engineer_ai)
- Sections: Scope & Context, Validated Findings (CONFIRM/CHALLENGE), Contested Findings, New Risks (NEW-RISK-###), Coverage Summary, Verdict
- Rules: do not delete contested risks; label new risks explicitly

Final_Implementation_Plan.md (output of principal_engineer_ai synthesis)
- Sections: Objectives & Scope, Assumptions & Constraints, Work Breakdown (tasks with owner/inputs/outputs/prereqs/priority/source refs), Execution Phases (entrance/exit), Rollback & Recovery, Risk-to-Task Mapping, Observability & Validation, Appendix (Traceability)

Acceptance mapping
- Audit gate passes when Summary_Report.md exists and is complete.
- Verification gate passes when Validation_Report.md exists with decisions.
- Synthesis gate passes when Final_Implementation_Plan.md exists with traceability.

Templates
- See frameworks/fwk-001-cursor-rules/examples/* for examples of each artifact.
