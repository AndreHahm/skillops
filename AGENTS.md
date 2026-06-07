# Agent Instructions

## Project Mission
SkillOps is an open-source control plane foundation for managed agent skill repositories.

## Agent Responsibilities
Implement only Phase 1 foundation work, keep code maintainable, and verify every change.

## Repository Structure
Core Python code lives in `packages/`, registries in `registry/`, schemas in `schemas/`, skills in `skills/`, docs in `docs/`, and agent knowledge in `llm-wiki/`.

## Skill Authoring Rules
Each skill must include `SKILL.md` and `skill.yaml` matching `schemas/skill.schema.json`.

## Registry Rules
`registry/skills.yaml` is the source of truth for registered skills and must use unique IDs.

## Validation Rules
Registry validation must fail on missing registry files, invalid YAML, duplicate IDs, invalid manifests, missing SKILL.md, missing owner, and missing risk tier.

## Testing Rules
Run Ruff, pytest, `skillops validate`, and `skillops health` before finalizing changes.

## Documentation Rules
Keep README, docs, and LLM-Wiki synchronized with code and governance behavior.

## Pull Request Expectations
Summarize files changed, validation performed, known limitations, and any intentional Phase 1 deferrals.
