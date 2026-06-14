# Hook authoring (the enforcement backbone)

Hooks are the only deterministic layer — they run every time. Write them in **Python 3.8+** so they run on
Windows/macOS/Linux. Each hook reads JSON on stdin and signals via exit code.

## Protocol
- **Exit 0** = allow / no feedback.
- **Exit 2** = block (PreToolUse) or feed message back to the model (PostToolUse/Stop). Put the message on **stderr**.
- Read the event JSON from stdin: `data = json.loads(sys.stdin.read())`. Useful keys: `tool_name`,
  `tool_input` (`.file_path`, `.content`, `.command`, `.new_string`, `.edits`), `prompt`, `stop_hook_active`.

## Fail mode — choose deliberately, document in the docstring
- **Fail OPEN** (default): a bug in the guard must NOT block the user's real work. Wrap `main()` in
  `try/except` that prints a warning and `sys.exit(0)`.
- **Fail CLOSED** (security-critical only, e.g. secret scanning): if the guard crashes, BLOCK
  (`sys.exit(2)`), so nothing slips past on error. Use sparingly — only where a miss is worse than a false block.

## Events & matchers (wire in `hooks/settings.json`)
- `PreToolUse` + matcher `Write|Edit|MultiEdit` or `Bash` — guards that approve/deny before the action.
- `PostToolUse` — formatters, validators, trackers (exit 2 feeds advice back without undoing the write).
- `UserPromptSubmit` — cheap nudges; stdout is added to context, so keep it ~0 tokens in the common case.
- `Stop` — end-of-turn checks; guard against loops with `if data.get("stop_hook_active"): sys.exit(0)`.
- Reference hooks via `$CLAUDE_PROJECT_DIR`: `python "$CLAUDE_PROJECT_DIR/.claude/hooks/NAME.py"`.

## Hook skeleton (fail-open guard)
```python
#!/usr/bin/env python3
"""NAME.py — <Event> hook (<matcher>). <what it does>. Fail policy: FAIL OPEN."""
import json, sys

def main():
    data = json.loads(sys.stdin.read())
    if data.get("tool_name") != "Bash":   # adjust per matcher
        sys.exit(0)
    cmd = (data.get("tool_input", {}) or {}).get("command", "")
    if BAD(cmd):
        print(f"[NAME] BLOCKED: <reason>. <how to proceed>", file=sys.stderr)
        sys.exit(2)
    sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:        # FAIL OPEN (flip to sys.exit(2) for security-critical)
        print(f"[NAME] internal error, allowing: {e}", file=sys.stderr)
        sys.exit(0)
```

## Committed test harness (proves the guards work — required)
`tests/test_hooks.py`: no third-party deps; run each hook as a subprocess with sample JSON and assert the
exit code. Pattern:
```python
import json, os, subprocess, sys, tempfile
HOOKS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hooks")
def run_hook(name, payload, env=None):
    e = dict(os.environ); e.update(env or {})
    p = subprocess.run([sys.executable, os.path.join(HOOKS, name)],
                       input=json.dumps(payload), capture_output=True, text=True, env=e)
    return p.returncode
# assert run_hook("secret-scan.py", {...}) == 2  (block)  /  == 0 (allow)
```
Every hook gets a block case AND an allow case. Wire it into `.github/workflows/` so CI re-proves it.

## Install / uninstall pattern (marker-based, reversible)
- Install: copy `hooks/*.py` → `.claude/hooks/`, `skills/*` → `.claude/skills/`, `loops/*` →
  `.claude/commands/`, `agents/*` → `.claude/agents/`; **append** rules between a unique marker comment
  (`<!-- ===== <pack> rules (auto-installed) ===== -->`) in `<project>/CLAUDE.md`; copy `settings.json`
  (or write `settings.<pack>.json` beside an existing one and warn to merge).
- Uninstall (safe): delete only the files the pack ships (iterate the pack's own filenames), strip the
  CLAUDE.md block from the marker onward, and remove `settings.json` only if byte-identical to the pack's.
- **Windows PowerShell traps (these will bite you):**
  - Scripts must be **pure ASCII** — an em-dash (`—`) makes PS 5.1's parser report a bogus "missing string
    terminator". Use `-` / `--`. Verify with the AST parser (see `references/verification.md`).
  - When appending rule files that contain `→`/`≥`/etc., read them with `Get-Content -Raw -Encoding UTF8`,
    or PS 5.1 reads them as ANSI and mojibakes the output.
