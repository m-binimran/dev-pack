#!/usr/bin/env python3
"""
test_hooks.py — self-contained test harness for the dev-pack hooks.

No third-party deps. Runs each hook as a subprocess with sample JSON on stdin and asserts the
exit code (0 = allow, 2 = block/warn). Run locally or in CI:

    python tests/test_hooks.py

Exit 0 if all pass, 1 if any fail.
"""
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOKS = os.path.join(ROOT, "hooks")
PY = sys.executable


def run_hook(name, payload, env=None):
    """Run a hook with payload (dict) on stdin; return exit code."""
    e = dict(os.environ)
    if env:
        e.update(env)
    p = subprocess.run(
        [PY, os.path.join(HOOKS, name)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        env=e,
    )
    return p.returncode


def write_payload(tool, file_path, content=None):
    ti = {"file_path": file_path}
    if content is not None:
        ti["content"] = content
    return {"tool_name": tool, "tool_input": ti}


CASES = []


def case(name, expected, fn):
    CASES.append((name, expected, fn))


# --- secret-scan (fail-closed) ---
case("secret-scan blocks stripe key", 2,
     lambda d: run_hook("secret-scan.py",
        write_payload("Write", "a.ts", 'const k = "sk_live_abcdefghijklmnop1234"')))
case("secret-scan allows env ref", 0,
     lambda d: run_hook("secret-scan.py",
        write_payload("Write", "a.ts", "const k = process.env.STRIPE_KEY")))
case("secret-scan allows .env.example", 0,
     lambda d: run_hook("secret-scan.py",
        write_payload("Write", ".env.example", 'STRIPE_KEY="sk_live_abcdefghijklmnop1234"')))

# --- file-size-guard ---
case("file-size-guard blocks 900 lines", 2,
     lambda d: run_hook("file-size-guard.py",
        write_payload("Write", "big.tsx", "\n".join(f"l{i}" for i in range(900)))))
case("file-size-guard allows small", 0,
     lambda d: run_hook("file-size-guard.py",
        write_payload("Write", "a.tsx", "const x = 1\n")))

# --- sql-safety-guard ---
case("sql-guard blocks DROP TABLE", 2,
     lambda d: run_hook("sql-safety-guard.py",
        {"tool_name": "Bash", "tool_input": {"command": 'psql -c "DROP TABLE users;"'}}))
case("sql-guard allows SELECT", 0,
     lambda d: run_hook("sql-safety-guard.py",
        {"tool_name": "Bash", "tool_input": {"command": 'psql -c "select 1"'}}))
case("sql-guard escape hatch allows", 0,
     lambda d: run_hook("sql-safety-guard.py",
        {"tool_name": "Bash", "tool_input": {"command": 'psql -c "TRUNCATE t;"'}},
        env={"DEV_PACK_ALLOW_DESTRUCTIVE": "1"}))

# --- danger-guard ---
case("danger-guard blocks rm -rf", 2,
     lambda d: run_hook("danger-guard.py",
        {"tool_name": "Bash", "tool_input": {"command": "rm -rf build/"}}))
case("danger-guard allows ls", 0,
     lambda d: run_hook("danger-guard.py",
        {"tool_name": "Bash", "tool_input": {"command": "ls -la"}}))

# --- token-guard ---
case("token-guard exits 0 on vague", 0,
     lambda d: run_hook("token-guard.py", {"prompt": "fix the codebase"}))

# --- reduced-motion-guard (needs real files) ---
def rmg(d):
    p = os.path.join(d, "anim.tsx")
    with open(p, "w", encoding="utf-8") as f:
        f.write('import { motion } from "motion/react"\nexport const C = () => <motion.div animate={{x:1}}/>\n')
    return run_hook("reduced-motion-guard.py", write_payload("Write", p))
case("reduced-motion-guard warns missing fallback", 2, rmg)

def rmg_ok(d):
    p = os.path.join(d, "anim2.tsx")
    with open(p, "w", encoding="utf-8") as f:
        f.write('import { motion, useReducedMotion } from "motion/react"\n'
                'export const C = () => { const r = useReducedMotion(); return <motion.div animate={{x:r?0:1}}/> }\n')
    return run_hook("reduced-motion-guard.py", write_payload("Write", p))
case("reduced-motion-guard passes with fallback", 0, rmg_ok)

# --- migration-validate (needs real file under migrations/) ---
def mig_bad(d):
    md = os.path.join(d, "supabase", "migrations")
    os.makedirs(md, exist_ok=True)
    p = os.path.join(md, "0001_add.sql")
    with open(p, "w", encoding="utf-8") as f:
        f.write("ALTER TABLE users ADD COLUMN age int NOT NULL;\n")
    return run_hook("migration-validate.py", write_payload("Write", p))
case("migration-validate flags bad migration", 2, mig_bad)


def main():
    passed = failed = 0
    with tempfile.TemporaryDirectory() as d:
        for name, expected, fn in CASES:
            try:
                got = fn(d)
            except Exception as e:  # a hook crash is a failure
                print(f"ERROR {name}: {e}")
                failed += 1
                continue
            ok = got == expected
            print(f"{'PASS' if ok else 'FAIL'}  {name}  (expected {expected}, got {got})")
            passed += ok
            failed += not ok
    print(f"\n{passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
