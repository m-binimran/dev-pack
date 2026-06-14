---
description: Reviews Postgres/Supabase schema, migrations, queries, and RLS for safety and performance. Use when DB code changes, before applying a migration, or inside /...
---

# /db-reviewer $ARGUMENTS

Launch the `db-reviewer` subagent to review: $ARGUMENTS

If no target is specified, review the most recent changes (run `git diff`). Relay the subagent's findings,
grouped by severity, with its verdict.
