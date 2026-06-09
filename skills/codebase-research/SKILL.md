---
name: Codebase Research
description: Guide coding agents through structured repository research before planning or implementing non-trivial changes.
---

# Codebase Research

## Purpose

Use this skill to help coding agents understand repository structure, architecture, source evidence, dependencies, and implementation risks before planning or changing code. Codebase research creates a concise, reviewable research report that guides implementation planning, but it does not replace direct source inspection of the files that will be changed.

## When to Use This Skill

Use this skill before:

- Implementing non-trivial changes.
- Touching multiple modules or packages.
- Changing architecture, control flow, or cross-cutting behavior.
- Modifying schemas or registries.
- Adding new packages.
- Changing CI, validation, health, or evaluation behavior.
- Refactoring existing code.
- Editing agent-facing instructions.
- Updating skill behavior.

## When Not to Use This Skill

Avoid this skill when the requested change is intentionally small and direct, including:

- Trivial typo fixes.
- Single-line documentation edits.
- Clearly isolated changes that have no architectural impact.
- Cases where the user explicitly asks for a small direct change and no broader investigation.

## Inputs

Collect these inputs before beginning research:

- The user request and acceptance criteria.
- The expected implementation scope and known out-of-scope items.
- Relevant package, skill, schema, registry, documentation, or CI areas.
- Constraints from repository instructions, package prompts, and AGENTS.md files.
- Any available issue, design note, ADR, failing test, or error output.

## Outputs

Produce these outputs before implementation planning:

- A concise research report under `reports/codebase-research/` when a durable artifact is useful.
- A list of relevant files and symbols inspected.
- Architecture observations supported by source evidence.
- Dependencies, coupling points, validation rules, and test surfaces.
- Risks, assumptions, and open questions.
- Recommended implementation boundaries and next steps.

## Research Workflow

Follow this workflow before planning or implementing non-trivial changes:

```text
scope request
  -> inspect repository structure
  -> identify relevant files
  -> run semantic or symbolic search if available
  -> generate or inspect repository context if needed
  -> inspect graph or relationship outputs if available
  -> summarize architecture observations
  -> identify dependencies and risks
  -> document source evidence
  -> produce a research report
  -> proceed to implementation planning
```

Research output should guide implementation decisions, test selection, and risk review. It is not authoritative by itself: confirm important claims by reading the source files, manifests, schemas, tests, and documentation directly.

## Tool Guidance

The tools below are optional research aids. They must not be required for baseline CI, repository validation, or local contribution workflows unless a future package explicitly implements and documents that requirement.

### Serena MCP

Serena MCP can support codebase research by helping with:

- Semantic code search.
- Symbol discovery.
- Finding definitions and references.
- Understanding code relationships.

Use Serena findings as leads, not final proof. Record the source files that support each finding. Do not commit Serena secrets, tokens, private endpoints, or machine-specific configuration. An unavailable Serena setup must not block baseline repository validation or CI.

### Repomix

Repomix can support codebase research by helping with:

- Packaging repository context for AI-assisted review.
- Creating AI-friendly summaries or context bundles.
- Excluding generated files, secrets, caches, dependency directories, and large artifacts.

Do not track large generated Repomix dumps by default. Generated full dumps should remain ignored or local. If a concise summary is useful, store it under `reports/codebase-research/` and label it as research support rather than source truth. Never include secrets, credentials, local user paths, or private machine-specific data in a committed report.

### graphify / Knowledge Graph Builders

Graph-oriented tools may help identify candidate relationships in a repository. Treat this package as generic adapter guidance only; do not assume or require a specific graph implementation.

A future conceptual adapter could be named:

```text
KnowledgeGraphBuilder
```

Possible graph-oriented outputs include:

- Entities.
- Relationships.
- Source files.
- Confidence.
- Generated report.

Do not implement the adapter in this skill package. Do not create dependency graph product behavior here. Mark inferred relationships clearly, keep confidence visible, and avoid treating inferred graph data as authoritative without source evidence from the repository.

### code-review-graph

code-review-graph can support local-first code intelligence by helping agents inspect relationships and change impact before implementation.

Keep generated state local unless the repository explicitly documents what may be committed. Do not require code-review-graph for CI. Summarize findings with source file references. Do not treat code-review-graph as an automatic PR review system in this package.

## Research Report Format

Use this format for durable reports when a report is warranted:

```markdown
# Codebase Research Report

## Scope

## Commands and Tools Used

## Relevant Files

## Architecture Observations

## Important Symbols

## Dependencies

## Risks

## Open Questions

## Recommendations

## Implementation Notes
```

Keep the report concise and evidence-based. Link observations to files, commands, and direct source inspection. If optional tools contributed findings, identify the tool and verify important findings against source files.

## Source Evidence Rules

- Prefer direct source files, schemas, manifests, tests, documentation, and command output.
- Cite file paths and relevant symbols for every important architecture claim.
- Distinguish observed source facts from inferences, assumptions, and recommendations.
- Verify generated summaries against direct source inspection before relying on them.
- Do not cite optional tool output as the only evidence for a code behavior claim.

## Safety Rules

- Do not commit secrets, tokens, credentials, private endpoints, or real API keys.
- Do not commit local absolute user paths such as home directories, user profile paths, workspace-specific cache paths, or private machine-specific data.
- Do not commit large generated context dumps, graph databases, caches, dependency directories, or tool state.
- Do not make external research tools mandatory for baseline CI or validation in this package.
- Do not add network calls to tests for research tooling.
- Keep research artifacts scoped to the request and remove irrelevant generated material before committing.

## Anti-Patterns

- Skipping source inspection because a generated summary seems complete.
- Treating inferred graph relationships as authoritative facts.
- Producing a large dump instead of a concise report.
- Expanding the task into a dependency graph product, observability feature, marketplace behavior, or self-improvement automation.
- Refactoring unrelated modules during research.
- Committing private machine state from optional tools.

## Completion Checklist

Before implementation planning, confirm that:

- The request scope and out-of-scope boundaries are clear.
- Relevant files, tests, schemas, registries, and documentation were identified.
- Optional semantic, symbolic, repository packaging, or graph tools were used only when available and useful.
- Architecture observations are backed by source evidence.
- Dependencies, risks, and open questions are documented.
- Any durable report is concise and stored under `reports/codebase-research/`.
- No generated dump, secret, credential, or local user path is included.
- Research findings have been translated into an implementation plan.

## Related Skills

- documentation-maintenance
- skill-manifest-authoring
- skill-registry-maintenance
- skill-health-review
