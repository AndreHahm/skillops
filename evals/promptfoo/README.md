# Promptfoo Configuration

This directory contains the Phase 2 Package 3 Promptfoo configuration layer for SkillOps. The configuration is local-first and deterministic: it uses Promptfoo-compatible YAML, local echo-style smoke prompts, and assertions mapped from the Golden Sets. It does not require model credentials by default.

## Implemented Now

- Root Promptfoo smoke config: `evals/promptfoo/promptfooconfig.yaml`
- Skill-specific Promptfoo configs under `evals/promptfoo/skills/`
- Deterministic `contains` and `not-contains` assertions derived from `evals/golden/*.yaml`
- Eval suite registry references from `registry/eval-suites.yaml`
- Structural tests that validate config presence, YAML shape, Golden Set alignment, references, and safety boundaries

## Planned Later

- DeepEval integration
- CI evaluation gate
- Richer judge-based scoring
- Production observability
- Langfuse/Phoenix tracing

## Config Layout

The root config is a lightweight smoke entry point that verifies Promptfoo can load a local SkillOps config and references each skill-specific config path. The skill-specific files are the scenario configs reviewers should inspect or run when checking a core skill:

- `skills/python-project-setup.promptfooconfig.yaml`
- `skills/skill-manifest-authoring.promptfooconfig.yaml`
- `skills/skill-registry-maintenance.promptfooconfig.yaml`
- `skills/skill-health-review.promptfooconfig.yaml`
- `skills/documentation-maintenance.promptfooconfig.yaml`

## Local Usage

If Promptfoo is available locally, run the root smoke config:

```bash
npx promptfoo@latest eval -c evals/promptfoo/promptfooconfig.yaml
```

Run a skill-specific config when reviewing one skill:

```bash
npx promptfoo@latest eval -c evals/promptfoo/skills/skill-manifest-authoring.promptfooconfig.yaml
```

These commands are documented as local smoke checks only. They are not a mandatory CI gate in this package.

## Relationship to Golden Sets

Golden Sets remain the canonical scenario assets. Promptfoo configs are an execution/configuration layer that mirrors Golden Set case IDs, categories, expected `contains` signals, and expected `not_contains` guards. When a Golden Set changes, update the matching Promptfoo test metadata and deterministic assertions in the corresponding skill config.

## Assertion Strategy

This package prefers deterministic assertions because they are stable in local development and do not require external model credentials. LLM-as-judge checks are not the default here because they introduce model variance, external service dependencies, and credential handling that belong in a later evaluation package.

