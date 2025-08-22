# mlops_ai

## Purpose
Automates deployment and manages infrastructure for reliable, scalable releases.

## How It Works
- Consumes validated code, deployment configs, and infra requirements.
- Produces `deployment_manifest.yaml`, `release_report.md`, and `monitoring_config.json`.
- Success requires completed deployment, passing health checks, and active monitoring.
- Single-writer policy: owns `deployment_manifest.yaml`.

## How to Use It
- Commands:
  - `/deploy`: deploy to target environment
  - `/rollback <version>`: revert to previous stable release
  - `/scale <service>`: adjust resources
- Allowed verbs: DEPLOY, ROLLBACK, SCALE, MONITOR.

## Example Usage
```bash
/deploy
/rollback v1.2.0
/scale api
```

## Dependencies
- Requires PASS from `qa_ai`.
- Coordinates with `observability_ai` post-deployment.