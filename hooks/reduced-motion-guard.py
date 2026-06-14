#!/usr/bin/env python3
"""
reduced-motion-guard.py  —  PostToolUse hook (Write|Edit|MultiEdit)

Enforces the MANDATORY prefers-reduced-motion rule deterministically. If a file introduces
animation (imports an animation engine, or defines CSS @keyframes/transitions) but contains no
reduced-motion handling, it warns so the gap gets fixed before it ships.

This is the deterministic backstop for an accessibility + legal requirement that's easy to forget.

Heuristic, so it only WARNS (PostToolUse exit 2 = feedback to Claude, write already applied).
Fail policy: FAIL OPEN.
"""
import json
import os
import re
import sys

ANIM_SIGNALS = re.compile(
    r"(?i)("
    r"from\s+['\"]motion/react['\"]|from\s+['\"]framer-motion['\"]|"
    r"from\s+['\"]gsap|import\s+gsap|ScrollTrigger|"
    r"from\s+['\"]animejs|from\s+['\"]@react-spring|useGSAP|"
    r"@keyframes|animation:\s|transition:\s|motion-preset-"
    r")"
)

REDUCED_SIGNALS = re.compile(
    r"(?i)(prefers-reduced-motion|useReducedMotion|shouldReduceMotion|reduced[_-]?motion)"
)

# tailwindcss-motion handles reduced-motion automatically; its presets are safe on their own.
TAILWIND_MOTION_ONLY = re.compile(r"(?i)motion-preset-")

CODE_EXT = {".tsx", ".jsx", ".ts", ".js", ".css", ".scss", ".mjs"}


def main():
    data = json.loads(sys.stdin.read())
    ti = data.get("tool_input", {}) or {}
    path = ti.get("file_path") or ti.get("path") or ""
    _, ext = os.path.splitext(path)
    if ext.lower() not in CODE_EXT or not os.path.isfile(path):
        sys.exit(0)

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    if not ANIM_SIGNALS.search(text):
        sys.exit(0)
    if REDUCED_SIGNALS.search(text):
        sys.exit(0)
    # If the only animation is tailwindcss-motion presets, that's auto-handled.
    non_tw = ANIM_SIGNALS.sub("", text)  # crude: still flag if other engines present
    if TAILWIND_MOTION_ONLY.search(text) and not re.search(
        r"(?i)(motion/react|framer-motion|gsap|animejs|@react-spring|@keyframes)", text
    ):
        sys.exit(0)

    print(
        f"[reduced-motion-guard] {os.path.basename(path)} adds animation but has no "
        f"prefers-reduced-motion fallback. This is MANDATORY (accessibility + legal). Add "
        f"useReducedMotion()/a matchMedia guard/the CSS reduce reset before shipping.",
        file=sys.stderr,
    )
    sys.exit(2)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # FAIL OPEN
        print(f"[reduced-motion-guard] internal error, skipping: {e}", file=sys.stderr)
        sys.exit(0)
