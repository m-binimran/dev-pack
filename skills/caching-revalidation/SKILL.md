---
name: caching-revalidation
description: Get Next.js App Router caching right — static vs dynamic rendering, fetch cache, revalidatePath/revalidateTag, and ISR. Use when data is stale, a page won't update, or you're tuning performance vs freshness.
---

# caching-revalidation

Next.js caches aggressively by default. Most "my data won't update" bugs are caching, not logic.

## Decide freshness per route
- **Static (default where possible):** marketing/content pages. Fast, cached at the edge.
- **ISR:** mostly-static with periodic refresh — `export const revalidate = 3600` (seconds).
- **Dynamic:** per-request/user data — reads of cookies/headers/`searchParams`, or `export const dynamic = 'force-dynamic'`.

## Invalidate on write
- After a mutation (server action/route handler) that changes displayed data, call **`revalidatePath('/path')`**
  or **`revalidateTag('tag')`** so caches refresh. Tag fetches you'll need to bust:
  `fetch(url, { next: { tags: ['projects'] } })`.
- For user-specific/never-cache reads, opt out: `fetch(url, { cache: 'no-store' })`.

## Common fixes
- "Stale after save" → you mutated but didn't `revalidatePath/Tag`.
- "User sees another user's data" → a per-user route got statically cached; make it dynamic.
- "Slow every load" → over-using `no-store`; cache + revalidate instead.

## Output
- Per affected route: static / ISR / dynamic, plus the revalidation call wired to each mutation.

## Guardrails
- Never cache per-user/authenticated data at a shared layer.
- Don't blanket `force-dynamic` to "fix" caching — target the actual route.
- Verify freshness by actually triggering the mutation and reloading (don't assume).
