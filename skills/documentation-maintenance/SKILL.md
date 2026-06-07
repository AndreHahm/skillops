# Documentation Maintenance

## Purpose
Keep README updates, docs updates, LLM-Wiki updates, ADR updates, and roadmap updates aligned with SkillOps schema and registry behavior.

## When to use
Use this skill when schema, registry, governance, CLI, or workflow changes affect user-facing or agent-facing documentation.

## Expected outcome
Documentation accurately describes current SkillOps concepts, registry structure, skill authoring rules, and any intentional Phase 1 limitations.

## Procedure
1. Update README content when quickstart commands, project scope, or core concepts change.
2. Apply docs updates under `docs/` for durable user guidance.
3. Apply LLM-Wiki updates under `llm-wiki/` for agent-readable concepts and playbooks.
4. Add ADR updates when a lasting architectural or governance decision changes.
5. Keep roadmap updates aligned with completed and deferred package work.
6. Run markdownlint when available, or note if the environment lacks it.

## Quality checklist
- README updates match current commands and repository name.
- Docs updates match schema and registry behavior.
- LLM-Wiki updates are concise and agent-readable.
- ADR updates capture durable decisions rather than transient implementation details.
- Roadmap updates distinguish completed Phase 1 work from later phases.
- markdownlint issues are fixed or explicitly reported.

## Do / don't
- Do keep documentation synchronized with code and governance behavior.
- Do cite files and commands in review notes when answering questions.
- Don't introduce stale references to old repository names.
- Don't document unimplemented Package 3+ features as available.
