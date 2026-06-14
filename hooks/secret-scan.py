#!/usr/bin/env python3
"""
secret-scan.py  —  PreToolUse hook (Write|Edit|MultiEdit)

Blocks hardcoded secrets from being written to disk.

Fail policy: FAIL CLOSED. If this script itself errors, it blocks the write — a crash
must not let a secret slip past. (Every other guard fails open.)

Block protocol: exit code 2 + reason on stderr  ->  Claude Code denies the tool call.
Allow:          exit code 0.
"""
import json
import re
import sys

# (name, compiled pattern). Patterns aim for real secrets, not placeholders.
PATTERNS = [
    ("AWS access key id", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("Private key block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")),
    ("Supabase service role / JWT", re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}")),
    ("Generic API key assignment", re.compile(
        r"""(?ix)
        (api[_-]?key|secret|token|passwd|password|client[_-]?secret)
        \s*[:=]\s*['"]([^'"\s]{12,})['"]
        """)),
    ("Stripe live key", re.compile(r"sk_live_[0-9a-zA-Z]{16,}")),
    ("GitHub token", re.compile(r"gh[pousr]_[0-9A-Za-z]{30,}")),
    ("OpenAI key", re.compile(r"sk-[A-Za-z0-9]{20,}")),
]

# Things that look like secrets but aren't — allow these.
PLACEHOLDER = re.compile(
    r"(?i)(process\.env|os\.environ|getenv|import\.meta\.env|\$\{?[A-Z_]+\}?"
    r"|your[_-]?(api[_-]?key|secret|token)|xxx+|placeholder|example|changeme|<[^>]+>)"
)


def extract_targets(tool_name: str, tool_input: dict):
    """Return the text content being written, plus the file path."""
    path = tool_input.get("file_path", "") or tool_input.get("path", "")
    chunks = []
    if tool_name == "Write":
        chunks.append(tool_input.get("content", ""))
    elif tool_name == "Edit":
        chunks.append(tool_input.get("new_string", ""))
    elif tool_name == "MultiEdit":
        for e in tool_input.get("edits", []):
            chunks.append(e.get("new_string", ""))
    return path, "\n".join(c for c in chunks if c)


def main():
    raw = sys.stdin.read()
    data = json.loads(raw)  # if this throws, except-block below fails closed
    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {}) or {}

    path, content = extract_targets(tool_name, tool_input)

    # Allow writes to example/template env files — they're meant to hold placeholders.
    if path.endswith(".env.example") or path.endswith(".env.template"):
        sys.exit(0)

    for line in content.splitlines():
        if PLACEHOLDER.search(line):
            continue
        for name, pat in PATTERNS:
            if pat.search(line):
                snippet = line.strip()[:60]
                print(
                    f"[secret-scan] BLOCKED: looks like a hardcoded secret "
                    f"({name}) in {path or 'file'}:\n  {snippet}...\n"
                    f"Move it to an environment variable (e.g. process.env.X) "
                    f"and reference it instead.",
                    file=sys.stderr,
                )
                sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:  # FAIL CLOSED
        print(f"[secret-scan] internal error, blocking to be safe: {e}", file=sys.stderr)
        sys.exit(2)
