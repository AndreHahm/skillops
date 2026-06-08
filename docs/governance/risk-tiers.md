---
description: Risk Tiers
---

# Risk Tiers

## Purpose

Risk tiers communicate how much care a skill needs before use or promotion. They help maintainers reason about tool permissions, filesystem access, external integrations, and potentially destructive actions.

## Risk Tier Values

The allowed Phase 1 risk tier values are:

- `low`
- `medium`
- `high`
- `restricted`

## Low Risk

Use `low` for instruction-only or read-oriented skills that do not require sensitive access and do not perform destructive actions. Phase 1 core skills are mostly low risk because they focus on repository maintenance guidance and local validation.

## Medium Risk

Use `medium` for skills that may write files, change structured repository content, or guide non-trivial maintenance workflows. Filesystem access and tool permissions can move a skill from low to medium risk.

## High Risk

Use `high` for script-backed or external-integration skills that can make broad changes, call external systems, affect production-like resources, or require careful review before use.

## Restricted

Use `restricted` for sensitive or potentially destructive capabilities. Restricted skills need explicit governance and should not be added or promoted casually.

## Assignment Guidance

Assign the lowest tier that accurately reflects the skill's behavior. Consider:

- whether the skill is instruction-only, script-backed, tool-mediated, MCP-enhanced, or subagent-spawning;
- whether shell and filesystem access are read-only, read-write, or absent;
- whether the skill depends on external services;
- whether mistakes could cause data loss, credential exposure, or broad repository changes.

## Phase 1 Notes

Risk tiers are metadata and review signals in Phase 1. They do not enforce runtime sandboxing by themselves.
