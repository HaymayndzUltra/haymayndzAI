# prompt_factory_ai

## Purpose
Bootstraps new frameworks and role templates; extends existing frameworks.

## How It Works
- Consumes framework specification, role definitions, template parameters, and extension requests.
- Produces framework skeletons, role templates (`.mdc`), and configuration files.
- Success requires complete, valid structure with all required components.
- Not single-writer; primarily creates new files.

## How to Use It
- Commands:
  - `/new_framework <name>`: create a new framework skeleton
  - `/extend_framework <name>`: add roles to an existing framework
  - `/template <role>`: generate a custom role template
- Allowed verbs: CREATE, EXTEND, TEMPLATE, BOOTSTRAP.

## Example Usage
```bash
/new_framework fwk-002-data-pipeline
/extend_framework fwk-001-cursor-rules
/template ingestion_ai
```

## Dependencies
- None at runtime; outputs are consumed by framework users and other roles.