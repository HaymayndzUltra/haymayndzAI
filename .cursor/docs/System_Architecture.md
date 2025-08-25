## AI Orchestration System Architecture

### Mission
Create an intelligent multi-agent AI development system that combines role-based specialists with framework-specific knowledge.

### Core Components
- execution_orchestrator.mdc: pipeline, gates, rule loading, handoffs
- rules_master_toggle.mdc: role activation and routing
- memory_ai.mdc: knowledge base, learning signals, pattern library
- framework_memory_bridge.mdc: sync with memory-bank system
- guidance_phase_awareness.mdc: phase detection and adjacent steps

### Framework Rules (Auto-Attach via Globs)
- Frontend: React, Vue, Angular, Svelte
- Backend: Node/Nest, Python/FastAPI/Django, PHP/Laravel, .NET, Go
- Mobile: React Native, Flutter, Ionic
- Specialized: Blockchain, AI/ML

### Pipeline Diagram
```mermaid
graph TD
    A[product_owner_ai] --> B[planning_ai]
    B --> X[auditor_ai]
    X --> Y[principal_engineer_ai]
    Y --> C[codegen_ai]
    C --> D[qa_ai]
    D --> E{QA Gate}
    E -->|PASS| F[mlops_ai]
    E -->|FAIL| C
    F --> G[observability_ai]
    C --> H[documentation_ai]
    H --> I[analyst_ai]
    J[memory_ai] --> K[All Phases]
    L[security_ai] --> C
```

### Rule Application Decision Tree
```mermaid
flowchart TD
    S[Start] --> P{Project markers}
    P -->|*.tsx/next.config| R[Attach React rules]
    P -->|nest-cli.json| N[Attach Node/Nest rules]
    P -->|*.py/FastAPI/Django| PY[Attach Python rules]
    P -->|*.php/artisan| L[Attach Laravel rules]
    P -->|*.go/go.mod| G[Attach Go rules]
    P -->|pubspec.yaml| FL[Attach Flutter rules]
    R --> RS[Select codegen/qa/docs]
    N --> NS[Select codegen/qa/security]
    PY --> PYS[Select codegen/qa/security]
```

### Context Switching Logic
- Orchestrator persists `workflow_state.json` and `handoff_log.json`.
- Memory signals saved to `pattern_library.json` after QA Gate PASS.
- Bridge syncs attach logs to memory-bank observability.

