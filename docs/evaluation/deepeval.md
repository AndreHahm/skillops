# DeepEval Integration

SkillOps uses DeepEval in Phase 2 as a developer-facing, local evaluation skeleton layer for the five core skills. DeepEval tests provide Python/pytest-style evaluation skeletons and future metric-oriented checks without requiring live model credentials by default.

## Implemented Now

- DeepEval test skeletons under `evals/deepeval/`
- Golden Set loading helpers in `evals/deepeval/helpers.py`
- guarded local DeepEval examples that require `SKILLOPS_RUN_DEEPEVAL=1`
- registry references from each eval suite to its DeepEval test file
- structural tests for file presence, registry references, safety boundaries, and Golden Set alignment

## Implemented Earlier

- Golden Sets in `evals/golden/*.yaml`
- Promptfoo configuration in `evals/promptfoo/`

## Planned Later

- CI evaluation gate in a later Phase 2 package; not implemented by this package
- richer LLM-as-judge scoring; not mandatory in this package
- production observability in Phase 4; not implemented in Phase 2
- Langfuse integration and Phoenix integration in later observability work; not implemented in Phase 2
- marketplace behavior in Phase 5; not implemented in Phase 2
- self-improvement automation and automatic skill patching in Phase 6; not implemented in Phase 2

The planned items above are not part of the current runtime behavior.

## Relationship to Golden Sets

In Skill-TDD, the eval case comes first and Golden Sets are the canonical scenario assets. Each DeepEval skeleton loads the corresponding Golden Set, checks that required scenario categories are present, and derives deterministic `contains`, `not_contains`, and `must_reference` assertions from the Golden Set case data.

This keeps expected behavior reviewable even when DeepEval is not installed.

## Relationship to Promptfoo

Promptfoo remains the declarative smoke/regression configuration layer. DeepEval complements it with Python and pytest-style evaluation skeletons where maintainers can later connect captured system outputs, non-LLM metrics, or optional judge metrics.

Both layers reference the same Golden Sets and are linked from `registry/eval-suites.yaml`.

## Local Usage

Run the safe default skeletons:

```bash
uv run pytest evals/deepeval
```

Optionally run DeepEval object-construction smoke checks after installing DeepEval locally:

```bash
SKILLOPS_RUN_DEEPEVAL=1 uv run pytest evals/deepeval
```

The optional command is not required for baseline repository validation. Normal `uv run pytest` must pass without DeepEval credentials or network access.

## Why Execution Is Guarded

Many DeepEval metrics can use model providers or LLM-as-judge behavior. Those checks can be valuable, but they may require credentials, network access, and careful flake management. Package 4 therefore keeps LLM-as-judge scoring optional or later work rather than a mandatory baseline test.

## Boundaries

This package does not add a `skillops eval` command, online evaluation, trace ingestion, external telemetry, marketplace promotion, automatic patching, release automation, deployment automation, or a web UI.
