# Golden Sets

A golden set is a versioned YAML file with representative scenarios for one skill. Golden sets help reviewers ask whether a skill recommends the right behavior for happy paths, edge cases, invalid input, scope creep, and safety-sensitive requests.

The Phase 2 Package 1 format is defined by `schemas/golden-set.schema.json`.

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
        - forbidden phrase or concept
      must_reference:
        - expected file, command, concept, or policy
    notes: Optional human-readable rationale.
```

Golden sets in this package are static seed data. Promptfoo execution and DeepEval execution are planned for later Phase 2 packages and are not implemented by these files.
