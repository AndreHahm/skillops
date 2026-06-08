# Skill Maintenance Playbook

## Purpose

This playbook gives agents and maintainers a repeatable workflow for adding, updating, or reviewing skills in `skillops`.

## When to Use

Use this playbook when a task changes a skill folder, `SKILL.md`, `skill.yaml`, `registry/skills.yaml`, skill documentation, or validation expectations.

## Inputs

- The requested skill change.
- The existing `SKILL.md` and `skill.yaml` files.
- The corresponding `registry/skills.yaml` entry.
- Relevant docs or LLM-Wiki pages when behavior or governance changes.

## Standard Workflow

1. Confirm the requested scope and avoid unrelated skills.
2. Read the current skill instructions, manifest, and registry entry.
3. Update `SKILL.md` for procedural changes.
4. Update `skill.yaml` for metadata changes.
5. Update `registry/skills.yaml` if the skill is added, moved, renamed, removed, or registry metadata changes.
6. Keep lifecycle status conservative; do not promote draft skills casually.
7. Do not document future features as implemented.
8. Run validation, health checks, tests, and linting.
9. Review the diff for stale names, secrets, broad permissions, and scope creep.

## Review Checklist

- The skill ID is stable lowercase kebab-case.
- `SKILL.md` is practical and agent-usable.
- `skill.yaml` matches the schema.
- Owner name and contact are present.
- Risk tier matches allowed tools and behavior.
- Registry ID and path match the manifest and filesystem.
- Validation and tests were not skipped.
- No unrelated skills were changed.
- No future marketplace, graph, observability, evaluation, or self-improvement system is described as current behavior.

## Common Failure Modes

- Changing a skill without updating its manifest.
- Adding a manifest without registering the skill.
- Promoting `draft` to `stable` without review evidence.
- Broadening shell or filesystem access without risk review.
- Skipping `uv run skillops validate`.
- Editing unrelated files during a narrow skill task.

## Escalation Rules

Escalate to maintainers when a change affects risk tier, ownership, lifecycle promotion, external integrations, restricted capabilities, destructive commands, credentials, or repository-wide governance.

## Commands

```bash
uv run skillops validate
uv run skillops health --no-write
uv run skillops list
uv run skillops inspect skill-registry-maintenance
uv run pytest
uv run ruff check .
```
