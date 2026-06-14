---
name: rls-policy
description: Write and test Supabase/Postgres Row-Level Security policies so users can only access their own rows. Use when a table holds user data, when enabling RLS, or when auditing access control on Supabase.
---

# rls-policy

On Supabase, RLS is the real authorization boundary. The anon/auth keys reach the DB directly,
so a missing policy = open data.

## Process
1. **Enable RLS** on the table: `alter table X enable row level security;` (denies all by default).
2. **Write explicit policies** per operation (`select`, `insert`, `update`, `delete`) — don't use one
   `for all` policy unless the rule is genuinely identical.
3. **Scope by `auth.uid()`** for owner-based access:
   ```sql
   create policy "owners read" on profiles
     for select using (auth.uid() = user_id);
   create policy "owners write" on profiles
     for insert with check (auth.uid() = user_id);
   ```
   `using` filters existing rows; `with check` validates new/changed rows. Insert/update need `with check`.
4. **Test both directions:** the owner CAN, a different user CANNOT. State both tests.

## Patterns
- Public-read, owner-write: `select using (true)`, write policies gated by `auth.uid()`.
- Team access: join through a membership table inside the `using` expression.
- Service tasks: use the service-role key on the server only — it bypasses RLS, so never expose it client-side.

## Guardrails
- Never disable RLS to "make it work." Fix the policy.
- `with check` is required on insert/update or users can write rows they can't read back.
- The service-role key is a secret — server-side only (the `secret-scan` hook will catch it in client code).
