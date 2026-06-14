---
name: error-states
description: Design the non-happy-path UI in Next.js — loading, error, not-found, and empty states with Suspense, error boundaries, and user-facing feedback. Use when a page fetches data, can fail, or can be empty.
---

# error-states

Most apps ship the happy path and forget the other three. A surface isn't done until loading, empty, and
error are all handled.

## The four states for every data surface
1. **Loading** — `loading.tsx` or `<Suspense fallback>`. Use skeletons that match the final layout (no CLS),
   not a bare spinner where possible.
2. **Empty** — designed empty state with a next action ("No projects yet — create one"), not a blank box.
3. **Error** — `error.tsx` (client error boundary) with a human message + a retry (`reset()`); log the real
   error server-side. Never show a raw stack trace to users.
4. **Not found** — `not-found.tsx` + `notFound()` for missing resources (real 404, not a 200 with "nothing here").

## Feedback for actions
- Mutations show pending state (disabled + spinner) and a success/error toast (`aria-live` for errors).
- Optimistic updates roll back visibly on failure (see `state-architect`).

## Output
- The loading/empty/error/not-found treatments for the surface, and the action feedback.
- State which of the four are implemented and which are N/A.

## Guardrails
- No surface ships with only the happy path.
- Error UI must not leak internal details; log them server-side instead.
- Skeletons must reserve the real layout's space to avoid layout shift.
