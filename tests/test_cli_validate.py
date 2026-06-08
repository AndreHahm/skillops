"""CLI validation command tests."""

from __future__ import annotations

from pathlib import Path

from skillops_cli.main import app
from typer.testing import CliRunner

REPO_ROOT = Path(__file__).resolve().parents[1]
runner = CliRunner()


def test_validate_succeeds_for_current_repository() -> None:
    result = runner.invoke(app, ["validate", "--repo-root", str(REPO_ROOT)])

    assert result.exit_code == 0
    assert "SkillOps Validation" in result.output
    assert "Errors" in result.output
    assert "Warnings" in result.output
    assert "Result" in result.output
    assert "PASS" in result.output


def test_validate_strict_fails_when_warnings_exist() -> None:
    result = runner.invoke(app, ["validate", "--repo-root", str(REPO_ROOT), "--strict"])

    assert result.exit_code == 1
    assert "SkillOps Validation" in result.output
    assert "Warnings" in result.output
    assert "Result" in result.output
    assert "FAIL" in result.output


def test_validate_returns_nonzero_for_invalid_registry(tmp_path: Path) -> None:
    registry_dir = tmp_path / "registry"
    registry_dir.mkdir()
    (registry_dir / "skills.yaml").write_text("version: [\n", encoding="utf-8")

    result = runner.invoke(app, ["validate", "--repo-root", str(tmp_path)])

    assert result.exit_code == 1
    assert "SkillOps Validation" in result.output
    assert "Errors" in result.output
    assert "Result" in result.output
    assert "FAIL" in result.output
