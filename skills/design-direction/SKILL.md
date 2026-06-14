---
name: design-direction
description: Choose an intentional, non-template visual direction (style, palette, type, motion) BEFORE writing any UI. Use at the start of a new site/page or when output looks generic. Enforces the anti-template policy.
---

# design-direction

The fastest way to ship template-looking UI is to start coding without a direction. Don't.

## Do this first
1. **Pick a named direction** — editorial/magazine, neo-brutalism, glass-with-real-depth, dark or light
   luxury, bento, scrollytelling, Swiss/International, retro-futurism. NOT "clean minimal." NOT auto dark mode.
2. **Palette intentionally:** a base, 1–2 surfaces, a semantic accent (success/warn/danger), and ONE
   brand-defining color used with purpose. Define as Tailwind v4 `@theme` tokens (hand to `theme-tokens`).
3. **Type pairing:** a display/heading face with character + a readable body face. State the pairing and why.
4. **Reference set:** name 2–3 real sites/products this should feel like.
5. **Motion intent:** how motion clarifies this product (subtle micro vs. cinematic scroll). Hand to
   `animation-implement`.

## Output
- A short "direction brief": style name, palette tokens, type pairing, references, motion intent.
- This brief is the contract the rest of the build is judged against.

## Guardrails (anti-template)
- Every surface must show ≥4 of: scale hierarchy, spacing rhythm, depth/layering, real type, semantic color,
  designed interaction states, grid-breaking composition, texture, purposeful motion, designed data viz.
- Final gut check: "would this look believable in a real product screenshot?" If no, iterate before building more.
