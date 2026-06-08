---
name: Skill Manifest Authoring
description: Create and maintain valid SkillOps skill.yaml manifests with clear ownership, compatibility, dependencies, permissions, eval metadata, provenance, and paths.
---

# Skill Manifest Authoring

## Purpose

Use this skill to create and maintain `skill.yaml` manifests. A skill manifest is the machine-readable contract for a skill: it tells SkillOps how to identify, validate, classify, govern, and locate the skill documentation.

## When to Use

Use this skill when:

- Creating a new skill.
- Updating metadata for an existing skill.
- Changing allowed tool access.
- Changing skill, tool, or MCP server dependencies.
- Preparing a skill for inclusion in `registry/skills.yaml`.
- Fixing manifest validation errors.
- Aligning a manifest with `schemas/skill.schema.json`.

## Expected Outcome

A completed manifest provides:

- A valid `skill.yaml` that passes SkillOps validation.
- A stable skill ID suitable for registry use.
- Clear ownership with name and contact.
- Correct risk tier for the skill's operational impact.
- Correct execution type for how the skill is used.
- Explicit dependencies instead of hidden prose-only requirements.
- Least-privilege allowed tool settings.
- Eval metadata that reflects the current lifecycle state.
- Provenance and license metadata.
- A valid `paths.skill_file` that points to `SKILL.md`.

## Inputs

Collect these inputs before editing the manifest:

- Skill ID.
- Skill name.
- Skill purpose and concise description.
- Owner name and contact.
- Risk tier.
- Lifecycle status.
- Execution type.
- Compatible agents.
- Compatible environments.
- Skill, tool, and MCP server dependencies.
- Allowed shell and filesystem access.
- Eval suite ID and eval status.
- Provenance source and license.
- Skill documentation path.

## Procedure

1. Choose a stable skill ID:
   - Use lowercase kebab-case.
   - Avoid renaming IDs after registry inclusion unless the rename is explicitly approved.
2. Write a concise description:
   - State what the skill helps an agent do.
   - Avoid generic descriptions that do not support discovery.
3. Assign owner:
   - Set both `owner.name` and `owner.contact`.
   - Use the accountable team or maintainer contact.
4. Choose status:
   - Use `draft` for early Phase 1 skills.
   - Promote only when repository governance documents support the promotion.
5. Choose risk tier:
   - Use `low` for documentation or instruction-only work with limited operational effect.
   - Use `medium`, `high`, or `restricted` when tool access, automation, data sensitivity, or production impact increases.
6. Choose execution type:
   - Use `instruction-only` when the skill is guidance without bundled scripts or direct integrations.
   - Select a broader execution type only when the skill actually requires that mode.
7. Declare compatibility:
   - List supported agents, such as `claude-code` and `codex`.
   - List supported environments, such as `ubuntu-24.04` and `windows-11-wsl2`.
8. Declare dependencies:
   - Put skill prerequisites in `dependencies.skills`.
   - Put command-line tools in `dependencies.tools`.
   - Put MCP requirements in `dependencies.mcp_servers`.
   - Use empty arrays when a dependency category is not required.
9. Declare allowed tools:
   - Choose least-privilege values for `shell` and `filesystem`.
   - Do not grant read-write access without a concrete editing need.
10. Set eval metadata:
    - Use `suite_id: null` and `status: not-configured` when no eval suite exists.
    - Update both fields together when evals are added.
11. Set provenance:
    - Use an approved provenance source.
    - Keep license accurate.
12. Set `paths.skill_file`:
    - Use `SKILL.md` for the standard file in the skill folder.
    - Confirm the file exists.
13. Run validation:

    ```bash
    uv run skillops validate
    ```

## Controlled Values

Status values:

- draft
- candidate
- reviewed
- stable
- deprecated
- archived

Risk tiers:

- low
- medium
- high
- restricted

Execution types:

- instruction-only
- script-backed
- tool-mediated
- mcp-enhanced
- subagent-spawning

Eval statuses:

- not-configured
- planned
- passing
- failing
- deprecated

Provenance sources:

- internal
- third-party
- fork
- generated
- unknown

## Quality Checklist

- ID is lowercase kebab-case.
- Version is semantic-version-like.
- Owner has name and contact.
- Description is specific enough for discovery.
- Status reflects current lifecycle state.
- Risk tier matches tool access and operational impact.
- Execution type matches how the skill is actually used.
- Dependencies are explicit.
- Tool permissions are not broader than needed.
- Eval metadata is honest and current.
- Provenance is clear.
- `SKILL.md` exists at `paths.skill_file`.
- `uv run skillops validate` passes.

## Do

- Use narrow descriptions that explain the skill's practical use.
- Choose least-privilege tool access.
- Declare dependencies explicitly in manifest fields.
- Keep metadata current when skill behavior changes.
- Keep registry ID, manifest ID, and folder name aligned when possible.

## Don't

- Do not use vague descriptions such as “helps with skills”.
- Do not omit owner information.
- Do not grant read-write access without reason.
- Do not hide dependencies in prose only.
- Do not invent controlled values outside the schema.
- Do not change a skill ID silently after registry inclusion.

## Examples

Minimal valid `skill.yaml` example:

```yaml
id: example-skill
name: Example Skill
version: 0.1.0
status: draft
risk_tier: low
description: Provides focused instructions for completing one SkillOps task.
owner:
  name: platform
  contact: platform@example.com
type:
  category: governance
  execution: instruction-only
compatibility:
  agents:
    - claude-code
    - codex
  environments:
    - ubuntu-24.04
    - windows-11-wsl2
dependencies:
  skills: []
  tools: []
  mcp_servers: []
allowed_tools:
  shell: read-only
  filesystem: read-write
evals:
  suite_id: null
  status: not-configured
provenance:
  source: internal
  license: MIT
paths:
  skill_file: SKILL.md
```

## Related Skills

- skill-registry-maintenance
- skill-health-review
