"""Health report generation for SkillOps."""

from __future__ import annotations

import json
from pathlib import Path

from skillops_core.models import (
    HealthReport,
    HealthSkillReport,
    Registry,
    SkillManifest,
    ValidationReport,
)
from skillops_core.validation import (
    load_registry,
    load_skill_manifest,
    validate_registry,
    validate_skill_manifest,
)


def calculate_skill_health(
    manifest: SkillManifest,
    validation_report: ValidationReport,
) -> HealthSkillReport:
    findings = validation_report.findings_for_skill(manifest.id)
    error_codes = {finding.code for finding in findings if finding.level == "error"}
    warning_codes = {finding.code for finding in findings if finding.level == "warning"}
    score = 0
    recommendations: list[str] = []

    if "invalid-skill-manifest" not in error_codes:
        score += 20
    else:
        recommendations.append("Fix manifest schema errors.")
    if "missing-skill-doc" not in error_codes:
        score += 15
    else:
        recommendations.append("Create the referenced SKILL.md file.")
    if manifest.owner.name and manifest.owner.contact:
        score += 15
    else:
        recommendations.append("Assign an owner with contact details.")
    if manifest.risk_tier:
        score += 10
    if manifest.status != "draft":
        score += 10
    else:
        recommendations.append("Move the skill out of draft after review.")
    if "missing-dependencies" not in error_codes:
        score += 10
    else:
        recommendations.append("Declare dependencies in the manifest.")
    if "missing-allowed-tools" not in error_codes:
        score += 10
    else:
        recommendations.append("Declare allowed tools in the manifest.")
    if "missing-evals" not in error_codes and "eval-suite-not-configured" not in warning_codes:
        score += 10
    else:
        recommendations.append("Add evaluation configuration.")
    if "eval-suite-not-configured" in warning_codes:
        recommendations.append("Configure an evaluation suite in a later evaluation phase.")

    return HealthSkillReport(
        id=manifest.id,
        name=manifest.name,
        version=manifest.version,
        status=str(manifest.status),
        risk_tier=str(manifest.risk_tier),
        owner=manifest.owner.name,
        score=min(score, 100),
        findings=findings,
        recommendations=recommendations,
    )


def generate_health_report(repo_root: Path) -> HealthReport:
    repo_root = repo_root.resolve()
    validation_report = validate_registry(repo_root)
    registry: Registry | None = None
    skills: list[HealthSkillReport] = []
    registry_path = repo_root / "registry" / "skills.yaml"
    if registry_path.exists():
        try:
            registry = load_registry(registry_path)
        except Exception:  # noqa: BLE001 - validation report carries the specific failure.
            registry = None
    if registry is not None:
        for entry in registry.skills:
            try:
                manifest = load_skill_manifest(repo_root / entry.path)
            except Exception:  # noqa: BLE001 - invalid manifests are represented by validation findings.
                findings = validation_report.findings_for_skill(entry.id)
                skills.append(
                    HealthSkillReport(
                        id=entry.id,
                        name=entry.id,
                        version="unknown",
                        status="invalid",
                        risk_tier="unknown",
                        owner="unknown",
                        score=0,
                        findings=findings,
                        recommendations=["Fix manifest validation errors before health scoring."],
                    )
                )
                continue
            skill_validation = validate_skill_manifest(repo_root / entry.path, repo_root)
            existing_keys = {
                (f.level, f.code, f.message, f.path) for f in skill_validation.findings
            }
            new_findings = [
                f
                for f in validation_report.findings_for_skill(manifest.id)
                if (f.level, f.code, f.message, f.path) not in existing_keys
            ]
            skill_validation.findings.extend(new_findings)
            skills.append(calculate_skill_health(manifest, skill_validation))
    overall_score = round(sum(skill.score for skill in skills) / len(skills), 2) if skills else 0.0
    return HealthReport(
        registry_version=registry.version if registry else None,
        overall_score=overall_score,
        skills=skills,
        validation=validation_report,
    )


def write_health_report_json(report: HealthReport, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report.to_jsonable(), indent=2) + "\n", encoding="utf-8")


def write_health_report_markdown(report: HealthReport, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# SkillOps Health Report",
        "",
        f"Generated at: {report.generated_at.isoformat()}",
        f"Registry version: {report.registry_version}",
        f"Overall score: {report.overall_score}",
        "",
        "| Skill | Status | Risk | Score | Findings |",
        "| --- | --- | --- | ---: | ---: |",
    ]
    for skill in report.skills:
        row = (
            f"| {skill.id} | {skill.status} | {skill.risk_tier} "
            f"| {skill.score} | {len(skill.findings)} |"
        )
        lines.append(row)
    lines.extend(["", "## Recommendations", ""])
    for skill in report.skills:
        if skill.recommendations:
            lines.append(f"### {skill.id}")
            for recommendation in skill.recommendations:
                lines.append(f"- {recommendation}")
            lines.append("")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
