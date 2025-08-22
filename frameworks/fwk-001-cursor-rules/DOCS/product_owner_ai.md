# product_owner_ai

## Purpose
Transforms business requirements into a prioritized backlog with clear acceptance criteria.

## How It Works
- Consumes business inputs (feature requests, objectives, feedback, market data).
- Produces `product_backlog.yaml`, `requirements_spec.md`, and `acceptance_criteria.json`.
- Success is defined by complete stories with explicit acceptance criteria.
- Single-writer policy: owns `product_backlog.yaml`.

## How to Use It
- Commands:
  - `/backlog <json|md>`: process new requirements
  - `/prioritize`: reorder backlog items
  - `/refine <story_id>`: refine a specific story
- Allowed verbs: CREATE, UPDATE, PRIORITIZE, REFINE.

## Example Usage
```bash
/backlog backlog_item:{id:"FEAT-001", title:"Auth", priority:"high", story:"As a user..."}
/prioritize
/refine FEAT-001
```

## Dependencies
- Inputs from stakeholders; downstream `planning_ai` consumes `product_backlog.yaml`.