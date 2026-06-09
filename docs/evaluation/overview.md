# Evaluation Foundation Overview

SkillOps Phase 2 Package 1 establishes the first evaluation foundation for skills. The foundation is metadata-only: it makes skill behavior reviewable through schemas, golden sets, and an eval suite registry.

Implemented in this package:

- evaluation directory structure under `evals/`
- `schemas/golden-set.schema.json`
- initial golden sets for the five Phase 1 core skills
- `schemas/eval-suite.schema.json`
- `registry/eval-suites.yaml`
- deterministic consistency tests for schemas, golden sets, registry references, and documentation claims

Planned for later Phase 2 packages, and not implemented here:

- Promptfoo configuration and execution
- DeepEval tests and execution
- CI smoke evaluation command
- richer Skill-TDD workflow
- production observability, dependency graph behavior, marketplace behavior, release automation, deployment automation, and self-improvement automation

The strategic shift is from file-only validity toward behavior-aware validation. This package prepares the contracts for that shift without running any evaluation engine.
