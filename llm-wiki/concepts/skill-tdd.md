# Skill-TDD

Skill-TDD is the SkillOps concept of changing agent skills test-first: define the behavioral scenario before changing the skill instructions, then use validation, scenario evaluation assets, review, and regression protection to keep the behavior stable.

The durable workflow is:

```text
eval case first
  -> skill update
  -> local validation
  -> scenario eval
  -> review
  -> regression protection
```

Golden Sets prevent evaluation debt because they preserve the behavioral reason for a skill change as canonical scenario assets. Without Golden Sets, maintainers may remember that a regression was fixed but lose the concrete scenario that future agents should continue to satisfy.

Promptfoo configs provide deterministic scenario-level assertions for local-first review. DeepEval tests provide Python/pytest-style evaluation skeletons and future metric-oriented checks. Both layers should derive from Golden Sets rather than becoming separate sources of truth.

Review gates are necessary because deterministic checks can be gamed and LLM-as-judge should not be treated as absolute truth. A reviewer must still inspect overfitting, scope creep, unsafe tool permission expansion, documentation drift, and whether the change remains useful for real agents.

Future observability and future self-improvement automation must be review-gated. Production observability is planned for Phase 4 and is not implemented in Phase 2. Marketplace behavior is planned for Phase 5 and is not implemented in Phase 2. Self-improvement automation and automatic skill patching are planned for Phase 6 and are not implemented in Phase 2. Langfuse integration, Phoenix integration, production traces, dependency graph analysis, and mandatory CI evaluation gates are not active behavior in this package.
