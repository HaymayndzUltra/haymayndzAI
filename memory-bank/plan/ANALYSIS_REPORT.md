# Common-Sense Plan vs Codebase Analysis (Human-Readable)

This analysis assumes `tasks_active.json` mirrors `organize.md`. It flags likely conflicts/missing items based on the plan’s contracts. Confirm/adjust as needed.

## Phase 1 — Foundational Hardening and Tooling Setup
- Checks
  - Critical transitions/guards enumerated and testable
  - Telemetry schema: `event_time_utc` (ISO8601 Z), `event_time_local` (+08:00), `correlation_id` (128-bit)
  - Versioned JSON Schemas: `VERIFICATION/*/findings.json`, `VERIFICATION/summary.json`, `monitoring_config.json`
  - Docs freshness SLO policy and CI lint
  - Centralized config + RBAC: `MEMORY_WRITES_MODE`, `AI_ENFORCEMENT_MODE`
- Potential issues
  - Missing concrete schema files or field-level versions
  - RBAC not enforced across toggles
  - Docs SLO not wired to CI

## Phase 2 — Memory Subsystem Remediation (with Safety Flags)
- Checks
  - `lib/atomic_io.py` with tests on ext4/overlayfs; NFS unsupported
  - Watcher adapters for rename vs in-place
  - Atomic writes with directory fsync for reports
  - Bridge: idempotent append, monotonic sequence, disk durability, retries/DLQ/backpressure
  - Rollout: direct → atomic → dual_write (divergence=0) → bridge
  - DR: snapshots/restore; streaming reads
- Potential issues
  - Missing bridge persistence queue / metrics
  - No divergence monitor for dual_write
  - Readers not adapted for rename semantics

## Phase 3 — QA Gate Remediation and CI Hardening
- Checks
  - Coverage ≥90% line, ≥80% branch; per-module floors; ≤2% regression
  - Trivy scan with waivers + expiry; `security_report.json`
  - Perf CI pinned to `acceptance_criteria.json` (p95 + variance)
  - Cross-vertical integration tests (routing, orchestrator transitions, memory, docs, deploy/obs)
- Potential issues
  - Missing perf harness or pinned env/data/seeds
  - Waiver ledger not enforced with expiry

## Phase 4 — Documentation, Deployability, and Observability Tightening
- Checks
  - Orchestrator critical transitions tests (≥90% handlers/guards)
  - Docs provenance lint; freshness SLO enforcement (block after 72h)
  - `monitoring_config.json` schema validation
  - Telemetry dual-stamp + `X-Correlation-Id` propagation
  - Monitors/alerts mapped to enforcement SLOs
- Potential issues
  - Incomplete docs provenance fields or missing CI hook
  - Healthcheck not standardized

## Phase 5 — Artifact Integrity, SBOM, Supply Chain
- Checks
  - SPDX SBOM with commit SHA; sha256 digests
  - Sign + attest (Cosign) and verify in CI
  - Publish `artifact_digests.json`
- Potential issues
  - Missing signing keys/config
  - SBOM not verified or not attached to builds

## Phase 6 — Concurrency-Safe Reporting & Governance
- Checks
  - PASS flips serialized via bridge/mutex
  - Atomic updates + dir fsync for master/summary
  - RBAC/audit for toggles/waivers/enforcement changes
- Potential issues
  - Non-atomic writes not blocked in CI
  - Audit log path undefined

## Phase 7 — Enforcement Mode Escalation
- Checks
  - solo → shadow → soft_block → hard_block (3 consecutive greens inc. integration)
  - Emergency override via expiring signed waivers; logged
- Potential issues
  - Escalation without stability criterion
  - Waivers lacking expiry/ownership

## Phase 8 — Verification & Close-out
- Checks
  - Re-run vertical verifications; atomically refresh reports
  - Freeze on all PASS + hard_block
  - Runbook includes commands/rollbacks/waivers/contacts
- Potential issues
  - Non-atomic final update; missing runbook contents

---

## Cross-Phase Conflicts/Missing (Observed)
- Schemas present vs. referenced: ensure actual files and versions exist for all referenced JSON schemas
- RBAC across toggles: confirm policy and CI check (no direct file edits bypassing RBAC)
- Telemetry contract: ensure all services emit required fields and correlation headers
- Build provenance: ensure SBOM/signing integrated in CI pipeline
- Reporting atomicity: enforce via CI guard; forbid direct concurrent writes

## Suggested Next Triggers (Advisory)
- I-validate ang plan
- Show hierarchy
- Execute the next unfinished phase (when ready)