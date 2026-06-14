---
name: claude-pack-builder
description: >
  Design, build, verify, and publish a curated Claude Code pack — a reusable collection of
  rules, skills, hooks, loops, and review agents — to GitHub. Trigger this skill whenever the
  user wants to "create a Claude Code pack", "build a rules/hooks/skills collection", "make a
  guardrail pack", "package my hooks/skills/agents", "publish a Claude Code config to GitHub",
  or assemble enforced standards for a stack (e.g. Next.js + Supabase, Django, etc.). This skill
  is the methodology that produced github.com/m-binimran/dev-pack; reuse it instead of
  re-deriving the process. Run it BEFORE writing any pack files — it sequences research,
  clarification, building, verification, and safe publishing.
---

# Claude Pack Builder

You are operating as a professional GitHub publisher. The deliverable is a small, **enforced**,
honestly-documented Claude Code pack — and a clean public repo. The reference implementation this
skill produced is **github.com/m-binimran/dev-pack** (Next.js + Supabase). Read it for examples.

## Reference Library — load per phase (NOT all at once)

| File | Load when |
|------|-----------|
| `references/hook-authoring.md` | Building hooks — stdin/exit-code protocol, fail-open vs fail-closed, settings.json wiring, hook + test-harness skeletons |
| `references/verification.md` | After building, before publishing — the full "did I actually verify it" checklist + commands |
| `references/safe-publish.md` | Publishing to GitHub — secret scan, naming/rename, privacy-safe identity, .gitattributes, gh repo create, confirm visibility, verify remote CI |

---

## The five goals (every item must serve ≥1)
🪙 fewer tokens · 🎯 accuracy · ✅ truth-telling · ⚡ speed · 💎 quality. If an item serves none, cut it.

## The core insight
**Rules are advisory** (the model may ignore them under load). **Hooks are deterministic** — they run
every time. So the guarantees come from **hooks**; rules, skills, loops, and agents layer on top. When the
user wants something *enforced*, it's a hook, not a rule.

## The layers
| Layer | Folder | Nature | Installs to |
|-------|--------|--------|-------------|
| Rules | `rules/` | Advisory `CLAUDE.md` fragments | appended to `<project>/CLAUDE.md` |
| Skills | `skills/<name>/SKILL.md` | On-demand capability packs | `.claude/skills/` |
| Hooks | `hooks/*.py` + `settings.json` | **Deterministic enforcement** | `.claude/hooks/` + merged settings |
| Loops | `loops/*.md` | Multi-step slash commands | `.claude/commands/` |
| Agents | `agents/*.md` | Review subagents | `.claude/agents/` |

---

## Phase 1 — Research first (never fabricate)
Survey the real ecosystem before designing. Use WebSearch/WebFetch and read any local reference libraries
the user already has (e.g. `~/Claude rules/ecc/`, their existing skills). Produce a short comparison of
comparable repos and name the **gap** this pack fills. Cite real repos with URLs. Do not invent star counts,
benchmarks, or repos.

## Phase 2 — Clarify, then present a plan (pull method)
Ask only what changes the build, via AskUserQuestion:
- **Target stack** (decides which linters/tools hooks call).
- **Scope** (full pack vs. backbone-first vs. one-of-each sample).
- **Publish preference** (you publish vs. user publishes; public vs. private — decide at publish time).
Then present the full inventory as a table (item → what it does → which goal) **before building**. Get a go.

## Phase 3 — Design the inventory
For the chosen stack, design across all five layers. Map the path the user walks
(schema → migration → query → API → auth → component → animation → ship) and make sure each step has a skill,
each risky step has a hook, and each review domain has an agent. Don't ship a loop that references a
skill/agent you didn't build (dangling refs). Keep rule/skill files short — they cost tokens every turn.

## Phase 4 — Build real, working files
Build actual files, not stubs. Use the folder layout above plus: `README.md`, `INVENTORY.md` (the full
table), `CHANGELOG.md`, `SECURITY.md` (document each hook's fail mode), `CONTRIBUTING.md`, `LICENSE`,
`CLAUDE.md` (for working ON the repo), `.env.example`, `templates/`, `mcp/`, `install.{ps1,sh}`,
`uninstall.{ps1,sh}`, `tests/test_hooks.py`, `.github/` (CI + issue/PR templates).
→ Load `references/hook-authoring.md` for the hook + harness skeletons and the install/uninstall pattern.

## Phase 5 — Verify (truth-telling, non-negotiable)
Run everything; never claim "tested" without running it. → Load `references/verification.md`.
At minimum: run `tests/test_hooks.py`, run a real **install→uninstall cycle** on a temp project that has its
own CLAUDE.md + a non-pack file (prove you remove only your own files), validate all JSON, parse both
installers (PowerShell AST + `bash -n`), confirm scripts are pure ASCII, and validate all frontmatter.

## Phase 6 — Publish safely (outward-facing, hard to reverse)
→ Load `references/safe-publish.md`. Secret-scan the whole pack, make naming consistent (repo name +
internal identifiers), set a **privacy-safe git identity** (GitHub noreply email), add `.gitattributes`,
confirm **public vs private** with the user, `gh repo create`, then **verify the remote CI ran green** and
report the URL. Repo names can't contain spaces (normalize to hyphens).

## Honesty rules (apply to the pack AND to you)
- New repos start at **0 stars**. No inflated claims anywhere.
- Document each hook's real limits (e.g. a `truth-gate` is a reminder, not a mind-reader).
- If a step couldn't run in this environment, say "unverified" — don't mark it passed.
