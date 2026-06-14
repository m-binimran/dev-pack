---
name: supabase-auth
description: Set up Supabase Auth in Next.js App Router — email/OAuth sign-in, server-side sessions, middleware refresh, and protected routes. Use when adding login, sign-up, OAuth, or gating pages behind auth.
---

# supabase-auth

Auth is the foundation RLS stands on (`auth.uid()`). Get the session right on the server.

## Process
1. **Two clients, two jobs:** a browser client (client components) and a server client (server components,
   actions, route handlers) via `@supabase/ssr`. Don't share one across the boundary.
2. **Middleware refreshes the session** on every request and writes cookies — without it, server reads see a
   stale/expired token. Keep the middleware matcher tight (skip static assets).
3. **Read the user on the server** in protected layouts/pages: `const { data: { user } } = await
   supabase.auth.getUser()`. Use `getUser()` (verifies with the auth server), not `getSession()`, for auth checks.
4. **Gate routes** in a server component/layout: no user → `redirect('/login')`. Don't gate only on the client.
5. **OAuth / email:** sign-in triggers a redirect to `/auth/callback` (a route handler that exchanges the code
   for a session). Sign-out calls `supabase.auth.signOut()` then redirects.

## Output
- The browser + server client setup, the middleware, the callback route, and one protected page example.
- State which routes are gated and where the check runs (server).

## Guardrails
- **Never trust the client for authorization** — the real boundary is server checks + RLS.
- The **service-role key bypasses RLS** — server-only, never in a client component (the `secret-scan` hook blocks it).
- Use `getUser()` for auth decisions; `getSession()` can return an unverified cached session.
