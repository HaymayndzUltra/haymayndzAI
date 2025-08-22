### QA Gate Policy — codegen_ai ↔ qa_ai (Independent of Implementation)

#### Scope & Objective
- **Objective**: Define quality gating criteria, loop controls, and escalation/exit conditions for the `codegen_ai → qa_ai → QA Gate` segment, with loop-back to `codegen_ai` on FAIL.
- **Independence**: This policy specifies states, artifacts, and decisions without prescribing specific tools/CLIs or changing tests/models.

#### Inputs / Grounding
- **Workflow**: `PROPOSAL/proposal_3.md`
- **Gate context**: `frameworks/fwk-001-cursor-rules/system-prompt/execution_orchestrator.mdc`
- **Role specs**:
  - `frameworks/fwk-001-cursor-rules/system-prompt/codegen_ai.mdc`
  - `frameworks/fwk-001-cursor-rules/system-prompt/qa_ai.mdc`

### 1) Gate Decision Model
- **Gate Name**: `quality_assurance_gate`
- **Required evidence (artifacts)**:
  - **source_code**: snapshot reference or digest
  - **acceptance_criteria.json**: explicit, testable conditions
  - **test_results.json**: test outcomes (unit/integration/e2e)
  - **coverage_report.(json|html)**: overall and per-file metrics
  - **quality_assessment.md**: structured QA findings
  - Optional: security scan report, performance benchmark report

- **PASS (all must hold)**:
  - **All required artifacts present** and well-formed
  - **Tests**: 100% of executed tests pass
  - **Coverage**: ≥ 90% line coverage overall (from orchestrator context)
  - **Security**: No critical (or higher) vulnerabilities
  - **Performance**: Benchmarks meet stated criteria in acceptance_criteria.json
  - **No open critical quality violations** in quality_assessment.md

- **FAIL (any of the below)**:
  - Missing required artifacts, malformed, or stale relative to source snapshot
  - Any test failures, or coverage < 90%
  - Any critical security issue
  - Performance below acceptance thresholds
  - Critical design/quality violation recorded by QA

- **Decision Evidence**: PASS/FAIL decision references artifact digests, key metrics (coverage_pct, perf), and rule evaluations captured in `VERIFICATION/qa_gate/findings.json`.

### 2) Decision Matrix (Criteria → Evidence → Decision)
- **C1 Tests pass** → test_results.json → PASS if 100% pass; else FAIL
- **C2 Coverage threshold** → coverage_report → PASS if coverage_pct ≥ 90; else FAIL
- **C3 Security** → security report → PASS if no critical+; else FAIL
- **C4 Performance** → benchmark report → PASS if meets criteria; else FAIL
- **C5 QA critical findings** → quality_assessment.md → PASS if none; else FAIL
- **C6 Artifact integrity** → digests/timestamps → PASS if consistent; else FAIL

Decision rule: PASS iff C1∧C2∧C3∧C4∧C5∧C6; otherwise FAIL.

### 3) Loop Policy (FAIL → codegen_ai)
- **Entry**: On FAIL, control loops back to `codegen_ai` with structured findings.
- **Retry classification**:
  - **Retryable**: test failures, coverage shortfall, non-critical style/quality issues, minor performance shortfall
  - **Non-retryable (immediate escalation)**: critical security issues; missing or invalid acceptance criteria; invalid architecture; repeated identical FAIL with no meaningful code delta
- **Attempt cap (termination guarantee)**: max_attempts = 3 per component/feature
- **Backoff**: exponential schedule in seconds = [0, 60, 300] for attempts 1..3
- **Escalation**:
  - On non-retryable: escalate immediately to `product_owner_ai` (requirements) and optionally human operator
  - On exhaustion (attempt > max_attempts): escalate with summary and recommend `planning_ai` review
- **Early exit**: If a subsequent attempt satisfies all PASS criteria, exit loop and proceed forward in pipeline

### 4) Observability & Audit (QA Gate)
- **Decision record**: Each attempt produces a record in `VERIFICATION/qa_gate/findings.json`
- **Minimum audit fields**:
  - gate_id, component_id/subject, attempt, decision (PASS|FAIL), timestamp (ISO-8601 +08:00)
  - actor_role (qa_ai), inputs (artifact list with type/path/sha256), metrics (coverage_pct, test_counts, perf), rule_evaluations (per-criterion PASS/FAIL with reason)
  - loop_control (max_attempts, attempts_used, next_action, backoff_seconds), escalation (target/reason when applicable)
  - documentation_interaction (events on PASS/FAIL)
- **Retention**:
  - Keep all QA gate decision records for ≥ 30 days and ≥ last 10 attempts per component, whichever is greater
  - Store artifact digests to ensure immutability checks; do not duplicate large binaries

### 5) Documentation Interaction (PASS/FAIL)
- **On PASS**:
  - Trigger documentation update for release readiness (e.g., release notes, link to QA artifacts)
  - Ensure `quality_assessment.md` summarizes the final PASS and references artifact digests
- **On FAIL**:
  - Produce a concise `qa_feedback` section summarizing root causes, reproduction hints, and links to artifacts
  - If escalation occurs, include an executive summary and explicit requested decisions (accept risk, defer, or rework)

### 6) Risks & Controls
- **Infinite loop risk**: Eliminated by attempt cap and non-retryable classification
- **QA false pos/neg**: Require explicit evidence references and allow manual override with signed rationale in audit record
- **Drift (qa_ai vs codegen_ai)**: Detect via source snapshot/digest; identical digests across attempts with same failure class triggers escalation

### 7) Acceptance Alignment
- **PASS/FAIL unambiguous**: Enumerated criteria and decision rule
- **Termination guaranteed**: max_attempts with escalation; early exit on PASS
- **Audit & retention**: Fields and retention windows defined above