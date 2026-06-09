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

Planned for later Phase 2 packages, and not active behavior here:

- mandatory CI smoke evaluation gate in a later Phase 2 package; not implemented by this package
- richer judge-based scoring; not mandatory in this package
- production observability in Phase 4; not implemented in Phase 2
- dependency graph behavior; not implemented in Phase 2
- marketplace behavior in Phase 5; not implemented in Phase 2
- self-improvement automation and automatic skill patching in Phase 6; not implemented in Phase 2

The files in this directory are not runtime outputs. They are reviewed scenario assets, local evaluation configuration, and guarded pytest skeletons.


Skill-TDD flow: eval case first -> skill update -> local validation -> scenario eval -> review -> regression protection. See `../docs/evaluation/skill-tdd.md` and `../docs/evaluation/review-gates.md` for the contributor workflow and review checklist.
