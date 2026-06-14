#!/usr/bin/env python3
"""
format-lint.py  —  PostToolUse hook (Write|Edit|MultiEdit)

Best-effort auto-format of the file that was just written, using whatever the
project already has installed. Never blocks: if a formatter is missing or errors,
it stays quiet. Output (if any) is informational.

Formatters by extension:
  .js .jsx .ts .tsx .json .css .md   -> npx prettier --write
  .sql                               -> sqlfluff fix (if installed)
  .py                                -> black / ruff (if installed)

Fail policy: FAIL OPEN, always exit 0 (formatting is cosmetic).
"""
import json
import os
import shutil
import subprocess
import sys

PRETTIER_EXT = {".js", ".jsx", ".ts", ".tsx", ".json", ".css", ".scss", ".md", ".mdx", ".html", ".yml", ".yaml"}


def run(cmd, cwd):
    try:
        subprocess.run(cmd, cwd=cwd, capture_output=True, timeout=60, check=False)
        return True
    except Exception:
        return False


def main():
    data = json.loads(sys.stdin.read())
    tool_input = data.get("tool_input", {}) or {}
    path = tool_input.get("file_path") or tool_input.get("path")
    if not path or not os.path.isfile(path):
        sys.exit(0)

    cwd = os.path.dirname(path) or "."
    _, ext = os.path.splitext(path)
    ext = ext.lower()

    did = None
    JS_TS = {".js", ".jsx", ".ts", ".tsx", ".mjs"}
    if ext in PRETTIER_EXT and shutil.which("npx"):
        if run(["npx", "--no-install", "prettier", "--write", path], cwd):
            did = "prettier"
        # also auto-fix lint issues on JS/TS, if eslint is wired in the project
        if ext in JS_TS:
            if run(["npx", "--no-install", "eslint", "--fix", path], cwd):
                did = (did + " + eslint") if did else "eslint"
    elif ext == ".sql" and shutil.which("sqlfluff"):
        run(["sqlfluff", "fix", "--force", path], cwd)
        did = "sqlfluff"
    elif ext == ".py":
        if shutil.which("ruff"):
            run(["ruff", "format", path], cwd)
            did = "ruff"
        elif shutil.which("black"):
            run(["black", "-q", path], cwd)
            did = "black"

    if did:
        print(f"[format-lint] formatted {os.path.basename(path)} with {did}")
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)  # cosmetic — never block
