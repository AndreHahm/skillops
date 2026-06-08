---
description: Architecture Overview
---

# Architecture Overview

## Purpose

This page explains the Phase 1 `skillops` architecture. It describes the current building blocks and the boundaries that prevent planned future systems from being mistaken for implemented behavior.

## Phase 1 Architecture

Phase 1 is a local repository control plane. It uses schemas, manifests, registries, validation, health reports, documentation, and agent setup files to make skill repositories easier to maintain.

The current architecture is file-based. Skills live in `skills/`, manifests are YAML files, registries are YAML files under `registry/`, schemas are JSON Schema files, and tests verify that these files remain consistent.

## Main Building Blocks

- `packages/skillops-core`: reusable Python library for structured models, YAML loading, validation findings, and health scoring.
- `packages/skillops-cli`: Typer-based CLI exposing the `skillops` commands used by maintainers and agents.
- `schemas`: JSON Schemas for skill manifests and related structured registry files.
- `registry`: canonical Phase 1 indexes, especially `registry/skills.yaml`.
- `skills`: managed skill folders with `SKILL.md` instructions and `skill.yaml` manifests.
- `docs`: human-facing documentation for architecture, governance, skill authoring, and roadmap context.
- `llm-wiki`: durable conceptual knowledge, decisions, glossary entries, and playbooks.
- Agent setup: `CLAUDE.md`, `AGENTS.md`, `.claude/`, `.codex/`, and `agents/` orient Claude Code and Codex.
- Hooks and MCP examples: `hooks/` and `mcp/` provide safe examples and placeholders only.

## Current Boundaries

Phase 1 does not include a database, web UI, production service, external marketplace, dependency graph engine, observability backend, Promptfoo integration, DeepEval integration, release automation, or deployment automation.

Hook and MCP files are examples. They should not be treated as active production integrations.

## Future Extension Points

The file-based foundation is designed so later packages can add deeper validation, evaluation integration, dependency graph generation, observability integration, marketplace workflows, third-party sync, and self-improvement automation without replacing the Phase 1 schemas and registry concepts.

Those systems are future extension points, not current implemented behavior.
