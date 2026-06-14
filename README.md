# dev-pack

**Guardrails, skills & agent loops for database + website builders on Claude Code.**
Targeted at the **Next.js + Supabase (Postgres)** stack.

Most "awesome" lists are broad and advisory. This pack is narrow and **enforced**: the
guarantees come from **hooks** (deterministic — they run every time), with rules, skills and
loops layered on top.

**Why this exists (vs. what's already out there):** existing collections ship *rules* you have to
hope the model follows. Almost none ship enforced hooks **+** loops **+** database safety **+**
frontend design quality together. dev-pack covers the full path a DB-and-website builder
walks — schema → migration → query → API → component → animation → ship — and enforces the parts
that matter at each step. Frontend is a first-class half, not an afterthought: an anti-template
design policy, the Motion/GSAP/Anime stack, and a hook that enforces `prefers-reduced-motion`.

Every item serves at least one goal:

| Icon | Goal |
|------|------|
| 🪙 | Fewer tokens |
| 🎯 | Accuracy |
| ✅ | Truth-telling (no false "it's done") |
| ⚡ | Speed |
| 💎 | Quality / standard |

---

## What's inside

| Folder | Contents | Layer |
|--------|----------|-------|
| `rules/` | Modular `CLAUDE.md` fragments | Advisory |
| `skills/` | DB + web skill packs (`SKILL.md`) | On-demand |
| `hooks/` | Deterministic enforcement scripts + `settings.json` | **Enforced** |
| `loops/` | Multi-step agent orchestrations (slash commands) | Workflow |
| `agents/` | Subagents (code / db / frontend reviewers) | Review |
| `mcp/` | Postgres + browser MCP config | Tooling |
| `templates/` | PRD / ARCHITECTURE / TASKS / CLAUDE.md starters | Docs |
| `tests/` | `test_hooks.py` — runs every hook against sample inputs | Proof |
| `meta/` | `claude-pack-builder` skill — the methodology that built this pack | How it was made |

See [`INVENTORY.md`](INVENTORY.md) for the full table of every item and why it exists.

---

## Install

**Windows (PowerShell):**
```powershell
./install.ps1 -ProjectPath "C:\path\to\your\project"
```

**macOS / Linux:**
```bash
./install.sh /path/to/your/project
```

The installer copies `hooks/` into `<project>/.claude/hooks/`, merges `hooks/settings.json`
into `<project>/.claude/settings.json`, concatenates `rules/` into `<project>/CLAUDE.md`,
and copies skills → `.claude/skills/`, loops → `.claude/commands/` (as slash commands), and
agents → `.claude/agents/`. (`mcp/` and `templates/` are copied to the repo for reference — wire
them in manually per the README in each folder.)

**Requires:** Python 3.8+ on PATH (the hooks are Python, so they run on Windows/macOS/Linux).

**Verify the pack itself:** `python tests/test_hooks.py` (14 cases across all 10 hooks).

**Uninstall** (removes only the files dev-pack installed, strips its CLAUDE.md block, and removes
`settings.json` only if it's unchanged from ours):
```powershell
./uninstall.ps1 -ProjectPath "C:\path\to\your\project"   # Windows
./uninstall.sh /path/to/your/project                      # macOS / Linux
```

---

## Slash commands
After install, type `/` in Claude Code to see them:
- **Workflows** (multi-step): `/plan-build-review-fix`, `/design-first`, `/migration-loop`, `/build-green`,
  `/ship-check`, `/db-tune`.
- **Skills** (one slash command per skill, 26 total): `/schema-designer`, `/migration-safety`,
  `/query-optimizer`, `/rls-policy`, `/supabase-auth`, `/api-design`, `/stripe-payments`, `/component-scaffold`,
  `/animation-implement`, `/theme-tokens`, `/test-author`, `/caching-revalidation`, ... (one for every skill in `skills/`).

Skills also auto-trigger from their description - the slash command is just the explicit way to call one.

## Honest scope (read this)

- This is a **new** repo. It starts at 0 stars like everything does. No inflated claims.
- It **builds on** real, maintained projects — see Credits. It does not replace them.
- The `truth-gate` hook is a **reminder**, not a mind-reader: it can't see the model's
  reasoning, only whether a verify step ran this session. Documented honestly in
  `hooks/truth-gate.py`.
- Hooks **fail open** on internal errors (a bug in a guard won't block your work) — except
  `secret-scan`, which fails closed (a bug there blocks the write, so secrets can't slip
  past a crash). This trade-off is intentional and documented per-hook.

---

## Credits / inspiration

Researched against the existing ecosystem so this fills gaps instead of duplicating:

- **ECC** — layered `common` + per-domain rule library (the structure + web `design-quality` /
  `prefers-reduced-motion` standard this pack's frontend layer is modeled on)
- [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)
- [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)
- [rohitg00/awesome-claude-code-toolkit](https://github.com/rohitg00/awesome-claude-code-toolkit)
- [PatrickJS/awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules) ·
  [sanjeed5/awesome-cursor-rules-mdc](https://github.com/sanjeed5/awesome-cursor-rules-mdc) ·
  [steipete/agent-rules](https://github.com/steipete/agent-rules) · [cursor.directory](https://cursor.directory/)
- [wilwaldon/Claude-Code-Frontend-Design-Toolkit](https://github.com/wilwaldon/Claude-Code-Frontend-Design-Toolkit) (frontend design precedent)
- Claude Code Hooks docs & community guides; database migration skill precedents on mcpmarket.com

## License

MIT — see [LICENSE](LICENSE).
