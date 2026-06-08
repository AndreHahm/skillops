---
description: skillops Documentation
---

# skillops Documentation

## Project Overview

`skillops` is the Phase 1 foundation for managing agent skill repositories with schemas, manifests, a canonical registry, validation, health reporting, core skills, agent setup, and documentation.

The project is intentionally small in Phase 1. It establishes repository hygiene and shared vocabulary before adding larger systems such as marketplace workflows, dependency graph generation, evaluation integrations, observability integrations, or release automation.

## Current MVP Scope

The current MVP scope includes:

- `skill.yaml` schema validation;
- `registry/skills.yaml` consistency checks;
- a reusable `skillops-core` package;
- a `skillops` CLI MVP with validate, health, list, and inspect commands;
- five core skills for repository maintenance;
- Claude Code and Codex setup files;
- hook examples and disabled MCP example configs;
- documentation and LLM-Wiki foundations.

Future phases are planned extension areas. They are not implemented unless explicitly described as current behavior in this repository.

## Quick Navigation

- [Architecture overview](architecture/overview.md)
- [Skill lifecycle](governance/skill-lifecycle.md)
- [Risk tiers](governance/risk-tiers.md)
- [Ownership](governance/ownership.md)
- [Skill manifest authoring](skill-authoring/skill-manifest.md)
- [Skill testing](skill-authoring/skill-testing.md)
- [Skill maintenance](skill-authoring/skill-maintenance.md)
- [Phase 1 roadmap](roadmap/phase-1-foundation.md)

## Relationship Between docs and LLM-Wiki

`docs/` is for user-facing and contributor-facing project documentation. It explains how to understand and operate the repository.

`llm-wiki/` is for durable conceptual knowledge, architecture decisions, glossary terms, and playbooks that help agents and maintainers reason consistently over time.

Use `docs/` for practical project pages. Use `llm-wiki/` for stable concepts and reusable operating knowledge.
