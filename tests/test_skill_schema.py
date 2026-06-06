from pathlib import Path

import pytest
from skillops_core.models import ModelValidationError
from skillops_core.validation import load_skill_manifest

FIXTURES = Path(__file__).parent / "fixtures"


def test_valid_skill_manifest_loads() -> None:
    manifest = load_skill_manifest(FIXTURES / "valid_skill.yaml")
    assert manifest.id == "valid-skill"
    assert manifest.owner.name == "platform"


def test_invalid_skill_without_owner_fails() -> None:
    with pytest.raises(ModelValidationError):
        load_skill_manifest(FIXTURES / "invalid_skill_missing_owner.yaml")
