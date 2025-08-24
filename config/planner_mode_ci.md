# Planner-First CI Bypass

## Goal
Allow non-interactive CI to proceed when planner-first mode requires confirmations.

## Mechanism
- Config file: `config/planner_mode.json`
- Env var override: `PLANNER_MODE_CI_BYPASS=true`

## Expected Behavior
- If CI bypass is enabled, confirmations are auto-approved for actions marked safe-for-ci.
- Log a clear audit entry: "planner_mode: ci_bypass active".

## Security
- Do NOT enable in developer workstations by default.
- Optionally require a CONFIRMATION_TOKEN in CI secrets for high-impact actions.

