#!/usr/bin/env python3
"""
token-guard.py  —  UserPromptSubmit hook

Keeps sessions lean. Two jobs, both cheap:
  1. If the prompt is vague ("fix the codebase", "make it better"), inject a tiny nudge
     asking for a specific target — vague prompts trigger expensive broad scans.
  2. Otherwise stay silent. (This hook runs on EVERY prompt, so it must add ~0 tokens
     in the common case — practicing the token budget it preaches.)

Anything printed to stdout by a UserPromptSubmit hook is added to the model's context,
so we print only when it's worth the tokens.

Fail policy: FAIL OPEN (silent).
"""
import json
import re
import sys

VAGUE = re.compile(
    r"(?i)^\s*("
    r"fix (the )?(codebase|everything|bugs)|make it better|improve (the )?(code|app|everything)|"
    r"clean up( everything)?|optimi[sz]e (the )?(codebase|everything)|refactor everything"
    r")\s*\.?\s*$"
)


def main():
    data = json.loads(sys.stdin.read())
    prompt = data.get("prompt", "") or ""

    if VAGUE.match(prompt.strip()):
        print(
            "[token-guard] That request is broad and will scan a lot of files. Name a "
            "specific file/function/symptom so the work stays cheap and accurate."
        )
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)
