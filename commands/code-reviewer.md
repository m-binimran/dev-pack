---
description: Reviews a diff for correctness, security, and maintainability against the dev-pack standards. Use after writing or modifying code, and inside /plan-build-rev...
---

# /code-reviewer $ARGUMENTS

Launch the `code-reviewer` subagent to review: $ARGUMENTS

If no target is specified, review the most recent changes (run `git diff`). Relay the subagent's findings,
grouped by severity, with its verdict.
