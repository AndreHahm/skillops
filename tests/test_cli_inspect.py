"""CLI inspect command tests."""

from __future__ import annotations

from pathlib import Path

from skillops_cli.main import app
from typer.testing import CliRunner

REPO_ROOT = Path(__file__).resolve().parents[1]
runner = CliRunner()


def test_inspect_known_skill_succeeds() -> None:
    result = runner.invoke(
        app,
        ["inspect", "skill-registry-maintenance", "--repo-root", str(REPO_ROOT)],
    )

    assert result.exit_code == 0
    assert "skill-registry-maintenance" in result.output
    assert "Skill Registry Maintenance" in result.output
    assert "Owner" in result.output
    assert "Dependencies" in result.output
    assert "Validation Findings" in result.output


def test_inspect_unknown_skill_fails() -> None:
    result = runner.invoke(app, ["inspect", "does-not-exist", "--repo-root", str(REPO_ROOT)])

    assert result.exit_code == 1
    assert "not found" in result.output.lower()
