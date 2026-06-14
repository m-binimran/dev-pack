#!/usr/bin/env python3
"""
migration-validate.py  —  PostToolUse hook (Write|Edit|MultiEdit)

Only acts on files under a migrations directory. Checks that a new/edited migration
is reversible and not obviously unsafe, then feeds findings back to Claude so it can
fix them before moving on.

Checks:
  - SQL migration has a rollback (a `down`, `-- rollback`, or a paired *.down.sql file)
  - flags un-gated destructive statements inside the migration
  - flags ADD COLUMN ... NOT NULL with no DEFAULT (locks / breaks existing rows)

Fail policy: FAIL OPEN. On a finding it exits 2 with advice (PostToolUse exit 2 shows
stderr to Claude without undoing the write) — advisory, not a hard block.
"""
import json
import os
import re
import sys

MIGRATION_DIR = re.compile(r"(?i)(^|[\\/])(migrations?|supabase[\\/]migrations)[\\/]")


def is_migration(path: str) -> bool:
    return bool(path) and MIGRATION_DIR.search(path) is not None and path.lower().endswith(".sql")


def main():
    data = json.loads(sys.stdin.read())
    tool_input = data.get("tool_input", {}) or {}
    path = tool_input.get("file_path") or tool_input.get("path") or ""
    if not is_migration(path) or not os.path.isfile(path):
        sys.exit(0)

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        sql = f.read()
    low = sql.lower()
    findings = []

    has_down = (
        "down" in low
        or "-- rollback" in low
        or "drop" in low and "create" in low  # crude reversibility hint
        or os.path.exists(path.replace(".sql", ".down.sql"))
        or os.path.exists(os.path.join(os.path.dirname(path), "down.sql"))
    )
    if not has_down:
        findings.append("No rollback found. Add a matching `down` migration (or a -- rollback section).")

    if re.search(r"(?i)\b(drop\s+table|truncate)\b", low):
        findings.append("Contains DROP TABLE / TRUNCATE. Confirm this is intended and backed up.")

    if re.search(r"(?i)add\s+column\s+\w+\s+[^;]*not\s+null(?![^;]*default)", low):
        findings.append("ADD COLUMN ... NOT NULL without DEFAULT will fail / lock on a non-empty table. "
                        "Add a DEFAULT, or use expand→backfill→contract.")

    if not findings:
        sys.exit(0)

    print("[migration-validate] review this migration before continuing:\n  - "
          + "\n  - ".join(findings), file=sys.stderr)
    sys.exit(2)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # FAIL OPEN
        print(f"[migration-validate] internal error, skipping: {e}", file=sys.stderr)
        sys.exit(0)
