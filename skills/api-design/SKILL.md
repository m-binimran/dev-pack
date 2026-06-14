---
name: api-design
description: Design Next.js route handlers and server actions with input validation, correct status codes, error handling, and rate limiting. Use when building an API endpoint, server action, or webhook receiver.
---

# api-design

The server boundary between UI and database. Validate everything; never trust the caller.

## Choose the right tool
- **Server Action** — form submits / mutations from your own UI. Co-located, type-safe, no manual fetch.
- **Route Handler** (`app/api/.../route.ts`) — webhooks, third-party callers, public/REST endpoints, file streams.

## Every endpoint
1. **Validate input with Zod at the top.** Reject early with `400` + a useful message. Re-validate even if the
   client already did.
2. **Authenticate + authorize:** get the user (server), check they may do this. RLS is the backstop, not the
   only gate for sensitive actions.
3. **Correct status codes:** 200/201 success, 400 bad input, 401 unauthenticated, 403 forbidden, 404 missing,
   409 conflict, 429 rate-limited, 500 only for true server faults.
4. **Handle errors explicitly.** Catch, log server-side, return a safe message — never leak stack traces or DB
   errors to the client.
5. **Rate-limit public/mutating endpoints** (e.g. Upstash). Idempotency keys for anything chargeable.
6. **Shape responses consistently** (`{ data }` / `{ error }`); don't return raw DB rows with internal columns.

## Output
- The handler/action, the Zod schema, the auth check, and the status codes it returns.
- Note what's validated, what's rate-limited, and what an attacker could try.

## Guardrails
- No unvalidated input reaching the DB or filesystem.
- No secrets or internal error details in responses.
- Mutations are POST/PUT/PATCH/DELETE, not GET.
