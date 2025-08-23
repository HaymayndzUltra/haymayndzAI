# Snapshot Format — artifacts_index.json

## Layout
- Directory: `frameworks/fwk-001-cursor-rules/promotion/snapshots/`
- Filename: `<sha256_of_index>.json`
- Content: exact JSON bytes of `artifacts_index.json` at capture time

## Integrity
- Digest: SHA-256 of bytes (used as filename)
- Optional signing: external command (PGP or sigstore) recorded alongside

## Metadata (optional sidecar)
```json
{ "createdAt": "2025-08-23T00:00:00Z", "creator": "CI", "notes": "post-synthesis" }
```


