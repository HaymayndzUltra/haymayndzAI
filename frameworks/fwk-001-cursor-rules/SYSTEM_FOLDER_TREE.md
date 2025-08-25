# 🌳 System Folder Tree Structure

```
HaymayndzAI/
├── 📁 frameworks/
│   └── 📁 fwk-001-cursor-rules/
│       ├── 📁 system-prompt/                    # AI Role Definitions
│       │   ├── 📄 rules_master_toggle.mdc       # Master control
│       │   ├── 📄 execution_orchestrator.mdc    # Pipeline control
│       │   ├── 📄 framework_memory_bridge.mdc   # Memory integration
│       │   ├── 📄 memory_ai.mdc                # Memory management
│       │   ├── 📄 product_owner_ai.mdc         # Product decisions
│       │   ├── 📄 planning_ai.mdc              # Technical planning
│       │   ├── 📄 codegen_ai.mdc               # Code generation
│       │   ├── 📄 qa_ai.mdc                    # Quality assurance
│       │   ├── 📄 auditor_ai.mdc               # Risk assessment
│       │   ├── 📄 principal_engineer_ai.mdc    # Technical review
│       │   ├── 📄 documentation_ai.mdc         # Documentation
│       │   ├── 📄 analyst_ai.mdc               # Data analysis
│       │   ├── 📄 mlops_ai.mdc                 # ML operations
│       │   ├── 📄 observability_ai.mdc         # Monitoring
│       │   ├── 📄 prompt_factory_ai.mdc        # Prompt creation
│       │   └── 📁 OPTIONAL/                    # Optional roles
│       │
│       ├── 📁 DOCS/                            # Documentation
│       │   ├── 📁 harvested/                   # External rules
│       │   │   ├── 📄 rules-for-*.mdc          # 67+ framework rules
│       │   │   └── 📄 try.md                   # System prompts collection
│       │   ├── 📁 changes/                     # Configuration changes
│       │   │   └── 📄 routing_override.yaml    # Progressive mode config
│       │   ├── 📄 Action_Plan.md               # Project action plan
│       │   ├── 📄 Final_Implementation_Plan.md # Implementation details
│       │   ├── 📄 Summary_Report.md            # Audit reports
│       │   ├── 📄 SESSION_NOTES.md             # Session tracking
│       │   ├── 📄 CHECKLIST.md                 # Task checklists
│       │   ├── 📄 QUICK_START.md               # Quick start guide
│       │   └── 📄 README.md                    # Main documentation
│       │
│       ├── 📁 sync/                            # Synchronization system
│       │   ├── 📄 enhanced_index_writer.py     # Index management
│       │   ├── 📄 index_cli.py                 # Command interface
│       │   ├── 📄 artifacts_index.json         # Artifact tracking
│       │   ├── 📄 concurrency_tests.yaml       # Test configurations
│       │   └── 📄 T-10_IMPLEMENTATION_SUMMARY.md
│       │
│       ├── 📁 routing/                         # Routing configuration
│       │   └── 📄 [routing configs]
│       │
│       ├── 📁 schemas/                         # Data schemas
│       │   └── 📄 [schema definitions]
│       │
│       ├── 📁 security/                        # Security configurations
│       │   └── 📄 [security rules]
│       │
│       ├── 📁 observability/                   # Monitoring & logging
│       │   └── 📄 [observability configs]
│       │
│       ├── 📁 promotion/                       # Promotion workflows
│       │   └── 📄 [promotion rules]
│       │
│       ├── 📁 contracts/                       # Service contracts
│       │   └── 📄 [contract definitions]
│       │
│       ├── 📁 examples/                        # Example implementations
│       │   ├── 📄 test_plan.md                 # Test strategy
│       │   └── 📄 [other examples]
│       │
│       ├── 📁 governance/                      # Governance rules
│       │   └── 📄 [governance policies]
│       │
│       ├── 📁 hydration/                       # Data hydration
│       │   └── 📄 [hydration configs]
│       │
│       ├── 📁 templates/                       # Template files
│       │   └── 📄 [template definitions]
│       │
│       ├── 📁 tests/                           # Testing framework
│       │   ├── 📄 pytest.ini                   # Test configuration
│       │   ├── 📄 requirements-test.txt        # Test dependencies
│       │   └── 📄 validation_results.json      # Test results
│       │
│       └── 📄 [configuration files]
│           ├── 📄 .pytest_cache/                # Test cache
│           └── 📄 [other configs]
│
└── 📁 [other project directories]
```

## 🔧 **Key System Components**

### **1. AI Role Management**
- **73+ System Prompts** available for different technologies
- **Role-based AI** for specialized tasks
- **Memory integration** for persistent knowledge

### **2. Progressive Mode Control**
- **Default: OFF** (production safety)
- **ON: Testing** (canary slices only)
- **Automatic OFF** before main merge

### **3. Memory System**
- **Persistent storage** for rules and decisions
- **Snapshot capability** for project state backup
- **Bridge integration** with existing systems

### **4. Synchronization**
- **Artifact tracking** across environments
- **Concurrency management** for safe operations
- **Index management** for efficient retrieval

## 📋 **File Naming Conventions**

- **`.mdc`** - AI role definitions and rules
- **`.md`** - Documentation and guides
- **`.yaml`** - Configuration files
- **`.py`** - Python implementation files
- **`.json`** - Data and state files

## 🚀 **System Capabilities**

1. **Multi-Role AI** - Specialized AI for different tasks
2. **Memory Persistence** - Store and retrieve knowledge
3. **Progressive Safety** - Controlled testing environment
4. **Framework Integration** - Bridge with existing systems
5. **Documentation Hub** - Centralized knowledge management

---

**Last Updated:** 2024-08-24  
**System Version:** v1.0.0  
**Progressive Mode:** OFF (Safe Default)
