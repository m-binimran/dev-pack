## Code quality

- **Functions < 50 lines. Files < 800 lines** (the `file-size-guard` hook blocks oversized writes). Split early.
- **KISS / DRY / YAGNI.** Simplest thing that works. No premature abstraction; no speculative generality.
- **Immutability by default.** Return new objects; don't mutate inputs/shared state (unless the language idiom
  is pointer mutation, e.g. Go — not relevant here).
- **Handle errors explicitly at every level. Never swallow silently.** No empty `catch {}`, no bare
  `except: pass`, no ignored promise rejections. Surface or propagate with context.
- **Validate input at system boundaries** — server actions, route handlers, public functions. Don't trust the client.
- **No `console.log` / `debugger` / dead code** committed. Remove scaffolding before done.
- **No hardcoded secrets** — env vars only (the `secret-scan` hook enforces).
- Name things for what they are. Comments explain *why*, not *what*. Match the surrounding code's style.
