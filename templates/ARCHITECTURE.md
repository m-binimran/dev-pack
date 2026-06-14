# ARCHITECTURE — <Project Name>

> Locks the stack and the big decisions. Don't change mid-build without updating this file.

## Stack (locked)
- Framework: Next.js (App Router)
- DB: Supabase (Postgres) + RLS
- Auth: Supabase Auth
- Styling: <Tailwind / CSS modules>
- Hosting: <Vercel>
- State: <one approach>

## Diagram
```
[ Browser ] → [ Next.js (server + client components) ] → [ Supabase: Postgres + Auth + Storage ]
```

## Data model
Owned by `schema-designer`. Summary of main tables + relationships here; full DDL in `/supabase/migrations`.

## Key decisions (ADR-lite)
| Decision | Choice | Why | Date |
|----------|--------|-----|------|
| | | | |

## Boundaries & security
- Secrets: env vars only (`secret-scan` hook enforces).
- RLS on all user-data tables (`rls-policy` skill).
- Input validated in server actions / route handlers.
- Service-role key: server-side only.

## Environments
| Env | DB | Notes |
|-----|----|-------|
| local | local/shadow Postgres | safe to reset/seed |
| prod | Supabase project | destructive ops human-confirmed only |
