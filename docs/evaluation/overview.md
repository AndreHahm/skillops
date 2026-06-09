# Evaluation Foundation Overview

SkillOps Phase 2 establishes the evaluation foundation for skills. The current foundation makes skill behavior reviewable through schemas, expanded Golden Sets, an eval suite registry, and local-first Promptfoo configuration files.

Implemented in this package:

- evaluation directory structure under `evals/`
- `schemas/golden-set.schema.json`
- expanded scenario-based Golden Sets for the five Phase 1 core skills
- `schemas/eval-suite.schema.json`
- `registry/eval-suites.yaml`
- Promptfoo configuration files for local deterministic smoke checks
- deterministic consistency tests for schemas, Golden Set completeness, required categories, Promptfoo config references, safety drift, and documentation claims

Planned for later Phase 2 packages, and not implemented here:

- DeepEval tests and execution
- mandatory CI smoke evaluation gate
- richer Promptfoo and DeepEval-backed Skill-TDD reporting
- production observability, dependency graph behavior, marketplace behavior, release automation, deployment automation, and self-improvement automation

The strategic shift is from file-only validity toward behavior-aware validation. This package prepares the contracts for that shift and adds Promptfoo configs that can be run locally when Promptfoo is installed, while repository tests remain structural and offline.
