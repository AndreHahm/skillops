# Registry

A registry is the canonical machine-readable index of known skills. In Phase 1, the skill registry is implemented as `registry/skills.yaml`.

The registry is used for validation and discovery. It should match the skill manifests and filesystem paths it references.

Future registries may cover plugins, tools, agents, MCP servers, and health metadata. Those future registries should build on the same principle: one canonical structured source of truth per registry type.
