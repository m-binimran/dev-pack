## Frontend design quality (anti-template)

Do not ship generic, template-looking UI. Output should look intentional and specific to the product.

### Banned by default
- Centered headline + gradient blob + generic CTA hero.
- Uniform card grids with no hierarchy; same radius/shadow/spacing on everything.
- Unmodified shadcn/Tailwind defaults passed off as finished design.
- Safe gray-on-white with one accent color; default font stacks with no reason.
- Dark mode chosen by default instead of by intent.

### Every meaningful surface shows ≥4 of:
1. Hierarchy through scale contrast  2. Intentional spacing rhythm (not uniform padding)
3. Depth/layering (overlap, surfaces, shadow, motion)  4. Typography with a real pairing
5. Semantic (not decorative) color  6. Designed hover/focus/active states
7. Grid-breaking editorial/bento composition where it fits  8. Texture/atmosphere when it fits
9. Motion that clarifies flow  10. Data viz treated as part of the system

### Before writing UI
Pick a specific direction (editorial, neo-brutalist, glass-with-depth, luxury, bento, scrollytelling,
Swiss, retro-futurist — not "clean minimal"). Define palette + type deliberately. Use the
`design-direction` skill. Component checklist: would this look believable in a real product screenshot?
