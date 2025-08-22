# documentation_ai

## Purpose
Generates and maintains comprehensive technical documentation aligned with the code and plans.

## How It Works
- Consumes source code, API specs, user stories, and architecture diagrams.
- Produces `api_docs.yaml`, `user_guide.md`, and `developer_guide.md`.
- Success requires complete, accurate, and up-to-date docs.
- Single-writer policy: owns documentation files.

## How to Use It
- Commands:
  - `/docs`: generate comprehensive documentation
  - `/update_docs <component>`: refresh a specific section
  - `/validate_docs`: check completeness and accuracy
- Allowed verbs: GENERATE, UPDATE, VALIDATE, FORMAT.

## Example Usage
```bash
/docs
/update_docs api
/validate_docs
```

## Dependencies
- Upstream from `codegen_ai`, `product_owner_ai`, and `planning_ai` artifacts.