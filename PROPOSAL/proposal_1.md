System Preservation Strategy
Principles
Preserve working core: Keep todo_manager.py, memory-bank/, auto_sync_manager.py, cursor_memory_bridge.py, and proven .cursor/rules/* triggers unchanged initially.
Config over code: Introduce new behaviors via flags/policies first; defer refactors.
Backward compatibility: All new features must degrade to current single-actor flow.
PH context: Retain +08:00 normalization and session persistence guarantees.
Single-operator safety: No concurrency assumptions; serialize role outputs via the command center.
Preserve vs Enhance (Decision Heuristic)
Preserve when: module is stable, has clear ownership, and direct user muscle memory exists.
Enhance when: friction is due to hard blocks, cross-role handoffs, or repeated manual orchestration.
Keep as-is (baseline)
Task orchestration: task_command_center.py interaction loop and trigger UX.
State sync: auto_sync_manager.py, PH timezone rules, monotonic updates.
SOT: memory-bank/queue-system/tasks_active.json as primary execution source.
Enhance (additive)
Enforcement modes: Solo vs Team policy switch (Warn → Soft-block → Hard-block).
Role router: Lightweight dispatcher inside task_command_center.py to route role-prefixed triggers.
Memory namespaces: Role-scoped memory domains under memory-bank/roles/<role>/.
Rule simplification: Consolidate overlapping gates; move non-critical checks to warnings in Solo Mode.
Decision ledger: Append-only decisions index to reduce back-and-forth and enable handoffs.
AI Role Design Guidelines
Role design principles
Crisp boundaries: Each role owns a stage artifact (draft, estimate, plan, checklist, invoice, syllabus).
Minimal coupling: Exchange via structured handoff records (inputs/outputs are files/IDs, not globals).
Deterministic triggers: Prefix grammar [Role]: <verb> <object> [modifiers].
Tight SLAs: Each role defines time-to-first-output and quality bar (checklist-based).
Freelancer-focused role set (Triggers, Inputs, Outputs, KPIs)
Client Management (ClientAgent)
Triggers: ClientAgent: summarize thread <id>, ClientAgent: draft reply <tone>
Inputs: Communication threads, meeting notes
Outputs: Reply drafts, next-step prompts
KPIs: Response time ≤ 15 min; 0 revisions for tone mismatch in 80% cases
Estimator (Estimator)
Triggers: Estimator: scope <project>, Estimator: estimate <feature set>
Inputs: Requirements brief, constraints
Outputs: WBS, assumptions, price–time ranges
KPIs: Variance vs actual ≤ 25%; assumptions explicitly listed
Architect (Architect)
Triggers: Architect: propose architecture <constraints>, Architect: review plan <ticket>
Inputs: Requirements, non-functionals, tech baseline
Outputs: Architecture notes, risks, decision records
KPIs: Risk coverage completeness; aligns with stack constraints
Coder (Coder)
Triggers: Coder: implementation plan <ticket>, Coder: scaffold <module>
Inputs: Architecture notes, ticket
Outputs: Step-by-step plan, file-level diffs checklist
KPIs: PR-ready with zero rework on structure in 70% cases
QA/Deliverables (QA)
Triggers: QA: acceptance checklist <ticket>, QA: verify <artifact>
Inputs: User stories, acceptance criteria
Outputs: Test checklist, verification report
KPIs: Missed-criteria rate ≤ 5%
Business Ops (Ops)
Triggers: Ops: invoice <client> <period>, Ops: time report <range>
Inputs: Time logs, SOW terms
Outputs: Invoice draft, summary report
KPIs: Draft accuracy; on-time invoicing
Learning (Learner)
Triggers: Learner: micro-plan <topic> 30m, Learner: summarize <paper>
Inputs: Topics, materials
Outputs: Micro-syllabus, spaced-repetition cards
KPIs: Retention checks weekly
Trigger Command Architecture
Grammar
Pattern: [RolePrefix]: <verb> <object> [qualifiers] [refs]
Examples:
ClientAgent: draft reply <thread:ACME-2025-02> polite concise
Estimator: scope <ticket:WEB-143> constraints=serverless budget=mid
Architect: review plan <ticket:WEB-143> risks+mitigations
QA: acceptance checklist <feature:billing-export>
Ops: time report <2025-02-01..2025-02-15>
Routing flow
Parse prefix → map to role → hydrate context (active tasks_active.json, recent memory-bank/clients/*, projects/*) → apply Solo Mode gates → execute → emit artifact + decision record.
Conflict resolution
If trigger is ambiguous, require one disambiguator: client|project|ticket|feature|range.
Priority
ClientAgent > Ops (time-bound) > Estimator > Architect > Coder > QA > Learner, unless a deadline tag is present.
Memory Integration Patterns
Namespaces
memory-bank/roles/<role>/:
context.json (role-specific priors), history/ (timestamped), summaries/ (rolling)
memory-bank/clients/<client>/:
threads/, agreements/, invoices/, decisions/
memory-bank/projects/<project>/:
requirements/, architecture/, tickets/, checklists/, decisions/
memory-bank/decisions/: flat append-only index with cross-links
Artifacts lifecycle
Capture → Summarize → Index → Reference → Expire/Archive (time or size thresholds)
Handoffs
Handoff record fields: id, origin_role, target_role, source_refs[], required_by, summary, acceptance_criteria[]
Learning loop
Weekly retrospective job: mine decisions, estimates vs actuals, missed criteria → update role context.json heuristics.
Implementation Roadmap
Phase 0 — Policy Switch & Audit
Add Solo/Team enforcement modes; inventory rule blocks; mark candidates to downgrade to warnings in Solo Mode.
Acceptance: Solo Mode produces no hard blocks on the golden path.
Phase 1 — Role Skeletons & Triggers
Define role prefixes and dispatcher map; add memory namespaces; no core refactors.
Acceptance: Triggers route and persist minimal artifacts (notes/checklists) reliably.
Phase 2 — Decision Ledger & Handoffs
Introduce decisions index and handoff records; wire to task_command_center.py after each role action.
Acceptance: End-to-end trace from trigger → artifact → next-role handoff.
Phase 3 — Pilot Roles
Pilot ClientAgent and Estimator; measure KPIs; tighten prompts and checklists.
Acceptance: SLA adherence ≥ 80%, low rework.
Phase 4 — Expand to Architect/QA/Ops
Add remaining roles incrementally; bake-in acceptance checklists; refine enforcement per role.
Acceptance: Deliverables pass QA checklists without manual rewrite in majority of cases.
Phase 5 — Stabilize & Document
Finalize rule catalog, policies, and playbooks; publish quick-reference trigger guide.
Risk Mitigation Strategies
Rule friction/blocks
Mitigation: Mode-based enforcement; log-and-proceed defaults in Solo Mode; retain hard blocks only for data loss/security.
Trigger ambiguity
Mitigation: Enforce one disambiguator per trigger; interactive clarify-once cache.
Memory bloat/drift
Mitigation: Retention windows, compaction, monthly archive; checksum decision index.
Context leakage
Mitigation: Role namespace isolation; explicit cross-linking; redaction pass for client PII.
Quality regressions
Mitigation: Role-specific acceptance checklists; sampling reviews weekly.
Rollback
Mitigation: Feature flags per role; toggle to baseline orchestration; keep schemas additive.
Decision Frameworks (cross-cutting)
Preserve vs Enhance
Preserve if stable + muscle memory + no cross-role dependency.
Enhance if causing repeat friction, blocking single-actor flow, or requires handoffs.
Warning vs Block (Solo Mode)
Warn: stylistic, completeness, sequencing suggestions.
Soft-block: missing required refs (e.g., no ticket), allow override.
Hard-block: data loss risks, irreversible state changes.
Role SLA Gate
Promote role maturity only when its SLA and quality KPIs meet thresholds for 2 consecutive weeks.