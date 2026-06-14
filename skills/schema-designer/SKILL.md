---
name: schema-designer
description: Design normalized Postgres/Supabase schemas — tables, columns, types, keys, indexes, and constraints with consistent naming. Use when creating a new database schema, adding tables, or reviewing a data model.
---

# schema-designer

Design a Postgres schema that's correct first, fast second.

## Process
1. **List the entities and relationships** before writing SQL. State cardinality (1:1, 1:N, N:M).
2. **Normalize to 3NF** unless there's a measured reason to denormalize. Note any denormalization explicitly.
3. **Write the DDL** following the conventions below.
4. **Add indexes** for every foreign key and every column used in frequent `WHERE`/`ORDER BY`. Justify each.
5. **Add constraints** — `NOT NULL`, `CHECK`, `UNIQUE`, FK `ON DELETE` behavior. Don't leave integrity to app code.

## Conventions
- Tables: plural snake_case (`order_items`). Columns: snake_case.
- Primary key: `id uuid primary key default gen_random_uuid()` (Supabase-friendly).
- Timestamps: `created_at timestamptz not null default now()`, `updated_at timestamptz` (with a trigger).
- Foreign keys: `<entity>_id`, always with an explicit `references` + `on delete` rule.
- Money: `numeric(12,2)`, never `float`. Booleans: `is_`/`has_` prefix.

## Output
- The `create table` statements.
- The index list with a one-line reason each.
- A note on which tables need RLS (hand off to `rls-policy`) and which columns hold PII.

## Guardrails
- Don't ship a table holding user data with RLS unconsidered.
- Don't use `text` for everything — pick real types and constraints.
- For N:M, create the explicit join table; don't fake it with arrays unless justified.
