# Cafe Web

## Setup
1. cd apps/cafe-web
2. cp .env.example .env.local and fill credentials
3. npm install
4. npm run dev

## Routes
- / : home
- /menu : browse menu
- /cart : view cart
- /checkout : checkout (PayPal)
- /admin : admin dashboard

## API (stubs)
- GET /api/menu
- GET/POST /api/orders
- POST /api/paypal