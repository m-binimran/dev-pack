#!/usr/bin/env python3
"""
verify-tracker.py  —  PostToolUse hook (Bash)

Records, per session, whether a *verification* command (test / build / typecheck / lint)
actually ran. Writes a small marker file that truth-gate.py reads at Stop time.

This is the data half of the truth-telling gate. It does not block anything.

Fail policy: FAIL OPEN.
"""
import json
import os
import re
import sys
import time

VERIFY = re.compile(
    r"(?i)\b("
    r"npm\s+(run\s+)?(test|build|lint|typecheck)|"
    r"pnpm\s+(test|build|lint)|yarn\s+(test|build|lint)|"
    r"jest|vitest|playwright\s+test|tsc\b|eslint\b|"
    r"next\s+build|supabase\s+db\s+(lint|diff|test)|pytest|ruff\s+check"
    r")\b"
)


def marker_path(project_dir: str) -> str:
    return os.path.join(project_dir, ".claude", ".dev-pack-verified")


def main():
    data = json.loads(sys.stdin.read())
    if data.get("tool_name") != "Bash":
        sys.exit(0)
    cmd = (data.get("tool_input", {}) or {}).get("command", "")
    if not VERIFY.search(cmd):
        sys.exit(0)

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    mp = marker_path(project_dir)
    os.makedirs(os.path.dirname(mp), exist_ok=True)
    with open(mp, "w", encoding="utf-8") as f:
        f.write(f"{int(time.time())}\t{cmd[:200]}\n")
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)
