# SkillOps Evaluation Foundation

This directory contains the Phase 2 evaluation assets for SkillOps. It stores canonical Golden Sets, local runner configuration, and guarded test skeletons.

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

- mandatory CI smoke evaluation gate
- richer judge-based scoring
- production observability, dependency graph behavior, marketplace behavior, and self-improvement candidate generation

The files in this directory are not runtime outputs. They are reviewed scenario assets, local evaluation configuration, and guarded pytest skeletons.
