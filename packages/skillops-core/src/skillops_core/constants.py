from typing import Final

"""Constants for SkillOps core controlled vocabularies and default paths."""

SKILL_STATUSES: Final[set[str]] = {
    "draft",
    "candidate",
    "reviewed",
    "stable",
    "deprecated",
    "archived",
}

RISK_TIERS: Final[set[str]] = {
    "low",
    "medium",
    "high",
    "restricted",
}

EXECUTION_TYPES: Final[set[str]] = {
    "instruction-only",
    "script-backed",
    "tool-mediated",
    "mcp-enhanced",
    "subagent-spawning",
}

EVAL_STATUSES: Final[set[str]] = {
    "not-configured",
    "planned",
    "passing",
    "failing",
    "deprecated",
}

PROVENANCE_SOURCES: Final[set[str]] = {
    "internal",
    "third-party",
    "fork",
    "generated",
    "unknown",
}

FINDING_LEVELS: Final[set[str]] = {
    "error",
    "warning",
    "info",
}

DEFAULT_SKILLS_REGISTRY_PATH: Final[str] = "registry/skills.yaml"
DEFAULT_HEALTH_REPORT_JSON_PATH: Final[str] = "reports/health/health-report.json"
DEFAULT_HEALTH_REPORT_MARKDOWN_PATH: Final[str] = "reports/health/health-report.md"
