# SkillOps LLM-Wiki

## Purpose

The LLM-Wiki stores durable knowledge that helps agents and maintainers reason consistently about `skillops`. It is for stable concepts, decisions, glossary terms, and playbooks.

## What Belongs Here

- Concept pages that define core ideas.
- Architecture Decision Records that explain accepted decisions.
- Glossary entries for shared vocabulary.
- Playbooks for repeatable maintenance workflows.

## What Does Not Belong Here

The LLM-Wiki is not a place for raw logs, temporary task notes, trace data, one-off implementation scratchpads, secrets, credentials, or details that belong in user-facing documentation.

## Main Sections

- `concepts/`: durable definitions of SkillOps concepts.
- `decisions/`: ADRs and other durable decisions.
- `glossary/`: concise term definitions.
- `playbooks/`: repeatable operating procedures.

## Relationship to docs/

`docs/` explains how humans use and maintain the project. `llm-wiki/` preserves concepts and operating knowledge for agents and maintainers. The two should agree, but they serve different reading paths.
