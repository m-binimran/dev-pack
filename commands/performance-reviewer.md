---
description: Reviews a change for performance - N+1 queries, missing indexes, slow queries, client bundle size, Core Web Vitals, caching/revalidation, render performance....
---

# /performance-reviewer $ARGUMENTS

Launch the `performance-reviewer` subagent to review: $ARGUMENTS

If no target is specified, review the most recent changes (run `git diff`). Relay the subagent's findings,
grouped by severity, with its verdict.
