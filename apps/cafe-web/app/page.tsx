import Link from 'next/link';

export default function HomePage() {
  return (
    <main style={{ padding: 24 }}>
      <h1>{process.env.NEXT_PUBLIC_SITE_NAME || 'Cafe'}</h1>
      <nav style={{ display: 'flex', gap: 12 }}>
        <Link href="/menu">Menu</Link>
        <Link href="/cart">Cart</Link>
        <Link href="/checkout">Checkout</Link>
        <Link href="/admin">Admin</Link>
      </nav>
      <p style={{ marginTop: 16 }}>Welcome! Order for pickup today.</p>
    </main>
  );
}