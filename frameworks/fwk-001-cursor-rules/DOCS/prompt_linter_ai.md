# prompt_linter_ai (optional)

## Purpose
Enforces corporate prompt engineering standards for clarity and consistency.

## How It Works
- Consumes prompt content, a style guide, quality metrics, and usage context.
- Produces `lint_report.json`, `style_violations.md`, and `improvement_suggestions.yaml`.
- Success requires all prompts to pass required quality checks.
- Single-writer policy: owns `lint_report.json`.

## How to Use It
- Commands:
  - `/lint_prompts`: validate all prompts
  - `/check_style <file>`: analyze a specific prompt file
  - `/suggest_improvements`: propose enhancements
- Allowed verbs: LINT, CHECK, VALIDATE, IMPROVE.

## Example Usage
```bash
/lint_prompts
/check_style system-prompt/codegen_ai.mdc
/suggest_improvements
```

## Dependencies
- Applies across roles; often used with `documentation_ai` for cohesive style in docs.