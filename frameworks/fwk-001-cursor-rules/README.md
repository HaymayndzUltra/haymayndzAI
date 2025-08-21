# fwk-001-cursor-rules Framework

[![Framework Version](https://img.shields.io/badge/version-v0.1.0-blue.svg)](https://github.com/your-org/frameworks)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![AI Roles](https://img.shields.io/badge/ai--roles-12-orange.svg)](system-prompt/)
[![Status](https://img.shields.io/badge/status-bootstrap-yellow.svg)](CHECKLIST.md)

A comprehensive AI framework skeleton for coordinated multi-role development workflows using Cursor IDE and AI assistants.

## Overview

This framework provides a structured approach to AI-assisted software development through specialized AI roles that handle different aspects of the development lifecycle. Each role has clearly defined responsibilities, input/output contracts, and interaction protocols.

## Quick Start

1. **Initialize Framework**: Review and customize role configurations in `system-prompt/`
2. **Configure Roles**: Enable desired roles in `system-prompt/rules_master_toggle.mdc`
3. **Start Development**: Begin with `/backlog` to feed requirements to the product owner AI
4. **Execute Pipeline**: Use `/run_pipeline` to orchestrate the complete development workflow

## Architecture

### Core Roles (Always Active)
- **product_owner_ai**: Requirements gathering and backlog management
- **planning_ai**: Technical architecture and implementation planning  
- **codegen_ai**: Production-ready code generation
- **qa_ai**: Comprehensive testing and quality assurance
- **mlops_ai**: Deployment automation and infrastructure management

### Support Roles
- **documentation_ai**: Technical documentation generation
- **analyst_ai**: Performance analysis and optimization
- **memory_ai**: Knowledge management and context preservation
- **observability_ai**: System monitoring and health tracking

### Orchestration
- **execution_orchestrator**: Pipeline coordination and workflow management
- **prompt_factory_ai**: Framework bootstrapping and role generation

### Optional Roles (Disabled by Default)
- **security_ai**: Security scanning and threat modeling
- **l10n_i18n_ai**: Localization and internationalization
- **prompt_linter_ai**: Prompt quality and style enforcement
- **data_ai**: Database schema design and migration management

## Command Reference

| Command | Role | Description |
|---------|------|-------------|
| `/backlog <data>` | product_owner_ai | Process requirements and create backlog |
| `/plan` | planning_ai | Generate technical implementation plan |
| `/gen_code <path>` | codegen_ai | Generate production-ready code |
| `/test` | qa_ai | Execute comprehensive test suite |
| `/deploy` | mlops_ai | Deploy to specified environment |
| `/run_pipeline` | execution_orchestrator | Execute complete development workflow |

## Directory Structure

```
frameworks/fwk-001-cursor-rules/
├── examples/                    # Usage examples and templates
├── src/                        # Generated source code
├── tests/                      # Test files and results
├── system-prompt/              # AI role definitions
│   ├── *.mdc                  # Core role specifications
│   ├── rules_master_toggle.mdc # Role activation control
│   ├── execution_orchestrator.mdc # Workflow coordination
│   └── OPTIONAL/              # Optional role definitions
├── README.md                  # This file
└── CHECKLIST.md              # Setup and customization tasks
```

## Next Steps

See [CHECKLIST.md](CHECKLIST.md) for detailed setup and customization tasks.

## Contributing

This framework follows the self-replicating pattern. Use `/new_framework <name>` to create additional framework variants or `/extend_framework` to add custom roles.

## License

MIT License - see LICENSE file for details.