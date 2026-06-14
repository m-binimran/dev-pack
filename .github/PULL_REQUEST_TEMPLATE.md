<!-- Keep PRs to one logical change. Commit format: <type>: <description> -->

## What & why
<!-- One or two lines. What does this change and why? -->

## Type
- [ ] New rule / skill / hook / loop / agent
- [ ] Fix
- [ ] Docs
- [ ] Refactor / chore

## Checklist
- [ ] Serves a stated goal (fewer tokens / accuracy / truth-telling / speed / quality)
- [ ] If a hook changed: `python tests/test_hooks.py` passes locally (paste result below)
- [ ] If a hook added: a test case added to `tests/test_hooks.py` + fail mode stated in its docstring
- [ ] `INVENTORY.md` updated if I added/removed an item
- [ ] No inflated claims in docs; anything I claim works, I actually ran

## Test output
```
<!-- paste `python tests/test_hooks.py` output -->
```
