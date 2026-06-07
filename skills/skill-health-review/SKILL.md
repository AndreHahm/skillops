# Skill Health Review

## Purpose
Review skill health using validation findings, a basic health score, and governance readiness criteria.

## When to use
Use this skill when evaluating whether registered skills are ready for review, identifying quality gaps, or preparing improvement recommendations.

## Expected outcome
Each reviewed skill has clear errors, warnings, info findings, health score context, and prioritized improvement recommendations.

## Procedure
1. Run registry validation and collect errors, warnings, and info findings.
2. Treat errors as blocking issues that must be fixed before trusting the registry.
3. Treat warnings as Phase 1 gaps, including draft status and missing eval suite configuration.
4. Treat info findings as useful context, such as intentionally empty dependency categories.
5. Review the health score and explain which findings affected it.
6. Recommend concrete improvements such as adding a missing eval suite, moving out of draft status after review, or completing documentation.

## Quality checklist
- Errors are listed before warnings and info findings.
- Draft status is called out as a readiness gap, not a schema failure.
- Missing eval suite configuration is identified for later evaluation work.
- Improvement recommendations are specific and assigned to the correct skill.
- Health score interpretation is consistent across skills.

## Do / don't
- Do separate blocking validation errors from non-blocking warnings.
- Do make recommendations actionable.
- Don't generate unrelated reports unless the repository workflow requires them.
- Don't treat planned later-phase eval work as a Package 2 blocker.
