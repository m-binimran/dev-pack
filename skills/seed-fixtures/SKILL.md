---
name: seed-fixtures
description: Generate realistic seed data and reset scripts for local Postgres/Supabase development and tests. Use when setting up a dev database, needing test fixtures, or making a reproducible local data state.
---

# seed-fixtures

Reproducible local data so dev and tests start from a known state.

## Process
1. **Respect FK order:** insert parents before children. Reset in reverse.
2. **Make it deterministic:** fixed UUIDs/timestamps for anything a test asserts on. Random is fine
   only for volume/noise data.
3. **Realistic, not lorem:** plausible names, emails (`@example.com`), prices, dates — so the UI looks real.
4. **Provide a reset:** a `seed.sql` that truncates (dev only!) then re-inserts, idempotent.

## Output
- `supabase/seed.sql` (runs on `supabase db reset`) or a `scripts/seed.ts`.
- A small "reset + seed" command in the README.

## Guardrails
- Seed/reset scripts touch the **local** DB only. Guard them so they can't point at prod
  (check the connection string / refuse if host looks like production).
- Use `@example.com` emails and obviously-fake data — never real customer data in fixtures.
