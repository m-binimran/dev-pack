---
name: perf-budget
description: Enforce a Core Web Vitals / Lighthouse performance budget on a Next.js site — LCP, CLS, INP, bundle size, images. Use before shipping a page or when a page feels slow.
---

# perf-budget

## The budget
- **LCP** < 2.5s · **CLS** < 0.1 · **INP** < 200ms (the three Core Web Vitals).
- JS shipped to the client kept lean; flag large client bundles.

## Checks & fixes
- **Images:** use `next/image` (lazy, sized, modern formats). Set `width`/`height` to reserve space → fixes CLS.
- **Fonts:** `next/font` (self-hosted, `display: swap`) — no layout shift, no render-block.
- **Client JS:** prefer Server Components; `"use client"` only where needed. `dynamic()` import heavy/below-fold
  components. Watch big date/icon/chart libs.
- **LCP element:** make the hero image/text fast — `priority` on the LCP image, no blocking work above it.
- **Caching:** static where possible; sensible `revalidate`.

## Measure, don't guess
- Run Lighthouse / `next build` and read the real numbers. Report measured values against the budget.
- If you can't measure in this environment, say the budget is "designed for" not "verified."

## Output
- Each metric: target vs. measured (or "unmeasured"), and the fix for any miss.

## Guardrails
- Don't claim a CWV pass without a real measurement.
- Don't ship a render-blocking third-party script without justifying it.
