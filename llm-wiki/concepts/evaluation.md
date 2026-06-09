# Evaluation

Evaluation in SkillOps means reviewing skill behavior against representative scenarios in addition to validating files and metadata.

Phase 2 currently implements the evaluation foundation and a local-first Promptfoo configuration layer, with full runner integration planned later:

- golden set schema
- initial golden set files
- eval suite schema
- eval suite registry
- Promptfoo configs for deterministic local smoke checks while broader execution is planned later
- consistency tests

A golden set describes inputs and expected response traits for one skill. An eval suite registry entry connects a skill to its golden set and Promptfoo config while keeping DeepEval fields empty until later work.

Promptfoo configs are implemented for local deterministic smoke usage, while broader Promptfoo execution remains planned later. DeepEval execution, production observability, dependency graph behavior, marketplace behavior, and self-improvement automation are planned later or out of scope for this package.
