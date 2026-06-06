# Skill Registry Maintenance Skill

## How to add a skill
Create `skills/<id>/SKILL.md` and `skills/<id>/skill.yaml`, then add the manifest path to `registry/skills.yaml`.

## How to remove a skill
Remove the registry entry first, then remove files only when no documentation or references still depend on them.

## How to rename a skill
Create the new manifest id and path, update registry references, and validate that no duplicate IDs remain.

## How to validate the registry
Run `uv run skillops validate` or `python scripts/validate_registry.py` from the repository root.

## Common errors
Common errors include duplicate skill IDs, missing manifests, missing SKILL.md files, missing owner data, and invalid risk tiers.

## Review checklist
Check unique IDs, valid manifest schema, owner assignment, status, risk tier, dependencies, allowed tools, and eval metadata.
