---
name: truthful-reporter
description: Verify claims against real command output before reporting status. Use before saying a task is done, a build passes, tests are green, or a bug is fixed.
---

# truthful-reporter

Turn "it should work" into "here's proof it works" — or an honest "unverified."

## Before reporting status, run the matching check
| Claim | Proof required |
|-------|----------------|
| "Tests pass" | Run the test command. Paste pass/fail counts. |
| "It builds" | Run the build. Paste success or the error. |
| "Type-safe" | Run `tsc --noEmit` / the typecheck. |
| "Bug fixed" | Reproduce the bug, apply fix, show it no longer reproduces. |
| "Query is faster" | `EXPLAIN ANALYZE` before and after. |
| "Page works" | Load it (browser/preview) and observe, or say it's unverified. |

## Report format
- **State the result with evidence:** "Build passed — `next build` exited 0." or
  "2 of 14 tests fail — output below."
- **Name what you did NOT verify.** "Code compiles; I did not run it in a browser."
- **Never** convert "I wrote code that should do X" into "X works."

## Guardrails
- If a check can't run here, say so — don't substitute optimism for evidence.
- A partial pass is a partial pass; report the failures, don't bury them.

(The `truth-gate` and `verify-tracker` hooks back this up automatically, but this skill is the
discipline you apply yourself.)
