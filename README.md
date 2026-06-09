# skillops

## What is SkillOps?

SkillOps is a governance and maintenance approach for agent skill repositories. The `skillops` repository provides a control plane foundation for skills, manifests, registries, validation, health reporting, documentation, agent setup, and initial evaluation metadata.

SkillOps treats agent-facing skill repositories like package ecosystems instead of loose prompt folders. Phase 1 focused on local repository structure and validation. Phase 2 now adds evaluation assets for Skill-TDD: Golden Sets, local-first Promptfoo configuration, guarded DeepEval skeletons, review-gate documentation, and a deterministic CI smoke gate. Full/live evaluation, marketplace mechanics, production observability, dependency graph behavior, and self-improvement automation remain planned later or not implemented.

## Why this project exists

Large skill collections become hard to maintain when each skill has different metadata, ownership, review status, tests, and documentation. Without shared structure, agents and maintainers cannot reliably answer basic questions such as which skills exist, who owns them, what tools they may use, and whether registry data matches files on disk.

SkillOps exists so skills can be managed with the same care expected from package ecosystems: clear manifests, canonical registries, validation, ownership, lifecycle status, review expectations, and documentation.

## Current Phase 1 MVP Scope

Phase 1 focuses on:

- repository foundation for a public `skillops` monorepo;
- JSON schemas for skills and registry-related structured files;
- the canonical `registry/skills.yaml` skill index;
- the reusable `skillops-core` library;
- the `skillops` CLI MVP;
- five core skills used to maintain this repository;
- Claude Code and Codex agent setup files;
- documentation and LLM-Wiki foundations.

Phase 2 adds a documentation-backed Skill-TDD evaluation foundation. SkillOps uses Skill-TDD for skill changes: add or update evaluation cases first, update the skill, run validation/evaluation checks, run the deterministic CI smoke gate, and review for regression, scope, and safety risks. This does not implement full/live evaluation, production observability, dependency graph behavior, marketplace behavior, or self-improvement automation.

## What is implemented now

The implemented foundation currently includes:

- the `skill.yaml` JSON Schema in `schemas/skill.schema.json`;
- the canonical skill registry at `registry/skills.yaml`;
- five core skill folders under `skills/`;
- the reusable `skillops-core` package for loading, validation, structured models, and health scoring;
- the `skillops` CLI commands:
  - `validate`;
  - `health`;
  - `list`;
  - `inspect`;
  - `eval --smoke`;
- Claude Code and Codex setup files;
- local hook examples and disabled MCP example configs;
- a MkDocs-compatible `docs/` structure;
- an `llm-wiki/` structure for durable concepts, ADRs, glossary entries, and playbooks;
- the `schemas/golden-set.schema.json` and `schemas/eval-suite.schema.json` evaluation schemas;
- Golden Sets under `evals/golden/`;
- local-first Promptfoo configuration under `evals/promptfoo/`, with mandatory CI Promptfoo execution not implemented;
- guarded DeepEval skeletons under `evals/deepeval/`, with mandatory CI DeepEval live scoring not implemented;
- the eval suite registry at `registry/eval-suites.yaml`;
- the deterministic `skillops eval --smoke` command and CI smoke step for offline asset validation;
- Skill-TDD, review-gate, and CI smoke-gate documentation under `docs/evaluation/`.

## What is intentionally not implemented yet

The repository does not implement these later capabilities yet:

- not implemented yet: full marketplace mechanics;
- not implemented yet: dependency graph generation;
- not implemented yet: full/live CI evaluation beyond the deterministic smoke gate;
- not implemented yet: Promptfoo execution as a required CI gate;
- not implemented yet: DeepEval live scoring as a required CI gate;
- not implemented yet: Langfuse or Phoenix observability integration;
- not implemented yet: third-party skill sync;
- not implemented yet: self-improvement automation;
- not implemented yet: release automation;
- not implemented yet: deployment automation;
- not implemented yet: web UI.

## Repository Structure

| Path | Purpose |
| --- | --- |
| `packages/skillops-core` | Reusable validation, loading, structured model, and health logic. |
| `packages/skillops-cli` | Typer-based `skillops` command-line interface. |
| `schemas` | JSON Schemas for skill manifests, registries, golden sets, and eval suites. |
| `registry` | Canonical registry files, including `registry/skills.yaml` and `registry/eval-suites.yaml`. |
| `skills` | Canonical core skill folders with `SKILL.md` and `skill.yaml`. |
| `evals` | Static evaluation assets, including Golden Sets, local-first Promptfoo configuration, and guarded DeepEval skeletons; full/live CI execution is planned later and not implemented. |
| `docs` | Human-facing project documentation prepared for MkDocs. |
| `llm-wiki` | Durable conceptual knowledge, ADRs, glossary entries, and playbooks. |
| `hooks` | Safe local hook examples and shared hook utilities. |
| `mcp` | Disabled MCP example configs with placeholders only. |
| `agents` | Agent-specific setup documentation. |
| `tests` | Pytest coverage for schemas, validation, CLI behavior, content quality, hooks, MCP examples, agent setup, docs, and LLM-Wiki pages. |

## Quickstart

```bash
uv sync
uv run pytest
uv run ruff check .
uv run skillops validate
uv run skillops health --no-write
```

## CI

The CI workflow runs on pull requests and pushes to `main`.

It checks:

- Ruff
- pytest
- SkillOps registry validation
- deterministic SkillOps evaluation smoke checks
- SkillOps health report generation
- Markdownlint when available

Generated health reports may be uploaded as CI artifacts.

## CLI Usage

```bash
uv run skillops validate
uv run skillops health
uv run skillops list
uv run skillops inspect skill-registry-maintenance
uv run skillops eval --smoke
```

## Core Concepts

- **Skill**: a reusable procedural capability for coding agents, represented by `SKILL.md` and described by `skill.yaml`.
- **Skill manifest**: the machine-readable `skill.yaml` metadata file for a skill.
- **Registry**: the canonical machine-readable index of known skills, currently `registry/skills.yaml`.
- **Health report**: a generated summary of Phase 1 validation and hygiene findings.
- **Golden set**: canonical scenario assets used as behavioral regression protection in Skill-TDD.
- **Eval suite registry**: suite metadata that maps core skills to Golden Sets, Promptfoo configs, and DeepEval skeletons; full/live CI evaluation behavior is not implemented beyond the deterministic smoke gate.
- **Skill-TDD**: eval case first, then skill update, local validation, scenario eval, review, and regression protection.
- **Agent setup**: repository files that orient Claude Code, Codex, hooks, and MCP examples.
- **LLM-Wiki**: durable conceptual knowledge for agents and maintainers, separate from task logs or temporary notes.

## Core Skills

The Phase 1 core skills are:

- `python-project-setup`;
- `skill-manifest-authoring`;
- `skill-registry-maintenance`;
- `skill-health-review`;
- `documentation-maintenance`.

## Agent Setup

Agent-facing setup includes:

- `CLAUDE.md`;
- `AGENTS.md`;
- `.claude/`;
- `.codex/`;
- `hooks/`;
- `mcp/`.

Hook and MCP files are examples only in Phase 1. They do not include real credentials and do not establish production integrations.

## Documentation and LLM-Wiki

- `docs/` contains human-facing project documentation, including architecture, governance, skill authoring, evaluation, and roadmap pages.
- `llm-wiki/` contains durable conceptual knowledge, architecture decisions, glossary definitions, and operational playbooks for agents and maintainers.

Start with `docs/index.md` for project documentation and `llm-wiki/index.md` for durable agent knowledge.

## Roadmap

Phase 1 Foundation establishes the repository, schemas, registry, core library, CLI MVP, core skills, agent setup, docs, and LLM-Wiki. Phase 2 establishes evaluation schemas, Golden Sets, local-first Promptfoo configuration, guarded DeepEval skeletons, Skill-TDD review documentation, and a deterministic CI smoke gate. Later phases may add codebase research support, dependency graph generation, Phase 4 production observability integrations, Phase 5 marketplace mechanics, Phase 6 self-improvement automation, and CI or release finalization.

Future roadmap items are planned extension areas, not current implemented behavior.

## Contributing

See `CONTRIBUTING.md` for contributor guidance. Run the quickstart checks before opening a pull request.

## Security

See `SECURITY.md` for security reporting guidance. Do not commit secrets, tokens, real API keys, or real MCP credentials.

## License

This repository is licensed under the MIT License. See `LICENSE`.
