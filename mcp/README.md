# MCP config

Two servers that let the agent **observe reality** instead of guessing — which is what makes
truth-telling and accuracy possible.

| Server | What it gives the agent | Why it matters |
|--------|-------------------------|----------------|
| `postgres` | Run read queries + `EXPLAIN ANALYZE` against your **local** DB | `query-optimizer` / `db-tune` can prove a query is fast instead of claiming it |
| `playwright` | Drive a real browser, take screenshots, read the DOM | `a11y-audit`, `perf-budget`, `ship-check` can *see* the page, not assume it works |

## Setup
1. Copy `.mcp.json` to your project root (or merge into an existing one).
2. Set `DATABASE_URL` to your **local/dev** database — never production.
3. The Postgres server here is read-capable; pair it with the `sql-safety-guard` hook so
   destructive statements are still blocked.

> Point the Postgres MCP at a local or read-replica DB. Giving an agent a writable prod
> connection string defeats every guardrail in this pack.
