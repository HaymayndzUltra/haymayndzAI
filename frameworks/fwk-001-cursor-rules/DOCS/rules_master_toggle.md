# rules_master_toggle

## Purpose
Central control for role activation and command routing for the framework.

## How It Works
- Maintains a YAML role activation matrix (`enabled`, `priority`, `triggers`, `dependencies`) for core, support, orchestration, and optional roles.
- Provides a command routing map from trigger strings (e.g., `/plan`, `/gen_code`) to handler roles.
- Supports interaction verbs: TOGGLE, STATUS, ROUTE, CONFIGURE.
- Single-writer policy: owns the role configuration.

## How to Use It
- Commands:
  - `/toggle <role> on|off`: enable or disable a role
  - `/status`: show current activation status for all roles
  - `/route <command>`: show which role will handle a command
- Typical flow: ensure required dependencies are enabled before enabling a downstream role.

## Example Usage
```bash
# Disable security temporarily
/toggle security_ai off

# Verify routing target
/route /gen_code

# Show all roles and states
/status
```

## Dependencies
- None at runtime; manages configuration referenced by all other roles.