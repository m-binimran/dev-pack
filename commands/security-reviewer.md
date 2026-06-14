---
description: Security-focused review of a diff - secrets, injection, auth/authz, RLS gaps, SSRF, XSS/CSRF, OWASP Top 10. Use after changes touching auth, input handling,...
---

# /security-reviewer $ARGUMENTS

Launch the `security-reviewer` subagent to review: $ARGUMENTS

If no target is specified, review the most recent changes (run `git diff`). Relay the subagent's findings,
grouped by severity, with its verdict.
