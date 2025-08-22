# Café Project Profile Summary

## Scope & Constraints
- Budget: $500
- Timeline: 3 weeks
- Features: Menu browsing, online ordering (pickup only), PayPal checkout, admin dashboard (orders, status updates, daily sales report).

## Enabled Roles
- product_owner_ai, planning_ai, data_ai, codegen_ai, qa_ai, mlops_ai, documentation_ai, security_ai

## Disabled Roles
- auditor_ai, principal_engineer_ai, observability_ai, analyst_ai, prompt_linter_ai, l10n_i18n_ai

## Routing Additions
- /design_schema, /create_migration, /optimize_queries → data_ai
- /security_scan, /threat_model, /compliance_check → security_ai

## QA Gate
- All tests pass (>= 80% coverage)

## Payments
- Provider: PayPal (Credit cards via PayPal Checkout)
- PCI scope minimized; no raw card handling on site

## Hosting & DB
- Hosting: Vercel
- Database: Supabase Postgres

## DB Artifacts
- Schema: examples/database_schema.cafe.sql
- Migration: examples/migration_001_init.cafe.sql
- View: daily_sales (orders/day, total revenue)

## Admin Ops
- Order status: NEW → IN_PROGRESS → READY_FOR_PICKUP → COMPLETED/CANCELLED
- Daily Sales from `daily_sales` view

## Next Steps
- Implement minimal UI with mobile-friendly design and branding
- Integrate PayPal Checkout
- Deploy to Vercel; provision Supabase; run migration