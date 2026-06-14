# Safe publish to GitHub

Publishing is outward-facing and effectively one-way (a public repo can be indexed/cached even if later
deleted). Do these in order. Don't push until the verification in `references/verification.md` is green.

## 0. Prerequisites
```bash
git --version; gh --version; gh auth status   # need gh logged in with 'repo' + 'workflow' scopes
```
The `workflow` scope is required to push `.github/workflows/`. If missing: `gh auth refresh -s workflow`.

## 1. Secret scan (don't trust — check)
```bash
# stray secret files
find . -name ".env" -o -name "*.pem" -o -name "*.key" | grep -v node_modules
# real tokens (exclude your own detection patterns / test fixtures, then eyeball the rest)
grep -rnE "gh[pous]_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|sk_live_[0-9a-zA-Z]{16,}" . | grep -v secret-scan
```
A pack's own regex patterns and an obvious dummy fixture (`sk_live_...mnop1234`) are fine; a real key is not.

## 2. Name consistency
GitHub repo names can't contain spaces → normalize ("dev pack" → `dev-pack`). If the user wants a name that
differs from the project's internal codename, decide whether to rename. If renaming, do it **everywhere and
consistently**: docs, the CLAUDE.md install marker, marker filenames (`.X-verified`), env vars (`X_*`),
fallback filenames. Then **re-run the full verification** — a rename touches tested code paths.

## 3. Privacy-safe git identity
Use the GitHub noreply email so the user's real email isn't published in commit history, while commits still
attribute to them:
```bash
ID=$(gh api user --jq .id); LOGIN=$(gh api user --jq .login)
git config user.name "$LOGIN"
git config user.email "${ID}+${LOGIN}@users.noreply.github.com"
```

## 4. Repo hygiene
- `.gitignore` excludes `.env*` (keep `.env.example`), `__pycache__`, build dirs.
- Add `.gitattributes` so shell scripts stay LF cross-platform:
  ```
  * text=auto eol=lf
  *.ps1 text eol=crlf
  ```
- Commit format `<type>: <description>`; end with the Co-Authored-By trailer per the harness rules.

## 5. Confirm visibility, then create + push
Ask the user **public vs private** (the one-way choice) before creating. Then:
```bash
gh repo create <name> --public --source=. --remote=origin --push \
  --description "<one line>"
```

## 6. Verify the published state (truth-telling)
```bash
gh repo view <owner>/<name> --json visibility,defaultBranchRef,url --jq '.visibility,.defaultBranchRef.name,.url'
gh api repos/<owner>/<name>/git/trees/main?recursive=1 --jq '[.tree[]|select(.type=="blob")]|length'  # file count
gh run list --repo <owner>/<name> --limit 1   # CI should run green on the remote, not just locally
```
Report the URL, the visibility, the file count, and the CI result. A green CI on GitHub's Linux runners
(when you built on Windows) is the strongest proof the pack is portable.

## Honesty at publish
New repos start at **0 stars** — say so; "millions of stars" is persona, not a claim. Optionally suggest
repo topics, a tagged release (`gh release create v0.1.0`), and a CI badge for discoverability.
