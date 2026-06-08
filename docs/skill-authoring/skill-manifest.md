---
description: Skill Manifest
---

# Skill Manifest

## Purpose

A skill manifest is the `skill.yaml` file that describes a skill in machine-readable form. It allows `skillops` validation, registry checks, health reporting, and future tooling to understand the skill without parsing prose from `SKILL.md`.

## Required Fields

The Phase 1 schema requires:

- `id`: stable lowercase kebab-case skill identifier.
- `name`: human-readable skill name.
- `version`: semantic version string such as `0.1.0`.
- `status`: lifecycle state.
- `risk_tier`: governance risk tier.
- `description`: concise description of the skill's purpose.
- `owner`: object with `name` and `contact`.
- `type`: object with `category` and `execution`.
- `compatibility`: supported `agents` and `environments`.
- `dependencies`: referenced `skills`, `tools`, and `mcp_servers`.
- `allowed_tools`: allowed shell and filesystem access.
- `evals`: evaluation suite metadata and status.
- `provenance`: source and license metadata.
- `paths`: file paths owned by the skill manifest, including `skill_file`.

## Controlled Values

- `status`: `draft`, `candidate`, `reviewed`, `stable`, `deprecated`, or `archived`.
- `risk_tier`: `low`, `medium`, `high`, or `restricted`.
- `type.execution`: `instruction-only`, `script-backed`, `tool-mediated`, `mcp-enhanced`, or `subagent-spawning`.
- `allowed_tools.shell`: `read-only`, `read-write`, or `none`.
- `allowed_tools.filesystem`: `read-only`, `read-write`, or `none`.
- `evals.status`: `not-configured`, `planned`, `passing`, `failing`, or `deprecated`.
- `provenance.source`: `internal`, `third-party`, `fork`, `generated`, or `unknown`.

## Minimal Example

```yaml
id: example-skill
name: Example Skill
version: 0.1.0
status: draft
risk_tier: low
description: A minimal example skill manifest for Phase 1 validation.
owner:
  name: platform
  contact: platform@example.com
type:
  category: documentation
  execution: instruction-only
compatibility:
  agents:
    - codex
  environments:
    - ubuntu-24.04
dependencies:
  skills: []
  tools: []
  mcp_servers: []
allowed_tools:
  shell: read-only
  filesystem: read-only
evals:
  suite_id: null
  status: not-configured
provenance:
  source: internal
  license: MIT
paths:
  skill_file: SKILL.md
```

## Validation

Run validation after changing a manifest:

```bash
uv run skillops validate
```

For broader confidence, run:

```bash
uv run pytest
uv run skillops health --no-write
```

## Common Mistakes

- using an `id` that does not match the registry entry;
- omitting required empty arrays under `dependencies`;
- using lifecycle or risk values outside the schema;
- leaving owner contact blank;
- claiming evaluation support when no suite is configured;
- setting broad tool access without matching the risk tier;
- forgetting to update `registry/skills.yaml` when adding or moving a skill.
