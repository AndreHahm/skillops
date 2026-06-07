import json
from pathlib import Path

from skillops_core.health import (
    calculate_skill_health,
    generate_health_report,
    write_health_report_json,
    write_health_report_markdown,
)
from skillops_core.loaders import load_skill_manifest
from skillops_core.models import ValidationReport

ROOT = Path(__file__).resolve().parents[1]


def test_health_score_is_calculated() -> None:
    manifest = load_skill_manifest(ROOT / "skills" / "skill-registry-maintenance" / "skill.yaml")
    report = calculate_skill_health(manifest, ValidationReport())
    assert report.score == 90
    assert report.status == "draft"


def test_health_report_json_and_markdown_can_be_generated(tmp_path: Path) -> None:
    report = generate_health_report(ROOT)
    json_path = tmp_path / "health-report.json"
    markdown_path = tmp_path / "health-report.md"
    write_health_report_json(report, json_path)
    write_health_report_markdown(report, markdown_path)
    assert json.loads(json_path.read_text(encoding="utf-8"))["skills"]
    assert "Skill Health Report" in markdown_path.read_text(encoding="utf-8")
