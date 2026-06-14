---
description: Run the build/tests, fix what fails, repeat until green or capped. Reports honestly.
---

# /build-green $ARGUMENTS

Get the project to a green build/test state. `$ARGUMENTS` may name a specific command or scope.

1. **Run** the build + tests (e.g. `next build`, `npm test`, `tsc --noEmit`). Capture the full output.
2. **If green:** report it with the actual summary line and stop.
3. **If red:** read the FIRST real error (not downstream noise). Fix only that. Don't shotgun-edit.
4. **Re-run** the same command.
5. **Repeat** up to **5 rounds**.
6. **If still red after 5 rounds:** STOP. Report exactly which errors remain, what you tried, and your best
   hypothesis. Do not claim it's fixed. Do not loosen configs (disable lint, `// @ts-ignore`, skip tests)
   just to go green unless the user approves — that's faking it.

Truthfulness: "green" requires the command to actually exit 0 this session. Paste the proof.
