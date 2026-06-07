# Python Project Setup

## Purpose
Provide a repeatable Python >=3.13 project setup workflow using uv, Ruff, ty, pytest, a clean package layout, and clear `pyproject.toml` configuration.

## When to use
Use this skill when creating a new Python package, refreshing project metadata, or checking that an existing SkillOps Python package follows Phase 1 conventions.

## Expected outcome
The project has a clean package layout, explicit Python >=3.13 metadata, reproducible uv dependency management, Ruff linting, ty type-checking guidance, and pytest coverage for core behavior.

## Procedure
1. Confirm the intended package name, import path, and Python >=3.13 requirement.
2. Create or update `pyproject.toml` with project metadata, dependencies, and tool configuration.
3. Keep source code in a clean package layout such as `src/<package_name>/` or the repository's established package structure.
4. Use uv for dependency sync and lockfile updates.
5. Configure Ruff for linting and formatting expectations.
6. Add or update pytest tests for user-visible behavior.
7. Treat ty as a useful type-checking signal when the repository enables it.
8. Run `uv run ruff check .` and `uv run pytest` before finalizing changes.

## Quality checklist
- `pyproject.toml` declares Python >=3.13.
- uv can install the project dependencies.
- Ruff passes without suppressing unrelated issues.
- pytest tests are deterministic and focused.
- The package layout is easy to navigate and avoids generated artifacts.

## Do / don't
- Do keep dependency changes minimal and explicit.
- Do document any intentional Phase 1 deferrals.
- Don't add unnecessary runtime dependencies.
- Don't mix unrelated refactors into setup work.
