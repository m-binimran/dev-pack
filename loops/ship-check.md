---
description: Pre-deploy gate. Runs lint, tests, a11y, SEO, perf budget, and the launch checklist before shipping.
---

# /ship-check $ARGUMENTS

Pre-deploy gate. Run each stage; a FAIL stops the ship until fixed. Report a clear pass/fail table.

1. **Lint + types** — eslint + `tsc --noEmit`. Must pass.
2. **Tests** — run the suite. Must pass (paste counts).
3. **Build** — `next build` exits 0.
4. **Accessibility** — run the `a11y-audit` skill on key pages. No must-fix issues.
5. **Design quality** — anti-template check: every key surface shows ≥4 required qualities; nothing looks
   like a raw shadcn/Tailwind default. (See `frontend-design` rule / `design-direction` skill.)
6. **Motion** — every animation has a prefers-reduced-motion fallback; runs at 60fps. No looping/flashing.
7. **SEO** — `seo-onpage` skill: title/meta/OG/canonical present; sitemap + robots exist.
8. **Performance** — `perf-budget` skill: CWV within budget (or measured + flagged).
9. **Launch checklist:**
   - [ ] Privacy policy live + linked
   - [ ] HTTPS / SSL active
   - [ ] OG tags (title, description, image, url) render in a real preview
   - [ ] Mobile responsive at 375px
   - [ ] Primary CTA tested and working
10. **Verdict.** A table: stage → PASS/FAIL/UNVERIFIED. If anything is UNVERIFIED (couldn't run here), say so —
    don't mark it PASS. Ship only when every stage is PASS.

Never report "ready to ship" with an unverified stage silently passed.
