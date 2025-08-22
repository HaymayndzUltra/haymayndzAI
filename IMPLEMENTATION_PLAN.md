# Final Implementation Plan

## Phase 1: Foundational Hardening and Tooling Setup

- [ ] 1.1 Define and publish orchestrator "critical transitions" and guards (state diagram + handlers list).
- [ ] 1.2 Define telemetry schema (dual timestamps: `event_time_utc` ISO8601 Z, `event_time_local` `+08:00`) and `correlation_id` (128-bit hex).
- [ ] 1.3 Publish versioned JSON Schemas for: `VERIFICATION/*/findings.json`, `VERIFICATION/summary.json`, `monitoring_config.json`, telemetry events.
- [ ] 1.4 Define docs freshness SLO (update ≤48h after public API change; block after 72h) and enforcement action.
- [ ] 1.5 Finalize `acceptance_criteria.json` (env profile, dataset, p50/p95/p99, variance, warm/cold policy).
- [ ] 1.6 Add CI schema-validation jobs for all new schemas.
- [ ] 1.7 Implement centralized config with RBAC: `MEMORY_WRITES_MODE={direct|atomic|dual_write|bridge}`, `AI_ENFORCEMENT_MODE={solo|shadow|soft_block|hard_block}`.
- [ ] 1.8 Implement waiver workflow with expiry in `memory-bank/decisions/index.jsonl` and CI enforcement.
- [ ] 1.9 Configure disk quotas/retention checks for state/queue/report directories; CI guard for free-space thresholds.

---

## Phase 2: Memory Subsystem Remediation (with Safety Flags)

- [ ] 2.1 Implement `lib/atomic_io.py` with unit/integration tests on ext4/overlayfs; document NFS unsupported.
- [ ] 2.2 Provide watcher adapters and guidance (rename-aware and in-place-aware).
- [ ] 2.3 Apply atomic writes to `VERIFICATION/master_report.md`, `VERIFICATION/summary.json`, and each vertical's `findings.json`; include directory `fsync`.
- [ ] 2.4 Serialize concurrent report updates (repo-wide mutex try-lock + timeout) or queue via bridge.
- [ ] 2.5 Implement the single-writer bridge (API: idempotent append, monotonic sequence; durability: disk-backed queue; retries; DLQ; backpressure; HA or client circuit-breaker fallback).
- [ ] 2.6 Add bridge metrics/health (queue depth, lag, error rates) and dashboards/alerts.
- [ ] 2.7 Stage rollout of memory writes:
  - [ ] 2.7.1 Set `MEMORY_WRITES_MODE=direct` baseline.
  - [ ] 2.7.2 Promote to `atomic` in dev; validate ext4/overlayfs; provide rollback toggle to `direct` on failure.
  - [ ] 2.7.3 Enable `dual_write` (direct + bridge) with divergence monitoring and alerts on mismatch >0.
  - [ ] 2.7.4 Switch to `bridge` after 2 weeks clean; remove remaining direct writers.
- [ ] 2.8 Implement DR: periodic snapshots for memory and reports with defined RPO/RTO; test restore; enable streaming reads for archives.
- [ ] 2.9 Migrate readers/watchers to support rename semantics; dual-read during migration; deprecate direct reads; alert on stragglers.

---

## Phase 3: QA Gate Remediation and CI Hardening

- [ ] 3.1 Enforce coverage thresholds: ≥90% line, ≥80% branch; per-module floors; fail regressions >2%.
- [ ] 3.2 Produce and publish `test_results.xml` and `coverage.xml`; gate on thresholds.
- [ ] 3.3 Add security scan with policy/waivers + expiry (`.trivyignore`); store `security_report.json`; gate on HIGH/CRITICAL (post-waiver rules).
- [ ] 3.4 Implement performance CI job pinned to `acceptance_criteria.json` (assert p95 and variance vs baseline with confidence intervals/trend windows).
- [ ] 3.5 Add cross-vertical integration tests: routing matrix invariants; orchestrator transitions/guards (mirror sync); memory (atomic & bridge); docs promotion/provenance gates; deploy/obs health.
- [ ] 3.6 Require 3 consecutive green CI runs (including integration) before enforcement escalation.

---

## Phase 4: Documentation, Deployability, and Observability Tightening

- [ ] 4.1 Orchestrator: enumerate and test "critical transitions"; target ≥90% coverage for handlers and guards.
- [ ] 4.2 Docs analyst: add provenance lint pre-promotion; scheduled freshness SLO check with breach ticket and promotion block after 72h.
- [ ] 4.3 Deploy/observability: JSON schema validation for `monitoring_config.json`; CI smoke health check (`/health`).
- [ ] 4.4 Telemetry enforcement: dual timestamps (UTC + +08:00) and `X-Correlation-Id` propagation across services.
- [ ] 4.5 Observability: monitors for atomic write failures, report-update latency, disk utilization; alerts tied to enforcement mode SLOs.

---

## Phase 5: Artifact Integrity, SBOM, and Supply Chain Security

- [ ] 5.1 Generate SPDX SBOM (`sbom.spdx.json`) and sha256 digests for images, manifests, configs; include commit SHA.
- [ ] 5.2 Sign artifacts and create attestations with Cosign; verify signatures and attestations in CI.
- [ ] 5.3 Produce and publish `artifact_digests.json`; store alongside build artifacts.

---

## Phase 6: Concurrency-Safe Reporting and Governance

- [ ] 6.1 Route all PASS flips via bridge queue or protected mutex; ensure serialized processing.
- [ ] 6.2 Apply atomic updates for `VERIFICATION/master_report.md` and `VERIFICATION/summary.json` with directory `fsync`; add CI guard rejecting non-atomic writes.
- [ ] 6.3 Enforce RBAC for toggles, waivers, enforcement changes; audit to `memory-bank/decisions/index.jsonl`; alert on unauthorized attempts.

---

## Phase 7: Enforcement Mode Escalation

- [ ] 7.1 Progress `AI_ENFORCEMENT_MODE`: `solo` → `shadow` (report-only) → `soft_block` (override via expiring waivers) → `hard_block` after 3 consecutive greens (incl. integration suites).
- [ ] 7.2 Provide emergency override with expiring, signed waivers (RBAC enforced and logged).

---

## Phase 8: Verification and Close-out

- [ ] 8.1 For each vertical: re-run verification, update `findings.json`, prepend Status/Rationale in `report.md`, and flip to PASS.
- [ ] 8.2 Atomically refresh `VERIFICATION/master_report.md` and `VERIFICATION/summary.json` via the reporting pipeline.
- [ ] 8.3 When all verticals PASS and enforcement is `hard_block`: freeze reports; append closing decision entries to `memory-bank/decisions/index.jsonl`; publish runbook/checklist in `README` (commands, rollbacks, waivers, contacts).