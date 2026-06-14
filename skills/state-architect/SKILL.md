---
name: state-architect
description: Decide where each piece of state lives — server, client, URL, or form — and avoid duplicating server state into client stores. Use when wiring data flow, adding a store, or when state feels tangled.
---

# state-architect

Most React state bugs come from putting state in the wrong place. Classify first.

## Classify every piece of state
| It is... | Put it in | Tool |
|----------|-----------|------|
| Fetched from the server | Server-state cache | TanStack Query / SWR / tRPC |
| UI-only (open/closed, theme, step) | Client state | Zustand / Jotai / `useState` |
| Shareable / bookmarkable (filters, sort, page, tab, search) | The URL | search params / route segments |
| Inputs being edited | Form state | React Hook Form |

## Rules
- **Don't copy server data into a client store.** Read it from the query cache; derive what you need.
- **Don't store computed values** you can derive from existing state.
- **URL-first for anything shareable** — a filtered/sorted view should survive a refresh and a copied link.
- Lift state only as high as the lowest common ancestor that needs it.

## Output
- A short table: each piece of state → where it lives → why.
- Flag any current duplication (same data in two places) and how to collapse it.

## Guardrails
- Adding a global store to hold server data is a smell — use the server-state library's cache instead.
- Prop-drilling more than ~2 levels → context or compound component, not more props.
