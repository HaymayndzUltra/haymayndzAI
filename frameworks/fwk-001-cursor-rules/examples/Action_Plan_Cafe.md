# Action Plan — Café Online Ordering (3 weeks)

## Week 1 — Plan & Data
- Confirm branding assets (logo/colors) and content (menu categories/items seed).
- Data schema finalize; run migration 001 to set up DB.
- Payment integration sandbox setup (PayPal Checkout credentials).
- Define acceptance criteria per feature (menu, order, payment, admin dashboard).

## Week 2 — Build & QA
- Implement Public Site:
  - Menu listing (categories: coffee, tea, pastries), item detail, add to cart.
  - Checkout (pickup time same-day-only, PayPal checkout redirect/return).
- Implement Admin Dashboard:
  - Orders list with status transitions; order detail view.
  - Daily Sales report view (from `daily_sales`).
- QA: unit/integration tests, target >=80% coverage; security scan (basic) for payment flow.

## Week 3 — Polish & Deploy
- Mobile responsiveness and accessibility checks.
- Documentation: Admin Guide, Menu update steps, Deployment notes.
- Deploy to Vercel; configure Supabase; set environment variables; smoke tests.

## Environments
- Hosting: Vercel
- DB: Supabase Postgres (apply migrations)
- Payments: PayPal Checkout (sandbox → live)

## Acceptance Gates (tailored)
- Code generation gate: build passes, tests included, docs present.
- QA gate: All tests pass (>= 80% coverage); no critical security issues; performance acceptable.
- Deployment gate: health checks pass; rollback plan ready; monitoring configured (basic provider-level).

## Traceability
- Artifacts:
  - Profile: `examples/project_profile.cafe.yaml`
  - Schema: `examples/database_schema.cafe.sql`
  - Migration: `examples/migration_001_init.cafe.sql`
  - Guides/Docs: `examples/Admin_Guide_Cafe.md`, `examples/Profile_Summary_Cafe.md`