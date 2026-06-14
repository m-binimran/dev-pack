#!/usr/bin/env python3
"""
danger-guard.py  —  PreToolUse hook (Bash)

Blocks shell commands that are destructive or bypass safety:
  - rm -rf on broad paths
  - git push --force / -f
  - git commit --no-verify / -n
  - curl|wget piped straight into a shell
  - chmod 777

Fail policy: FAIL OPEN.
"""
import json
import re
import sys

RULES = [
    ("recursive force delete", re.compile(r"(?i)\brm\s+(-[a-z]*r[a-z]*f|-[a-z]*f[a-z]*r)\b")),
    ("force push", re.compile(r"(?i)\bgit\s+push\b.*(--force\b|-f\b|--force-with-lease=[^ ]*$)")),
    ("skip git hooks", re.compile(r"(?i)\bgit\s+commit\b.*(--no-verify|\s-n\b)")),
    ("pipe download to shell", re.compile(r"(?i)(curl|wget)\s+[^|]*\|\s*(sudo\s+)?(bash|sh|zsh)\b")),
    ("world-writable chmod", re.compile(r"(?i)\bchmod\s+(-R\s+)?777\b")),
]


def main():
    data = json.loads(sys.stdin.read())
    if data.get("tool_name") != "Bash":
        sys.exit(0)
    cmd = (data.get("tool_input", {}) or {}).get("command", "")

    for name, pat in RULES:
        if pat.search(cmd):
            print(
                f"[danger-guard] BLOCKED: {name}.\n  command: {cmd[:160]}\n"
                f"If you truly intend this, run it yourself outside the agent, or narrow the scope.",
                file=sys.stderr,
            )
            sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # FAIL OPEN
        print(f"[danger-guard] internal error, allowing: {e}", file=sys.stderr)
        sys.exit(0)
