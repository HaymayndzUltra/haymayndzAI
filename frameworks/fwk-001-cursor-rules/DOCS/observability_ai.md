# observability_ai

## Purpose
Monitors system health, alerts on anomalies, and reports operational status.

## How It Works
- Consumes system metrics, log streams, alert configurations, and health check results.
- Produces `monitoring_dashboard.json`, `alert_history.log`, and `health_report.md`.
- Success requires full coverage, working alerts, and accurate dashboards.
- Single-writer policy: owns `monitoring_dashboard.json`.

## How to Use It
- Commands:
  - `/observe`: activate monitoring
  - `/alert <condition>`: configure custom rule
  - `/health`: generate current health report
- Allowed verbs: MONITOR, ALERT, TRACK, REPORT.

## Example Usage
```bash
/observe
/alert "p95 > 500ms"
/health
```

## Dependencies
- Consumes deployment outputs and configs from `mlops_ai`.
- Shares telemetry with `analyst_ai`.