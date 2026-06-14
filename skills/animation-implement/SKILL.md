---
name: animation-implement
description: Implement web animations with the right engine (Motion, GSAP, Anime.js, React Spring, tailwindcss-motion) and a mandatory prefers-reduced-motion fallback at 60fps. Use when adding any motion to a site.
---

# animation-implement

Pick one primary engine, animate cheap properties, and never ship motion without a reduced-motion path.

## Choose the engine
| Need | Tool |
|------|------|
| React enter/exit, layout, stagger | Motion (`motion/react`) |
| Scroll timelines, pinning, parallax | GSAP + ScrollTrigger (`useGSAP`) |
| SVG path draw / morph | Anime.js (`strokeDashoffset`) |
| Physics / drag | React Spring |
| Zero-JS micro-interaction | tailwindcss-motion classes |
| Prebuilt animated marketing bits | Magic UI |

Primary = Motion (UI) or GSAP (cinematic scroll). Use the other sparingly. Don't ship both heavily.

## MANDATORY reduced-motion (the `reduced-motion-guard` hook checks this)
- Motion: `useReducedMotion()` → zero distance/duration when reduced.
- GSAP: `if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;` before building the timeline.
- CSS: ship the global `@media (prefers-reduced-motion: reduce)` reset.
- Content must be fully visible/readable with motion off.

## Performance
- Animate only `transform` + `opacity`. No animating width/top/left (layout thrash).
- 60fps — verify in DevTools Performance. Kill GSAP timelines on unmount (`return () => tl.kill()`).

## Output
- The animation code, the engine chosen + why, and the reduced-motion fallback shown explicitly.

## Guardrails
- No looping/flashing/rapid motion (seizure risk) regardless of preference.
- Don't mix two heavy engines on the same surface.
