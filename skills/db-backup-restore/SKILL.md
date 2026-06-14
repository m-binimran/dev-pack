---
name: db-backup-restore
description: Safely back up and restore a Postgres/Supabase database — pg_dump/pg_restore, Supabase backups/PITR, and a no-data-loss restore runbook. Use before risky migrations, for disaster recovery, or when cloning prod to staging.
---

# db-backup-restore

Backups are only real if you've restored one. Treat restore as the thing you're actually buying.

## Back up
- **Logical (portable):** `pg_dump --format=custom --no-owner --file=backup.dump "$DATABASE_URL"`.
  Custom format restores selectively and in parallel.
- **Supabase:** managed daily backups; enable **Point-in-Time Recovery (PITR)** for anything important.
- **Before a risky migration:** take a fresh dump first. Note the timestamp and what it covers.
- Store backups off the database host. Never commit a dump (it's data — and may contain PII).

## Restore (runbook)
1. **Restore into a NEW/empty target first** (staging or a scratch DB), never straight over a live one:
   `pg_restore --no-owner --clean --if-exists -d "$TARGET_URL" backup.dump`
2. **Verify** row counts and a few key records match expectations before pointing anything at it.
3. Only then, if replacing prod, do it in a maintenance window with a fresh backup taken immediately prior.

## Safety
- **Never restore over production without an explicit human OK and a just-taken backup.** A restore is
  destructive — it can overwrite newer data.
- Test the restore path periodically; an untested backup is a hope, not a recovery plan.
- Scrub or limit PII when cloning prod → staging.

## Output
- The exact backup/restore commands for the situation, the target (never prod by default), and the
  verification step. State clearly when an action is destructive.
