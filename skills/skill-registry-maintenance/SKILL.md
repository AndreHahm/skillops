---
name: Skill Registry Maintenance
description: Maintain registry/skills.yaml as the canonical SkillOps index and keep registry entries consistent with skill folders and manifests.
---

# Skill Registry Maintenance

## Purpose

Use this skill to maintain `registry/skills.yaml`. The registry is the canonical index of skills known to SkillOps, and it must stay consistent with skill folders, `skill.yaml` manifests, and each `SKILL.md` file.

## When to Use

Use this skill when:

- Adding a new skill folder.
- Removing a skill from active tracking.
- Renaming a skill.
- Fixing broken registry paths.
- Reviewing registry-related pull requests.
- Investigating validation failures.
- Confirming Phase 1 core skills remain registered.

## Expected Outcome

A completed registry change ensures:

- `registry/skills.yaml` is valid.
- All registered skill paths exist.
- All registered manifests are valid.
- Registry IDs match manifest IDs.
- No duplicate skill IDs exist.
- The current Phase 1 registry contains exactly these five core skills: `python-project-setup`, `skill-manifest-authoring`, `skill-registry-maintenance`, `skill-health-review`, and `documentation-maintenance`.
- CLI list and inspect behavior still works for registered skills.

## Inputs

Collect these inputs before editing the registry:

- Target skill ID.
- Skill manifest path.
- Reason for the registry change.
- Expected lifecycle status.
- Related pull request or issue, if available.
- Whether the change is an add, remove, archive, or rename.

## Procedure

1. Inspect `registry/skills.yaml`:
   - Confirm the registry version exists.
   - Review the existing grouping or ordering convention.
2. Check the target skill folder:
   - Confirm the folder name matches the skill ID unless a documented exception exists.
3. Confirm `skill.yaml` exists at the intended registry path.
4. Confirm `SKILL.md` exists at the manifest's `paths.skill_file` value.
5. Check ID consistency:
   - Registry `id` must match manifest `id`.
6. Check duplicate IDs:
   - Verify no skill ID appears more than once in the registry.
7. Run validation and listing commands:

   ```bash
   uv run skillops validate
   uv run skillops list
   ```

8. Review validation findings:
   - Fix errors before finalizing.
   - Explain warnings that are expected during Phase 1.
9. Update documentation if registry semantics changed:
   - Update README, docs, or LLM-Wiki only when public behavior or durable governance changed.

### Add Skill Procedure

1. Create `skills/<skill-id>/SKILL.md` with required frontmatter and required sections.
2. Create `skills/<skill-id>/skill.yaml` using `skill-manifest-authoring`.
3. Add one registry entry that points to `skills/<skill-id>/skill.yaml`.
4. Keep the new entry sorted or consistently grouped with existing entries.
5. Run `uv run skillops validate` and `uv run skillops list`.
6. Inspect the new skill with the CLI when available.

### Remove Skill Procedure

1. Decide whether the skill should be removed, deprecated, or archived.
2. Prefer `deprecated` or `archived` status when history should remain visible.
3. Remove the registry entry only when the skill should no longer be actively tracked.
4. Check for references in manifests, docs, and tests before deleting files.
5. Run `uv run skillops validate` after the change.
6. Document the reason if the removal changes public project behavior.

### Rename Skill Procedure

1. Treat renames as identity changes unless governance says otherwise.
2. Update the folder name, manifest `id`, registry `id`, registry path, and related references together.
3. Check dependent skill manifests for references to the old ID.
4. Preserve history through deprecation when users or downstream repositories may rely on the old ID.
5. Run `uv run skillops validate`, `uv run skillops list`, and inspect the renamed skill.

## Quality Checklist

- Registry version exists.
- Registry references the expected manifest path.
- Skill ID is unique.
- Manifest ID matches registry ID.
- `skill.yaml` exists at every registry path.
- `SKILL.md` exists for every registered skill.
- Validation passes.
- CLI list output includes expected skills.
- No unrelated registry changes were made.
- Phase 1 registry still contains the five core skills unless the package scope explicitly changes.

## Do

- Keep registry entries sorted or consistently grouped.
- Make small registry changes that are easy to review.
- Validate after every registry edit.
- Preserve history via deprecation when appropriate.
- Reference exact skill IDs and paths in review notes.

## Don't

- Do not leave orphan skill folders unintentionally.
- Do not silently rename IDs.
- Do not add skills without manifests.
- Do not register a skill before `SKILL.md` exists.
- Do not remove skills without checking dependents in later phases.
- Do not change registry semantics while doing content-only maintenance.

## Examples

Example registry entry:

```yaml
- id: skill-registry-maintenance
  path: skills/skill-registry-maintenance/skill.yaml
```

Example consistency check:

```text
registry id: skill-registry-maintenance
manifest id: skill-registry-maintenance
manifest path: skills/skill-registry-maintenance/skill.yaml
skill file: skills/skill-registry-maintenance/SKILL.md
```

## Related Skills

- skill-manifest-authoring
- skill-health-review
- documentation-maintenance
