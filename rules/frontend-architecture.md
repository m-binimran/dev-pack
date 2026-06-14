## Frontend architecture (Next.js + React)

### Components
- Server Components by default; add `"use client"` only where interactivity needs it.
- Compound components (parent owns state, children consume via context) for complex widgets — not prop drilling.
- Container (data + effects) vs. presentational (pure, props-in) split. Keep presentational pure.
- Keep keyboard handling, ARIA, and focus logic in a headless layer when behavior is shared.
- Files < 800 lines (the `file-size-guard` hook enforces). Split into modules before that.

### State — keep these concerns separate
| Concern | Tool |
|---------|------|
| Server state | TanStack Query / SWR / tRPC |
| Client state | Zustand / Jotai |
| URL state (filters, sort, page, tab, query) | search params / route segments |
| Form state | React Hook Form (+ Zod) |

- Don't duplicate server state into a client store. Derive computed values; don't store them.
- Persist shareable state (filters, sort, pagination, active tab) in the URL.

### Data fetching
- Stale-while-revalidate via the library, not by hand.
- Optimistic updates: snapshot → apply → roll back on failure with visible error feedback.
- Fetch independent data in parallel; avoid parent→child request waterfalls.
