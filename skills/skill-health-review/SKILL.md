---
name: Skill Health Review
description: Interpret SkillOps validation and health output, separate blocking issues from warnings, and produce actionable maintenance recommendations.
---

# Skill Health Review

## Purpose

Use this skill to turn validation and scoring output into actionable maintenance recommendations. Health review explains errors, warnings, info findings, health score changes, draft status, missing eval suite metadata, and review comments without expanding work beyond the current package scope.

## When to Use

Use this skill when:

- After running `uv run skillops health`.
- Before merging a skill pull request.
- After adding or changing a skill.
- When a skill has a low health score.
- When registry validation emits warnings.
- During periodic skill maintenance.
- When reviewers need concise recommendations tied to findings.

## Expected Outcome

A completed review provides:

- Health findings that are understood and summarized.
- Blocking errors separated from non-blocking warnings.
- Info findings treated as maintenance hints.
- Concrete improvements tied to exact findings.
- Review comments that are actionable.
- No unnecessary or out-of-scope changes suggested.

## Inputs

Collect these inputs before reviewing health:

- Health report JSON or Markdown.
- Validation report.
- Affected skill IDs.
- Pull request context, if available.
- Intended lifecycle status for each affected skill.
- Package or phase scope for the current work.

## Procedure

1. Run validation and health commands:

   ```bash
   uv run skillops validate
   uv run skillops health
   ```

2. Read errors first:
   - Treat schema failures, missing registry files, invalid YAML, duplicate IDs, missing manifests, missing `SKILL.md`, missing owner, and missing risk tier as blockers.
3. Read warnings second:
   - Review warning details and decide whether they need immediate fixes in the current scope.
4. Read info findings last:
   - Treat info findings as useful maintenance context, not automatic work items.
5. Check health score:
   - Identify which findings reduced the score.
   - Avoid optimizing the score through unrelated changes.
6. Identify blocking issues:
   - List the exact skill ID, file, and finding code when available.
7. Identify reasonable improvements:
   - Recommend focused fixes that match the current package scope.
8. Prepare concise review comments:
   - State the issue, impact, and requested action.
   - Separate required fixes from optional improvements.
9. Avoid out-of-scope recommendations:
   - Do not request marketplace, dependency graph, observability, or eval automation features during Phase 1 content work.

### Health Interpretation

- Errors block completion and must be fixed or explicitly justified before merge.
- Warnings require review but may not block if they reflect accepted Phase 1 limitations.
- Info findings are maintenance hints and should not inflate scope.
- Draft status is expected for early skills and is not a defect by itself.
- Missing eval suite metadata is expected in Phase 1 when evals are not configured, but it should remain visible for later phases.
- A low health score should lead to targeted fixes, not broad refactoring.

## Quality Checklist

- All errors are addressed or explicitly justified.
- Warnings are reviewed and categorized.
- Info findings are not treated as blockers.
- Recommendations are tied to validation or health findings.
- Suggested changes stay within scope.
- No unrelated refactoring is requested.
- Review comments reference exact skill IDs and files.
- Phase 1 limitations are distinguished from defects.

## Do

- Prioritize errors over warnings.
- Keep recommendations actionable and specific.
- Reference exact skill IDs and files.
- Distinguish MVP limitations from defects.
- Explain why a warning is acceptable when leaving it unresolved.
- Keep review comments concise enough for a pull request discussion.

## Don't

- Do not request marketplace features during Phase 1.
- Do not require eval suites before Phase 2 unless explicitly scoped.
- Do not inflate scope based on info findings.
- Do not treat draft status as a defect by itself.
- Do not suggest unrelated refactors to improve a health score.
- Do not hide blocking validation errors behind general quality language.

## Examples

Example review comment:

```text
Blocking: `skill-registry-maintenance` is registered, but validation reports `skill_file.missing` for `skills/skill-registry-maintenance/SKILL.md`. Restore the file or update `paths.skill_file`, then rerun `uv run skillops validate`.
```

Example non-blocking Phase 1 comment:

```text
Non-blocking: `documentation-maintenance` has eval status `not-configured`. This is acceptable for Phase 1, but keep the finding visible for the Phase 2 eval package.
```

## Related Skills

- skill-registry-maintenance
- documentation-maintenance
- skill-manifest-authoring
