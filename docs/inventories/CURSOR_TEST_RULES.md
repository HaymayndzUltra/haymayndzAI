## Folder: /.cursor/test and /.cursor/test-rules

Purpose: Large library of framework- and domain-specific `.mdc` rule prompts. Used for scoping behavior to particular stacks (React, Python, PHP, mobile, blockchain, etc.).

Highlights:
- Frontend: React/Next.js, Vue/Nuxt, Angular, Svelte, Remix/Astro/HTMX/Bootstrap.
- Backend: Node/Nest/Fastify, Python (Django/FastAPI/Flask), PHP (Laravel/WordPress/Drupal), Go, .NET, Ruby on Rails.
- Mobile: React Native/Expo, Flutter/Dart, Ionic/Capacitor.
- Specialized: AI/ML, Blockchain (Solidity/Solana), Game Dev (Unity/C#), Shopify/Liquid, Salesforce/Apex.

Auto-attach:
- Each file includes frontmatter with globs mapping to the relevant file types (e.g., `**/*.tsx` for React, `**/*.py` for Python, `**/*.php` for PHP).

Usage:
- The orchestrator maps file markers to attach the appropriate framework rules. These complements the universal rules under `/.cursor/rules`.

### Hydration Flow (Detector → Selector → Linter)
- Promote matching `.mdc` from `.cursor/test-rules/` into `.cursor/rules/` using repository markers:
```bash
python3 tools/rule_attach_detector.py --output rule_attach_log.json
python3 tools/hydration_selector.py --attach-log rule_attach_log.json --source .cursor/test-rules --dest .cursor/rules
python3 tools/mdc_linter.py --paths .cursor/rules .cursor/test-rules --write
```
- Artifacts: `rule_attach_log.json`, promoted `.mdc` files, and normalized frontmatter.