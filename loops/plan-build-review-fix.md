---
description: Plan → build → review → fix loop. Implements a feature, runs a code review, fixes findings, repeats until clean.
---

# /plan-build-review-fix $ARGUMENTS

Run this loop for the task in `$ARGUMENTS`. Do not skip steps.

1. **Plan.** Restate the goal in one line. List the files you'll touch and the approach. If anything is
   ambiguous, ask ONE question, then proceed. Keep the plan short.
2. **Build.** Implement the change. Small, focused edits. Follow the project CLAUDE.md rules.
3. **Verify.** Run the relevant build/test/typecheck. Paste the real result. (The `verify-tracker` hook
   notices this; the `truth-gate` hook will flag you at the end if you skipped it.)
4. **Review.** Spawn the reviewer subagent that fits the change: `code-reviewer` (general),
   `db-reviewer` (schema/migration/query/RLS), or `frontend-reviewer` (UI/a11y/motion/design). Collect findings.
5. **Fix.** Address every must-fix finding. Re-run the checks from step 3.
6. **Repeat** steps 4–5 until the review is clean or only has accepted nits. Cap at **3 rounds**; if still
   not clean, stop and report what's left honestly.
7. **Report.** One-line status with evidence: what changed, what passed, what's still open.

Stop conditions: review clean, or 3 rounds reached, or a blocker you can't resolve (report it).
