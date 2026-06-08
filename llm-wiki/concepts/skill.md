# Skill

A skill is a reusable procedural capability for coding agents. In `skillops`, a skill is represented by `SKILL.md`, described by `skill.yaml`, registered in the skill registry, and written so coding agents can apply it during scoped work.

A skill is different from:

- a prompt, which may be a single instruction or template without lifecycle metadata;
- a workflow, which may coordinate multiple skills or project steps;
- a tool, which is executable capability exposed to an agent;
- a plugin, which packages additional extension behavior;
- an agent, which is the actor that reads and applies the skill.

A good skill combines practical instructions with enough metadata for validation, ownership, review, and discovery.
