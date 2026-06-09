"""CLI list command tests."""

from __future__ import annotations

from pathlib import Path

from skillops_cli.main import app
from typer.testing import CliRunner

REPO_ROOT = Path(__file__).resolve().parents[1]
runner = CliRunner()

CORE_SKILL_IDS = {
    "python-project-setup",
    "skill-manifest-authoring",
    "skill-registry-maintenance",
    "skill-health-review",
    "documentation-maintenance",
    "codebase-research",
}


def test_list_succeeds_for_current_repository() -> None:
    result = runner.invoke(app, ["list", "--repo-root", str(REPO_ROOT)])

    assert result.exit_code == 0
    for skill_id in CORE_SKILL_IDS:
        assert skill_id in result.output


def test_list_status_filter_succeeds() -> None:
    result = runner.invoke(app, ["list", "--repo-root", str(REPO_ROOT), "--status", "draft"])

    assert result.exit_code == 0
    assert "Registered Skills" in result.output


def test_list_risk_tier_filter_succeeds() -> None:
    result = runner.invoke(app, ["list", "--repo-root", str(REPO_ROOT), "--risk-tier", "low"])

    assert result.exit_code == 0
    assert "Registered Skills" in result.output
