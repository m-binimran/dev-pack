# CLAUDE.md — working ON dev-pack

This is the repo for the pack itself. (For using the pack in *your* project, run an installer — see README.)

## What this repo is
A curated, **enforced** Claude Code pack for database + website builders on Next.js + Supabase.
Layers: `rules/` (advisory) · `skills/` (on-demand) · `hooks/` (deterministic) · `loops/` (slash commands) ·
`agents/` (subagents) · `mcp/` · `templates/`. Full list in [INVENTORY.md](INVENTORY.md).

## House rules for changing this repo
- Every item must serve a stated goal: fewer tokens, accuracy, truth-telling, speed, quality.
- **Hooks must be tested.** Add a case to `tests/test_hooks.py` and run it: `python tests/test_hooks.py`.
  State the fail mode (open/closed) in the hook docstring.
- Keep rule/skill files short — they cost tokens every turn.
- **No inflated claims** anywhere. Anything documented as working must actually have been run. This repo
  practices the truth-telling it preaches.
- Update `INVENTORY.md` and `CHANGELOG.md` when adding/removing items.

## Verify
```bash
python tests/test_hooks.py        # all hook behavior
python -c "import json;json.load(open('hooks/settings.json'))"   # config valid
```

## Conventions
- Commit format: `<type>: <description>` (feat/fix/docs/refactor/test/chore).
- Hooks are Python 3.8+ (cross-platform). One logical change per PR.
