-- Café Project: Postgres schema
-- Tables: users (staff), menu_categories, menu_items, orders, order_items, payments

create table if not exists users (
  id uuid primary key default gen_random_uuid(),
  email text unique not null,
  password_hash text not null,
  role text not null check (role in ('admin','staff')),
  created_at timestamptz not null default now()
);

create table if not exists menu_categories (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  position int not null default 0
);

create table if not exists menu_items (
  id uuid primary key default gen_random_uuid(),
  category_id uuid not null references menu_categories(id) on delete cascade,
  name text not null,
  description text,
  price_cents int not null check (price_cents >= 0),
  is_active boolean not null default true,
  created_at timestamptz not null default now()
);

create type order_status as enum ('NEW','IN_PROGRESS','READY_FOR_PICKUP','COMPLETED','CANCELLED');

create table if not exists orders (
  id uuid primary key default gen_random_uuid(),
  customer_name text not null,
  customer_phone text,
  pickup_time timestamptz not null,
  status order_status not null default 'NEW',
  total_cents int not null default 0,
  created_at timestamptz not null default now()
);

create table if not exists order_items (
  id uuid primary key default gen_random_uuid(),
  order_id uuid not null references orders(id) on delete cascade,
  item_id uuid not null references menu_items(id),
  quantity int not null check (quantity > 0),
  unit_price_cents int not null check (unit_price_cents >= 0)
);

create type payment_status as enum ('PENDING','PAID','FAILED','REFUNDED');

create table if not exists payments (
  id uuid primary key default gen_random_uuid(),
  order_id uuid not null references orders(id) on delete cascade,
  provider text not null check (provider in ('paypal')),
  provider_ref text,
  amount_cents int not null check (amount_cents >= 0),
  status payment_status not null default 'PENDING',
  created_at timestamptz not null default now()
);

-- indexes for admin dashboard
create index if not exists idx_orders_created_at on orders(created_at desc);
create index if not exists idx_orders_status on orders(status, created_at desc);

-- view for daily sales report
create or replace view daily_sales as
select
  date_trunc('day', created_at) as day,
  count(*) filter (where status in ('READY_FOR_PICKUP','COMPLETED')) as num_orders,
  sum(total_cents) filter (where status in ('READY_FOR_PICKUP','COMPLETED')) as total_revenue_cents
from orders
group by 1
order by 1 desc;