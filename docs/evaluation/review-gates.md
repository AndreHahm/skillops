# Evaluation Review Gates

Review gates are the human and agent review layer in Skill-TDD. They decide whether a skill change is ready after the eval case first, skill update, local validation, and scenario eval steps are complete.

Review gates are required because deterministic checks can confirm structure and key phrases, but they cannot fully prove intent, safety, scope discipline, or resistance to overfitting. In Phase 2, review gates are documented process gates backed by structural tests; this package implements only the deterministic CI smoke gate, not a full/live CI evaluation gate.

## What Reviewers Should Inspect

Reviewers should inspect:

- the changed `SKILL.md` instructions;
- `skill.yaml` metadata when scope, risk, ownership, inputs, outputs, or tool expectations change;
- Golden Set changes as the canonical scenario assets;
- Promptfoo configs as deterministic scenario-level assertion mappings;
- DeepEval tests as Python/pytest-style evaluation skeletons and future metric-oriented checks;
- documentation updates for user-facing behavior;
- validation and test output;
- review notes explaining why the change is safe, scoped, and regression-protected.

## Detecting Overfitting

Overfitting happens when a skill is changed to satisfy a narrow test phrase instead of the intended behavior. Warning signs include:

- assertions that require one exact prose sentence when a concept-level check would work;
- skill text that repeats Golden Set wording awkwardly without improving guidance;
- cases that cover only happy paths and omit edge, scope-control, or safety-sensitive scenarios;
- new instructions that optimize for one runner while weakening general agent usability.

Review response: ask for broader scenarios, concept-level assertions, and skill text that remains practical for real agent use.

## Detecting Scope Creep

Scope creep happens when a skill begins doing work outside its manifest, risk tier, package boundary, or repository role. Warning signs include:

- a documentation skill adding release automation instructions;
- a manifest skill changing registry governance behavior;
- a local validation skill describing production observability as active behavior;
- a skill encouraging agents to modify unrelated packages without a prompt.

Review response: require narrower wording, metadata updates if scope truly changed, or a separate package proposal.

## Detecting Unsafe Tool Permission Expansion

Unsafe tool permission expansion happens when a skill encourages broader access than the task requires. Warning signs include:

- broad shell access when a specific command or read-only inspection is enough;
- instructions to use unrestricted filesystem or network access by default;
- examples that expose secrets, tokens, real API keys, real MCP credentials, or local user paths;
- destructive commands without explicit human intent and safety checks.

Review response: require least-privilege instructions, safe examples, placeholder credentials only, and clear boundaries for destructive or external actions.

## Reviewing Golden Sets

Golden Sets are canonical scenario assets. Confirm that each changed case:

- has a stable lowercase kebab-case ID;
- uses the correct skill ID and category;
- captures behavior before the skill text is changed;
- includes deterministic `contains`, `not_contains`, or `must_reference` expectations;
- includes negative, scope-control, or safety-sensitive coverage when relevant;
- avoids secrets, local absolute user paths, and future-feature overclaims.

## Reviewing Promptfoo Configs

Promptfoo configs provide deterministic scenario-level assertions. Confirm that each changed config:

- references the matching Golden Set case ID;
- preserves the Golden Set category in metadata;
- maps `expected.contains` to deterministic `contains` assertions;
- maps `expected.not_contains` to deterministic `not-contains` assertions when applicable;
- avoids mandatory network calls, cloud login assumptions, or full-evaluation claims.

## Reviewing DeepEval Tests

DeepEval tests provide Python/pytest-style evaluation skeletons and future metric-oriented checks. Confirm that each changed test:

- loads the intended Golden Set;
- validates required categories and deterministic expectations;
- keeps optional DeepEval object construction guarded;
- does not require live model scoring, credentials, or external services for baseline tests;
- does not claim that LLM-as-judge output is absolute truth.

## Reviewing Documentation Changes

Documentation should distinguish implemented assets from planned capabilities. Confirm that docs say:

- CI smoke evaluation uses `skillops eval --smoke` for deterministic evaluation asset validation;
- production observability is planned for Phase 4 and is not implemented in Phase 2;
- marketplace behavior is planned for Phase 5 and is not implemented in Phase 2;
- self-improvement automation and automatic skill patching are planned for Phase 6 and are not implemented in Phase 2;
- Langfuse integration, Phoenix integration, production traces, and dependency graph analysis are not implemented in this package.

## When Human Review Is Required

Human review is required when a change affects safety-sensitive instructions, tool permissions, scope boundaries, public documentation, governance language, skill metadata, or any scenario that could encourage destructive actions, credential exposure, external service use, or future-feature overclaiming.

## Skill-TDD Review Checklist

### Scenario Coverage

- Does the change start with an eval case first?
- Are happy path, edge, negative, scope-control, or safety-sensitive cases updated as needed?
- Does the scenario represent real maintainer or agent behavior?

### Golden Set Quality

- Are Golden Sets treated as canonical scenario assets?
- Are expected traits deterministic but not brittle?
- Are forbidden behaviors and required references clear?

### Promptfoo Alignment

- Do Promptfoo assertions map to Golden Set expectations?
- Are config metadata fields aligned with the Golden Set case ID and category?
- Is Promptfoo described as local-first configuration rather than a mandatory CI gate?

### DeepEval Alignment

- Do DeepEval skeletons load the correct Golden Set?
- Are Python/pytest-style checks deterministic by default?
- Are optional judge or metric-oriented checks guarded and not treated as absolute truth?

### Skill Scope

- Does the skill remain within its stated purpose?
- Are metadata changes included if the scope truly changed?
- Is unrelated package or future-phase behavior avoided?

### Safety and Permissions

- Are tool permissions least-privilege?
- Are broad shell access, broad filesystem access, unsafe network calls, and destructive commands avoided unless explicitly required?
- Are secrets, tokens, real API keys, real MCP credentials, and local absolute user paths absent?

### Documentation Accuracy

- Do docs match implemented behavior?
- Are full/live evaluation, production observability, marketplace behavior, and self-improvement automation marked as planned rather than implemented?
- Are stale names and unsupported Python version references absent?

### Regression Risk

- Does the change preserve existing behavior not intentionally changed?
- Is the reason for the new or changed scenario clear?
- Would a future reviewer understand why the regression protection exists?

### Final Recommendation

Choose one:

- **Approve**: evaluation assets, skill changes, validation, safety, and documentation are aligned.
- **Request changes**: specific issues must be fixed before merge.
- **Escalate to human owner**: safety, scope, governance, or credential risk requires human decision.


## Evaluation CI Smoke Check

Reviewers should expect CI to run `uv run skillops eval --smoke`. The step verifies Golden Set and eval suite schema alignment, Promptfoo and DeepEval references, guarded DeepEval files, and documentation/safety boundaries. It is not a live LLM evaluation, not mandatory LLM-as-judge scoring, and not a production observability signal.
