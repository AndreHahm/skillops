"""YAML and model loading utilities for SkillOps core."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from skillops_core.errors import SkillOpsFileNotFoundError, SkillOpsValidationError
from skillops_core.models import ModelValidationError, SkillManifest, SkillsRegistry


def load_yaml(path: Path) -> dict[str, Any]:
    """Load a YAML mapping from disk."""

    if not path.exists():
        raise SkillOpsFileNotFoundError(f"Required file does not exist: {path}")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise SkillOpsValidationError(f"Invalid YAML in {path}: {exc}") from exc
    except (OSError, UnicodeDecodeError) as exc:
        raise SkillOpsValidationError(f"Could not read {path}: {exc}") from exc
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise SkillOpsValidationError(f"YAML document must be a mapping: {path}")
    return data


def load_skill_manifest(path: Path) -> SkillManifest:
    """Load and parse a skill manifest."""

    data = load_yaml(path)
    try:
        return SkillManifest.model_validate(data)
    except ModelValidationError as exc:
        raise SkillOpsValidationError(f"Invalid skill manifest {path}: {exc}") from exc


def load_skills_registry(path: Path) -> SkillsRegistry:
    """Load and parse a skills registry."""

    data = load_yaml(path)
    try:
        return SkillsRegistry.model_validate(data)
    except ModelValidationError as exc:
        raise SkillOpsValidationError(f"Invalid skills registry {path}: {exc}") from exc


# Backward-compatible alias for the existing CLI from Package 2.
load_registry = load_skills_registry
