# Golden Sets

A Golden Set is a versioned YAML file with representative scenarios for one SkillOps skill. Golden Sets make behavior reviewable by defining what a good skill response should include, what it should avoid, and which files, commands, or concepts it should reference.

Golden Sets support Skill-TDD by giving reviewers regression assets before executable evaluation runners exist. A maintainer can add or update cases for desired behavior, review the skill against those cases, and later reuse the same assets when Promptfoo and DeepEval integration packages are implemented.

## Implemented Now

- scenario-based golden cases
- structured YAML Golden Set files
- schema validation through `schemas/golden-set.schema.json`
- consistency tests for completeness, required categories, registry references, future-feature overclaims, secrets, and local path drift

## Planned for Later Phase 2 Packages

- Promptfoo configuration and execution
- DeepEval tests and execution
- CI smoke eval command
- richer judge-based scoring

Promptfoo execution and DeepEval execution are not implemented by the current Golden Set files.

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
