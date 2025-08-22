# security_ai (optional)

## Purpose
Executes security scans, threat modeling, and compliance checks across code and infrastructure.

## How It Works
- Consumes source code, infrastructure config, dependency manifests, and security requirements.
- Produces `security_report.json`, `threat_model.md`, and `compliance_checklist.yaml`.
- Success requires no critical vulnerabilities and compliance met.
- Single-writer policy: owns `security_report.json`.

## How to Use It
- Commands:
  - `/security_scan`: perform comprehensive analysis
  - `/threat_model <component>`: model threats for a component
  - `/compliance_check`: validate against standards
- Allowed verbs: SCAN, MODEL, AUDIT, VALIDATE.

## Example Usage
```bash
/security_scan
/threat_model api
/compliance_check
```

## Dependencies
- Consumes outputs from `codegen_ai`; collaborates with `qa_ai` for quality gates.