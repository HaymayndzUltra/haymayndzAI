# l10n_i18n_ai (optional)

## Purpose
Generates localization templates and validates internationalization readiness.

## How It Works
- Consumes source content, target languages, cultural requirements, and translation context.
- Produces `translation_templates.json`, `locale_configs.yaml`, and `l10n_guidelines.md`.
- Success requires complete templates and valid locale configurations.
- Single-writer policy: owns `translation_templates.json`.

## How to Use It
- Commands:
  - `/l10n_setup`: initialize i18n framework
  - `/generate_templates`: create translation templates
  - `/validate_locale <language>`: validate a specific locale
- Allowed verbs: SETUP, GENERATE, VALIDATE, TRANSLATE.

## Example Usage
```bash
/l10n_setup
/generate_templates
/validate_locale es-ES
```

## Dependencies
- Works with `documentation_ai` and product content; can be used pre-release.