# Evaluation Foundation Overview

SkillOps Phase 2 establishes structured evaluation assets for skills. The current foundation makes skill behavior reviewable through schemas, expanded Golden Sets, an eval suite registry, local-first Promptfoo configuration files, and guarded DeepEval pytest skeletons.

Implemented now:

- evaluation directory structure under `evals/`
- `schemas/golden-set.schema.json`
- expanded scenario-based Golden Sets for the five Phase 1 core skills
- `schemas/eval-suite.schema.json`
- `registry/eval-suites.yaml`
- Promptfoo configuration files for local deterministic smoke checks
- DeepEval test skeletons and helper utilities for local pytest-style checks
- deterministic consistency tests for schemas, Golden Set completeness, required categories, Promptfoo config references, DeepEval references, safety drift, and documentation claims

Implemented earlier:

- Golden Sets
- Promptfoo configuration

Planned later, and not active behavior here:

- mandatory CI evaluation gate
- richer Promptfoo and DeepEval-backed Skill-TDD reporting
- LLM-as-judge scoring that is explicitly credentialed and flake-managed
- production observability, Langfuse/Phoenix tracing, dependency graph behavior, marketplace behavior, release automation, deployment automation, and self-improvement candidate generation

The strategic shift is from file-only validity toward behavior-aware validation. Golden Sets remain the canonical scenario source. Promptfoo provides declarative smoke/regression configuration, while DeepEval provides Python and pytest-style skeletons that can later receive captured system outputs. Repository tests remain structural and offline by default.
