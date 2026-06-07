# Skill Registry Maintenance

## Purpose
Maintain `registry/skills.yaml` as the source of truth for registered SkillOps skills and keep it consistent with skill folders.

## When to use
Use this skill when adding skills, removing skills, renaming skills, checking registry paths, or reviewing registry consistency before a release.

## Expected outcome
The registry validates against schema, references existing `skill.yaml` files, has no duplicate skill IDs, and each registered manifest points to an existing `SKILL.md`.

## Procedure
1. For adding skills, create `skills/<id>/skill.yaml` and `skills/<id>/SKILL.md`, then add one registry entry.
2. For removing skills, remove the registry entry and then remove files only when no active references remain.
3. For renaming skills, update the folder, manifest `id`, registry `id`, registry path, and dependent references together.
4. Check registry paths are relative to the repository root and end with `skill.yaml`.
5. Check duplicate skill IDs before and after editing.
6. Validate the registry against `schemas/registry.schema.json`.
7. Validate each referenced manifest against `schemas/skill.schema.json`.
8. Run `uv run skillops validate` when the CLI is available.

## Quality checklist
- `registry/skills.yaml` contains the expected version and skills array.
- Every registry path exists.
- Every registry `id` matches the manifest `id`.
- Every registered skill has a `SKILL.md`.
- Duplicate skill IDs are detected during review.
- The review checklist covers schema validation, paths, IDs, owners, risk tiers, and eval metadata.

## Do / don't
- Do keep registry changes small and auditable.
- Do preserve stable IDs unless a rename is intentional.
- Don't leave stale paths after moving skill folders.
- Don't register a skill before its manifest and documentation are valid.
