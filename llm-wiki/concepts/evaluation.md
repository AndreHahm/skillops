# Evaluation

Evaluation in SkillOps means reviewing skill behavior against representative scenarios in addition to validating files and metadata.

Phase 2 Package 1 implements the evaluation foundation only:

- golden set schema
- initial golden set files
- eval suite schema
- eval suite registry
- consistency tests

A golden set describes inputs and expected response traits for one skill. An eval suite registry entry connects a skill to its golden set and records future execution integration fields.

Promptfoo execution and DeepEval execution are planned for later Phase 2 packages and are not implemented by this foundation. Production observability, dependency graph behavior, marketplace behavior, and self-improvement automation are also planned later or out of scope for this package.
