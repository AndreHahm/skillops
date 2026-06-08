# Glossary

## Agent

An actor, such as Codex or Claude Code, that can read repository instructions and perform scoped work.

## Agent Setup

Repository files that orient agents, including `AGENTS.md`, `CLAUDE.md`, `.codex/`, `.claude/`, and agent documentation.

<!-- markdownlint-disable MD044 -->

## AGENTS.md

Agent-facing repository instructions used to guide Codex and other agents working in this repository.

## CLAUDE.md

Claude Code-facing repository instructions and context.

<!-- markdownlint-enable MD044 -->

## Codex

An OpenAI coding agent that can apply repository instructions, inspect files, edit code or documentation, and run checks.

## Claude Code

An Anthropic coding agent that can use repository instructions and local setup files to perform scoped development work.

## Core Skill

One of the initial Phase 1 skills maintained in this repository to support project setup, manifest authoring, registry maintenance, health review, and documentation maintenance.

## Dependency

A skill, tool, or MCP server that another skill declares as related or required in its manifest metadata.

## Evaluation

A structured check of skill behavior or quality. Full evaluation integrations are planned for later phases.

## Health Report

A generated report that summarizes Phase 1 validation and health findings.

## Health Score

A basic Phase 1 score that summarizes repository hygiene signals. It is not a complete measure of end-to-end skill quality.

## Hook

A local example script or configuration point that demonstrates how agent actions might be checked or observed.

## LLM-Wiki

Durable conceptual knowledge for agents and maintainers, including concepts, decisions, glossary entries, and playbooks.

## Manifest

The `skill.yaml` metadata file that describes a skill in machine-readable form.

## MCP Server

A Model Context Protocol server that can expose tools or resources to compatible agents. Phase 1 includes example configs only.

## Registry

A canonical machine-readable index of known entities. The Phase 1 skill registry is `registry/skills.yaml`.

## Risk Tier

A manifest value that communicates the review and safety sensitivity of a skill: `low`, `medium`, `high`, or `restricted`.

## Skill

A reusable procedural capability for coding agents, represented by `SKILL.md` and described by `skill.yaml`.

## SkillOps

A maintenance and governance discipline for agent skill repositories.

## Status

A lifecycle value in a skill manifest, such as `draft`, `candidate`, `reviewed`, `stable`, `deprecated`, or `archived`.

## Validation

Checks that structured files, registry entries, and repository paths satisfy expected schemas and consistency rules.
