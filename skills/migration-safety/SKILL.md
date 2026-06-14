---
name: migration-safety
description: Generate safe, reversible Postgres/Supabase migrations using the expand→backfill→contract pattern, avoiding locks and data loss. Use when altering schema, adding/removing columns, or changing types on tables that already hold data.
---

# migration-safety

Every migration must be reversible and must not lock a busy table or drop data by surprise.
(The `migration-validate` hook checks your output — design to pass it.)

## Always produce a pair
- `up`: the change.
- `down`: the exact rollback. If a change is truly irreversible (dropping data), say so loudly
  and require explicit confirmation.

## Expand → backfill → contract (for column changes)
1. **Expand:** add the new column/table, nullable, no constraint. Cheap, non-locking.
2. **Backfill:** populate in batches (`update ... where id between ...`), not one giant statement.
3. **Contract:** add the `NOT NULL`/constraint and drop the old column — in a *later* migration,
   after the app writes both.

## Locking traps to avoid
- `ADD COLUMN ... NOT NULL` with no `DEFAULT` on a non-empty table → fails / full rewrite. Add a default.
- `ALTER COLUMN TYPE` → rewrites + locks. Prefer add-new-column + backfill.
- Creating an index on a hot table → use `CREATE INDEX CONCURRENTLY` (outside a txn).

## Output
- `up` SQL, `down` SQL, and a one-line risk note (lock risk / data-loss risk / safe).
- For destructive steps, an explicit "this cannot be undone" line.

## Guardrails
- No migration without a rollback path.
- Never combine a destructive drop with the additive change in the same migration — separate them.
