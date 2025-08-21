# Quick Start Guide - Tagalog

## Mga Hakbang Para Magamit Agad (30 Minutes)

### Step 1: I-enable ang Mga Roles (5 minutes)
1. Buksan ang `system-prompt/rules_master_toggle.mdc`
2. I-check kung tama ang mga enabled roles:
   ```yaml
   # Mga kailangan lang for basic usage:
   product_owner_ai: enabled: true
   planning_ai: enabled: true  
   codegen_ai: enabled: true
   qa_ai: enabled: true
   ```

### Step 2: I-customize ang Core Roles (15 minutes)

#### A. Product Owner AI
Buksan `system-prompt/product_owner_ai.mdc`, palitan ang:
```yaml
# Section 2: INPUT CONTRACT
# I-customize mo ang business_objectives para sa inyong project
business_objectives: 
  - "Build e-commerce platform"  # Example - palitan mo
  - "Improve user experience"
  - "Increase conversion rate"
```

#### B. Planning AI  
Buksan `system-prompt/planning_ai.mdc`, i-update ang:
```yaml
# Section 2: INPUT CONTRACT
# I-specify ang inyong tech stack
architecture_preferences:
  frontend: "React + TypeScript"     # O kung ano man ginagamit ninyo
  backend: "Node.js + Express"      # Palitan based sa inyong setup
  database: "PostgreSQL"           # MySQL, MongoDB, etc.
  cloud: "AWS"                     # Azure, GCP, etc.
```

#### C. Code Generation AI
Buksan `system-prompt/codegen_ai.mdc`, i-set ang:
```yaml
# Section 2: INPUT CONTRACT  
coding_standards:
  language: "typescript"           # O kung ano primary language ninyo
  framework: "react"              # Vue, Angular, etc.
  patterns: ["clean-architecture", "repository-pattern"]
  style_guide: "airbnb"           # Prettier, ESLint rules
```

### Step 3: Test Basic Functionality (10 minutes)

#### A. Test Product Owner AI
Sa Cursor chat, subukan:
```
/backlog {"feature": "user login system", "priority": "high"}
```

#### B. Test Planning AI  
```
/plan
```

#### C. Test Code Generation
```
/gen_code src/auth/login.ts
```

### Step 4: Quick Validation
I-check kung may na-generate na files sa:
- `src/` folder - may mga generated code
- May mga output files from AI roles

## Mga Pwedeng I-skip Muna (Para sa later)

❌ **Hindi kailangan agad:**
- Optional roles (security_ai, l10n_ai, etc.) - disable muna
- Documentation AI - pwede later
- MLOps AI - kung hindi pa ready mag-deploy
- Observability - advanced feature

❌ **Advanced na setup:**
- Performance benchmarks
- Security scanning
- Complete test coverage
- Production deployment

## Troubleshooting

### Kung hindi gumagana ang commands:
1. I-check kung tama ang role activation sa `rules_master_toggle.mdc`
2. Tignan kung may typo sa command routing
3. I-verify kung naka-save lahat ng changes

### Kung may errors sa code generation:
1. I-check kung complete ang tech stack specification sa `planning_ai.mdc`
2. I-validate kung tama ang coding standards sa `codegen_ai.mdc`

## Next Steps After Basic Setup

1. **I-customize pa lalo ang roles** - Add more domain-specific details
2. **I-enable ang optional roles** - Kung kailangan na ng security, l10n, etc.
3. **I-setup ang complete pipeline** - Full workflow from requirements to deployment
4. **I-configure ang monitoring** - Para sa production readiness

---

**Target Time**: 30 minutes para sa basic working framework
**Goal**: Makakagawa na ng `/backlog` → `/plan` → `/gen_code` workflow