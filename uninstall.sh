#!/usr/bin/env bash
# Remove dev-pack from a target project. Only deletes files dev-pack installed.
# Usage: ./uninstall.sh /path/to/your/project
set -euo pipefail

PROJECT_PATH="${1:-}"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ -z "$PROJECT_PATH" || ! -d "$PROJECT_PATH" ]]; then
  echo "Usage: ./uninstall.sh /path/to/your/project" >&2
  exit 1
fi

echo "Removing dev-pack from $PROJECT_PATH"

# 1-4. remove only our own files
for f in "$SRC"/hooks/*.py;  do rm -f "$PROJECT_PATH/.claude/hooks/$(basename "$f")"; done
for d in "$SRC"/skills/*/;   do rm -rf "$PROJECT_PATH/.claude/skills/$(basename "$d")"; done
for f in "$SRC"/loops/*.md;  do rm -f "$PROJECT_PATH/.claude/commands/$(basename "$f")"; done
for f in "$SRC"/commands/*.md; do rm -f "$PROJECT_PATH/.claude/commands/$(basename "$f")"; done
for f in "$SRC"/agents/*.md; do rm -f "$PROJECT_PATH/.claude/agents/$(basename "$f")"; done
echo "  removed hooks, skills, commands, agents"

# 5. strip the appended rules block from CLAUDE.md (everything from our marker onward)
CLAUDE="$PROJECT_PATH/CLAUDE.md"
MARKER="<!-- ===== dev-pack rules (auto-installed) ===== -->"
if [[ -f "$CLAUDE" ]] && grep -qF "$MARKER" "$CLAUDE"; then
  awk -v m="$MARKER" 'index($0,m){exit} {print}' "$CLAUDE" > "$CLAUDE.tmp"
  mv "$CLAUDE.tmp" "$CLAUDE"
  echo "  stripped dev-pack rules from CLAUDE.md"
elif [[ -f "$CLAUDE" ]]; then
  echo "  WARNING: marker not found in CLAUDE.md; remove the rules manually" >&2
fi

# 6. settings.json (only remove if it is exactly ours)
DEST="$PROJECT_PATH/.claude/settings.json"
if [[ -f "$DEST" ]]; then
  if diff -q "$DEST" "$SRC/hooks/settings.json" >/dev/null 2>&1; then
    rm -f "$DEST"
    echo "  removed .claude/settings.json (was dev-pack's)"
  else
    echo "  WARNING: settings.json has your own changes; remove the 'hooks' block manually" >&2
  fi
fi

echo "Done. Restart Claude Code so the changes take effect."
