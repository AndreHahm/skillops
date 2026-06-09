# Evaluation

Evaluation in SkillOps means reviewing skill behavior against representative scenarios in addition to validating files and metadata.

Phase 2 now includes Golden Set schema, Golden Set files for the five Phase 1 core skills, eval suite schema, eval suite registry, consistency tests, planned-safe Promptfoo configs for deterministic local smoke checks, and planned-safe DeepEval pytest skeletons for guarded local checks.

A Golden Set describes inputs and expected response traits for one skill. An eval suite registry entry connects a skill to its Golden Set, planned-safe Promptfoo config, and planned-safe DeepEval test file.

Promptfoo is the local declarative smoke/regression layer introduced before broader future evaluation gates. DeepEval is the local Python and pytest-style skeleton layer introduced before future judge-based scoring. Both use Golden Sets as the source of truth and avoid external model calls in baseline repository tests.

Later packages may add CI evaluation gates, richer LLM-as-judge scoring, production observability, Langfuse/Phoenix tracing, and self-improvement candidate generation. Those are not active behavior in this package.
