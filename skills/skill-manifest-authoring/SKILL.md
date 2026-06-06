# Skill Manifest Authoring Skill

## Required fields
Every `skill.yaml` includes id, name, version, status, risk_tier, description, owner, type, compatibility, dependencies, allowed_tools, evals, provenance, and paths.

## Status values
Use draft, candidate, reviewed, stable, deprecated, or archived.

## Risk tiers
Use low, medium, high, or restricted based on tool access, data sensitivity, and operational impact.

## Dependencies
Declare skill, tool, and MCP server dependencies as arrays, even when empty.

## Allowed tools
Describe shell, filesystem, network, and other tool access using least privilege.

## Provenance
Record source and license so downstream users can review origin and reuse rights.

## Example checklist
Confirm schema validity, owner contact, risk tier, SKILL.md path, and evaluation status before registration.
