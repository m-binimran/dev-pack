---
name: theme-tokens
description: Define a design system as Tailwind v4 @theme tokens (color, type scale, spacing, radius, shadow) with intentional light + dark themes. Use when setting up a project's visual system or making theming consistent.
---

# theme-tokens

A real token system makes every component consistent and re-skinnable per client. Tailwind v4 is CSS-first.

## Process
1. **Define tokens in CSS** with Tailwind v4 `@theme`:
   ```css
   @theme {
     --color-brand: oklch(0.62 0.19 256);
     --color-surface: oklch(0.98 0 0);
     --font-display: "…", serif;
     --font-body: "…", sans-serif;
     --radius: 0.75rem;
   }
   ```
2. **Scale, don't hardcode:** a type scale (e.g. fluid `clamp()` steps), a spacing rhythm, 2–3 radii, a small
   shadow set. Components reference tokens, never raw hex/px.
3. **Themes are intentional:** if you support dark, design it — don't auto-invert. Define dark token overrides
   under a `.dark` / `[data-theme=dark]` scope. Don't default to dark mode unless the product wants it.
4. **Semantic aliases:** map raw scales to roles (`--color-success`, `--color-danger`, `--color-muted`) so
   components read by meaning.

## Output
- The `@theme` token block, the semantic aliases, and the dark overrides (if any).
- A note: which tokens are brand-specific (swap per client) vs. structural.

## Guardrails
- No raw hex/px in components once tokens exist — reference the token.
- Light and dark must each feel intentional (anti-template policy), not one auto-generated from the other.
