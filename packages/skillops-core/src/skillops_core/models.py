"""Pydantic models for SkillOps manifests, registries, validation, and health."""

from __future__ import annotations

import re
from enum import StrEnum
from typing import Any, Literal, Self

import pydantic
from pydantic import BaseModel, ConfigDict, Field, model_validator

from skillops_core.constants import (
    EVAL_STATUSES,
    EXECUTION_TYPES,
    FINDING_LEVELS,
    PROVENANCE_SOURCES,
    RISK_TIERS,
    SKILL_STATUSES,
)
from skillops_core.errors import SkillOpsValidationError

SKILL_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$")
SEMVER_LIKE_PATTERN = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
ALLOWED_TOOL_ACCESS = {"read-only", "read-write", "none"}


class ModelValidationError(SkillOpsValidationError):
    """Raised when SkillOps model validation fails."""


class FindingLevel(StrEnum):
    """Validation finding severity levels."""

    error = "error"
    warning = "warning"
    info = "info"


class StrictModel(BaseModel):
    """Base model with strict fields and SkillOps validation errors."""

    model_config = ConfigDict(extra="forbid")

    @classmethod
    def model_validate(cls, obj: Any, **kwargs: Any) -> Self:
        try:
            return super().model_validate(obj, **kwargs)  # type: ignore[return-value]
        except pydantic.ValidationError as exc:
            raise ModelValidationError(str(exc)) from exc


class SkillOwner(StrictModel):
    """Owner metadata for a skill."""

    name: str
    contact: str


class SkillType(StrictModel):
    """Skill type metadata."""

    category: str | list[str]
    execution: str

    @model_validator(mode="after")
    def _validate_execution(self) -> SkillType:
        if self.execution not in EXECUTION_TYPES:
            raise ValueError(f"type.execution must be one of: {sorted(EXECUTION_TYPES)}")
        return self


class SkillCompatibility(StrictModel):
    """Agent and environment compatibility metadata."""

    agents: list[str]
    environments: list[str]


class SkillDependencies(StrictModel):
    """Skill dependency metadata."""

    skills: list[str]
    tools: list[str]
    mcp_servers: list[str]


class SkillAllowedTools(StrictModel):
    """Allowed shell and filesystem access for a skill."""

    shell: str
    filesystem: str

    @model_validator(mode="after")
    def _validate_allowed_tools(self) -> SkillAllowedTools:
        for field_name in ("shell", "filesystem"):
            value = getattr(self, field_name)
            if value not in ALLOWED_TOOL_ACCESS:
                raise ValueError(
                    f"allowed_tools.{field_name} must be one of: "
                    f"{sorted(ALLOWED_TOOL_ACCESS)}"
                )
        return self


class SkillEvals(StrictModel):
    """Evaluation configuration for a skill."""

    suite_id: str | None
    status: str

    @model_validator(mode="after")
    def _validate_status(self) -> SkillEvals:
        if self.status not in EVAL_STATUSES:
            raise ValueError(f"evals.status must be one of: {sorted(EVAL_STATUSES)}")
        return self


class SkillProvenance(StrictModel):
    """Provenance metadata for a skill."""

    source: str
    license: str

    @model_validator(mode="after")
    def _validate_source(self) -> SkillProvenance:
        if self.source not in PROVENANCE_SOURCES:
            raise ValueError(f"provenance.source must be one of: {sorted(PROVENANCE_SOURCES)}")
        return self


class SkillPaths(StrictModel):
    """Repository-relative paths declared by a skill manifest."""

    skill_file: str


class SkillManifest(StrictModel):
    """SkillOps skill manifest model."""

    id: str
    name: str
    version: str
    status: str
    risk_tier: str
    description: str
    owner: SkillOwner
    type: SkillType
    compatibility: SkillCompatibility
    dependencies: SkillDependencies
    allowed_tools: SkillAllowedTools
    evals: SkillEvals
    provenance: SkillProvenance
    paths: SkillPaths

    @model_validator(mode="after")
    def _validate_manifest(self) -> SkillManifest:
        if not SKILL_ID_PATTERN.match(self.id):
            raise ValueError("id must match ^[a-z0-9][a-z0-9-]*[a-z0-9]$")
        if len(self.name) < 3:
            raise ValueError("name must be at least 3 characters")
        if not SEMVER_LIKE_PATTERN.match(self.version):
            raise ValueError("version must be semantic-version-like, for example 0.1.0")
        if self.status not in SKILL_STATUSES:
            raise ValueError(f"status must be one of: {sorted(SKILL_STATUSES)}")
        if self.risk_tier not in RISK_TIERS:
            raise ValueError(f"risk_tier must be one of: {sorted(RISK_TIERS)}")
        if len(self.description) < 20:
            raise ValueError("description must be at least 20 characters")
        return self


class RegistrySkillEntry(StrictModel):
    """One skill entry in registry/skills.yaml."""

    id: str
    path: str

    @model_validator(mode="after")
    def _validate_entry(self) -> RegistrySkillEntry:
        if not SKILL_ID_PATTERN.match(self.id):
            raise ValueError("registry skill id must match ^[a-z0-9][a-z0-9-]*[a-z0-9]$")
        if not self.path.endswith("skill.yaml"):
            raise ValueError("registry skill path must end with skill.yaml")
        return self


class SkillsRegistry(StrictModel):
    """SkillOps skills registry model."""

    version: int
    skills: list[RegistrySkillEntry]


# Backward-compatible alias for the existing CLI/tests from Package 2.
Registry = SkillsRegistry


class ValidationFinding(StrictModel):
    """A structured validation finding."""

    level: str
    code: str
    message: str
    path: str | None = None
    skill_id: str | None = None

    @model_validator(mode="after")
    def _validate_level(self) -> ValidationFinding:
        if self.level not in FINDING_LEVELS:
            raise ValueError(f"level must be one of: {sorted(FINDING_LEVELS)}")
        return self


class ValidationReport(StrictModel):
    """Collection of validation findings with convenience counters."""

    findings: list[ValidationFinding] = Field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        return self.error_count > 0

    @property
    def error_count(self) -> int:
        return sum(1 for finding in self.findings if finding.level == "error")

    @property
    def warning_count(self) -> int:
        return sum(1 for finding in self.findings if finding.level == "warning")

    @property
    def info_count(self) -> int:
        return sum(1 for finding in self.findings if finding.level == "info")

    def add_error(
        self, code: str, message: str, path: str | None = None, skill_id: str | None = None
    ) -> None:
        self.findings.append(
            ValidationFinding(
                level="error", code=code, message=message, path=path, skill_id=skill_id
            )
        )

    def add_warning(
        self, code: str, message: str, path: str | None = None, skill_id: str | None = None
    ) -> None:
        self.findings.append(
            ValidationFinding(
                level="warning", code=code, message=message, path=path, skill_id=skill_id
            )
        )

    def add_info(
        self, code: str, message: str, path: str | None = None, skill_id: str | None = None
    ) -> None:
        self.findings.append(
            ValidationFinding(
                level="info", code=code, message=message, path=path, skill_id=skill_id
            )
        )

    def add(
        self,
        level: Literal["error", "warning", "info"],
        code: str,
        message: str,
        path: str | None = None,
        skill_id: str | None = None,
    ) -> None:
        if level == "error":
            self.add_error(code, message, path, skill_id)
        elif level == "warning":
            self.add_warning(code, message, path, skill_id)
        elif level == "info":
            self.add_info(code, message, path, skill_id)
        else:
            msg = f"Invalid finding level {level!r}; expected 'error', 'warning', 'info'"
            raise ValueError(msg)

    def extend(self, other: ValidationReport) -> None:
        self.findings.extend(other.findings)

    def findings_for_skill(self, skill_id: str) -> list[ValidationFinding]:
        return [finding for finding in self.findings if finding.skill_id == skill_id]


class HealthSkillReport(StrictModel):
    """Health score and findings for one skill."""

    id: str
    score: int
    status: str
    risk_tier: str
    errors: list[str]
    warnings: list[str]
    info: list[str]


class HealthReport(StrictModel):
    """Repository-level SkillOps health report."""

    total_skills: int
    average_health_score: float
    errors: int
    warnings: int
    skills: list[HealthSkillReport]

    @property
    def overall_score(self) -> float:
        """Backward-compatible alias for the existing CLI."""

        return self.average_health_score
