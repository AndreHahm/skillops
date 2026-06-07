# Python Project Setup Skill

## When to use
Use this skill when creating or maintaining Python projects that use uv, Ruff, ty, and pytest.

## Expected outcome
A predictable Python project structure with reproducible dependency installation, blocking lint checks, and passing tests.

## Steps
1. Confirm the required Python version and package boundaries.
2. Create or update `pyproject.toml` with project metadata and tool configuration.
3. Use uv for dependency management and lockfile updates.
4. Add pytest tests near the repository test suite.
5. Run linting and tests before proposing changes.

## uv commands
- `uv sync --all-packages --dev`
- `uv run pytest`
- `uv run ruff check .`

## Ruff conventions
Use clear imports, type hints, and simple functions. Fix Ruff errors before committing.

## ty note
ty is useful as an early type-checking signal but is not a Phase 1 blocking gate.

## pytest conventions
Tests should be deterministic, small, and focused on public behavior.

## Do / don't
Do keep setup explicit and documented. Do not add unnecessary dependencies or generated artifacts.
