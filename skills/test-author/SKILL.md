---
name: test-author
description: Write tests first (RED→GREEN→REFACTOR) with Vitest, Testing Library, and Playwright for a Next.js + Supabase app. Use when adding a feature, fixing a bug, or raising coverage.
---

# test-author

Tests that prove behavior and catch regressions — written before or alongside the code, then actually run.

## Process
1. **Start RED.** Write a failing test that states the expected behavior. Run it; confirm it fails for the
   right reason.
2. **GREEN.** Write the minimum code to pass. Run it.
3. **REFACTOR.** Clean up with the test as a safety net. Re-run.

## What to write where
- **Unit (Vitest):** pure functions, Zod schemas, utils. Cover edge cases + error paths, not just happy path.
- **Component (Vitest + Testing Library):** query by role/label (also exercises a11y), simulate user events,
  assert visible outcomes — not internal state.
- **E2E (Playwright):** the critical flows only (auth, core task, checkout). Keep these few and stable.

## Patterns
- **Bug fix → regression test** that fails before the fix, passes after. Reference the bug.
- **Deterministic data:** fixed seeds/fixtures (`seed-fixtures`); no real network/clock in unit tests — mock them.
- **Arrange-Act-Assert**, one behavior per test, names that read as sentences.

## Output
- The test file(s), and the **real run output** (pass/fail counts). A test you didn't run is unverified — say so.

## Guardrails
- Don't test implementation details that change on every refactor.
- Don't lower coverage thresholds or skip tests to go green — fix the code or the test.
