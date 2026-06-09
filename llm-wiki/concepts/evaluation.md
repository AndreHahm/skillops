# Evaluation

Evaluation in SkillOps means reviewing skill behavior against representative scenarios in addition to validating files and metadata. It is a quality discipline, not only a runner or score.

The Phase 2 evaluation model is layered:

1. Static validation checks schemas, registries, manifests, and health inputs.
2. Golden Sets act as canonical scenario assets for behavioral regression protection.
3. Promptfoo configs provide deterministic scenario-level assertions for local-first review.
4. DeepEval tests provide Python/pytest-style evaluation skeletons and future metric-oriented checks.
5. Review gates inspect overfitting, scope creep, safety, and documentation accuracy.
6. A CI smoke evaluation gate is planned for a later Phase 2 package and is not implemented by this package.

Behavioral regression is a skill quality problem: a skill can remain schema-valid while becoming less safe, less scoped, or less useful. Golden Sets reduce that risk by making expected behavior explicit and version-controlled.

Deterministic checks are useful because they are stable, reviewable, and do not require external model calls. They are not complete proof of quality, so review gates remain required.

LLM-as-judge can be useful in later evaluation work, but it should not be treated as absolute truth. Judge results may vary by model, prompt, provider, credentials, and context; they need deterministic anchors, flake management, and human review.

Future production observability is planned for Phase 4 and is not implemented in Phase 2. Future marketplace behavior is planned for Phase 5 and is not implemented in Phase 2. Future self-improvement automation and automatic skill patching are planned for Phase 6 and are not implemented in Phase 2. Langfuse integration, Phoenix integration, production traces, dependency graph analysis, and mandatory full/live CI evaluation gates are not active behavior in this package; only the deterministic smoke gate is active.

## Phase 2 Package 6 CI Smoke Gate

Phase 2 Package 6 adds a deterministic evaluation smoke gate. The local and CI command is:

```bash
uv run skillops eval --smoke
```

The smoke gate checks Golden Sets, eval suite registry alignment, Promptfoo config references, DeepEval test references, documentation guardrails, and safety scans. It does not perform live LLM evaluation, mandatory LLM-as-judge scoring, Promptfoo cloud upload, DeepEval cloud login, Langfuse or Phoenix tracing, production observability, marketplace behavior, or self-improvement automation. Production observability is planned for Phase 4, marketplace behavior is planned for Phase 5, and self-improvement automation is planned for Phase 6.
