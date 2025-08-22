import { NextResponse } from 'next/server';

export async function POST(req: Request) {
  const body = await req.json().catch(() => ({}));
  // TODO: integrate with PayPal Orders API
  return NextResponse.json({ id: 'TEST_ORDER_ID', mode: process.env.PAYPAL_MODE || 'sandbox', received: body });
}