# ADR-0001: Use a public monorepo as the Phase 1 SkillOps foundation

## Status

Accepted

## Context

SkillOps needs a shared foundation for schemas, registries, validation, health reporting, documentation, agent setup, and core maintenance workflows. Phase 1 should be easy for maintainers and agents to inspect without requiring external services.

Starting with too many repositories or a future marketplace-first design would increase coordination cost before the core concepts are stable.

## Decision

We start with a clean public monorepo to establish shared schemas, registry validation, documentation, agent setup, and core SkillOps workflows before introducing federation, marketplace mechanics, observability, and self-improvement automation.

The monorepo contains the core library, CLI package, schemas, registry files, skills, docs, LLM-Wiki, hooks examples, MCP examples, and tests.

## Consequences

Benefits:

- Maintainers and agents can review the complete Phase 1 foundation in one repository.
- Schemas, registries, docs, tests, and skills can evolve together during early design.
- Local validation can run without external services.
- The public repository creates a clear baseline for contributors.

Tradeoffs:

- A monorepo can become crowded if future packages are not kept scoped.
- Federation and marketplace mechanics must be added later instead of being assumed from the start.
- Repository boundaries for external skill sources are deferred.
- CI and release workflows must eventually distinguish package-specific responsibilities.

## Alternatives Considered

- Start with multi-repo: rejected because it would add coordination overhead before schemas and workflows are stable.
- Start with marketplace first: rejected because marketplace mechanics need reliable manifests, registries, and governance first.
- Start with CLI-only tool: rejected because SkillOps also needs documentation, skills, schemas, and agent setup.
- Start with documentation-only repository: rejected because validation and health reporting need executable code and tests.

## Follow-up Work

Later packages may add CI foundation, richer validation, evaluation integrations, dependency graph generation, observability integrations, marketplace workflows, third-party sync, and self-improvement automation. These should be introduced only after the Phase 1 foundation remains accurate and tested.
