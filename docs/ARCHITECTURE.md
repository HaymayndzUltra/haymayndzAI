# Architecture Overview

This project combines Cursor Rules, a curated rule library, and an orchestrated multi‑role development pipeline with CI validation and promotion/rollback safety.

## Rules activation model
- Always rules (global): `alwaysApply: true` in `.cursor/rules/*` (e.g., `development-excellence.mdc`, `security-and-compliance.mdc`).
- Auto Attached rules (by globs): e.g., `python-development-standards.mdc` with `**/*.py`, `pyproject.toml`, `requirements.txt`.
- Nested rules (per-folder auto-attach): `src/frontend/.cursor/rules/frontend-standards.mdc`, `src/backend/.cursor/rules/backend-standards.mdc`.

## Curated rule generation
- Generator step (local/CI): detector → curated selector → linter
  - Detector writes `rule_attach_log.json` (stack markers).
  - Curated selector promotes relevant `.cursor/test-rules/*.mdc` into `.cursor/rules/` and writes `.selected.json`.
  - Linter normalizes frontmatter without altering explicit `alwaysApply: true`.
- Run locally:
```bash
python tools/generate_cursor_rules.py --lint
```

## Orchestrated pipeline (execution)
- Orchestrator and roles: planning → codegen → qa → mlops → observability, with audit/verification/synthesis inserted between planning and codegen.
- Gate checks, error handling, and handoff logs are enforced via `execution_orchestrator.mdc`.

## Memory, promotion, and rollback
- Memory bridge coordinates state with `memory-bank/` artifacts.
- Promotion safety:
  - `promotion/snapshot_cli.py` creates snapshots with metadata.
  - `promotion/rollback_rehearsal.py` verifies restore + gates (contracts/hydration/routing).

## Routing & progressive mode
- Config under `frameworks/fwk-001-cursor-rules/DOCS/changes/` (`routing_override.yaml`, shadow/baseline).
- `scripts/progressive_monitor.py` checks allowlist + drift; `.bak` flow enables safe rollback.

## CI workflow
- Runs generator step before tests; uploads `rule_attach_log.json` and `.cursor/rules/.selected.json` artifacts.
- Executes attach mapping tests (incl. Java/Rust/iOS/E‑commerce), hydration tests, concurrency smoke.

## System diagram
```mermaid
graph TD
  subgraph Rules
    A1[.cursor/rules<br/>Always + Auto Attached]
    A2[.cursor/test-rules<br/>Curated Library]
    A3[src/*/.cursor/rules<br/>Nested (per-folder)]
  end

  subgraph Generator
    G1[Detector<br/>rule_attach_log.json]
    G2[Curated Selector<br/>.selected.json]
    G3[Linter<br/>normalize frontmatter]
  end

  subgraph Pipeline
    P1[product_owner_ai]
    P2[planning_ai]
    P3[auditor_ai]
    P4[principal_engineer_ai]
    P5[codegen_ai]
    P6[qa_ai]
    P7[mlops_ai]
    P8[observability_ai]
  end

  A2 -->|promote| A1
  A3 --> A1

  G1 --> G2 --> G3 --> A1

  P1 --> P2 --> P3 --> P4 --> P5 --> P6 --> P7 --> P8

  subgraph Safety
    S1[Snapshots]
    S2[Rollback Rehearsal]
  end
  P6 -->|PASS| P7 --> S1
  S1 --> S2

  subgraph Routing
    R1[routing_override.yaml]
    R2[progressive_monitor]
  end
  R1 --> R2 --> P5
```

## Quick references
- Generate curated rules: `python tools/generate_cursor_rules.py --lint`
- Artifacts: `rule_attach_log.json`, `.cursor/rules/.selected.json`
- CI: `.github/workflows/ci.yml`
- Orchestrator: `.cursor/rules/execution_orchestrator.mdc`
- Promotion: `frameworks/fwk-001-cursor-rules/promotion/`