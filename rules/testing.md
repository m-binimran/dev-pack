## Testing

- **Write the test first** where practical: RED (failing test) → GREEN (make it pass) → REFACTOR.
- **Coverage floor 80%** on the code you touch. Don't chase 100%; do cover branches and edge cases.
- **Test the behavior, not the implementation.** A test that breaks on every refactor is testing the wrong thing.
- **Layers:**
  | Layer | Tool | For |
  |-------|------|-----|
  | Unit | Vitest | pure logic, utils, schemas |
  | Component | Vitest + Testing Library | rendering, interaction, a11y roles |
  | E2E | Playwright | critical user flows (signup, checkout, core path) |
- **Every bug fix gets a regression test** that fails before the fix and passes after.
- **No flaky tests.** Deterministic data (see `seed-fixtures`); no real network/time in unit tests.
- **"Tests pass" requires actually running them** and pasting the result (truth-telling). A written test that
  hasn't been run is unverified.
