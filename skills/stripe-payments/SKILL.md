---
name: stripe-payments
description: Integrate Stripe payments in Next.js — Checkout/Payment Intents, webhooks with signature verification and idempotency, and reconciling state to the database. Use when adding payments, subscriptions, or one-off charges.
---

# stripe-payments

Money is the highest-stakes path. The webhook — not the browser redirect — is the source of truth.

## Process
1. **Create the session server-side** (Checkout Session or Payment Intent) in a route handler/action. Pass a
   stable reference (user id, order id) in `metadata`. Never set prices from client input — look them up server-side.
2. **The browser redirect is a hint, not a fact.** Don't grant access on the success URL alone.
3. **Webhooks are the source of truth:** a route handler that **verifies the signature** with the webhook
   secret, then updates the DB (`checkout.session.completed`, `invoice.paid`, etc.).
4. **Idempotency:** webhooks retry. Record processed event ids and ignore duplicates; make DB updates idempotent.
5. **Reconcile to your DB:** subscription status, entitlements, order state — driven by webhook events, not
   client calls.

## Output
- The session-creation handler, the signature-verified webhook handler, the idempotency guard, and the DB
  updates each event triggers.

## Guardrails
- **Verify every webhook signature.** An unverified webhook endpoint is a way to grant yourself free product.
- Stripe secret + webhook secret are server-only secrets (the `secret-scan` hook blocks them in client code).
- Use Stripe **test mode** keys in dev; never run real charges while building.
- Read the raw request body for signature verification (don't let a framework parse it first).
