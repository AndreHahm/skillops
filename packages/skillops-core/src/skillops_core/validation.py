"""Validation logic for SkillOps manifests and skills registries."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from skillops_core.constants import DEFAULT_SKILLS_REGISTRY_PATH
from skillops_core.errors import SkillOpsFileNotFoundError, SkillOpsValidationError
from skillops_core.loaders import load_skill_manifest, load_skills_registry, load_yaml
from skillops_core.models import SkillManifest, SkillsRegistry, ValidationReport

REQUIRED_CORE_SKILL_IDS = {
    "python-project-setup",
    "skill-manifest-authoring",
    "skill-registry-maintenance",
    "skill-health-review",
    "documentation-maintenance",
}


def _display_path(path: Path, repo_root: Path) -> str:
    try:
        return str(path.resolve().relative_to(repo_root.resolve()))
    except ValueError:
        return str(path)


def _manifest_skill_id(raw: dict[str, Any]) -> str | None:
    skill_id = raw.get("id")
    return skill_id if isinstance(skill_id, str) else None


def validate_skill_manifest(path: Path, repo_root: Path) -> ValidationReport:
    """Validate one skill manifest and its referenced skill file."""

    report = ValidationReport()
    display_path = _display_path(path, repo_root)
    if not path.exists():
        report.add_error("manifest.missing", "Skill manifest is missing.", display_path)
        return report

    try:
        raw_manifest = load_yaml(path)
    except SkillOpsFileNotFoundError:
        report.add_error("manifest.missing", "Skill manifest is missing.", display_path)
        return report
    except SkillOpsValidationError as exc:
        report.add_error(
            "manifest.invalid_yaml", f"Invalid skill manifest YAML: {exc}", display_path
        )
        return report
    except OSError as exc:
        report.add_error(
            "manifest.invalid_yaml", f"Could not read skill manifest: {exc}", display_path
        )
        return report

    raw_skill_id = _manifest_skill_id(raw_manifest)
    if "owner" not in raw_manifest or raw_manifest.get("owner") in (None, ""):
        report.add_error(
            "owner.missing", "Required owner metadata is missing.", display_path, raw_skill_id
        )
    if "risk_tier" not in raw_manifest or raw_manifest.get("risk_tier") in (None, ""):
        report.add_error(
            "risk_tier.missing", "Required risk tier is missing.", display_path, raw_skill_id
        )

    try:
        manifest = SkillManifest.model_validate(raw_manifest)
    except SkillOpsValidationError as exc:
        report.add_error(
            "manifest.invalid_schema",
            f"Skill manifest does not match the SkillOps schema: {exc}",
            display_path,
            raw_skill_id,
        )
        return report

    skill_file_path = path.parent / manifest.paths.skill_file
    if not skill_file_path.exists():
        report.add_error(
            "skill_file.missing",
            f"Referenced skill file is missing: {manifest.paths.skill_file}",
            _display_path(skill_file_path, repo_root),
            manifest.id,
        )

    if manifest.evals.suite_id is None or manifest.evals.status == "not-configured":
        report.add_warning(
            "evals.not_configured",
            "Evaluation suite is not configured.",
            display_path,
            manifest.id,
        )
    if manifest.status == "draft":
        report.add_warning("status.draft", "Skill is still draft.", display_path, manifest.id)
    if not manifest.dependencies.skills:
        report.add_info(
            "dependencies.skills.empty",
            "No skill dependencies declared.",
            display_path,
            manifest.id,
        )
    if not manifest.dependencies.mcp_servers:
        report.add_info(
            "dependencies.mcp_servers.empty",
            "No MCP server dependencies declared.",
            display_path,
            manifest.id,
        )
    return report


def _add_duplicate_id_findings(raw_registry: dict[str, Any], report: ValidationReport) -> None:
    raw_entries = raw_registry.get("skills", [])
    if not isinstance(raw_entries, list):
        return
    seen: set[str] = set()
    duplicate_ids: set[str] = set()
    for entry in raw_entries:
        if not isinstance(entry, dict):
            continue
        skill_id = entry.get("id")
        if not isinstance(skill_id, str):
            continue
        if skill_id in seen and skill_id not in duplicate_ids:
            report.add_error(
                "registry.duplicate_skill_id",
                f"Duplicate registry skill id: {skill_id}",
                DEFAULT_SKILLS_REGISTRY_PATH,
                skill_id,
            )
            duplicate_ids.add(skill_id)
        seen.add(skill_id)


def _validate_required_and_unexpected_ids(
    registry: SkillsRegistry, report: ValidationReport
) -> None:
    registry_ids = {entry.id for entry in registry.skills}
    for skill_id in sorted(REQUIRED_CORE_SKILL_IDS - registry_ids):
        report.add_error(
            "registry.required_skill_missing",
            f"Required Phase 1 core skill is missing from registry: {skill_id}",
            DEFAULT_SKILLS_REGISTRY_PATH,
            skill_id,
        )
    for skill_id in sorted(registry_ids - REQUIRED_CORE_SKILL_IDS):
        report.add_error(
            "registry.unexpected_skill",
            f"Unexpected skill registered for Package 3: {skill_id}",
            DEFAULT_SKILLS_REGISTRY_PATH,
            skill_id,
        )


def validate_skills_registry(repo_root: Path) -> ValidationReport:
    """Validate registry/skills.yaml and all registered manifests."""

    repo_root = repo_root.resolve()
    report = ValidationReport()
    registry_path = repo_root / DEFAULT_SKILLS_REGISTRY_PATH
    if not registry_path.exists():
        report.add_error(
            "registry.missing",
            f"Required registry file is missing: {DEFAULT_SKILLS_REGISTRY_PATH}",
            DEFAULT_SKILLS_REGISTRY_PATH,
        )
        return report

    try:
        raw_registry = load_yaml(registry_path)
    except SkillOpsFileNotFoundError:
        report.add_error(
            "registry.missing",
            f"Required registry file is missing: {DEFAULT_SKILLS_REGISTRY_PATH}",
            DEFAULT_SKILLS_REGISTRY_PATH,
        )
        return report
    except SkillOpsValidationError as exc:
        report.add_error(
            "registry.invalid_yaml",
            f"Invalid skills registry YAML: {exc}",
            DEFAULT_SKILLS_REGISTRY_PATH,
        )
        return report
    except OSError as exc:
        report.add_error(
            "registry.invalid_yaml",
            f"Could not read skills registry: {exc}",
            DEFAULT_SKILLS_REGISTRY_PATH,
        )
        return report

    _add_duplicate_id_findings(raw_registry, report)

    try:
        registry = SkillsRegistry.model_validate(raw_registry)
    except SkillOpsValidationError as exc:
        report.add_error(
            "registry.invalid_schema",
            f"Skills registry does not match the SkillOps schema: {exc}",
            DEFAULT_SKILLS_REGISTRY_PATH,
        )
        return report

    _validate_required_and_unexpected_ids(registry, report)

    for entry in registry.skills:
        manifest_path = repo_root / entry.path
        if not manifest_path.exists():
            report.add_error(
                "registry.skill_path_missing",
                f"Registered skill manifest is missing: {entry.path}",
                entry.path,
                entry.id,
            )
            continue

        manifest_report = validate_skill_manifest(manifest_path, repo_root)
        report.extend(manifest_report)
        try:
            manifest = load_skill_manifest(manifest_path)
        except SkillOpsValidationError:
            continue
        if manifest.id != entry.id:
            report.add_error(
                "registry.skill_id_mismatch",
                f"Registry id '{entry.id}' does not match manifest id '{manifest.id}'.",
                entry.path,
                entry.id,
            )
    return report


# Backward-compatible alias for the existing CLI from Package 2.
validate_registry = validate_skills_registry
load_registry = load_skills_registry
