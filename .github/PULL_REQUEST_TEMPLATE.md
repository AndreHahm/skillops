## Summary

## Scope

## Changed Files

## Validation

- [ ] `uv run ruff check .`
- [ ] `uv run pytest`
- [ ] `uv run skillops validate`
- [ ] `uv run skillops health --no-write`

## Package Boundary Check

- [ ] This PR stays within the intended package/scope.
- [ ] No unrelated functionality was changed.
- [ ] No future package functionality was implemented early.

## SkillOps Checks

- [ ] Skill manifests remain valid.
- [ ] Registry entries remain consistent.
- [ ] Documentation was updated if behavior changed.

## Safety Check

- [ ] No secrets, tokens, API keys, or credentials were added.
- [ ] No user-specific absolute paths were added.
- [ ] No unsafe automation was added.

## Self-Review

- [ ] I reviewed the changes against the acceptance criteria.
- [ ] I removed accidental scope creep.
- [ ] I documented deviations or limitations.
