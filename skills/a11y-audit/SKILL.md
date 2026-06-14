---
name: a11y-audit
description: Audit a web page/component against WCAG 2.2 AA — semantics, keyboard, contrast, labels, focus, alt text. Use when reviewing UI for accessibility or before shipping a page.
---

# a11y-audit

Check against WCAG 2.2 AA. Report findings as must-fix vs. should-fix.

## Checklist
- **Semantics:** real elements — `<button>` not a clickable `<div>`; `<nav>/<main>/<header>` landmarks; lists are lists.
- **Keyboard:** every interactive element reachable and operable by Tab/Enter/Space; logical order; no traps.
- **Focus:** visible focus indicator (don't `outline: none` without a replacement).
- **Labels:** every input has a `<label>`/`aria-label`; icon-only buttons have accessible names.
- **Images:** meaningful `alt`; decorative images `alt=""`.
- **Contrast:** text ≥ 4.5:1 (≥ 3:1 for large text). State the measured ratio, don't eyeball it.
- **Forms:** errors announced (`aria-live`), associated with their field, not color-only.
- **Motion:** respect `prefers-reduced-motion`.

## Output
- Findings grouped must-fix / should-fix, each with the exact element and the fix.
- Don't claim "accessible" from reading code alone — say what was checked statically vs. needs a real
  screen-reader/keyboard pass.

## Guardrails
- ARIA is a last resort — prefer native HTML semantics.
- Don't add `role`/`aria-*` that contradicts the element.
