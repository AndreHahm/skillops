---
name: Python Project Setup
description: Set up and maintain Python packages in the SkillOps monorepo using Python >=3.13, uv, Ruff, ty, pytest, and clean package structure.
---

# Python Project Setup

## Purpose

Use this skill to create or adjust Python package structure in the SkillOps monorepo. It keeps Python packages compatible with Python >=3.13, uv workspace conventions, `pyproject.toml` metadata, Ruff linting, ty type-checking expectations, pytest coverage, and a minimal dependency footprint.

## When to Use

Use this skill when:

- Creating a new Python package under `packages/`.
- Updating package metadata in a root or package-level `pyproject.toml`.
- Adding or reorganizing tests for package behavior.
- Adjusting runtime or development dependency groups.
- Checking that a local package is wired into the uv workspace.
- Preparing package code for CI validation.

## Expected Outcome

A completed setup produces:

- Valid package metadata with `requires-python` set to Python >=3.13.
- Reproducible dependency management through uv.
- Workspace membership that matches the repository layout.
- A clean `src/<package_name>/` package layout.
- Focused pytest tests for new behavior.
- Ruff passing without broad suppressions.
- pytest passing from the repository root.
- ty-compatible type hints for public functions and important internal boundaries.
- No unnecessary runtime or development dependencies.

## Inputs

Collect these inputs before editing files:

- Package name, such as `skillops-core`.
- Intended import package name, such as `skillops_core`.
- Package purpose and public responsibilities.
- Runtime dependencies with justification for each dependency.
- Development dependencies with justification for each dependency.
- Entry points, if the package exposes a CLI or script.
- Expected tests and fixtures for the package behavior.

## Procedure

1. Inspect the existing workspace structure:
   - Read the root `pyproject.toml`.
   - Review existing packages under `packages/`.
   - Follow the established `src/` layout and test style.
2. Check the root `pyproject.toml`:
   - Confirm `requires-python` remains `>=3.13`.
   - Confirm `[tool.uv.workspace]` includes package members that should participate in workspace sync.
   - Confirm Ruff, pytest, and ty-related settings remain consistent with current repository conventions.
3. Add or update the package `pyproject.toml`:
   - Use stable package metadata.
   - Keep runtime dependencies minimal and explicit.
   - Put development-only tools in the existing dev dependency group rather than package runtime dependencies.
   - Declare CLI entry points only when the package actually owns CLI behavior.
4. Create or update `src/<package_name>/`:
   - Match the import package name, for example `src/skillops_core/`.
   - Keep modules small and named after responsibilities.
   - Use `pathlib.Path` for filesystem paths.
   - Add explicit type hints to public functions and data structures.
5. Add tests:
   - Place tests under `tests/` or the repository's established test location.
   - Test user-visible behavior and important error paths.
   - Keep fixtures small and deterministic.
6. Run validation commands from the repository root:

   ```bash
   uv sync
   uv run ruff check .
   uv run pytest
   ```

7. Document deviations:
   - Explain any skipped command, missing tool, or intentional package-layout exception in the final report.
   - Avoid leaving unexplained differences from existing workspace conventions.

## Quality Checklist

- Python version is >=3.13 in every touched package metadata file.
- Package name and import package name are consistent and understandable.
- The package is included in the uv workspace when it should be managed by the monorepo.
- No unused dependencies were added.
- Runtime dependencies are not used for test-only or lint-only needs.
- Tests exist for new behavior.
- Ruff passes.
- Pytest passes.
- ty-relevant type hints are present for public interfaces.
- CLI entry points are declared only when needed.
- No generated artifacts, virtual environments, or cache directories are committed.

## Do

- Prefer a simple package structure with `src/<package_name>/` and focused modules.
- Keep dependencies minimal and justify each new dependency.
- Use `pathlib.Path` instead of stringly typed path manipulation.
- Use explicit type hints for public APIs and validation boundaries.
- Write tests before or alongside implementation.
- Keep CLI concerns in CLI packages and reusable logic in core packages.
- Run commands from the repository root so uv workspace behavior is exercised.

## Don't

- Do not add dependencies for convenience only.
- Do not hardcode user-specific paths, home directories, or machine-local absolute paths.
- Do not introduce Python <3.13 references in package metadata or examples.
- Do not mix CLI concerns into core packages.
- Do not hide package behavior in tests without documenting the public interface.
- Do not broaden lint suppressions to avoid fixing focused issues.

## Examples

Minimal package layout:

```text
packages/example-package/
├── pyproject.toml
└── src/
    └── example_package/
        ├── __init__.py
        └── service.py

tests/
└── test_example_package.py
```

Minimal package metadata shape:

```toml
[project]
name = "example-package"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

Use this command sequence before finalizing package setup work:

```bash
uv sync
uv run ruff check .
uv run pytest
```

## Related Skills

- skill-manifest-authoring
- documentation-maintenance
