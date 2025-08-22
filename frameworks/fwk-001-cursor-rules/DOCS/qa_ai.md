# qa_ai

## Purpose
Validates functionality and quality through automated tests and reviews.

## How It Works
- Consumes generated `source_code`, `acceptance_criteria.json`, and test requirements.
- Produces `test_results.json`, `coverage_report.html`, and `quality_assessment.md`.
- Success requires all tests to pass, target coverage, and no critical issues.
- Single-writer policy: owns `test_results.json`.

## How to Use It
- Commands:
  - `/test`: execute full suite
  - `/review <component>`: code quality review
  - `/validate <feature>`: check against acceptance criteria
- Allowed verbs: TEST, REVIEW, VALIDATE, ANALYZE.

## Example Usage
```bash
/test
/review user-authentication
/validate FEAT-001
```

## Dependencies
- Depends on outputs from `codegen_ai` and `product_owner_ai`.
- Upstream gate for `mlops_ai` deployment.