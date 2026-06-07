# Skill Manifest Authoring

## Purpose
Create and maintain `skill.yaml` files that satisfy the SkillOps skill manifest schema and carry enough governance metadata for Phase 1 validation.

## When to use
Use this skill when adding a skill folder, editing a manifest, reviewing a manifest, or preparing a skill for registry inclusion.

## Expected outcome
The manifest includes all required fields, uses accepted status values and risk tiers, declares dependencies and allowed tools, records provenance, and points `paths.skill_file` to `SKILL.md`.

## Procedure
1. Set a lowercase kebab-case `id` that matches the skill folder name.
2. Provide `name`, semantic-version-like `version`, and a description of at least one clear sentence.
3. Choose one status value: `draft`, `candidate`, `reviewed`, `stable`, `deprecated`, or `archived`.
4. Choose one risk tier: `low`, `medium`, `high`, or `restricted`.
5. Add `owner.name` and `owner.contact`.
6. Define `type.category` and `type.execution`.
7. Declare compatibility agents and environments.
8. Declare `dependencies.skills`, `dependencies.tools`, and `dependencies.mcp_servers` as arrays, even when empty.
9. Set allowed tools for `shell` and `filesystem` using `read-only`, `read-write`, or `none`.
10. Record eval configuration, provenance source, license, and `paths.skill_file: SKILL.md`.

## Quality checklist
- Required fields are present and non-empty where required.
- Status values and risk tiers use the schema enums exactly.
- Dependencies are complete arrays.
- Allowed tools follow least privilege.
- Provenance includes source and license.
- `paths.skill_file` resolves to an existing `SKILL.md`.
- The validation checklist includes schema validation and registry consistency.

## Do / don't
- Do keep manifests concise and machine-readable.
- Do update the registry when a skill is added, removed, or renamed.
- Don't use legacy repository names in new manifest text.
- Don't add unapproved tool access to make validation easier.
