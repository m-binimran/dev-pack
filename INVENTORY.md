# Inventory — every item, what it does, why it exists

Goals: 🪙 fewer tokens · 🎯 accuracy · ✅ truth-telling · ⚡ speed · 💎 quality

## Rules (`rules/` → appended to CLAUDE.md)
| File | What it does | Goals |
|------|--------------|-------|
| `core-terse.md` | Forces short, code-first answers; no filler | 🪙⚡ |
| `truth-telling.md` | No "done/passing" without proof; no invented numbers | ✅ |
| `token-budget.md` | Grep before read, line-ranges, no re-reads, `/clear` between tasks | 🪙⚡ |
| `code-quality.md` | Functions <50, files <800, immutability, explicit errors, validate boundaries, no console.log | 💎🎯 |
| `database.md` | Parameterized queries, reversible migrations, no prod by default, EXPLAIN heavy queries, RLS on | 🎯💎 |
| `web.md` | WCAG AA, 375px responsive, SEO basics, CWV budget, no client secrets | 💎 |
| `frontend-design.md` | Anti-template policy: banned defaults, ≥4 required qualities, named style directions | 💎 |
| `frontend-architecture.md` | Server Components default, compound/container split, state placement, data-fetch patterns, <800 lines | 💎🎯 |
| `frontend-animation.md` | Engine selection + MANDATORY prefers-reduced-motion + 60fps transform/opacity only | 💎 |
| `testing.md` | RED→GREEN→REFACTOR, 80% floor, Vitest/Playwright layers, regression test per bug | 💎✅ |
| `deployment.md` | Vercel+Supabase: host-side secrets, migrate before deploy, preview first, verify after | 💎✅ |
| `stack-lock.md` | Don't swap framework/ORM/DB mid-build; no needless deps | 💎 |
| `git.md` | Commit format, branch-first, no force-push/--no-verify | 💎 |

## Skills (`skills/` → `.claude/skills/`)

**Database & backend**
| Skill | What it does | Goals |
|-------|--------------|-------|
| `schema-designer` | Normalized schema: types, keys, indexes, naming | 💎🎯 |
| `migration-safety` | Reversible up/down; expand→backfill→contract; avoid locks | 🎯💎 |
| `query-optimizer` | EXPLAIN ANALYZE, index suggestions, N+1, before/after proof | ⚡🎯 |
| `rls-policy` | Supabase row-level security + owner/team patterns + tests | 💎🎯 |
| `seed-fixtures` | Deterministic seed/reset data, prod-guarded | ⚡ |
| `db-backup-restore` | pg_dump/restore + Supabase PITR; restore-into-new runbook; never over prod | 🎯💎 |

**Frontend (Next.js + shadcn + Motion/GSAP)**
| Skill | What it does | Goals |
|-------|--------------|-------|
| `design-direction` | Pick a non-template style/palette/type/motion BEFORE coding | 💎 |
| `component-scaffold` | shadcn/Radix component: cva variants, compound pattern, designed states, a11y | 💎🎯 |
| `animation-implement` | Right engine (Motion/GSAP/Anime/Spring/tw-motion) + reduced-motion + 60fps | 💎 |
| `responsive-layout` | Mobile-first ≥375px, fluid `clamp()`, container queries, bento composition | 💎 |
| `form-builder` | React Hook Form + Zod + shadcn Form + server action, validated both sides | 💎🎯 |
| `state-architect` | Place state correctly (server/client/url/form); no duplicated server state | 🎯💎 |
| `theme-tokens` | Tailwind v4 `@theme` tokens, semantic aliases, intentional light+dark | 💎 |

**API, auth & platform**
| Skill | What it does | Goals |
|-------|--------------|-------|
| `supabase-auth` | Supabase Auth in Next.js: server sessions, middleware refresh, protected routes | 💎🎯 |
| `api-design` | Route handlers / server actions: Zod validation, status codes, errors, rate limiting | 🎯💎 |
| `storage-upload` | Supabase Storage: private buckets, object RLS, signed URLs, size/type limits | 💎🎯 |
| `stripe-payments` | Checkout/PaymentIntents + signature-verified, idempotent webhooks as source of truth | 🎯💎 |
| `error-states` | Next.js loading/empty/error/not-found + action feedback for every data surface | 💎 |
| `caching-revalidation` | Static/ISR/dynamic choice + revalidatePath/Tag on writes | ⚡🎯 |
| `realtime-subscriptions` | Supabase Realtime (changes/broadcast/presence) with cleanup + RLS awareness | 💎 |
| `observability` | Sentry + structured logging with PII scrubbing; what to watch post-deploy | ✅💎 |

**SEO / a11y / perf / truth**
| Skill | What it does | Goals |
|-------|--------------|-------|
| `seo-onpage` | Title/meta/OG/canonical, sitemap, JSON-LD | 💎 |
| `a11y-audit` | WCAG 2.2 AA checklist, must-fix vs should-fix | 💎 |
| `perf-budget` | Core Web Vitals budget, measured not guessed | ⚡💎 |
| `test-author` | RED→GREEN→REFACTOR with Vitest/RTL/Playwright; regression test per bug | 💎✅ |
| `truthful-reporter` | Map each claim → required proof before reporting | ✅ |

## Hooks (`hooks/` → `.claude/hooks/`, wired by `settings.json`)
| Hook (event) | What it does | Fail mode | Goals |
|--------------|--------------|-----------|-------|
| `secret-scan` (PreToolUse Write/Edit) | Blocks hardcoded secrets hitting disk | closed | 💎✅ |
| `file-size-guard` (PreToolUse Write) | Blocks writing a file > 800 lines (split it) | open | 💎 |
| `sql-safety-guard` (PreToolUse Bash) | Blocks DROP/TRUNCATE/WHERE-less DELETE, prod targets | open | 🎯💎 |
| `danger-guard` (PreToolUse Bash) | Blocks rm -rf, force-push, --no-verify, curl\|sh, chmod 777 | open | 💎 |
| `format-lint` (PostToolUse Write/Edit) | Auto-formats + eslint-fixes touched files (prettier/eslint/sqlfluff/ruff) | open | ⚡💎 |
| `reduced-motion-guard` (PostToolUse Write/Edit) | Flags animated files with no prefers-reduced-motion fallback | open | 💎 |
| `migration-validate` (PostToolUse Write/Edit) | Flags non-reversible / locking migrations | open | 🎯 |
| `verify-tracker` (PostToolUse Bash) | Records that a test/build/lint ran this session | open | ✅ |
| `truth-gate` (Stop) | Reminds if code changed but nothing was verified | open | ✅ |
| `token-guard` (UserPromptSubmit) | Nudges on vague prompts that trigger broad scans | open | 🪙 |

## Loops (`loops/` → `.claude/commands/`, run as slash commands)
| Command | What it does | Goals |
|---------|--------------|-------|
| `/design-first` | Direction → tokens → layout → components → motion → a11y/design review (anti-template) | 💎 |
| `/plan-build-review-fix` | Plan → build → verify → review → fix, capped at 3 rounds | 💎🎯 |
| `/migration-loop` | Design → up/down → shadow-DB dry-run → verify rollback | 🎯💎 |
| `/build-green` | Run build/tests → fix first error → repeat ≤5, honest stop | ⚡✅ |
| `/ship-check` | Lint/test/a11y/SEO/perf + launch checklist gate | 💎 |
| `/db-tune` | EXPLAIN → diagnose → smallest fix → re-measure | ⚡🎯 |

## Agents (`agents/` → `.claude/agents/`, spawned as subagents)
| Agent | What it does | Goals |
|-------|--------------|-------|
| `code-reviewer` | General diff review: correctness, security, error handling, maintainability | 💎🎯 |
| `db-reviewer` | Schema/migration/query/RLS review: locks, data-loss, perf, security | 🎯💎 |
| `frontend-reviewer` | UI review: a11y, reduced-motion, anti-template design, architecture | 💎 |

## Supporting
| Item | What it does | Goals |
|------|--------------|-------|
| `mcp/.mcp.json` | Postgres (local) + Playwright servers so the agent observes reality | ✅🎯 |
| `templates/` | PRD / ARCHITECTURE / TASKS / CLAUDE.md starters | 💎 |
| `tests/test_hooks.py` | Runs every hook against sample inputs (14 cases) — proves the guards work | ✅ |
| `.github/` | CI (tests hooks on 3 Python versions) + issue/PR templates | ✅💎 |
| `.env.example` | Next.js + Supabase env template (secrets host-side) | 💎 |
| `install.ps1` / `install.sh` | One-command setup into any project | ⚡ |
