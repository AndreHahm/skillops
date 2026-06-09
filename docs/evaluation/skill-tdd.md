# Skill-TDD

Skill-TDD is the planned practice of designing representative skill behavior scenarios before changing a skill. Phase 2 now provides Golden Sets plus local-first Promptfoo configuration for deterministic smoke checks.

Implemented now:

- golden sets for the five Phase 1 core skills
- schemas that make golden sets and eval suites reviewable
- Promptfoo configs that map Golden Set expectations to deterministic assertions
- tests that check consistency between skill IDs, golden set files, Promptfoo configs, and eval suite entries

Planned later, and not implemented here:

- DeepEval execution
- mandatory CI smoke evaluation gate
- richer judge-based pass/fail reporting for skill behavior

Reviewers should treat Golden Sets as canonical acceptance scenarios and Promptfoo configs as local smoke assets, not as proof of production behavior.
