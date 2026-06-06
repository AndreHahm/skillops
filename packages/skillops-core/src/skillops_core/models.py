"""Models for Phase 1 SkillOps manifests, registries, validation, and health."""

from __future__ import annotations

import re
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Literal, Self

import pydantic
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class ModelValidationError(ValueError):
    """Raised when model validation fails."""


class SkillStatus(StrEnum):
    draft = "draft"
    candidate = "candidate"
    reviewed = "reviewed"
    stable = "stable"
    deprecated = "deprecated"
    archived = "archived"


class RiskTier(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"
    restricted = "restricted"


class ExecutionType(StrEnum):
    instruction_only = "instruction-only"
    script_backed = "script-backed"
    tool_mediated = "tool-mediated"
    mcp_enhanced = "mcp-enhanced"
    subagent_spawning = "subagent-spawning"


class FindingLevel(StrEnum):
    error = "error"
    warning = "warning"
    info = "info"


class StrictModel(BaseModel):
    """Pydantic BaseModel base; re-raises ValidationError as ModelValidationError."""

    model_config = ConfigDict(extra="forbid")

    @classmethod
    def model_validate(cls, obj: Any, **kwargs: Any) -> Self:
        try:
            return super().model_validate(obj, **kwargs)
        except pydantic.ValidationError as exc:
            raise ModelValidationError(str(exc)) from exc


class SkillOwner(StrictModel):
    name: str
    contact: str

    @model_validator(mode="after")
    def _validate(self) -> SkillOwner:
        if not self.name or not self.contact:
            raise ValueError("owner name and contact are required")
        return self


class SkillType(StrictModel):
    category: str
    execution: ExecutionType

    @model_validator(mode="after")
    def _validate(self) -> SkillType:
        if not self.category:
            raise ValueError("type.category is required")
        return self


class SkillCompatibility(StrictModel):
    agents: list[str] = Field(default_factory=list)
    environments: list[str] = Field(default_factory=list)


class SkillDependencies(StrictModel):
    skills: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)
    mcp_servers: list[str] = Field(default_factory=list)


class SkillAllowedTools(StrictModel):
    shell: str | None = None
    filesystem: str | None = None
    network: str | None = None
    other: list[str] = Field(default_factory=list)


class SkillEvals(StrictModel):
    suite_id: str | None = None
    status: str = "not-configured"

    @model_validator(mode="after")
    def _validate(self) -> SkillEvals:
        if not self.status:
            raise ValueError("evals.status is required")
        return self


class SkillProvenance(StrictModel):
    source: str
    license: str
    url: str | None = None

    @model_validator(mode="after")
    def _validate(self) -> SkillProvenance:
        if not self.source or not self.license:
            raise ValueError("provenance source and license are required")
        return self


class SkillPaths(StrictModel):
    skill_file: str = "SKILL.md"

    @model_validator(mode="after")
    def _validate(self) -> SkillPaths:
        if not self.skill_file:
            raise ValueError("paths.skill_file is required")
        return self


class SkillManifest(StrictModel):
    id: str
    name: str
    version: str
    status: SkillStatus
    risk_tier: RiskTier
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
    def _validate(self) -> SkillManifest:
        if not re.match(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$", self.id):
            raise ValueError("skill id must be lowercase kebab-case")
        for name in ["name", "version", "description"]:
            if not getattr(self, name):
                raise ValueError(f"{name} is required")
        return self


class RegistrySkillEntry(StrictModel):
    id: str
    path: str

    @model_validator(mode="after")
    def _validate(self) -> RegistrySkillEntry:
        if not self.id or not self.path:
            raise ValueError("registry skill id and path are required")
        return self


class Registry(StrictModel):
    version: int
    skills: list[RegistrySkillEntry] = Field(default_factory=list)

    @field_validator("version", mode="before")
    @classmethod
    def _coerce_version(cls, v: Any) -> int:
        try:
            return int(v)
        except (ValueError, TypeError) as exc:
            raise ValueError(f"registry version must be an integer: {v}") from exc

    @model_validator(mode="after")
    def _validate(self) -> Registry:
        if self.version < 1:
            raise ValueError("registry version must be >= 1")
        if not self.skills:
            raise ValueError("registry must contain at least one skill")
        return self


class ValidationFinding(StrictModel):
    level: FindingLevel
    code: str
    message: str
    path: str | None = None
    skill_id: str | None = None


class ValidationReport(StrictModel):
    findings: list[ValidationFinding] = Field(default_factory=list)

    @property
    def error_count(self) -> int:
        return sum(1 for finding in self.findings if finding.level == FindingLevel.error)

    @property
    def warning_count(self) -> int:
        return sum(1 for finding in self.findings if finding.level == FindingLevel.warning)

    @property
    def info_count(self) -> int:
        return sum(1 for finding in self.findings if finding.level == FindingLevel.info)

    @property
    def has_errors(self) -> bool:
        return self.error_count > 0

    def add(
        self,
        level: FindingLevel | Literal["error", "warning", "info"],
        code: str,
        message: str,
        path: str | None = None,
        skill_id: str | None = None,
    ) -> None:
        self.findings.append(
            ValidationFinding(
                level=FindingLevel(level),
                code=code,
                message=message,
                path=path,
                skill_id=skill_id,
            )
        )

    def findings_for_skill(self, skill_id: str) -> list[ValidationFinding]:
        return [finding for finding in self.findings if finding.skill_id == skill_id]


class HealthSkillReport(StrictModel):
    id: str
    name: str
    version: str
    status: str
    risk_tier: str
    owner: str
    score: int
    findings: list[ValidationFinding] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)


class HealthReport(StrictModel):
    overall_score: float
    validation: ValidationReport
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    registry_version: int | None = None
    skills: list[HealthSkillReport] = Field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        return self.model_dump(mode="json")
