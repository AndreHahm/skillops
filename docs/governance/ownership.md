---
description: Ownership
---

# Ownership

## Purpose

Ownership makes every skill accountable. A skill owner is the first point of contact for manifest quality, content updates, validation readiness, and review coordination.

## Owner Fields

Every `skill.yaml` manifest needs an `owner` object with:

- `name`: the responsible person, team, or default owner group;
- `contact`: a contact route for questions and review.

## Responsibilities

The owner is responsible for:

- keeping `skill.yaml` accurate;
- keeping `SKILL.md` practical and agent-usable;
- ensuring registry entries match the manifest and filesystem;
- running validation and relevant tests before review;
- updating documentation when behavior or governance changes.

## Review Expectations

Reviewers should verify that ownership is not empty, stale, or misleading. Ownership should be specific enough that maintainers know where to route questions.

## Phase 1 Defaults

Phase 1 may use `platform` as the default owner for core skills until more specific maintainers are assigned.
