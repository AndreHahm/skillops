---
description: Skill Lifecycle
---

# Skill Lifecycle

## Purpose

The skill lifecycle defines how a skill moves from early drafting to review, stable use, deprecation, and archival. It gives maintainers and agents shared language for interpreting a skill manifest's `status` value.

## Phase 1 Lifecycle States

The allowed Phase 1 lifecycle states are:

- `draft`
- `candidate`
- `reviewed`
- `stable`
- `deprecated`
- `archived`

Phase 1 skills are expected to be `draft` unless explicitly promoted later through review.

## State Definitions

- `draft`: the skill exists and can be validated, but it is still being shaped.
- `candidate`: the skill is ready for focused review and trial use.
- `reviewed`: the skill has passed validation and human review for its intended scope.
- `stable`: the skill is considered reliable for routine use and should not be changed casually.
- `deprecated`: the skill should not be selected for new work, but it remains traceable.
- `archived`: the skill is retained for history and should not be active in normal workflows.

## Promotion Rules

Promotion requires validation and review. A maintainer should check the manifest, `SKILL.md`, registry entry, risk tier, ownership, and relevant tests before changing status.

Do not promote a skill directly to `stable` without clear evidence that it is mature, maintained, and safe for routine use.

## Deprecation Rules

Deprecated skills should remain traceable. Keep enough manifest and registry information for maintainers to understand what the skill was, why it changed status, and what should replace it when applicable.

Archived skills should not appear as active recommendations.

## Review Expectations

Reviewers should confirm that the skill has a valid manifest, clear owner, practical instructions, accurate tool permissions, appropriate risk tier, and no claims about future functionality as if it were current behavior.
