#!/usr/bin/env bash
# Install dev-pack into a target project.
# Usage: ./install.sh /path/to/your/project
set -euo pipefail

PROJECT_PATH="${1:-}"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ -z "$PROJECT_PATH" || ! -d "$PROJECT_PATH" ]]; then
  echo "Usage: ./install.sh /path/to/your/project" >&2
  exit 1
fi

echo "Installing dev-pack into $PROJECT_PATH"

command -v python3 >/dev/null 2>&1 || \
  echo "WARNING: python3 not found on PATH. Hooks won't run until installed." >&2

# 1. hooks
mkdir -p "$PROJECT_PATH/.claude/hooks"
cp "$SRC"/hooks/*.py "$PROJECT_PATH/.claude/hooks/"
echo "  hooks  -> .claude/hooks"

# 2. skills -> .claude/skills, loops -> .claude/commands, agents -> .claude/agents
mkdir -p "$PROJECT_PATH/.claude/skills" "$PROJECT_PATH/.claude/commands" "$PROJECT_PATH/.claude/agents"
cp -R "$SRC/skills/." "$PROJECT_PATH/.claude/skills/"
echo "  skills -> .claude/skills"
cp -R "$SRC/loops/." "$PROJECT_PATH/.claude/commands/"
echo "  loops  -> .claude/commands"
cp -R "$SRC/agents/." "$PROJECT_PATH/.claude/agents/"
echo "  agents -> .claude/agents"

# 3. rules -> CLAUDE.md
{
  printf '\n\n<!-- ===== dev-pack rules (auto-installed) ===== -->\n'
  for f in "$SRC"/rules/*.md; do cat "$f"; printf '\n'; done
} >> "$PROJECT_PATH/CLAUDE.md"
echo "  rules  -> CLAUDE.md (appended)"

# 4. settings.json
DEST="$PROJECT_PATH/.claude/settings.json"
if [[ -f "$DEST" ]]; then
  cp "$SRC/hooks/settings.json" "$PROJECT_PATH/.claude/settings.dev-pack.json"
  echo "WARNING: settings.json exists. Wrote settings.dev-pack.json — merge 'hooks' manually." >&2
else
  cp "$SRC/hooks/settings.json" "$DEST"
  echo "  hooks  -> .claude/settings.json"
fi

echo ""
echo "Done. Restart Claude Code in the project so hooks load."
