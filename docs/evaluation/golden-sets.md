# Golden Sets

A Golden Set is a versioned YAML file with representative scenarios for one SkillOps skill. Golden Sets make behavior reviewable by defining what a good skill response should include, what it should avoid, and which files, commands, or concepts it should reference.

Golden Sets support Skill-TDD by making the eval case first. They are the canonical scenario assets: a maintainer adds or updates cases for desired behavior, then aligns the skill, Promptfoo configuration, DeepEval skeletons, and review notes to those cases.

## Implemented Now

- scenario-based golden cases
- structured YAML Golden Set files
- schema validation through `schemas/golden-set.schema.json`
- consistency tests for completeness, required categories, registry references, future-feature overclaims, secrets, and local path drift

## Relationship to Other Skill-TDD Layers

- Promptfoo configs provide deterministic scenario-level assertions derived from Golden Set expectations.
- DeepEval tests provide Python/pytest-style evaluation skeletons and future metric-oriented checks derived from Golden Set cases.
- Review gates inspect Golden Set quality, overfitting risk, scope creep, and unsafe tool permission expansion.
- CI smoke evaluation is planned for a later Phase 2 package and is not implemented by this package.

Promptfoo execution is local-first configuration work, and DeepEval live scoring is optional or later work. The Golden Set files themselves do not implement production observability, marketplace behavior, self-improvement automation, or automatic skill patching.

## Format

```yaml
version: 1
skill_id: skill-manifest-authoring
cases:
  - id: manifest-happy-path
    title: Manifest happy path
    category: happy_path
    input: |
      User request or scenario prompt here.
    expected:
      contains:
        - required phrase or concept
      not_contains:
        - forbidden phrase, claim, or action
      must_reference:
        - expected file, command, concept, or policy
    notes: Optional human-readable rationale.
```

## Required Categories

Each core skill Golden Set must include at least one case for each category:

- `happy_path`: normal intended use
- `edge_case`: valid request with a nuance or partial state
- `invalid_input`: request missing required details or containing invalid instructions
- `scope_creep`: request to add behavior outside the current package or skill scope
- `safety_sensitive`: request involving secrets, credentials, unsafe permissions, destructive actions, local paths, or inappropriate automation

## Authoring Guidance

Good Golden Set cases should:

- test one clear behavior
- use realistic but concise prompts
- keep IDs stable, lowercase, and slug-like
- use deterministic `expected.contains` assertions such as commands, file names, schema fields, or policy concepts
- use deterministic `expected.not_contains` assertions to guard against overclaims, unsafe actions, stale names, or version drift
- include `expected.must_reference` when a file, command, schema, registry, or governance concept is central to the behavior
- avoid huge prompts, vague expected text, full-output matching, real secrets, and user-specific absolute paths

Golden Sets should not describe future work as complete. Documentation, cases, and expected assertions should distinguish implemented regression assets from later execution engines.
