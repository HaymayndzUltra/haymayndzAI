# Secrets Management Policy

## Storage & Access
- Use environment variables or secret managers (never commit secrets).
- Restrict CI access to least privilege; rotate tokens every 90 days.

## Redaction
- All logs and artifacts must pass through `security/redact_filter.py`.
- Patterns: API keys, tokens, passwords, private keys, cloud creds.

## Validation
- CI step: run redaction in check mode; fail on unredacted secrets.

