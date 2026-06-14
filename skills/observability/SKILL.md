---
name: observability
description: Add error monitoring and structured logging to a Next.js + Supabase app — Sentry for errors, request-scoped logs, and useful context without leaking PII. Use when setting up monitoring or debugging production issues.
---

# observability

You can't fix what you can't see. Capture errors with context; don't capture secrets.

## Error monitoring
- **Sentry (or equivalent)** on client, server, and edge. Source maps uploaded so stack traces are readable.
- Capture in `error.tsx` boundaries and in route handler/action catch blocks — re-throw or report, don't swallow.
- Attach context: route, user id (not email/PII), request id. **Scrub** tokens, passwords, card data, full emails.

## Logging
- **Structured (JSON) logs** with a level (`info`/`warn`/`error`) and a request/correlation id, not bare
  `console.log` strings. Log decisions and failures, not noise.
- Log server-side only; never log secrets, full request bodies with credentials, or PII.
- One line per meaningful event; include enough to reproduce, nothing more.

## What to watch
- Error rate + new error types after a deploy, slow routes/queries (pair with `query-optimizer`),
  failed webhooks/payments, auth failures spiking.

## Output
- The Sentry init (client/server/edge), the logging helper, and the PII-scrubbing rules applied.

## Guardrails
- Monitoring must not become a leak: no secrets/PII in events or logs (the `secret-scan` hook guards code,
  but you must scrub runtime values too).
- Don't ship `console.log` debugging to production (the `code-quality` rule forbids it) — use the logger.
