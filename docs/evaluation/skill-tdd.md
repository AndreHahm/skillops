# Skill-TDD

Skill-TDD is the practice of designing representative skill behavior scenarios before changing a skill. Phase 2 currently provides Golden Sets, local-first Promptfoo configuration, and guarded DeepEval skeletons.

Implemented now:

- Golden Sets for the five Phase 1 core skills
- schemas that make Golden Sets and eval suites reviewable
- Promptfoo configs that map Golden Set expectations to deterministic assertions
- DeepEval pytest skeletons that load Golden Sets and run deterministic local checks
- tests that check consistency between skill IDs, Golden Set files, Promptfoo configs, DeepEval files, and eval suite entries

How to use these assets during skill work:

1. Review or update the relevant Golden Set first.
2. Keep categories such as `happy_path`, `edge_case`, `invalid_input`, `scope_creep`, and `safety_sensitive` explicit.
3. Keep Promptfoo configs aligned with deterministic Golden Set assertions.
4. Keep DeepEval skeletons aligned with the Golden Set path and skill ID.
5. Run `uv run pytest` and `uv run skillops validate` before reporting completion.

Optional local DeepEval construction checks can be run with:

```bash
SKILLOPS_RUN_DEEPEVAL=1 uv run pytest evals/deepeval
```

LLM-as-judge scoring, mandatory CI evaluation gates, and richer automated Skill-TDD reporting are planned later. Reviewers should treat Golden Sets as canonical acceptance scenarios, Promptfoo configs as local smoke assets, and DeepEval files as guarded Python skeletons rather than proof of production behavior.
