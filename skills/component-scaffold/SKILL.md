---
name: component-scaffold
description: Build a production React component on shadcn/ui + Tailwind — variants, compound pattern, accessible states, and a clean prop API. Use when creating a new UI component or refactoring a messy one.
---

# component-scaffold

Build components that own their code (shadcn model), are accessible, and don't look like defaults.

## Process
1. **Classify:** presentational (pure, props-in) or container (data/effects)? Keep them separate.
2. **Start from primitives:** shadcn/ui (Radix under the hood) for anything interactive — you get a11y for free.
   Customize in your own `components/ui/*` file; it's yours.
3. **Variants via `cva`:** define `variant`/`size` with a `brand` variant wired to your theme tokens — don't
   ship the raw default look.
4. **Compound pattern** for widgets with shared state (`<Tabs><Tabs.List>…`): parent owns state, children
   consume via context. No prop drilling.
5. **Design the states:** hover, focus-visible, active, disabled, loading, empty, error — all intentional.
6. **Accessibility:** real semantics, labelled controls, visible focus, keyboard operable. Icon-only buttons
   get an accessible name.

## Output
- The component file(s), typed props, variants, and the states handled.
- A one-line note on which states were implemented and which are N/A.

## Guardrails
- Don't reinvent an accessible primitive Radix/shadcn already provides.
- Don't exceed 800 lines (the `file-size-guard` hook blocks it) — split sub-components out.
- No unmodified default styling passed off as finished (anti-template policy).
