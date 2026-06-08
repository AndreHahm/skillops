# Claude Code Agent Setup

Claude Code is a coding and local review agent for this repository.

- Read `CLAUDE.md` before making changes.
- Use canonical core skills from `skills/`, `registry/skills.yaml`, and each skill manifest instead of duplicating skill content.
- Keep changes scoped to the active package prompt.
- Validate registry and skill changes before reporting completion.

Expected validation commands include:

```bash
uv run pytest
uv run ruff check .
uv run skillops validate
uv run skillops health --no-write
```

Safety expectations:

- Do not commit secrets, API keys, tokens, or real MCP credentials.
- Do not hardcode user-specific absolute paths.
- Treat hook and MCP files as examples only in Phase 1.

Out-of-scope Phase 1 behavior includes observability backend integration, full marketplace logic, dependency graph automation, Promptfoo integration, DeepEval integration, and self-improvement automation.
