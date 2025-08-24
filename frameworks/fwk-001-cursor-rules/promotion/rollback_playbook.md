# Rollback Playbook — artifacts_index.json

## Emergency Rollback Procedure

### Phase 1: Freeze and Assess
1) **Freeze all promotions** - Set `PROMOTION_FROZEN=true` in environment
2) **Stop index writers** - Prevent new artifacts from being indexed
3) **Assess impact** - Document what artifacts will be lost/restored
4) **Notify stakeholders** - Alert team of rollback initiation

### Phase 2: Snapshot Selection and Verification
1) **List available snapshots**:
   ```bash
   python3 frameworks/fwk-001-cursor-rules/promotion/snapshot_cli.py list
   ```
2) **Verify snapshot integrity**:
   ```bash
   python3 frameworks/fwk-001-cursor-rules/promotion/snapshot_cli.py verify
   ```
3) **Select target snapshot** by digest (SHA-256)
4) **Verify signature** if snapshot is signed (optional but recommended)

### Phase 3: Rollback Execution
1) **Create backup** of current index:
   ```bash
   cp frameworks/fwk-001-cursor-rules/sync/artifacts_index.json \
      frameworks/fwk-001-cursor-rules/sync/artifacts_index.json.backup.$(date +%Y%m%d_%H%M%S)
   ```
2) **Execute rollback**:
   ```bash
   python3 frameworks/fwk-001-cursor-rules/promotion/snapshot_cli.py rollback <digest>
   ```
3) **Verify restoration** - Confirm index content matches snapshot

### Phase 4: Post-Rollback Validation
1) **Re-run verification gate**:
   ```bash
   python3 frameworks/fwk-001-cursor-rules/contracts/validate_contract.py
   ```
2) **Run hydration tests** to ensure consistency:
   ```bash
   python3 frameworks/fwk-001-cursor-rules/hydration/run_hydration_tests.py \
      frameworks/fwk-001-cursor-rules/hydration/hydration_tests.yaml
   ```
3) **Check routing conflicts**:
   ```bash
   python3 frameworks/fwk-001-cursor-rules/routing/check_routing_conflicts.py
   ```

### Phase 5: Recovery and Monitoring
1) **Unfreeze promotions** - Set `PROMOTION_FROZEN=false`
2) **Resume index writers** - Allow new artifacts to be indexed
3) **Monitor system health** - Watch for any post-rollback issues
4) **Document incident** - Record rollback reason and outcome

## Rollback Rehearsal (Required for Acceptance)

### Pre-Rehearsal Checklist
- [ ] Test environment available
- [ ] Backup procedures tested
- [ ] Team notified of rehearsal
- [ ] Rollback window scheduled

### Rehearsal Steps
1) **Create test snapshot** with known artifacts
2) **Simulate corruption** or issue
3) **Execute rollback** following full procedure
4) **Verify system state** matches snapshot
5) **Test post-rollback operations**
6) **Document lessons learned**

### Success Criteria
- [ ] Rollback completes within 5 minutes
- [ ] Zero data loss during rollback
- [ ] All verification gates pass post-rollback
- [ ] System resumes normal operation
- [ ] Audit trail maintained throughout

## Emergency Contacts
- **Platform Engineering**: Primary rollback executor
- **DevOps**: Infrastructure support
- **Security**: Signature verification (if applicable)
- **Product**: Business impact assessment

## Rollback Triggers
- **Critical**: Data corruption, security breach
- **High**: Schema validation failures, routing conflicts
- **Medium**: Performance degradation, partial failures
- **Low**: Minor inconsistencies, cosmetic issues

## Recovery Time Objectives (RTO)
- **Critical**: < 5 minutes
- **High**: < 15 minutes  
- **Medium**: < 1 hour
- **Low**: < 4 hours


