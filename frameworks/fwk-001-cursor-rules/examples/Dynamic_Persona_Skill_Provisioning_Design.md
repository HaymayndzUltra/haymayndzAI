## Dynamic Persona & Skill Provisioning System (DP/SP)

Author: Lead Metasystem Architect
Scope: fwk-001-cursor-rules

### 1) Overview
- Goal: Dynamically provision task‑specific personas to agents (e.g., transform `codegen_ai` from “Go/Clean Architecture” to “Django expert” on demand).
- Inputs: `.mdc` rules library (harvested), project artifacts (e.g., `product_backlog.yaml`).
- Outputs: `rule_index.json` (card catalog), persona payloads (instructions + guardrails) injected per task.

### 2) Rule Indexing & Discovery Engine
- Source: `/workspace/frameworks/fwk-001-cursor-rules/DOCS/harvested/**/*.mdc`
- Parse for:
  - Metadata block `%% ... %%`: extract `hash`, `tags` (split on comma/space; normalize lowercase).
  - Body sections:
    - `[INTENT]` → single token/category (e.g., planning, codegen, qa, mlops).
    - `[GUARDRAILS]` → preserved verbatim for constraints.
    - `[INSTRUCTIONS]` → summarize to keywords (tf-idf-ish) and store raw excerpt.
- Output: `rule_index.json` entries:
```json
{
  "path": ".../django_codegen.mdc",
  "hash": "...",
  "tags": ["django","python","web","orm"],
  "intent": "codegen",
  "instructions_excerpt": "...",
  "instructions_keywords": ["django","views","models","tests"],
  "guardrails_present": true,
  "sections": {"INSTRUCTIONS": [start,end], "GUARDRAILS": [start,end]}
}
```
- Indexing algorithm:
  1) Walk files; read text.
  2) Regex extract `%%(.*?)%%` (DOTALL) → parse `hash:`, `tags:`.
  3) Section parser: detect headers `^[[]INTENT[]]`, `^[[]GUARDRAILS[]]`, `^[[]INSTRUCTIONS[]]` … capture until next section or EOF.
  4) Keyword extraction: lowercase, strip stopwords, take top‑N terms.
  5) Emit single JSON array `rule_index.json`.

### 3) Project Requirement Analysis Engine
- Inputs: `examples/product_backlog.yaml` (or task descriptor). Extract:
  - `task.intent` (if present) else infer from verbs → {planning, codegen, qa, mlops}.
  - Tech signals: scan for known techs ("django","go","react","node","postgres","k8s").
- Query strategy over `rule_index.json`:
  - Score = w1*intent_match + w2*tag_overlap + w3*keyword_hit + w4*path/filename hints.
  - Intent match: exact = 1.0, related = 0.6, else 0.
  - Tag overlap: Jaccard(tags_proj, tags_rule).
  - Keyword hit: fraction of tech tokens found in `instructions_keywords`.
  - Tie‑breakers: prefer entries with explicit `[GUARDRAILS]` and longer instructions.
- Returns top‑K rule candidates with scores and rationale.

### 4) Just‑In‑Time (JIT) Persona Orchestrator
- Trigger: `execution_orchestrator` assigns a task `{agent, intent, context}`.
- Steps:
  1) Identify skills: run Analysis Engine with `{intent, techs}`.
  2) Select best rule (score ≥ threshold) → load full `.mdc`.
  3) Persona Construction:
     - Primary Directive: extract `[INSTRUCTIONS]` body (verbatim) → `persona.instructions`.
     - Constraints: extract `[GUARDRAILS]` body (verbatim) → `persona.guardrails`.
     - Metadata: `persona.tags`, `persona.hash`, `persona.intent`.
  4) Context Injection:
     - Inject persona into the agent’s session context as a top‑priority system segment for the task lifetime.
     - Mark as `temporary=true`, with `expires_on_task_complete=true`.
  5) Audit: write `personas/persona_injection_log.jsonl` with `{task_id, agent, rule_path, score, timestamp}`.

### 5) Dynamic Persona Management Strategy (Layering)
- Base Persona (per agent): e.g., `codegen_ai` = Go/Clean Architecture.
- Task‑Specific Persona (overlay): constructed from the selected rule; precedence > base during task.
- Clearing/Isolation:
  - On task completion, orchestrator calls `context.reset(agent_id)` to remove overlays.
  - Snapshots: store last N overlays for audit only; not reused unless reselected by scoring.
  - Memory hygiene: no cross‑task carryover; feature flags to prevent leakage.

### 6) Data Contracts
- `rule_index.json` (JSON array) — fields: `path, hash, tags[], intent, instructions_excerpt, instructions_keywords[], guardrails_present, sections{}`.
- `persona_payload.json` — fields: `agent, intent, instructions, guardrails, tags[], hash, source_rule`.
- `task_descriptor.json` — fields: `task_id, agent, intent, description, techs[]`.

### 7) Security & Guardrails
- Only allow `.mdc` from trusted paths; validate hash if provided.
- Normalize and sanitize instructions/guardrails (strip non‑printing, enforce size caps).
- Enforce deny‑list in guardrails (e.g., no code execution unless authorized).

### 8) Observability
- Metrics: index size, index latency, JIT selection latency, per‑agent overlay counts.
- Logs: `rule_index_build.json`, `persona_injection_log.jsonl`.
- Alerts: index missing, stale (>24h), or empty → block persona selection.

### 9) Failure Modes & Recovery
- Missing index: build on demand; if build fails, fall back to base persona.
- No match: degrade to base persona with a warning; attach “skills needed” hint.
- Multiple close matches: pick highest score; include alternates in log.

### 10) Rollout Plan
- Phase A: Indexer + scoring PoC; manual persona injection.
- Phase B: Wire to `execution_orchestrator`; add audit logs.
- Phase C: Add caching and incremental indexing.

### 11) Appendix — Section Parsing Spec
- Sections recognized: `[INTENT]`, `[GUARDRAILS]`, `[INSTRUCTIONS]`, optional others ignored.
- Regex anchors with `^\[([A-Z_]+)\]\s*$` and capture until next header or EOF.

