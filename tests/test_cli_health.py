"""CLI health command tests."""

from __future__ import annotations

import json
from pathlib import Path

from skillops_cli.main import app
from typer.testing import CliRunner

REPO_ROOT = Path(__file__).resolve().parents[1]
runner = CliRunner()


def test_health_no_write_succeeds() -> None:
    result = runner.invoke(app, ["health", "--repo-root", str(REPO_ROOT), "--no-write"])

    assert result.exit_code == 0
    assert "SkillOps Health" in result.output
    assert "Total Skills" in result.output
    assert "Average Health Score" in result.output


def test_health_writes_json_and_markdown_reports(tmp_path: Path) -> None:
    json_path = tmp_path / "health-report.json"
    markdown_path = tmp_path / "health-report.md"

    result = runner.invoke(
        app,
        [
            "health",
            "--repo-root",
            str(REPO_ROOT),
            "--json-path",
            str(json_path),
            "--markdown-path",
            str(markdown_path),
        ],
    )

    assert result.exit_code == 0
    assert "SkillOps Health" in result.output
    assert "Total Skills" in result.output
    assert "Average Health Score" in result.output
    data = json.loads(json_path.read_text(encoding="utf-8"))
    assert data["total_skills"] == 5
    assert "# Skill Health Report" in markdown_path.read_text(encoding="utf-8")
