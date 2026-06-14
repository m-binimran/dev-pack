---
description: Safe schema-change loop. Design → generate reversible up/down → validate on a shadow DB → apply.
---

# /migration-loop $ARGUMENTS

Make the schema change described in `$ARGUMENTS` safely. Use the `migration-safety` skill.

1. **Design.** State the change and its risk (lock risk / data-loss risk / safe). If it touches a column on
   a table with data, plan expand → backfill → contract.
2. **Generate the pair.** Write the `up` and the matching `down`. No migration without a rollback.
3. **Self-check.** Confirm: reversible? any `ADD COLUMN NOT NULL` without default? any unguarded
   DROP/TRUNCATE? (The `migration-validate` hook will also check the file when you write it.)
4. **Dry-run on a shadow/local DB.** Apply to local (e.g. `supabase db reset` + the migration, or a shadow
   branch). Never the production DB. Paste the result.
5. **Verify the rollback.** Apply `down`, confirm the schema returns to the prior state.
6. **Report.** Show the up/down SQL, the dry-run result, and the explicit risk note. If any step is
   destructive, say "this cannot be undone" and require confirmation before any prod apply.

Hard rule: this loop never applies to production. Promoting to prod is a separate, human-confirmed step.
