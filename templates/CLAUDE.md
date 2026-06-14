# CLAUDE.md — <Project Name>

> Project rules Claude reads every session. Keep it short — long files cost tokens every turn.
> The dev-pack installer appends its rule fragments below the marker.

## Project
- What this is: <one line>
- Stack: Next.js + Supabase (Postgres). See ARCHITECTURE.md (locked).
- Docs: PRD.md (what) · ARCHITECTURE.md (how) · TASKS.md (live status).

## How to work here
- Read TASKS.md first; work the "Now" item.
- Verify before claiming done (run build/test, paste result).
- Update TASKS.md after each task.

## Commands
- Dev: `npm run dev`
- Build: `npm run build`
- Test: `npm test`
- DB reset+seed (local only): `supabase db reset`

<!-- ===== dev-pack rules (auto-installed) ===== -->
<!-- installer appends rules/*.md here -->
