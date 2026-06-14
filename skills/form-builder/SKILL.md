---
name: form-builder
description: Build accessible, validated forms with React Hook Form + Zod + shadcn Form, wired to a Next.js server action. Use when adding any form (contact, signup, checkout, settings).
---

# form-builder

One source of truth for validation (Zod), shared by client and server. Accessible by construction.

## Process
1. **Define the Zod schema once.** It validates on the client AND in the server action — no drift.
2. **React Hook Form + shadcn `Form`:** `useForm({ resolver: zodResolver(schema) })`. Use `FormField`,
   `FormLabel`, `FormControl`, `FormMessage` so each input is labelled and errors are associated + announced.
3. **Server action does the real validation:** re-parse with the same schema in the action; never trust the client.
4. **States:** disabled while submitting, visible loading, success + error feedback (`aria-live` for errors).
5. **Honeypot / basic spam guard** on public forms; rate-limit the action.

## Accessibility
- Every field has a real `<label>`. Errors are text (not color-only) and linked via `aria-describedby`.
- Submit reachable by keyboard; focus moves to the first error on failed submit.

## Output
- The schema, the form component, and the server action — with the shared schema referenced in both.
- Note what validation runs client-side vs. server-side.

## Guardrails
- No validation that exists only on the client.
- Don't put secrets/keys in the form component (client code — the `secret-scan` hook will block it).
