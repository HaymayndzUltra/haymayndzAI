# codegen_ai

## Purpose
Generates production-grade code from a reviewed technical plan with strong quality gates.

## How It Works
- Consumes `technical_plan.md`, `task_breakdown.yaml`, coding standards, and existing codebase context.
- Produces source files, unit tests, and API documentation.
- Success requires clean build, passing tests, and linting compliance.
- Collaborates with `qa_ai` for review (not single-writer).

## How to Use It
- Commands:
  - `/gen_code <path>`: generate code into target path
  - `/implement <task_id>`: implement a specific task
  - `/refactor <component>`: improve structure
- Allowed verbs: GENERATE, IMPLEMENT, REFACTOR, OPTIMIZE.

## Example Usage
```bash
/gen_code src/services/auth
/implement TASK-001
/refactor user-service
```

## Dependencies
- Requires outputs from `planning_ai`.
- Downstream consumer: `qa_ai` for validation.