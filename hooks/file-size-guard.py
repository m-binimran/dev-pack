#!/usr/bin/env python3
"""
file-size-guard.py  —  PreToolUse hook (Write)

Blocks writing a file larger than the line budget (default 800). Big files are hard to review,
slow to type-check, and usually mean a component/module should be split.

Checks the tool INPUT content (the file may not exist yet), per ECC's pattern.
Env override: DEV_PACK_MAX_LINES (e.g. 1200).

Fail policy: FAIL OPEN.
"""
import json
import os
import sys

DEFAULT_MAX = 800


def main():
    data = json.loads(sys.stdin.read())
    if data.get("tool_name") != "Write":
        sys.exit(0)
    ti = data.get("tool_input", {}) or {}
    content = ti.get("content", "") or ""
    path = ti.get("file_path", "") or "file"

    try:
        max_lines = int(os.environ.get("DEV_PACK_MAX_LINES", DEFAULT_MAX))
    except ValueError:
        max_lines = DEFAULT_MAX

    lines = content.count("\n") + 1
    if lines > max_lines:
        print(
            f"[file-size-guard] BLOCKED: {os.path.basename(path)} is {lines} lines "
            f"(limit {max_lines}). Split it into smaller modules/components before writing. "
            f"(Override for this write with DEV_PACK_MAX_LINES if truly justified.)",
            file=sys.stderr,
        )
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # FAIL OPEN
        print(f"[file-size-guard] internal error, allowing: {e}", file=sys.stderr)
        sys.exit(0)
