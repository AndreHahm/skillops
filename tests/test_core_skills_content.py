"""Content checks for the five Phase 1 core skills."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from skillops_cli.main import app
from typer.testing import CliRunner

ROOT = Path(__file__).resolve().parents[1]
CORE_SKILL_IDS = (
    "python-project-setup",
    "skill-manifest-authoring",
    "skill-registry-maintenance",
    "skill-health-review",
    "documentation-maintenance",
)
REQUIRED_SECTIONS = (
    "Purpose",
    "When to Use",
    "Expected Outcome",
    "Inputs",
    "Procedure",
    "Quality Checklist",
    "Do",
    "Don't",
    "Examples",
    "Related Skills",
)
PYTHON_COMPATIBLE_ENVIRONMENTS = {"ubuntu-24.04", "windows-11-wsl2"}
runner = CliRunner()


def _skill_dir(skill_id: str) -> Path:
    return ROOT / "skills" / skill_id


def _load_manifest(skill_id: str) -> dict:
    data = yaml.safe_load((_skill_dir(skill_id) / "skill.yaml").read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


@pytest.mark.parametrize("skill_id", CORE_SKILL_IDS)
def test_core_skill_folder_and_required_files_exist(skill_id: str) -> None:
    skill_dir = _skill_dir(skill_id)

    assert skill_dir.is_dir()
    assert (skill_dir / "SKILL.md").is_file()
    assert (skill_dir / "skill.yaml").is_file()


@pytest.mark.parametrize("skill_id", CORE_SKILL_IDS)
def test_core_skill_markdown_has_frontmatter_and_required_sections(skill_id: str) -> None:
    skill_md = (_skill_dir(skill_id) / "SKILL.md").read_text(encoding="utf-8")

    assert skill_md.startswith("---\n")
    parts = skill_md.split("---", maxsplit=2)
    assert len(parts) >= 3
    frontmatter = yaml.safe_load(parts[1])
    assert isinstance(frontmatter, dict)
    assert "name" in frontmatter
    assert "description" in frontmatter
    for section in REQUIRED_SECTIONS:
        assert f"## {section}" in skill_md


@pytest.mark.parametrize("skill_id", CORE_SKILL_IDS)
def test_core_skill_markdown_avoids_placeholders_and_stale_names(skill_id: str) -> None:
    skill_md = (_skill_dir(skill_id) / "SKILL.md").read_text(encoding="utf-8")

    placeholder = "TO" + "DO"
    stale_name = "agent" + "-skillops"

    assert placeholder not in skill_md
    assert stale_name not in skill_md


@pytest.mark.parametrize("skill_id", CORE_SKILL_IDS)
def test_core_skill_manifest_keeps_package_five_baseline_values(skill_id: str) -> None:
    manifest = _load_manifest(skill_id)

    assert manifest["id"] == skill_id
    assert manifest["version"] == "0.1.0"
    assert manifest["status"] == "draft"
    assert manifest["provenance"] == {"source": "internal", "license": "MIT"}
    assert manifest["paths"]["skill_file"] == "SKILL.md"
    assert manifest["compatibility"]["agents"] == ["claude-code", "codex"]
    assert set(manifest["compatibility"]["environments"]) == PYTHON_COMPATIBLE_ENVIRONMENTS


@pytest.mark.parametrize("skill_id", CORE_SKILL_IDS)
def test_core_skill_files_do_not_introduce_python_less_than_313_references(skill_id: str) -> None:
    combined_text = (
        (_skill_dir(skill_id) / "SKILL.md").read_text(encoding="utf-8")
        + "\n"
        + (_skill_dir(skill_id) / "skill.yaml").read_text(encoding="utf-8")
    )

    forbidden_python_references = (
        "Python 3." + "12",
        "python 3." + "12",
        "py3" + "12",
        "requires-python = \"<3." + "13",
    )
    for reference in forbidden_python_references:
        assert reference not in combined_text


def test_core_skill_registry_validation_passes_through_cli() -> None:
    result = runner.invoke(app, ["validate", "--repo-root", str(ROOT)])

    assert result.exit_code == 0
    assert "PASS" in result.output
