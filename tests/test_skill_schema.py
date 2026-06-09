from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError
from skillops_core.errors import SkillOpsValidationError
from skillops_core.loaders import load_skill_manifest

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).parent / "fixtures"
CORE_SKILL_MANIFESTS = [
    ROOT / "skills" / "python-project-setup" / "skill.yaml",
    ROOT / "skills" / "skill-manifest-authoring" / "skill.yaml",
    ROOT / "skills" / "skill-registry-maintenance" / "skill.yaml",
    ROOT / "skills" / "skill-health-review" / "skill.yaml",
    ROOT / "skills" / "documentation-maintenance" / "skill.yaml",
    ROOT / "skills" / "codebase-research" / "skill.yaml",
]


def _load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def _skill_schema_validator() -> Draft202012Validator:
    schema = _load_yaml(ROOT / "schemas" / "skill.schema.json")
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def test_valid_skill_manifest_loads() -> None:
    manifest = load_skill_manifest(FIXTURES / "valid_skill.yaml")
    assert manifest.id == "valid-skill"
    assert manifest.owner.name == "platform"


def test_valid_skill_fixture_validates_against_json_schema() -> None:
    validator = _skill_schema_validator()
    validator.validate(_load_yaml(FIXTURES / "valid_skill.yaml"))


def test_invalid_skill_without_owner_fails() -> None:
    with pytest.raises(SkillOpsValidationError):
        load_skill_manifest(FIXTURES / "invalid_skill_missing_owner.yaml")


def test_invalid_skill_without_owner_fails_json_schema_validation() -> None:
    validator = _skill_schema_validator()
    with pytest.raises(ValidationError):
        validator.validate(_load_yaml(FIXTURES / "invalid_skill_missing_owner.yaml"))


@pytest.mark.parametrize("manifest_path", CORE_SKILL_MANIFESTS)
def test_core_skill_manifests_validate_against_json_schema(manifest_path: Path) -> None:
    validator = _skill_schema_validator()
    validator.validate(_load_yaml(manifest_path))
