## Frontend animation

Animation is what separates a custom site from a template — but it's also an accessibility and legal line.

### Pick the right tool
| Need | Tool |
|------|------|
| React enter/exit, layout, stagger | Motion (Framer Motion) |
| Cinematic scroll timelines / pinning | GSAP + ScrollTrigger |
| SVG path / morph | Anime.js |
| Physics / gesture | React Spring |
| Zero-JS micro-interactions | tailwindcss-motion |
| Animated marketing components | Magic UI |

Pick ONE primary engine (Motion for UI, GSAP for cinematic scroll); use the other sparingly. Don't ship both heavily.

### MANDATORY: prefers-reduced-motion
- **Every animation must respect `prefers-reduced-motion: reduce`.** Non-negotiable — vestibular/seizure safety.
  The `reduced-motion-guard` hook flags animated files that don't.
- Content must be fully readable with motion off (final opacity/position/scale reached immediately).
- No looping/flashing/rapid motion regardless of preference.

### Performance
- Animate `transform` and `opacity` only (no layout thrash). Target 60fps; verify in DevTools Performance.
- `will-change` sparingly. Kill GSAP timelines on unmount.
