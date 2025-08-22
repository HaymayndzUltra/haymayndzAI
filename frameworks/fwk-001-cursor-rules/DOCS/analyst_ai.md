# analyst_ai

## Purpose
Provides performance and system analysis to drive optimization decisions.

## How It Works
- Consumes performance metrics, code quality reports, deployment logs, and user feedback.
- Produces `analysis_report.md`, `metrics_dashboard.json`, and `optimization_plan.yaml`.
- Success requires actionable, data-backed recommendations.
- Single-writer policy: owns `analysis_report.md`.

## How to Use It
- Commands:
  - `/review`: comprehensive system analysis
  - `/analyze <component>`: focused analysis
  - `/benchmark`: performance comparison and baselining
- Allowed verbs: ANALYZE, REVIEW, BENCHMARK, OPTIMIZE.

## Example Usage
```bash
/review
/analyze api
/benchmark
```

## Dependencies
- Pulls telemetry from `observability_ai` and release data from `mlops_ai`.