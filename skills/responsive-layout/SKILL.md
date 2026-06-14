---
name: responsive-layout
description: Build mobile-first responsive layouts (≥375px) with fluid type, container queries, and grid/bento composition that doesn't break. Use when laying out a page or fixing responsive issues.
---

# responsive-layout

Mobile-first, fluid, and composed — not a desktop layout crammed onto a phone.

## Process
1. **Design at 375px first**, then scale up. Every layout must work at 375px width.
2. **Fluid type & spacing:** `clamp()` for headings and section padding so it scales smoothly between
   breakpoints instead of jumping.
3. **Use the right query:** media queries for page layout; **container queries** for components that appear
   in multiple widths (cards, sidebars).
4. **Composition with intent:** CSS grid for structure; break the grid (bento/editorial/overlap) where the
   design direction calls for it — don't default to uniform columns.
5. **Touch targets ≥44px**, no hover-only interactions on touch, test the mobile nav (Sheet/Drawer).

## Checklist
- [ ] No horizontal scroll at 375px.
- [ ] Text never below ~14px on mobile; line length readable on desktop (~60–75ch).
- [ ] Images sized/`next/image` to avoid CLS.
- [ ] Tap targets large enough; nav works on touch.

## Output
- The responsive layout, breakpoints used, and confirmation it was checked at 375px (or flagged unverified).

## Guardrails
- Don't claim "responsive" from code alone — view it at 375px (Playwright/preview) or say it's unverified.
- Avoid fixed heights that clip content when text wraps on small screens.
