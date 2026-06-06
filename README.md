# SkillOps

## What is SkillOps?
SkillOps is an open-source control plane foundation for managed agent skill repositories. It helps teams validate skill manifests, maintain a central registry, generate health reports, and document operational governance.

## Why this project exists
Agent skill collections need consistent ownership, risk classification, documentation, and validation before they can safely scale into marketplaces, evaluations, observability, and automation.

## Current MVP Scope
Phase 1 includes the monorepo structure, Python workspace, schemas, registry validation, health report generation, CLI commands, five core skills, agent setup, hooks, MCP examples, LLM-Wiki, documentation, and CI.

## Repository Structure
- `packages/skillops-core`: Pydantic models, validation, and health scoring.
- `packages/skillops-cli`: Typer CLI exposed as `skillops`.
- `registry/`: central SkillOps registries.
- `schemas/`: JSON Schemas for manifests and placeholder registries.
- `skills/`: five initial managed skills.
- `docs/`: human documentation.
- `llm-wiki/`: agent-readable project knowledge.
- `hooks/` and `mcp/`: local examples without external integrations.

## Quickstart
```bash
uv sync --all-packages --dev
uv run skillops list
```

## Validate the Registry
```bash
uv run skillops validate
```

## Generate a Health Report
```bash
uv run skillops health
```
Reports are written to `reports/health/health-report.json` and `reports/health/health-report.md`.

## Core Concepts
A skill has a manifest, owner, risk tier, allowed tools, dependencies, provenance, and documentation. The registry is the central source of truth. Health scores summarize Phase 1 hygiene.

## Roadmap
Phase 1 establishes the foundation. Later phases may add marketplace mechanics, observability, evaluations, automation, and deployment workflows.

## Contributing
See `CONTRIBUTING.md` and run the local CI commands before opening a pull request.

## License
MIT. See `LICENSE`.
