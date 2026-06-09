# Golden Sets

Golden sets are static scenario files that describe representative prompts and expected behavior for SkillOps skills.

Each golden set uses `schemas/golden-set.schema.json` and contains:

- `version`: schema version, currently `1`
- `skill_id`: the skill being reviewed
- `cases`: one or more scenarios with a stable id, title, category, input, and expected response traits

Supported case categories are:

- `happy_path`
- `edge_case`
- `invalid_input`
- `scope_creep`
- `safety_sensitive`

Golden sets are not executed by Promptfoo or DeepEval in this package. Promptfoo execution and DeepEval execution are planned for later Phase 2 packages.
