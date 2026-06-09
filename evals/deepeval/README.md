# DeepEval Evaluation Skeletons

This directory contains the SkillOps Phase 2 Package 4 DeepEval integration layer. It is intentionally local-first and pytest-compatible: normal repository tests do not require DeepEval, model credentials, cloud login, or external network access.

## Implemented Now

- `helpers.py` loads canonical Golden Sets and turns cases into deterministic Python checks.
- One guarded pytest skeleton exists for each Phase 1 core skill.
- Optional DeepEval examples construct `LLMTestCase` objects only when explicitly enabled.
- `registry/eval-suites.yaml` links each core skill eval suite to its DeepEval test file.
- Structural repository tests verify file presence, registry references, guards, safety boundaries, and Golden Set alignment.

## Implemented Earlier

- Golden Sets in `evals/golden/*.yaml`
- Promptfoo configuration in `evals/promptfoo/`

## Planned Later

- CI evaluation gate
- richer LLM-as-judge scoring
- production observability
- Langfuse/Phoenix tracing
- self-improvement candidate generation

Those planned items are not active behavior in this package.

## File Map

- `helpers.py`: evaluation glue for loading Golden Sets and building deterministic checks.
- `conftest.py`: local pytest path setup for this directory.
- `test_python_project_setup.py`: skeleton for `python-project-setup`.
- `test_skill_manifest_authoring.py`: skeleton for `skill-manifest-authoring`.
- `test_skill_registry_maintenance.py`: skeleton for `skill-registry-maintenance`.
- `test_skill_health_review.py`: skeleton for `skill-health-review`.
- `test_documentation_maintenance.py`: skeleton for `documentation-maintenance`.

## Running Local Checks

Run the default structural DeepEval skeletons without live model calls:

```bash
uv run pytest evals/deepeval
```

Run optional DeepEval construction smoke checks only after installing DeepEval locally:

```bash
SKILLOPS_RUN_DEEPEVAL=1 uv run pytest evals/deepeval
```

The optional mode still uses deterministic placeholder outputs. It is a construction smoke test for DeepEval test-case objects, not a live model evaluation.

## Guardrails

- DeepEval imports stay inside guarded tests.
- `SKILLOPS_RUN_DEEPEVAL=1` is required before optional DeepEval code runs.
- LLM-as-judge metrics are optional later work and are not blocking baseline CI.
- Golden Sets remain the canonical scenario source.
- No API keys, local absolute user paths, external telemetry, or cloud login flows belong in these files.
