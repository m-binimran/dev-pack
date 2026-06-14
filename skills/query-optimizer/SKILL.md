---
name: query-optimizer
description: Diagnose and fix slow Postgres queries using EXPLAIN ANALYZE, index suggestions, and N+1 detection. Use when a query is slow, a page is slow because of the DB, or before shipping a query that touches a large table.
---

# query-optimizer

Make the query fast based on evidence, not guesses.

## Process
1. **Get the plan:** run `EXPLAIN (ANALYZE, BUFFERS) <query>`. Never optimize without it.
2. **Read the plan top-down:** find the costliest node. Look for:
   - `Seq Scan` on a big table where an index could be used.
   - `Rows Removed by Filter` high → missing/!selective index.
   - Estimated vs actual rows far apart → stale stats (`ANALYZE`).
   - Nested loop over many rows → maybe a hash/merge join is better.
3. **Propose the smallest fix:** an index, a rewritten predicate, a `LIMIT`, or pagination.
4. **Re-measure** with `EXPLAIN ANALYZE` and report before/after timing. Don't claim a win without it.

## Common fixes
- Composite index ordered by selectivity for multi-column filters.
- Partial index (`where active`) for queries that always filter the same way.
- Replace `OFFSET` pagination with keyset (`where id > $last`) for deep pages.
- Kill **N+1**: one query per row in app code → use a join or `IN (...)`/`= ANY`.

## Output
- The plan's bottleneck in one sentence.
- The fix (SQL/DDL).
- Before/after timing from real `EXPLAIN ANALYZE` runs.

## Guardrails
- An index isn't free — it slows writes. Only add what the plan justifies.
- Don't add an index that duplicates an existing one's prefix.
