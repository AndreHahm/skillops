# Evaluation Foundation Overview

SkillOps Phase 2 establishes structured, local-first evaluation assets for skills. The model is layered: validate files, define canonical scenarios, map deterministic assertions, keep Python/pytest-style skeletons, use review gates, and run a deterministic CI smoke gate for asset alignment.

## Phase 2 Evaluation Layers

| Layer | Status | Notes |
| --- | --- | --- |
| Static validation | Implemented in Phase 1 | Existing schema, registry, CLI validation, and health checks. |
| Golden Scenario Tests | Implemented in Phase 2 | Golden Sets are canonical scenario assets for the five Phase 1 core skills. |
| Promptfoo configuration | Implemented in Phase 2 | Promptfoo configs provide deterministic scenario-level assertions for local-first review. |
| DeepEval test skeletons | Implemented in Phase 2 | DeepEval tests provide Python/pytest-style evaluation skeletons and future metric-oriented checks. |
| Review Gate | Documented in Phase 2 Package 5 | Reviewers inspect coverage, overfitting, scope creep, unsafe tool permission expansion, and documentation accuracy. |
| CI smoke gate | Available in Phase 2 Package 6 | Runs `skillops eval --smoke` for deterministic asset validation without live model calls, credentials, or network requirements. |
| Production observability | Planned for Phase 4 | Not implemented in Phase 2; production traces, Langfuse integration, and Phoenix integration are not active behavior. |
| Marketplace behavior | Planned for Phase 5 | Not implemented in Phase 2. |
| Self-improvement automation | Planned for Phase 6 | Not implemented in Phase 2; automatic skill patching is not active behavior. |

## Skill-TDD Flow

SkillOps uses Skill-TDD for skill changes:

```text
eval case first
  -> skill update
  -> local validation
  -> scenario eval
  -> review
  -> regression protection
```

See [Skill-TDD](skill-tdd.md) for the contributor workflow and [Review Gates](review-gates.md) for review criteria.

## How the Assets Work Together

- [Golden Sets](golden-sets.md) capture canonical scenarios and expected response traits.
- [Promptfoo configs](promptfoo.md) map those scenarios into deterministic config-level assertions.
- [DeepEval skeletons](deepeval.md) load Golden Sets from Python tests and keep optional metric-oriented checks guarded.
- `registry/eval-suites.yaml` links each core skill to its Golden Set, Promptfoo config, and DeepEval test file.
- `evals/README.md` describes the evaluation asset directory and links to runner-specific READMEs.
- [Evaluation CI Smoke Gate](ci-gate.md) documents `skillops eval --smoke` for local and CI usage.

Repository tests and the evaluation smoke gate remain structural and offline by default. They verify schemas, references, deterministic assertion alignment, documentation claims, and safety boundaries. They do not require external services, cloud login, production telemetry, or live model scoring.

## Boundaries

This package adds only a narrow `skillops eval --smoke` command and CI smoke step. It does not add full evaluation, production observability, online evaluation, trace ingestion, dependency graph analysis, marketplace behavior, self-improvement automation, automatic skill patching, release automation, deployment automation, database support, scheduled workflows, or a web UI. Full/live evaluation is not implemented by this package.
