# Skill-TDD

Skill-TDD is the SkillOps workflow of writing or updating representative skill behavior scenarios before changing a skill implementation.

The current Phase 2 assets support Skill-TDD through Golden Sets, planned-safe Promptfoo smoke configuration, and planned-safe DeepEval skeletons before future evaluation gates are introduced.

Current local practice is to define Golden Set cases for expected skill behavior, keep case categories explicit, connect each core skill to one draft eval suite, map Golden Set expectations to deterministic Promptfoo assertions with broader execution planned later, load Golden Sets from DeepEval pytest skeletons with judge scoring planned later, and validate that files and references are consistent.

DeepEval-dependent imports are guarded by `SKILLOPS_RUN_DEEPEVAL=1`, and baseline repository tests do not require model credentials. Mandatory CI smoke evaluation gates, richer automated Skill-TDD reporting, and LLM-as-judge score thresholds are planned for later Phase 2 packages.
