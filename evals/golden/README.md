# Golden Sets

Golden Sets are structured, versioned YAML regression assets for SkillOps skills. Each file captures scenario prompts and deterministic expectations that reviewers can use to check whether a skill still gives scoped, safe, and useful guidance.

Golden Sets are review inputs, not an evaluation engine. In this package they are validated as data and covered by consistency tests, but they are not executed by Promptfoo or DeepEval.

## File Format

Each Golden Set uses `schemas/golden-set.schema.json` and includes:

- `version`: schema version, currently `1`
- `skill_id`: the stable ID of the skill being reviewed
- `cases`: scenario cases with stable IDs, titles, categories, input prompts, expected assertions, and notes

Each case must include:

- `id`: lowercase kebab-case and stable over time
- `title`: concise human-readable case title
- `category`: one of the required coverage categories
- `input`: realistic user request or review scenario
- `expected.contains`: deterministic concepts, commands, or phrases a good answer should include
- `expected.not_contains`: deterministic concepts, claims, or actions a good answer should avoid
- `expected.must_reference`: optional non-empty files, commands, or concepts that should be referenced
- `notes`: short review rationale

## Required Categories

Every core skill Golden Set must include at least one case in each category:

- `happy_path`: normal successful guidance
- `edge_case`: nuanced but valid request
- `invalid_input`: missing, contradictory, or invalid request details
- `scope_creep`: request that tries to add unrelated future behavior
- `safety_sensitive`: request involving secrets, unsafe permissions, destructive actions, credentials, or inappropriate automation

## Writing Good Assertions

Use deterministic partial assertions that survive reasonable wording changes. Prefer concrete expectations such as `Python >=3.13`, `uv run pytest`, `registry/skills.yaml`, or `least privilege`. Avoid vague expectations such as `good answer` or full-output matching.

Do not include real secrets, real credentials, user-specific absolute paths, or claims that future runtime systems already exist.

## Implemented Now

- scenario-based golden cases
- structured YAML Golden Set files
- schema validation
- consistency tests

## Planned for Later Phase 2 Packages

- Promptfoo configuration and execution
- DeepEval tests and execution
- CI smoke eval command
- richer judge-based scoring
