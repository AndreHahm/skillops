from pathlib import Path

import pytest
from skillops_core.errors import SkillOpsFileNotFoundError, SkillOpsValidationError
from skillops_core.loaders import load_skill_manifest, load_skills_registry, load_yaml

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).parent / "fixtures"


def test_load_yaml_loads_valid_yaml() -> None:
    data = load_yaml(FIXTURES / "valid_skill.yaml")

    assert data["id"] == "valid-skill"


def test_load_yaml_returns_empty_dict_for_empty_yaml(tmp_path: Path) -> None:
    path = tmp_path / "empty.yaml"
    path.write_text("", encoding="utf-8")

    assert load_yaml(path) == {}


def test_load_yaml_raises_file_not_found_for_missing_file(tmp_path: Path) -> None:
    with pytest.raises(SkillOpsFileNotFoundError):
        load_yaml(tmp_path / "missing.yaml")


def test_load_yaml_raises_validation_error_for_invalid_yaml(tmp_path: Path) -> None:
    path = tmp_path / "invalid.yaml"
    path.write_text(": : invalid: yaml: [", encoding="utf-8")

    with pytest.raises(SkillOpsValidationError):
        load_yaml(path)


def test_load_skill_manifest_loads_valid_fixture() -> None:
    manifest = load_skill_manifest(FIXTURES / "valid_skill.yaml")

    assert manifest.id == "valid-skill"


def test_load_skills_registry_loads_current_registry() -> None:
    registry = load_skills_registry(ROOT / "registry" / "skills.yaml")

    assert registry.version == 1
    assert len(registry.skills) == 5
