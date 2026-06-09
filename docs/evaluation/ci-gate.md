# Evaluation CI Smoke Gate

The Evaluation CI Smoke Gate is the Phase 2 Package 6 check for evaluation assets. It is deterministic, local-first, and intended for pull-request confidence rather than full benchmark scoring.

Run it locally with:

```bash
uv run skillops eval --smoke
```

CI invokes the same command in `.github/workflows/ci.yml` after the Phase 1 registry validation step.

## What the Smoke Gate Checks

Available now:

- deterministic evaluation smoke gate through `skillops eval --smoke`
- CI step for evaluation asset validation
- Golden Set schema presence and JSON Schema validity
- Eval Suite schema presence and JSON Schema validity
- all Golden Sets under `evals/golden/` against the Golden Set schema
- `registry/eval-suites.yaml` against the Eval Suite schema
- one eval suite for each Phase 1 core skill
- eval suite references to existing Golden Sets
- Promptfoo config references and parseable Promptfoo YAML structure
- DeepEval test references and Python syntax
- guarded DeepEval runtime examples that do not run unless explicitly enabled
- evaluation documentation guardrails for future-phase overclaims
- obvious secret-like values, local absolute user paths, and stale project names in repository text files

## What the Smoke Gate Does Not Check

Not implemented in this package:

- live LLM evaluation
- mandatory LLM-as-judge scoring
- Promptfoo cloud upload
- DeepEval cloud login
- Langfuse or Phoenix tracing
- production observability; production observability is planned for Phase 4
- marketplace behavior; marketplace behavior is planned for Phase 5
- self-improvement automation or automatic skill patching; self-improvement automation is planned for Phase 6
- release automation, deployment automation, scheduled workflows, or generated report publishing

The smoke gate does not call model providers, does not require API keys, does not require network access, and does not require `SKILLOPS_RUN_DEEPEVAL=1`.

## Relationship to Golden Sets, Promptfoo, and DeepEval

Golden Sets remain the canonical scenario assets. Promptfoo configs provide deterministic scenario-level assertions that can be inspected structurally by the smoke gate. DeepEval files remain guarded Python/pytest-style evaluation skeletons; optional DeepEval construction checks are controlled by `SKILLOPS_RUN_DEEPEVAL=1` for local experiments only.

The CI smoke gate validates alignment among those assets. It intentionally stops short of full evaluation, live model scoring, judge-based quality scores, production traces, or online observability.

## Skill-TDD Usage

For Skill-TDD, run the smoke gate after adding or changing Golden Sets, Promptfoo configs, DeepEval skeletons, or evaluation docs:

```bash
uv run skillops eval --smoke
```

Use this with the usual local checks:

```bash
uv run skillops validate
uv run pytest
uv run ruff check .
```

A passing smoke gate means evaluation assets are present, parseable, schema-valid, linked, and safe for deterministic CI. It does not mean a skill has passed a full benchmark or live model evaluation.

## Optional Full Checks Later

Future packages may add explicit full-evaluation commands or reports. Those additions should stay opt-in, should document any provider or credential requirements, and should not replace this deterministic baseline gate.
