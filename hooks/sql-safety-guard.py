#!/usr/bin/env python3
"""
sql-safety-guard.py  —  PreToolUse hook (Bash)

Blocks catastrophic database commands:
  - DROP DATABASE / DROP TABLE / TRUNCATE
  - DELETE / UPDATE with no WHERE clause
  - any of the above aimed at a production-looking connection

Escape hatch (intentional, documented): set  DEV_PACK_ALLOW_DESTRUCTIVE=1
in the env for the one command you really mean. The guard then allows it.

Fail policy: FAIL OPEN. A bug here must not block normal shell work.
"""
import json
import os
import re
import sys

DESTRUCTIVE = [
    ("DROP DATABASE", re.compile(r"(?i)\bdrop\s+database\b")),
    ("DROP TABLE", re.compile(r"(?i)\bdrop\s+table\b")),
    ("TRUNCATE", re.compile(r"(?i)\btruncate\b")),
    ("DELETE without WHERE", re.compile(r"(?i)\bdelete\s+from\s+\w+\s*(;|$)")),
    ("UPDATE without WHERE", re.compile(r"(?i)\bupdate\s+\w+\s+set\b(?!.*\bwhere\b)")),
]

PROD_SIGNALS = re.compile(
    r"(?i)(prod|production|\.supabase\.co|amazonaws\.com|NODE_ENV\s*=\s*production)"
)


def main():
    data = json.loads(sys.stdin.read())
    if data.get("tool_name") != "Bash":
        sys.exit(0)
    cmd = (data.get("tool_input", {}) or {}).get("command", "")

    if os.environ.get("DEV_PACK_ALLOW_DESTRUCTIVE") == "1":
        sys.exit(0)

    hits = [name for name, pat in DESTRUCTIVE if pat.search(cmd)]
    if not hits:
        sys.exit(0)

    prod = " AND it targets a PRODUCTION-looking host" if PROD_SIGNALS.search(cmd) else ""
    print(
        f"[sql-safety-guard] BLOCKED: destructive SQL detected ({', '.join(hits)}){prod}.\n"
        f"  command: {cmd[:160]}\n"
        f"If this is intentional, re-run with DEV_PACK_ALLOW_DESTRUCTIVE=1 set for that "
        f"command, and make sure you have a backup. Prefer a WHERE clause or a soft delete.",
        file=sys.stderr,
    )
    sys.exit(2)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # FAIL OPEN
        print(f"[sql-safety-guard] internal error, allowing: {e}", file=sys.stderr)
        sys.exit(0)
