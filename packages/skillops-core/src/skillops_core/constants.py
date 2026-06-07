"""Constants for SkillOps core controlled vocabularies and default paths."""

SKILL_STATUSES = {
    "draft",
    "candidate",
    "reviewed",
    "stable",
    "deprecated",
    "archived",
}

RISK_TIERS = {
    "low",
    "medium",
    "high",
    "restricted",
}

EXECUTION_TYPES = {
    "instruction-only",
    "script-backed",
    "tool-mediated",
    "mcp-enhanced",
    "subagent-spawning",
}

EVAL_STATUSES = {
    "not-configured",
    "planned",
    "passing",
    "failing",
    "deprecated",
}

PROVENANCE_SOURCES = {
    "internal",
    "third-party",
    "fork",
    "generated",
    "unknown",
}

FINDING_LEVELS = {
    "error",
    "warning",
    "info",
}

DEFAULT_SKILLS_REGISTRY_PATH = "registry/skills.yaml"
DEFAULT_HEALTH_REPORT_JSON_PATH = "reports/health/health-report.json"
DEFAULT_HEALTH_REPORT_MARKDOWN_PATH = "reports/health/health-report.md"
