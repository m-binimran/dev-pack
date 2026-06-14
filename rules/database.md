## Database (Postgres / Supabase)

- **Parameterized queries only.** Never build SQL by string-concatenating user input.
- **Migrations are reversible.** Every `up` has a matching `down`. No migration without a rollback path.
- **No destructive SQL without an explicit OK.** `DROP`, `TRUNCATE`, and `DELETE`/`UPDATE` without a
  `WHERE` are blocked by the `sql-safety-guard` hook — don't try to route around it.
- **Never run against production** unless the user explicitly names prod and confirms. Default to local/shadow DB.
- **Index intentionally.** Add indexes for foreign keys and frequent filters; justify each one.
- **`EXPLAIN ANALYZE` before shipping** any query expected to scan a large table.
- **RLS on by default** for Supabase tables holding user data. No table ships with RLS off silently.
- Prefer the expand → migrate → contract pattern for column changes to avoid downtime.
