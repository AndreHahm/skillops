---
description: skillops Documentation
---

# skillops Documentation

## Project Overview

`skillops` is the foundation for managing agent skill repositories with schemas, manifests, canonical registries, validation, health reporting, core skills, agent setup, documentation, and initial evaluation metadata.

The project remains intentionally small. Phase 2 establishes static evaluation schemas, golden sets, suite metadata, and local evaluation scaffolding. Phase 2a has started with a draft codebase research skill and minimal report location, while Serena, Repomix, graphify, code-review-graph, marketplace workflows, dependency graph generation, production observability integrations, and release automation are planned later or not implemented.

## Current MVP Scope

The current MVP scope includes:

- `skill.yaml` schema validation;
- `registry/skills.yaml` consistency checks;
- a reusable `skillops-core` package;
- a `skillops` CLI MVP with validate, health, list, and inspect commands;
- five Phase 1 core skills for repository maintenance plus the draft Phase 2a codebase research skill;
- Claude Code and Codex setup files;
- hook examples and disabled MCP example configs;
- documentation and LLM-Wiki foundations;
- metadata-only evaluation schemas, golden sets, and eval suite registry entries;
- the `codebase-research` skill and `reports/codebase-research/` location for optional research reports.

Future phases are planned extension areas. They are not implemented unless explicitly described as current behavior in this repository.

## Quick Navigation

- [Architecture overview](architecture/overview.md)
- [Skill lifecycle](governance/skill-lifecycle.md)
- [Risk tiers](governance/risk-tiers.md)
- [Ownership](governance/ownership.md)
- [Skill manifest authoring](skill-authoring/skill-manifest.md)
- [Skill testing](skill-authoring/skill-testing.md)
- [Skill maintenance](skill-authoring/skill-maintenance.md)
- [Evaluation overview](evaluation/overview.md)
- [Golden sets](evaluation/golden-sets.md)
- [Evaluation review gates](evaluation/review-gates.md)
- [Skill-TDD](evaluation/skill-tdd.md)
- [Phase 1 roadmap](roadmap/phase-1-foundation.md)

## Relationship Between docs and LLM-Wiki

`docs/` is for user-facing and contributor-facing project documentation. It explains how to understand and operate the repository.

`llm-wiki/` is for durable conceptual knowledge, architecture decisions, glossary terms, and playbooks that help agents and maintainers reason consistently over time.

Use `docs/` for practical project pages. Use `llm-wiki/` for stable concepts and reusable operating knowledge.
