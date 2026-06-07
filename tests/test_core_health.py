import json
from pathlib import Path

from skillops_core.health import (
    calculate_skill_health,
    generate_health_report,
    write_health_report_json,
    write_health_report_markdown,
)
from skillops_core.loaders import load_skill_manifest
from skillops_core.validation import validate_skill_manifest

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).parent / "fixtures"


def _valid_draft_manifest_with_skill_md(tmp_path: Path):
    manifest_path = tmp_path / "skill.yaml"
    manifest_path.write_text(
        (FIXTURES / "valid_skill.yaml").read_text(encoding="utf-8"), encoding="utf-8"
    )
    (tmp_path / "SKILL.md").write_text("# Valid Skill\n", encoding="utf-8")
    return manifest_path, load_skill_manifest(manifest_path)


def test_calculate_skill_health_returns_expected_score_for_valid_draft_skill(
    tmp_path: Path,
) -> None:
    manifest_path, manifest = _valid_draft_manifest_with_skill_md(tmp_path)
    validation_report = validate_skill_manifest(manifest_path, tmp_path)

    health = calculate_skill_health(manifest, validation_report, manifest_path)

    assert health.score == 90


def test_draft_skill_does_not_receive_status_not_draft_points(tmp_path: Path) -> None:
    manifest_path, manifest = _valid_draft_manifest_with_skill_md(tmp_path)
    validation_report = validate_skill_manifest(manifest_path, tmp_path)

    health = calculate_skill_health(manifest, validation_report, manifest_path)

    assert manifest.status == "draft"
    assert health.score == 90
    assert "Skill is still draft." in health.warnings


def test_missing_eval_suite_is_warning_but_keeps_eval_field_points(tmp_path: Path) -> None:
    manifest_path, manifest = _valid_draft_manifest_with_skill_md(tmp_path)
    validation_report = validate_skill_manifest(manifest_path, tmp_path)

    health = calculate_skill_health(manifest, validation_report, manifest_path)

    assert "Evaluation suite is not configured." in health.warnings
    assert health.score == 90


def test_generate_health_report_returns_five_skills_for_current_repository() -> None:
    report = generate_health_report(ROOT)

    assert report.total_skills == 5
    assert len(report.skills) == 5


def test_write_health_report_json_writes_valid_json(tmp_path: Path) -> None:
    report = generate_health_report(ROOT)
    path = tmp_path / "health-report.json"

    write_health_report_json(report, path)

    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["total_skills"] == 5
    assert "average_health_score" in data


def test_write_health_report_markdown_writes_expected_headings(tmp_path: Path) -> None:
    report = generate_health_report(ROOT)
    path = tmp_path / "health-report.md"

    write_health_report_markdown(report, path)

    markdown = path.read_text(encoding="utf-8")
    assert "# Skill Health Report" in markdown
    assert "## Summary" in markdown
    assert "## Skills" in markdown
