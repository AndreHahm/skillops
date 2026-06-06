# Claude Code Guide

## Project Mission
Build the Phase 1 SkillOps foundation for validating, documenting, and governing managed agent skills.

## Repository Rules
Keep the monorepo structure stable, avoid secrets, and do not implement later-phase marketplace, observability, or deployment systems.

## Coding Standards
Use Python 3.13, pathlib, type hints, Pydantic models, simple functions, Ruff, and pytest.

## SkillOps Rules
Every registered skill needs a valid `skill.yaml`, a `SKILL.md`, owner data, risk tier, dependencies, allowed tools, eval metadata, provenance, and paths.

## Required Workflow
Inspect relevant files, make focused changes, run validation, run tests, and document outcomes.

## Testing Requirements
Ruff and pytest are blocking. ty may be used as an advisory signal.

## Documentation Requirements
Update README, docs, LLM-Wiki, and ADRs when concepts, schemas, CLI behavior, or governance change.

## Safety Rules
Do not commit secrets, real tokens, or external service credentials. Keep hooks local and transparent.

## Preferred Commands
- `uv sync --all-packages --dev`
- `uv run ruff check .`
- `uv run pytest`
- `uv run skillops validate`
- `uv run skillops health`
