# Evaluation Foundation Overview

SkillOps Phase 2 establishes the evaluation foundation for skills. The current foundation is metadata-only: it makes skill behavior reviewable through schemas, expanded Golden Sets, and an eval suite registry.

Implemented in this package:

- evaluation directory structure under `evals/`
- `schemas/golden-set.schema.json`
- expanded scenario-based Golden Sets for the five Phase 1 core skills
- `schemas/eval-suite.schema.json`
- `registry/eval-suites.yaml`
- deterministic consistency tests for schemas, Golden Set completeness, required categories, registry references, safety drift, and documentation claims

Planned for later Phase 2 packages, and not implemented here:

- Promptfoo configuration and execution
- DeepEval tests and execution
- CI smoke evaluation command
- Promptfoo and DeepEval-backed Skill-TDD execution
- production observability, dependency graph behavior, marketplace behavior, release automation, deployment automation, and self-improvement automation

The strategic shift is from file-only validity toward behavior-aware validation. This package prepares the contracts for that shift without running any evaluation engine.
