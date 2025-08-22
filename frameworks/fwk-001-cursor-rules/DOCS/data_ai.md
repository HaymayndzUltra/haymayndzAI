# data_ai (optional)

## Purpose
Designs database schemas, manages migrations, and optimizes data models.

## How It Works
- Consumes data requirements, performance constraints, existing schema, and migration needs.
- Produces `database_schema.sql`, `migration_scripts.sql`, and `data_model.mermaid`.
- Success requires validated schema, tested migrations, and good performance.
- Single-writer policy: owns `database_schema.sql`.

## How to Use It
- Commands:
  - `/design_schema`: create schema from requirements
  - `/create_migration`: generate migration scripts
  - `/optimize_queries`: tune performance
- Allowed verbs: DESIGN, MIGRATE, OPTIMIZE, MODEL.

## Example Usage
```bash
/design_schema
/create_migration
/optimize_queries
```

## Dependencies
- Consumes requirements from `planning_ai`; supports `codegen_ai` with models and migrations.