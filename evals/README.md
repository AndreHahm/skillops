# SkillOps Evaluation Foundation

This directory contains the Phase 2 evaluation assets for SkillOps. It stores canonical Golden Sets, local Promptfoo configuration, and guarded DeepEval test skeletons used by the Skill-TDD workflow.

Implemented now:

- evaluation directory structure
- Golden Set schema
- Golden Sets for the five Phase 1 core skills
- eval suite schema
- eval suite registry
- Promptfoo configuration for local deterministic smoke checks
- DeepEval pytest skeletons and Golden Set helper utilities
- consistency tests
- deterministic CI smoke gate through `skillops eval --smoke`

Planned for later Phase 2 packages, and not active behavior here:

- richer judge-based scoring; not mandatory in this package
- production observability in Phase 4; not implemented in Phase 2
- dependency graph behavior; not implemented in Phase 2
- marketplace behavior in Phase 5; not implemented in Phase 2
- self-improvement automation and automatic skill patching in Phase 6; not implemented in Phase 2

The files in this directory are not runtime outputs. They are reviewed scenario assets, local evaluation configuration, and guarded pytest skeletons.


Skill-TDD flow: eval case first -> skill update -> local validation -> scenario eval -> review -> regression protection. See `../docs/evaluation/skill-tdd.md` and `../docs/evaluation/review-gates.md` for the contributor workflow and review checklist.


## CI Smoke Gate

Run the deterministic evaluation smoke gate locally with:

```bash
uv run skillops eval --smoke
```

The gate validates Golden Sets, `registry/eval-suites.yaml`, Promptfoo config references, DeepEval test references, documentation guardrails, and basic safety boundaries. It does not execute live model calls, Promptfoo cloud upload, DeepEval cloud login, production observability, marketplace behavior, or self-improvement automation. Production observability is planned for Phase 4, marketplace behavior is planned for Phase 5, and self-improvement automation is planned for Phase 6.
