---
description: Skill Maintenance
---

# Skill Maintenance

## Purpose

Skill maintenance keeps `SKILL.md`, `skill.yaml`, registry entries, tests, and documentation aligned. The goal is to make skill updates safe, reviewable, and limited to the requested scope.

## Maintenance Workflow

1. Read the current `SKILL.md`, `skill.yaml`, and registry entry.
2. Make the smallest change that satisfies the requested scope.
3. Update `SKILL.md` when procedural instructions change.
4. Update `skill.yaml` when metadata, ownership, status, risk, compatibility, dependencies, tool permissions, evaluation metadata, provenance, or paths change.
5. Update `registry/skills.yaml` when adding, moving, removing, or changing registry-facing metadata for a skill.
6. Update documentation if behavior or governance changes.
7. Run validation and tests.

## Adding a Skill

A new skill needs a folder under `skills/`, a practical `SKILL.md`, a valid `skill.yaml`, and a matching `registry/skills.yaml` entry. Use a stable lowercase kebab-case ID.

## Updating a Skill

When updating a skill, keep the change scoped. Avoid modifying unrelated skills, unrelated registry entries, or future roadmap language unless the requested behavior changes require it.

## Reviewing a Skill

Review the manifest, registry entry, skill instructions, owner fields, risk tier, allowed tools, dependencies, lifecycle status, and validation output. Do not promote draft skills casually.

## Common Failure Modes

- `SKILL.md` and `skill.yaml` describe different behavior.
- The registry path does not exist.
- The registry ID does not match the manifest ID.
- Tool permissions are broader than the instructions need.
- Documentation describes future features as current behavior.
- Tests or validation were skipped.

## Phase 1 Boundaries

Phase 1 maintenance is file-based. Do not implement marketplace logic, dependency graph generation, observability integrations, Promptfoo integration, DeepEval integration, self-improvement automation, release automation, deployment automation, databases, or a web UI as part of routine skill maintenance.
