## Deployment (Vercel + Supabase)

- **Secrets live in the host, not the repo.** Set env vars in the Vercel dashboard (and Supabase). Only
  `NEXT_PUBLIC_*` is exposed to the browser — never put a secret behind that prefix.
- **Migrations before deploy.** Apply DB migrations to the target environment *before* shipping code that
  depends on them. Use the expand→contract pattern so old and new code both work during the rollout.
- **Preview first.** Every PR gets a Vercel preview deploy; verify it there before promoting to production.
- **Run `/ship-check` before promoting** — lint, tests, build, a11y, design, motion, SEO, perf, launch checklist.
- **Production DB changes are human-confirmed.** Never let the agent apply a destructive migration to prod
  (the `sql-safety-guard` hook blocks it; keep it that way).
- **Have a rollback path.** Know how to revert the deploy (Vercel instant rollback) and the migration (`down`).
- **Verify after deploy:** load the production URL, check the critical flow + CTA actually work. "Deployed"
  ≠ "working" until observed.
