# Contributing

Thanks for improving dev-pack. Keep the bar high and the scope tight (DB + web on Next.js + Supabase).

## Principles
- Every item must serve a stated goal: fewer tokens, accuracy, truth-telling, speed, or quality. If it
  doesn't, it doesn't belong here.
- **Hooks must be tested.** Include a sample-input test (see how `hooks/` were verified) and state the
  fail mode (open vs. closed) in the docstring.
- **No inflated claims** anywhere in docs. This repo practices the truth-telling it preaches.
- Keep rule/skill files short — they cost tokens on every turn.

## Adding a hook
1. Read JSON from stdin, decide, exit 0 (allow) or 2 (block, reason on stderr).
2. Pick a fail mode deliberately: fail-closed only when a crash must not let something through.
3. Wire it in `hooks/settings.json` with the right event + matcher.
4. Add a row to `INVENTORY.md`.

## Adding a skill, loop, or agent
- **Skill:** a folder under `skills/` with `SKILL.md` (YAML frontmatter: `name`, `description`).
- **Loop:** a `.md` under `loops/` with a `description` frontmatter; it installs as a slash command in
  `.claude/commands/`.
- **Agent:** a `.md` under `agents/` with frontmatter (`name`, `description`, `tools`, `model`); it installs
  as a subagent in `.claude/agents/`. Keep the system prompt terse and scoped to one review domain, and make
  it honour the truth-telling rule (cite lines, don't invent findings).
- Update `INVENTORY.md` and `CHANGELOG.md`. If a loop references a skill/agent, make sure that file exists.

## PRs
- One logical change per PR. Commit format: `<type>: <description>`.
- Note what you tested and paste the result.
