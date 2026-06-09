# Skill-TDD

Skill-TDD is the default SkillOps workflow for changing skills: start with the evaluation case, then update the skill, validate locally, run scenario-oriented checks, review the change, and preserve regression protection.

```text
eval case first
  -> skill update
  -> local validation
  -> scenario eval
  -> review
  -> regression protection
```

SkillOps uses Skill-TDD because skill repositories can regress quietly. A small wording change in `SKILL.md` can weaken safety guidance, expand tool permissions, or remove a behavior that another agent relied on. Evaluation cases make the intended behavior visible before the skill text changes.

## Current Phase 2 Status

Implemented Phase 2 assets that support Skill-TDD:

- Golden Sets are canonical scenario assets for the five Phase 1 core skills.
- Promptfoo configs provide deterministic scenario-level assertions derived from Golden Sets.
- DeepEval tests provide Python/pytest-style evaluation skeletons and future metric-oriented checks.
- Registry references connect each core skill to its Golden Set, Promptfoo config, and DeepEval test file.
- Repository tests check schema validity, registry consistency, documentation presence, and overclaiming boundaries.
- The deterministic CI smoke gate runs `skillops eval --smoke` to verify evaluation asset presence, references, and structural safety without live model calls.

Not implemented by this package:

- Production observability; planned for Phase 4, not implemented in Phase 2.
- Marketplace behavior; planned for Phase 5, not implemented in Phase 2.
- Self-improvement automation and automatic skill patching; planned for Phase 6, not implemented in Phase 2.
- Production traces, Langfuse integration, Phoenix integration, dependency graph analysis, release automation, deployment automation, or a web UI.

## When to Add or Change Evaluation Cases

Add or update an evaluation case before changing a skill when the change affects:

- agent instructions in `SKILL.md`;
- skill metadata in `skill.yaml`;
- expected files, commands, schemas, or registries the skill should reference;
- safety behavior, tool permissions, or least-privilege guidance;
- scope boundaries, refusals, or handoff instructions;
- user-facing documentation or contributor guidance;
- regression risk for a previous bug or review finding.

A skill change should usually include:

1. Updated `SKILL.md`.
2. Updated `skill.yaml` if metadata changes.
3. Updated Golden Set cases when behavior changes.
4. Updated Promptfoo cases when deterministic scenario assertions change.
5. Updated DeepEval tests when structured Python assertions or metric-oriented evaluation changes.
6. Run `uv run skillops eval --smoke` when evaluation assets or evaluation docs change.
7. Updated documentation if user-facing behavior changes.
8. Review notes explaining why the change is safe and within scope.

## Writing the Evaluation Case First

Use the Golden Set as the starting point because it is the canonical scenario asset. A good case states the requested behavior, the scenario category, required response traits, forbidden claims or unsafe actions, and the files or concepts the agent should reference.

Prefer cases that are:

- representative of real maintainer requests;
- deterministic enough to review without live model scoring;
- specific about expected safety or scope behavior;
- broad enough to avoid overfitting to one exact sentence;
- connected to a known risk, feature request, or regression.

Do not add a case that merely blesses the exact text you plan to write. The case should test the behavior that matters, not force a single prose answer.

## How the Layers Fit Together

1. **Static validation** checks schemas, registries, manifests, links, and health-report inputs.
2. **Golden Sets** define canonical behavior scenarios and expected traits.
3. **Promptfoo configuration** maps Golden Set scenarios into deterministic config-level assertions such as `contains` and `not-contains`.
4. **DeepEval skeletons** map Golden Set scenarios into Python/pytest-style checks and leave optional judge or metric work guarded for later.
5. **Review gates** ask humans or reviewing agents to inspect coverage, safety, scope, and overfitting.
6. **Later CI smoke gate** is planned for a later Phase 2 package and is not implemented by this package.

## Local Validation and Scenario Evaluation

Run the baseline local checks before reporting completion:

```bash
uv run pytest
uv run ruff check .
uv run skillops validate
uv run skillops health --no-write
```

For evaluation-specific work, inspect or run the relevant local assets when available:

```bash
uv run pytest tests/test_golden_sets.py
uv run pytest tests/test_promptfoo_integration.py
uv run pytest tests/test_deepeval_integration.py
uv run pytest evals/deepeval
```

Promptfoo execution is local-first configuration work, not a required CI gate in this package. DeepEval live or judge-style scoring is optional and guarded; baseline repository validation must not require credentials, network calls, or cloud login.

## Review and Regression Protection

The review gate protects against:

- **overfitting**, where a skill is tuned to pass a narrow case while failing the broader behavior;
- **scope creep**, where a skill starts performing work outside its manifest, risk tier, or operational boundary;
- **unsafe tool permission expansion**, where instructions encourage broad shell access, broad filesystem access, secrets exposure, or destructive operations;
- **documentation drift**, where docs describe later systems as already implemented;
- **regression debt**, where a fixed behavior is not captured in Golden Sets, Promptfoo configs, or DeepEval skeletons.

Regression protection means the accepted scenario remains in version-controlled evaluation assets so future reviewers can see why the behavior exists.

## Handling Documentation and Metadata Changes

Update documentation when a skill change alters user-facing behavior, contributor workflow, safety guidance, or review expectations. Keep `docs/` practical and user-facing, and keep `llm-wiki/` focused on durable concepts.

Update `skill.yaml` only when metadata changes, such as scope, owner, status, risk, inputs, outputs, or tool expectations. Then run schema and registry validation.

## Example: Broad Shell Access Warning

Change request: improve `skill-manifest-authoring` so it warns against broad shell access.

Skill-TDD flow:

1. Add a safety-sensitive Golden Set case under `evals/golden/skill-manifest-authoring.yaml` that expects least-privilege tool guidance and rejects broad shell access.
2. Update the matching Promptfoo assertions in `evals/promptfoo/skills/skill-manifest-authoring.promptfooconfig.yaml` with deterministic phrases from the Golden Set expectations.
3. Add or adjust DeepEval structural checks if the Golden Set categories or expected fields require new Python assertions.
4. Update `skills/skill-manifest-authoring/SKILL.md` with practical least-privilege guidance.
5. Run validation and evaluation checks.
6. Review for overfitting, scope creep, unsafe tool permission expansion, and regression protection.

## What Not to Do

Do not use Skill-TDD work to add new runtime evaluation platforms, full benchmark CI eval gates, production observability, dependency graph generation, marketplace behavior, self-improvement automation, automatic skill patching, release automation, deployment automation, or web UI behavior.

Do not claim implemented status for Langfuse, Phoenix, production traces, marketplace promotion, automatic patching, or mandatory CI evaluation gates. Those capabilities are later-phase work unless a future package explicitly implements them.


## Evaluation Smoke Gate in Skill-TDD

Use the smoke gate as regression protection after the eval case first and skill update steps:

```bash
uv run skillops eval --smoke
```

The command checks Golden Sets, the eval suite registry, Promptfoo config references, DeepEval test references, documentation guardrails, and safety scans. It does not require real credentials, network calls, live LLM calls, Promptfoo cloud usage, DeepEval cloud login, or `SKILLOPS_RUN_DEEPEVAL=1`. A pass means the evaluation assets are structurally aligned for CI; it does not mean full benchmark evaluation or live model scoring has run.
