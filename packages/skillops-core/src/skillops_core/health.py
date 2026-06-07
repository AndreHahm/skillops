"""Health scoring and report generation for SkillOps core."""

from __future__ import annotations

import json
from pathlib import Path

from skillops_core.constants import (
    DEFAULT_HEALTH_REPORT_JSON_PATH,
    DEFAULT_HEALTH_REPORT_MARKDOWN_PATH,
    DEFAULT_SKILLS_REGISTRY_PATH,
)
from skillops_core.errors import SkillOpsValidationError
from skillops_core.loaders import load_skill_manifest, load_skills_registry
from skillops_core.models import HealthReport, HealthSkillReport, SkillManifest, ValidationReport
from skillops_core.validation import validate_skill_manifest, validate_skills_registry


def _messages_by_level(validation_report: ValidationReport, level: str, skill_id: str) -> list[str]:
    return [
        finding.message
        for finding in validation_report.findings
        if finding.level == level and (finding.skill_id in {None, skill_id})
    ]


def _codes_by_level(validation_report: ValidationReport, level: str, skill_id: str) -> set[str]:
    return {
        finding.code
        for finding in validation_report.findings
        if finding.level == level and (finding.skill_id in {None, skill_id})
    }


def calculate_skill_health(
    manifest: SkillManifest,
    validation_report: ValidationReport,
    manifest_path: Path | None = None,
) -> HealthSkillReport:
    """Calculate a Phase 1 health score for one parsed skill manifest."""

    error_codes = _codes_by_level(validation_report, "error", manifest.id)
    score = 0
    if "manifest.invalid_schema" not in error_codes:
        score += 20
    if "skill_file.missing" not in error_codes:
        if manifest_path is None or (manifest_path.parent / manifest.paths.skill_file).exists():
            score += 15
    if manifest.owner.name and manifest.owner.contact and "owner.missing" not in error_codes:
        score += 15
    if manifest.risk_tier and "risk_tier.missing" not in error_codes:
        score += 10
    if manifest.status != "draft":
        score += 10
    if any([manifest.dependencies.skills, manifest.dependencies.tools, manifest.dependencies.mcp_servers]):
        score += 10
    if manifest.allowed_tools.shell != "none" or manifest.allowed_tools.filesystem != "none":
        score += 10
    if manifest.evals.suite_id is not None and manifest.evals.status != "not-configured":
        score += 10

    return HealthSkillReport(
        id=manifest.id,
        score=min(score, 100),
        status=manifest.status,
        risk_tier=manifest.risk_tier,
        errors=_messages_by_level(validation_report, "error", manifest.id),
        warnings=_messages_by_level(validation_report, "warning", manifest.id),
        info=_messages_by_level(validation_report, "info", manifest.id),
    )


def _invalid_skill_health(skill_id: str, validation_report: ValidationReport) -> HealthSkillReport:
    return HealthSkillReport(
        id=skill_id,
        score=0,
        status="invalid",
        risk_tier="unknown",
        errors=_messages_by_level(validation_report, "error", skill_id),
        warnings=_messages_by_level(validation_report, "warning", skill_id),
        info=_messages_by_level(validation_report, "info", skill_id),
    )


def generate_health_report(repo_root: Path) -> HealthReport:
    """Generate a repository-level health report for registered skills."""

    repo_root = repo_root.resolve()
    registry_path = repo_root / DEFAULT_SKILLS_REGISTRY_PATH
    registry_validation_report = validate_skills_registry(repo_root)
    skills: list[HealthSkillReport] = []

    try:
        registry = load_skills_registry(registry_path)
    except SkillOpsValidationError:
        return HealthReport(
            total_skills=0,
            average_health_score=0.0,
            errors=registry_validation_report.error_count,
            warnings=registry_validation_report.warning_count,
            skills=[],
        )

    for entry in registry.skills:
        manifest_path = repo_root / entry.path
        try:
            manifest = load_skill_manifest(manifest_path)
        except SkillOpsValidationError:
            skills.append(_invalid_skill_health(entry.id, registry_validation_report))
            continue
        skill_validation_report = validate_skill_manifest(manifest_path, repo_root)
        registry_findings = [
            f.model_copy(update={"skill_id": manifest.id})
            for f in registry_validation_report.findings
            if f.skill_id is None
        ]
        for finding in registry_findings:
            finding.skill_id = entry.id
        skill_validation_report.findings.extend(registry_findings)
        skills.append(calculate_skill_health(manifest, skill_validation_report, manifest_path))

    average = round(sum(skill.score for skill in skills) / len(skills), 2) if skills else 0.0
    return HealthReport(
        total_skills=len(skills),
        average_health_score=average,
        errors=registry_validation_report.error_count,
        warnings=registry_validation_report.warning_count,
        skills=sorted(skills, key=lambda skill: skill.id),
    )


def write_health_report_json(report: HealthReport, path: Path) -> None:
    """Write a health report JSON file."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report.model_dump(mode="json"), indent=2) + "\n", encoding="utf-8")


def _finding_summary(skill: HealthSkillReport) -> str:
    parts: list[str] = []
    if skill.errors:
        parts.append(f"{len(skill.errors)} errors")
    if skill.warnings:
        parts.append(f"{len(skill.warnings)} warnings")
    if skill.info:
        parts.append(f"{len(skill.info)} info")
    return ", ".join(parts) if parts else "none"


def write_health_report_markdown(report: HealthReport, path: Path) -> None:
    """Write a health report Markdown file."""

    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Skill Health Report",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Total Skills | {report.total_skills} |",
        f"| Average Health Score | {report.average_health_score} |",
        f"| Errors | {report.errors} |",
        f"| Warnings | {report.warnings} |",
        "",
        "## Skills",
        "",
        "| Skill | Score | Status | Risk | Findings |",
        "|---|---:|---|---|---|",
    ]
    for skill in report.skills:
        lines.append(
            f"| {skill.id} | {skill.score} | {skill.status} | {skill.risk_tier} | "
            f"{_finding_summary(skill)} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


DEFAULT_JSON_OUTPUT_PATH = DEFAULT_HEALTH_REPORT_JSON_PATH
DEFAULT_MARKDOWN_OUTPUT_PATH = DEFAULT_HEALTH_REPORT_MARKDOWN_PATH
