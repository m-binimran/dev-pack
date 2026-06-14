# Verification (truth-telling, before publishing)

Run every check below and paste real output. Never claim "tested/works" without having run it. If something
can't run in this environment, label it **unverified** — don't mark it passed.

## 1. Hook test harness
```bash
python tests/test_hooks.py        # expect "N passed, 0 failed", exit 0
```
Every hook needs a block case AND an allow case. A guard you didn't prove is a guard you don't have.

## 2. JSON validity
```bash
python -c "import json; json.load(open('hooks/settings.json')); json.load(open('mcp/.mcp.json')); print('valid')"
```

## 3. Installer syntax — both shells
PowerShell (AST parse, and confirm pure ASCII — the em-dash trap):
```powershell
$p = "install.ps1"; $e=$null
[System.Management.Automation.Language.Parser]::ParseFile($p,[ref]$null,[ref]$e) | Out-Null
if ($e) { $e | % { "Line $($_.Extent.StartLineNumber): $($_.Message)" } } else { "parses cleanly" }
([System.IO.File]::ReadAllBytes($p) | ? { $_ -gt 127 }).Count   # must be 0 for .ps1/.sh
```
Bash:
```bash
bash -n install.sh && bash -n uninstall.sh && echo OK
```

## 4. Install → uninstall cycle (the real proof)
On a TEMP project that already has its own `CLAUDE.md` content AND a non-pack file in `.claude/hooks/`:
1. run the installer → confirm files land in `.claude/{hooks,skills,commands,agents}`, `settings.json` written,
   rules appended to CLAUDE.md (and any non-ASCII like `→` survived — proves the UTF-8 read).
2. run the uninstaller → confirm: the pack's own files are gone, **the user's own file is preserved**, the
   CLAUDE.md block is stripped, the original user content is byte-identical, `settings.json` removed only if
   it was the pack's.
This single test is what separates "looks done" from "done".

## 5. Frontmatter + corruption scan
For every `skills/*/SKILL.md`, `agents/*.md`, `loops/*.md`: starts with `---`, has required keys
(`name`+`description` for skills/agents; `description` for loops), and the declared `name` matches the folder.
Scan all files for stray non-ASCII that indicates corruption — but know that `·`, `→`, `≥`, em-dash, and emoji
in **markdown docs** are intentional; only non-ASCII in **scripts** (`.ps1`/`.sh`/`.py`/`.json`) is a red flag.

## 6. Cross-references
No loop or agent may reference a skill/agent that doesn't exist as a file (dangling refs). Grep the
referenced names against the actual folders.
