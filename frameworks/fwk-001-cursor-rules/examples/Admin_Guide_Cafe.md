# Admin Guide — Café Ordering Site

## Login
- Use provided admin credentials to access the dashboard.

## Update Menu Items
1. Go to Menu → Items.
2. Create/Update items with: name, description, category, price.
3. Toggle `Active` to hide/show items.

## Manage Categories
1. Go to Menu → Categories.
2. Add/Edit categories (Coffee, Tea, Pastries).
3. Reorder by position.

## View Incoming Orders
- Dashboard shows newest first.
- Status transitions:
  - NEW → IN_PROGRESS → READY_FOR_PICKUP → COMPLETED/CANCELLED

## Update Order Status
1. Open order details.
2. Set status based on progress.

## Daily Sales Report
- Go to Reports → Daily Sales.
- Shows per-day:
  - Number of orders
  - Total revenue
- Backed by DB view `daily_sales`.

## Prices and Taxes
- Update item `price` to change price.
- Tax handling depends on deployment region; set in environment config.

## Payments
- PayPal Checkout handles payments; refunds via PayPal dashboard.

## Support
- For account issues or outages, contact the site owner or hosting provider.