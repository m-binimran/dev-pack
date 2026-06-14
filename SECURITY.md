# Security policy

## Scope
dev-pack ships shell-invoked Python hooks that run inside your Claude Code sessions. Treat them as code
that executes on your machine — read a hook before trusting it. Each hook documents its **fail mode**
(fail-open vs. fail-closed) in its docstring.

## Design stance
- `secret-scan` fails **closed**: if it errors, it blocks the write, so a crash can't let a secret through.
- All other guards fail **open**: a bug in a guard must not block your legitimate work.
- Guards are defense-in-depth, **not** a guarantee. `secret-scan` uses pattern matching and will miss novel
  secret formats; `sql-safety-guard` matches common destructive shapes, not every possible one. Don't rely on
  them as your only control — keep real secret management and DB backups.

## Reporting a vulnerability
If you find a way a guard can be trivially bypassed in a way that matters (e.g. an obvious secret pattern it
misses, or a destructive command it lets through), open a **private** security advisory on the repo, or a
regular issue if it's low-risk. Include a minimal repro. We'll add a regression test to `tests/test_hooks.py`
for the fix.

## What this project will never do
- Phone home or transmit your code/secrets anywhere. Hooks read stdin and write to stderr/stdout only.
- Auto-run destructive commands. The point of the pack is the opposite.
