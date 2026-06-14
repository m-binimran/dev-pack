---
description: Diagnose and fix a slow query end-to-end with EXPLAIN ANALYZE, then prove the improvement.
---

# /db-tune $ARGUMENTS

Speed up the slow query/endpoint in `$ARGUMENTS` using the `query-optimizer` skill. Evidence at every step.

1. **Reproduce.** Identify the exact query (from code or logs). Run `EXPLAIN (ANALYZE, BUFFERS)` and record
   the baseline time and the bottleneck node.
2. **Diagnose.** Name the cause: seq scan, missing index, N+1, bad join, deep OFFSET, stale stats.
3. **Fix — smallest change first.** Add one index, rewrite one predicate, or fix the N+1. Use
   `CREATE INDEX CONCURRENTLY` on busy tables.
4. **Re-measure.** Run `EXPLAIN ANALYZE` again. Report baseline → new time. If no improvement, revert and
   try the next hypothesis — don't leave a useless index behind.
5. **Report.** Cause, fix, and the real before/after numbers. State the write-cost of any new index.

Truthfulness: a "faster" claim requires before/after `EXPLAIN ANALYZE` from this session.
