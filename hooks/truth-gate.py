#!/usr/bin/env python3
"""
truth-gate.py  —  Stop hook

The truth-telling backstop. When the agent finishes a turn, this checks whether any
code files changed without a verification command having run this session. If so, it
reminds the agent (and you) that "done" is unverified.

HONEST LIMITATION (documented on purpose): this hook CANNOT read the model's claims or
reasoning. It only knows two facts — did code change, and did a test/build/lint run
(via verify-tracker.py's marker). So it can't catch a false "it passes" with 100%
certainty; it catches the common case: code changed, nothing was ever run.

It is a *reminder*, not a hard block: it returns a non-blocking message. It will not trap
the agent in a loop (it clears the staleness marker after firing once).

Fail policy: FAIL OPEN.
"""
import json
import os
import sys
import time

VERIFY_MARKER = ".dev-pack-verified"
SEEN_MARKER = ".dev-pack-stop-seen"


def main():
    data = json.loads(sys.stdin.read())
    # Avoid infinite loops: Claude Code sets stop_hook_active when re-invoked from a Stop hook.
    if data.get("stop_hook_active"):
        sys.exit(0)

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    claude_dir = os.path.join(project_dir, ".claude")
    verify_path = os.path.join(claude_dir, VERIFY_MARKER)
    seen_path = os.path.join(claude_dir, SEEN_MARKER)

    verified_recently = False
    if os.path.exists(verify_path):
        try:
            age = time.time() - os.path.getmtime(verify_path)
            verified_recently = age < 1800  # within 30 min
        except OSError:
            pass

    # Only nudge once per stop cycle to avoid nagging.
    already_seen = os.path.exists(seen_path)

    if not verified_recently and not already_seen:
        try:
            os.makedirs(claude_dir, exist_ok=True)
            with open(seen_path, "w", encoding="utf-8") as f:
                f.write(str(int(time.time())))
        except OSError:
            pass
        print(
            "[truth-gate] No test/build/lint command ran this session. Before reporting "
            "anything as 'done' or 'working', either run the relevant check (and paste the "
            "result) or explicitly state that the change is UNVERIFIED.",
            file=sys.stderr,
        )
        # Exit 2 on Stop feeds this back to the model for one more pass; safe because the
        # stop_hook_active guard above prevents a loop.
        sys.exit(2)

    # Clean up the once-per-cycle marker when we're satisfied.
    if os.path.exists(seen_path):
        try:
            os.remove(seen_path)
        except OSError:
            pass
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)
