# Skill-TDD

Skill-TDD is the planned practice of designing representative skill behavior scenarios before changing a skill. Phase 2 Package 1 only provides the metadata foundation for that practice.

Implemented now:

- initial golden sets for the five Phase 1 core skills
- schemas that make golden sets and eval suites reviewable
- tests that check consistency between skill IDs, golden set files, and eval suite entries

Planned later, and not implemented here:

- Promptfoo execution
- DeepEval execution
- CI smoke evaluation command
- richer pass/fail reporting for skill behavior

Until those later packages exist, reviewers should treat golden sets as static acceptance scenarios, not as executed evaluation results.
