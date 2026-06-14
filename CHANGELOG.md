# Changelog

All notable changes to this project are documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/). This project uses [SemVer](https://semver.org/).

## [Unreleased]

### Added
- **Per-skill slash commands** (`commands/` -> `.claude/commands/`): every skill is now directly callable as
  `/<skill-name>` (e.g. `/schema-designer`, `/api-design`), alongside the workflow loops. Installer +
  uninstaller updated to copy/remove them.
- **`meta/claude-pack-builder`** — the reusable skill (methodology + references) that built this pack:
  research → design → build → verify → safe-publish. Lives under `meta/` so the installer doesn't copy it
  into end-user projects.
- **8 platform skills** (skills now 26 total): `supabase-auth`, `api-design`, `storage-upload`,
  `stripe-payments`, `error-states`, `caching-revalidation`, `realtime-subscriptions`, `observability`.
  These close the API and auth steps the README's path claims, plus common client-site needs
  (uploads, payments, error UI, caching, live data, monitoring).

## [0.1.0] - 2026-06-14
Initial pack.

### Added
- **Rules (13):** core-terse, truth-telling, token-budget, code-quality, database, web,
  frontend-design, frontend-architecture, frontend-animation, testing, deployment, stack-lock, git.
- **Skills (18):** schema-designer, migration-safety, query-optimizer, rls-policy, seed-fixtures,
  db-backup-restore, design-direction, component-scaffold, animation-implement, responsive-layout,
  form-builder, state-architect, theme-tokens, seo-onpage, a11y-audit, perf-budget, test-author,
  truthful-reporter.
- **Hooks (10):** secret-scan (fail-closed), file-size-guard, sql-safety-guard, danger-guard,
  format-lint, migration-validate, reduced-motion-guard, verify-tracker, truth-gate, token-guard.
- **Loops (6):** /plan-build-review-fix, /design-first, /migration-loop, /build-green, /ship-check, /db-tune.
- **Agents (3):** code-reviewer, db-reviewer, frontend-reviewer.
- MCP config (postgres + playwright), templates (PRD/ARCHITECTURE/TASKS/CLAUDE.md), install +
  uninstall scripts (PowerShell + bash), committed test harness (`tests/test_hooks.py`, 14 cases),
  CI workflow, issue/PR templates, SECURITY.md, .env.example.

### Notes
- Targets the Next.js + Supabase (Postgres) stack with a first-class frontend layer
  (shadcn/ui, Magic UI, Motion/GSAP/Anime, Tailwind v4).
- All 10 hooks verified by the committed test harness.
