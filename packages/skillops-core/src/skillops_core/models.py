"""Models for Phase 1 SkillOps manifests, registries, validation, and health."""

from __future__ import annotations

from dataclasses import MISSING, dataclass, field, fields, is_dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Literal, get_args, get_origin


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


class StrictModel:
    """Small validation base with Pydantic-like methods used by Phase 1."""

    @classmethod
    def model_validate(cls, data: dict[str, Any]):
        if not isinstance(data, dict):
            raise ModelValidationError(f"{cls.__name__} expects a mapping")
        allowed = {item.name for item in fields(cls)}
        extra = set(data) - allowed
        if extra:
            raise ModelValidationError(f"Unexpected fields for {cls.__name__}: {sorted(extra)}")
        kwargs: dict[str, Any] = {}
        for item in fields(cls):
            if item.name in data:
                value = data[item.name]
            elif item.default is not MISSING:
                value = item.default
            elif item.default_factory is not MISSING:
                value = item.default_factory()  # type: ignore[misc]
            else:
                raise ModelValidationError(f"Missing required field: {item.name}")
            kwargs[item.name] = _coerce(value, item.type, item.name)
        obj = cls(**kwargs)
        validate = getattr(obj, "_validate", None)
        if validate:
            validate()
        return obj

    def model_dump(self, mode: str | None = None, exclude_none: bool = False) -> dict[str, Any]:
        return {
            item.name: _dump(getattr(self, item.name), mode, exclude_none)
            for item in fields(self)
            if not (exclude_none and getattr(self, item.name) is None)
        }


def _coerce(value: Any, typ: Any, name: str) -> Any:
    origin = get_origin(typ)
    args = get_args(typ)
    if isinstance(typ, str):
        # Future annotations are strings in Python 3.13+; validate in _validate methods.
        return value
    if origin is list:
        if not isinstance(value, list):
            raise ModelValidationError(f"{name} must be a list")
        return [_coerce(item, args[0], name) for item in value]
    if origin is dict:
        if not isinstance(value, dict):
            raise ModelValidationError(f"{name} must be a mapping")
        return value
    if origin in {Literal, type(Literal)}:
        if value not in args:
            raise ModelValidationError(f"{name} has invalid value: {value}")
        return value
    if origin is not None and type(None) in args:
        if value is None:
            return None
        non_none = next(arg for arg in args if arg is not type(None))
        return _coerce(value, non_none, name)
    if isinstance(typ, type) and issubclass(typ, StrEnum):
        try:
            return typ(value)
        except ValueError as exc:
            raise ModelValidationError(f"{name} has invalid value: {value}") from exc
    if isinstance(typ, type) and is_dataclass(typ) and issubclass(typ, StrictModel):
        return typ.model_validate(value)
    return value


def _dump(value: Any, mode: str | None, exclude_none: bool) -> Any:
    if isinstance(value, StrEnum):
        return str(value)
    if isinstance(value, datetime):
        return value.isoformat() if mode == "json" else value
    if isinstance(value, StrictModel):
        return value.model_dump(mode=mode, exclude_none=exclude_none)
    if isinstance(value, list):
        return [_dump(item, mode, exclude_none) for item in value]
    return value


@dataclass
class SkillOwner(StrictModel):
    name: str
    contact: str

    def _validate(self) -> None:
        if not self.name or not self.contact:
            raise ModelValidationError("owner name and contact are required")


@dataclass
class SkillType(StrictModel):
    category: str
    execution: ExecutionType

    def _validate(self) -> None:
        if not self.category:
            raise ModelValidationError("type.category is required")
        self.execution = ExecutionType(self.execution)


@dataclass
class SkillCompatibility(StrictModel):
    agents: list[str] = field(default_factory=list)
    environments: list[str] = field(default_factory=list)


@dataclass
class SkillDependencies(StrictModel):
    skills: list[str] = field(default_factory=list)
    tools: list[str] = field(default_factory=list)
    mcp_servers: list[str] = field(default_factory=list)


@dataclass
class SkillAllowedTools(StrictModel):
    shell: str | None = None
    filesystem: str | None = None
    network: str | None = None
    other: list[str] = field(default_factory=list)


@dataclass
class SkillEvals(StrictModel):
    suite_id: str | None = None
    status: str = "not-configured"

    def _validate(self) -> None:
        if not self.status:
            raise ModelValidationError("evals.status is required")


@dataclass
class SkillProvenance(StrictModel):
    source: str
    license: str
    url: str | None = None

    def _validate(self) -> None:
        if not self.source or not self.license:
            raise ModelValidationError("provenance source and license are required")


@dataclass
class SkillPaths(StrictModel):
    skill_file: str = "SKILL.md"

    def _validate(self) -> None:
        if not self.skill_file:
            raise ModelValidationError("paths.skill_file is required")


@dataclass
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

    def _validate(self) -> None:
        import re

        if not re.match(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$", self.id):
            raise ModelValidationError("skill id must be lowercase kebab-case")
        for name in ["name", "version", "description"]:
            if not getattr(self, name):
                raise ModelValidationError(f"{name} is required")
        self.status = SkillStatus(self.status)
        self.risk_tier = RiskTier(self.risk_tier)
        if isinstance(self.owner, dict):
            self.owner = SkillOwner.model_validate(self.owner)
        if isinstance(self.type, dict):
            self.type = SkillType.model_validate(self.type)
        if isinstance(self.compatibility, dict):
            self.compatibility = SkillCompatibility.model_validate(self.compatibility)
        if isinstance(self.dependencies, dict):
            self.dependencies = SkillDependencies.model_validate(self.dependencies)
        if isinstance(self.allowed_tools, dict):
            self.allowed_tools = SkillAllowedTools.model_validate(self.allowed_tools)
        if isinstance(self.evals, dict):
            self.evals = SkillEvals.model_validate(self.evals)
        if isinstance(self.provenance, dict):
            self.provenance = SkillProvenance.model_validate(self.provenance)
        if isinstance(self.paths, dict):
            self.paths = SkillPaths.model_validate(self.paths)


@dataclass
class RegistrySkillEntry(StrictModel):
    id: str
    path: str

    def _validate(self) -> None:
        if not self.id or not self.path:
            raise ModelValidationError("registry skill id and path are required")


@dataclass
class Registry(StrictModel):
    version: int
    skills: list[RegistrySkillEntry] = field(default_factory=list)

    def _validate(self) -> None:
        self.version = int(self.version)
        if self.version < 1:
            raise ModelValidationError("registry version must be >= 1")
        self.skills = [
            RegistrySkillEntry.model_validate(item) if isinstance(item, dict) else item
            for item in self.skills
        ]
        if not self.skills:
            raise ModelValidationError("registry must contain at least one skill")


@dataclass
class ValidationFinding(StrictModel):
    level: FindingLevel
    code: str
    message: str
    path: str | None = None
    skill_id: str | None = None

    def _validate(self) -> None:
        self.level = FindingLevel(self.level)


@dataclass
class ValidationReport(StrictModel):
    findings: list[ValidationFinding] = field(default_factory=list)

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
        self.findings.append(ValidationFinding(FindingLevel(level), code, message, path, skill_id))

    def findings_for_skill(self, skill_id: str) -> list[ValidationFinding]:
        return [finding for finding in self.findings if finding.skill_id == skill_id]


@dataclass
class HealthSkillReport(StrictModel):
    id: str
    name: str
    version: str
    status: str
    risk_tier: str
    owner: str
    score: int
    findings: list[ValidationFinding] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)


@dataclass
class HealthReport(StrictModel):
    overall_score: float
    validation: ValidationReport
    generated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    registry_version: int | None = None
    skills: list[HealthSkillReport] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        return self.model_dump(mode="json")
