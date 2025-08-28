Status: PASS

### Deployment → Observability Contract Summary (mlops_ai → observability_ai)

**Scope**: Define deployment outputs consumed by observability after QA Gate PASS. Excludes creating dashboards/alerts/pipelines or changing CI/CD.

## Rationale
- Versioned contract and required artifacts enumerated, including hashes and owners (Contract section).
- Health/readiness and rollback signals are explicit and testable with simulate hooks (Health & Readiness; Rollback Signals).
- Telemetry events and common fields defined with +08:00 timestamp requirement (Telemetry Events).
- Post-deploy validation steps map to orchestrator transitions (Post‑Deploy Validation & Orchestrator Transitions).
- Risks and mitigations address format mismatches, blind spots, and observability of rollback.

#### Contract
- **Versioning**: schema_version=1.0.0; producer=mlops_ai; consumer=observability_ai
- **Artifacts**:
  - `deploy/deployment_manifest.yaml` (env, version, rollout_strategy, services, images[git_sha, tag], config)
  - `deploy/monitoring_config.json` (metrics list; references for dashboards/alerts only)
  - `deploy/release_report.md` (status, timestamps, env, version, notes)
- **Build metadata**: git_sha, git_ref, artifact_registry, timestamp (+08:00)

#### Health & Readiness
- Heartbeat: GET /health → 200 {status:"ok"}; interval=10s, timeout=2s, success_threshold=3, failure_threshold=3, grace=30s
- Readiness: e.g., migrations applied (timeout=120s, retries=3)
- Blind-spots: pre-health gap 15s; canary 5% for ≥300s

#### Rollback Signals (observable & testable)
- canary_error_rate_exceeds_threshold: http.server.errors.rate > 2% (5m) → action=ROLLBACK
- healthcheck_failure_breach: breach of failure_threshold during canary/steady-state → action=ROLLBACK
- Emit hook topic: `observability/deploy/rollback`; event `rollback.requested` includes service, env, version, reason, observed(metric/value/window), correlation_id, timestamp (+08:00)

#### Telemetry Events
- deploy.started, deploy.completed, health.ok, health.failed, canary.started, canary.completed, rollback.requested, rollback.completed
- Common fields: correlation_id, task_id, phase_index, environment, version, timestamp

#### Post‑Deploy Validation & Orchestrator Transitions
- Step: heartbeat_endpoints_pass → pass: DEPLOYMENT→MONITORING; fail: DEPLOYMENT→ROLLBACK
- Step: canary_window_complete → pass: increase traffic/finalize; fail: DEPLOYMENT→ROLLBACK
- Gates:
  - DEPLOYMENT→MONITORING iff all health checks pass and no rollback signals active
  - DEPLOYMENT→ROLLBACK if any rollback signal triggers

#### Risks & Mitigations
- Format mismatches → versioned schema + JSON schema validation + artifact hashes
- Blind spots pre‑health → grace window + canary gating
- Rollback not observable → explicit emit hook + event schema

Acceptance: contract fields complete/versioned; health & rollback signals unambiguous/testable; validation steps declared and tied to orchestrator transitions.