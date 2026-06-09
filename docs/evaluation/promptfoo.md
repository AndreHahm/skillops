# Promptfoo Evaluation Configs

SkillOps uses Promptfoo in Phase 2 Package 3 as a local-first configuration and smoke-evaluation layer for the five core skills. The current integration checks configuration mechanics and Golden Set alignment with deterministic assertions; it does not add a CI evaluation gate or external model calls.

## Implemented Now

- Promptfoo configuration files
- Skill-specific Promptfoo scenario configs
- Deterministic assertion mapping from Golden Sets
- Registry references to Promptfoo configs
- Structural tests for Promptfoo integration

## Planned Later

- CI evaluation gate
- Richer judge-based scoring
- Production observability
- Langfuse/Phoenix tracing

## File Locations

- Root smoke config: `evals/promptfoo/promptfooconfig.yaml`
- Skill configs: `evals/promptfoo/skills/*.promptfooconfig.yaml`
- Canonical scenarios: `evals/golden/*.yaml`
- Eval suite registry: `registry/eval-suites.yaml`

The root config is intentionally small. It is a smoke entry point and points reviewers toward the skill-specific configs. The skill-specific configs contain one Promptfoo test per mapped Golden Set case.

## How Promptfoo Relates to Golden Sets

Golden Sets are the source of truth for behavioral scenarios. Each Promptfoo test records metadata for the source `skill_id`, `golden_case_id`, category, and Golden Set path. The Promptfoo assertions mirror Golden Set `expected.contains` values with `contains` checks and Golden Set `expected.not_contains` values with `not-contains` checks.

This separation keeps scenarios reviewable independent of any runner while still making the runner configuration inspectable and testable.

## Local Smoke Usage

Install or invoke Promptfoo outside the repository dependency set, then run:

```bash
npx promptfoo@latest eval -c evals/promptfoo/promptfooconfig.yaml
```

For one skill, run:

```bash
npx promptfoo@latest eval -c evals/promptfoo/skills/python-project-setup.promptfooconfig.yaml
```

The repository tests validate the YAML structure and references without requiring Promptfoo installation, network calls, model credentials, or cloud login.

## Updating Tests When Golden Sets Change

When a Golden Set case is added or changed:

1. Keep the Golden Set as the canonical scenario source.
2. Add or update the matching Promptfoo test in the skill-specific config.
3. Copy the Golden Set case ID into `metadata.golden_case_id`.
4. Copy the Golden Set category into `metadata.category`.
5. Map `expected.contains` entries to Promptfoo `contains` assertions.
6. Map `expected.not_contains` entries to Promptfoo `not-contains` assertions where applicable.
7. Run `uv run pytest` and `uv run skillops validate`.

Avoid brittle full-output matching. Prefer short, deterministic phrases, commands, schema fields, and policy concepts.

## Boundaries

This Promptfoo package does not implement DeepEval runtime scoring, production observability, marketplace behavior, dependency graph behavior, release automation, deployment automation, self-improvement automation, or a full `skillops eval` platform. Red-team seed files may inform later work, but this package does not add Promptfoo red-team execution.
