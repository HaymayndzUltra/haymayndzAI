# Rollback Playbook — artifacts_index.json

1) Freeze promotions
2) Locate snapshot digest to restore
3) Verify digest (and signature if present)
4) Restore `artifacts_index.json` to bytes from snapshot
5) Re-run verification gate
6) Unfreeze promotions


