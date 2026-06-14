---
description: Build a UI surface the anti-template way — direction → tokens → components → motion → a11y/design review.
---

# /design-first $ARGUMENTS

Build the page/section in `$ARGUMENTS` so it looks intentional, not templated. Don't skip step 1.

1. **Direction (use `design-direction`).** Pick a named style, palette, type pairing, references, motion
   intent. Output the direction brief. Don't write UI before this exists.
2. **Tokens (use `theme-tokens`).** Encode palette/type/spacing/radius as Tailwind v4 `@theme` tokens +
   semantic aliases. Components reference tokens, not raw values.
3. **Layout (use `responsive-layout`).** Compose mobile-first at 375px; break the grid (bento/editorial)
   where the direction wants it.
4. **Components (use `component-scaffold`).** shadcn/Radix primitives, `cva` variants wired to tokens,
   designed hover/focus/active states. Each file < 800 lines.
5. **Motion (use `animation-implement`).** One primary engine; animate transform/opacity; **add the
   prefers-reduced-motion fallback** (the `reduced-motion-guard` hook will flag you if you forget).
6. **Review against the anti-template checklist.** Does every surface show ≥4 required qualities? Would it
   look believable in a real product screenshot? If no, iterate.
7. **Verify.** Build it, view it at 375px and desktop (Playwright/preview) or say it's unverified. Run
   `a11y-audit`. Report with evidence.

Stop when: the surface passes the anti-template checklist + a11y, motion has a reduced-motion path, and the
build is verified — or report honestly what's still open.
