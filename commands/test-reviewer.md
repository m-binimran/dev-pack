---
description: Reviews test quality and coverage - behavioral vs implementation tests, edge cases, regression tests for bug fixes, flakiness, and whether the change is actu...
---

# /test-reviewer $ARGUMENTS

Launch the `test-reviewer` subagent to review: $ARGUMENTS

If no target is specified, review the most recent changes (run `git diff`). Relay the subagent's findings,
grouped by severity, with its verdict.
