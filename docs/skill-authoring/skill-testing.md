---
description: Skill Testing
---

# Skill Testing

## Purpose

Skill testing keeps manifests, registries, skill instructions, and documentation consistent. Phase 1 focuses on repository-level validation and content quality checks.

## Phase 1 Testing

Phase 1 validates structure and consistency. Tests check schemas, registry references, core library behavior, CLI behavior, hook examples, MCP examples, agent setup, docs structure, and LLM-Wiki structure.

## Validation Tests

Validation checks confirm that `skill.yaml` files match the schema, registry entries point to existing paths, registry IDs match manifest IDs, and no duplicate skill IDs are introduced.

## Content Tests

Content tests check practical repository expectations such as required files, required headings, stale names, and missing core skill content.

## What Comes Later

Full Promptfoo and DeepEval integrations are planned for later phases. Test-driven development for skills will also expand in later phases as evaluation suites and richer quality gates are introduced.

These systems are not implemented in Phase 1.

## Recommended Commands

```bash
uv run pytest
uv run skillops validate
uv run skillops health --no-write
```
