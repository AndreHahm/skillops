---
name: Documentation Maintenance
description: Keep README, docs, LLM-Wiki, ADRs, roadmap notes, and skill documentation aligned with implemented SkillOps behavior.
---

# Documentation Maintenance

## Purpose

Use this skill to keep human-readable documentation aligned with machine-readable SkillOps artifacts. Documentation maintenance connects implemented behavior in schemas, registries, manifests, CLI commands, and governance rules to README, docs, LLM-Wiki, ADRs, roadmap notes, and skill files.

## When to Use

Use this skill when:

- Changing schemas.
- Changing registry behavior.
- Adding, removing, archiving, or renaming skills.
- Changing CLI usage or command output.
- Changing governance rules.
- Adding architecture decisions.
- Updating roadmap scope.
- Reviewing a pull request for documentation drift.

## Expected Outcome

A completed documentation update ensures:

- README remains accurate for public project usage.
- Docs match implemented behavior.
- LLM-Wiki concepts are updated for agent-readable project knowledge.
- ADRs record important durable decisions.
- Roadmap notes distinguish implemented work from future work.
- Markdownlint passes when configured.
- No stale references are introduced.

## Inputs

Collect these inputs before editing documentation:

- Changed files.
- Feature or package scope.
- Affected documentation targets.
- Affected skill IDs.
- Related ADR or issue, if available.
- Commands whose usage or output changed.
- Governance rule or schema behavior that changed.

## Procedure

1. Identify user-facing behavior changes:
   - Check CLI commands, validation behavior, registry behavior, and package usage.
2. Identify governance or schema changes:
   - Check whether skill authoring rules, registry rules, risk tiers, or lifecycle status guidance changed.
3. Update README only if public usage changed:
   - Keep quickstart commands and project scope accurate.
   - Avoid adding internal implementation notes that belong in docs or LLM-Wiki.
4. Update docs for durable project knowledge:
   - Explain behavior that maintainers and contributors need over time.
5. Update LLM-Wiki for conceptual knowledge:
   - Keep agent-facing concepts, workflows, and package context synchronized.
6. Add or update ADRs for important decisions:
   - Record durable architecture or governance decisions.
   - Do not create ADRs for routine copy edits.
7. Run code checks when documentation is part of a code change:

   ```bash
   uv run ruff check .
   uv run pytest
   ```

8. Run markdownlint if configured:
   - Use the repository's configured markdownlint command when one exists.
   - If markdownlint is not configured, report that limitation instead of inventing a new dependency.

### Documentation Targets

- README: Public entry point, quickstart, project scope, and common commands.
- `docs/`: Durable contributor and user documentation for implemented behavior.
- `llm-wiki/`: Agent-readable concepts, workflows, and project knowledge.
- ADRs: Durable architecture or governance decisions and their rationale.
- Skill files: Operational instructions for agents using or maintaining SkillOps skills.

## Quality Checklist

- Docs match current behavior.
- CLI examples are accurate.
- No old repository name is introduced.
- Python version remains >=3.13.
- Markdown headings are consistent.
- Links are relative where practical.
- README, docs, LLM-Wiki, ADRs, and skill files are updated only when their target audience needs the change.
- Markdownlint passes if configured.
- Planned features are clearly labeled as future work and not described as implemented.

## Do

- Keep docs close to implemented behavior.
- Update examples when commands change.
- Write ADRs for durable decisions.
- Keep documentation concise and easy to scan.
- Use consistent names for skills, registries, schemas, and packages.
- Cite exact commands and files in review notes when answering documentation questions.

## Don't

- Do not document planned features as implemented.
- Do not add vague roadmap promises.
- Do not duplicate the same concept in many places unnecessarily.
- Do not introduce stale or historical repository names.
- Do not update README for purely internal changes that have no public usage effect.
- Do not add markdown tooling dependencies without explicit package scope.

## Examples

README update example:

```text
If `skillops inspect <skill-id>` gains a new required argument, update README quickstart examples and any CLI docs that show the command.
```

LLM-Wiki update example:

```text
If validation governance changes how risk tiers are interpreted, update LLM-Wiki concepts so agents make the same distinction during future reviews.
```

ADR example:

```text
If the project decides that `registry/skills.yaml` remains the canonical skill index for all Phase 1 packages, record that durable governance decision in an ADR.
```

## Related Skills

- skill-registry-maintenance
- skill-health-review
