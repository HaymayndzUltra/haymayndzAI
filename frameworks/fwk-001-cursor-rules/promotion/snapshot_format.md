# Snapshot Format — artifacts_index.json

## Overview
Content-addressable snapshots of the artifacts index for promotion governance, disaster recovery, and audit compliance.

## File Structure
- **Directory**: `frameworks/fwk-001-cursor-rules/promotion/snapshots/`
- **Filename**: `<sha256_of_index>.json`
- **Content**: Exact JSON bytes of `artifacts_index.json` at capture time
- **Sidecar**: `<sha256_of_index>.json.metadata` (optional)

## Snapshot Content
```json
{
  "artifacts": [
    {
      "id": "artifact_name",
      "version": "1.0.0",
      "status": "approved",
      "framework": "fwk-001-cursor-rules",
      "kind": "artifact_type",
      "checksumSha256": "hash_value",
      "createdAt": "2025-08-23T00:00:00Z",
      "updatedAt": "2025-08-23T19:11:16Z"
    }
  ],
  "simulated": false,
  "version": 1
}
```

## Integrity Verification

### Primary Integrity (SHA-256)
- **Digest**: SHA-256 of the exact JSON bytes (used as filename)
- **Verification**: `sha256sum <snapshot_file>` should match filename
- **Collision resistance**: 2^128 security level

### Optional Digital Signing
- **Format**: PGP or Sigstore signatures
- **Location**: `<snapshot_file>.sig` or `<snapshot_file>.sigstore`
- **Verification**: External signature verification tools
- **Key management**: Framework signing keys stored securely

## Metadata Sidecar (Optional)
```json
{
  "snapshot": {
    "digest": "sha256_hash",
    "createdAt": "2025-08-23T00:00:00Z",
    "creator": "CI_SYSTEM",
    "trigger": "scheduled|manual|promotion",
    "environment": "production|staging|development"
  },
  "artifacts": {
    "count": 6,
    "statuses": {
      "approved": 4,
      "review": 1,
      "draft": 1
    },
    "kinds": ["action_plan", "summary_report", "validation_report"]
  },
  "promotion": {
    "gate": "verification_gate",
    "checksum": "gate_checksum",
    "timestamp": "2025-08-23T19:11:16Z"
  },
  "notes": "Post-synthesis snapshot for T-06 completion"
}
```

## Snapshot Lifecycle

### Creation
1) **Trigger**: Scheduled, manual, or promotion-based
2) **Capture**: Atomic read of current index
3) **Validation**: Verify index integrity before snapshot
4) **Storage**: Write to snapshots directory with digest filename
5) **Metadata**: Generate and store sidecar information

### Retention Policy
- **Keep last N**: 20 snapshots (configurable)
- **Purge older**: Automatic cleanup with audit logging
- **Critical snapshots**: Marked for extended retention
- **Archive**: Long-term storage for compliance

### Verification
1) **Integrity check**: SHA-256 digest validation
2) **Signature verification**: If signed snapshots enabled
3) **Content validation**: JSON schema compliance
4) **Cross-reference**: Verify against current index

## Security Considerations

### Access Control
- **Read access**: Framework team members
- **Write access**: CI/CD systems and authorized users
- **Delete access**: DevOps and platform engineering only
- **Audit logging**: All operations logged with timestamps

### Encryption
- **At rest**: Optional encryption for sensitive snapshots
- **In transit**: TLS for remote snapshot storage
- **Key rotation**: Regular signing key updates

### Compliance
- **GDPR**: Data retention and deletion policies
- **SOC 2**: Access controls and audit trails
- **ISO 27001**: Information security management

## Operational Procedures

### Creating Snapshots
```bash
# Manual snapshot
python3 frameworks/fwk-001-cursor-rules/promotion/snapshot_cli.py create

# Scheduled snapshot (cron)
0 */4 * * * cd /path/to/framework && \
  python3 frameworks/fwk-001-cursor-rules/promotion/snapshot_cli.py create
```

### Verifying Snapshots
```bash
# Verify all snapshots
python3 frameworks/fwk-001-cursor-rules/promotion/snapshot_cli.py verify

# Verify specific snapshot
sha256sum frameworks/fwk-001-cursor-rules/promotion/snapshots/<digest>.json
```

### Managing Retention
```bash
# Keep last 20 snapshots
python3 frameworks/fwk-001-cursor-rules/promotion/snapshot_cli.py prune 20

# List all snapshots
python3 frameworks/fwk-001-cursor-rules/promotion/snapshot_cli.py list
```

## Best Practices

### Snapshot Frequency
- **Development**: Every commit or PR merge
- **Staging**: Every deployment
- **Production**: Every promotion or significant change

### Storage Optimization
- **Compression**: Gzip for long-term storage
- **Deduplication**: Identify and remove duplicate content
- **Tiering**: Hot (recent), warm (monthly), cold (quarterly)

### Monitoring and Alerting
- **Snapshot failures**: Alert on creation failures
- **Storage usage**: Monitor disk space consumption
- **Verification failures**: Alert on integrity check failures
- **Retention violations**: Alert on policy violations


