## Git

- Commit message format: `<type>: <description>` — types: feat, fix, refactor, docs, test, chore, perf, ci.
- Branch before committing if you're on the default branch. Don't commit straight to main.
- Commit/push only when the user asks.
- Never `--force` push or `--no-verify` unless the user explicitly says to. The `danger-guard` hook blocks these.
- Keep commits small and scoped to one logical change.
