from pathlib import Path

import pytest
import yaml
from skillops_core.errors import SkillOpsValidationError
from skillops_core.models import RegistrySkillEntry, SkillManifest, ValidationReport

FIXTURES = Path(__file__).parent / "fixtures"


def _load_fixture(name: str) -> dict:
    data = yaml.safe_load((FIXTURES / name).read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def test_valid_skill_fixture_parses_as_skill_manifest() -> None:
    manifest = SkillManifest.model_validate(_load_fixture("valid_skill.yaml"))

    assert manifest.id == "valid-skill"
    assert manifest.owner.name == "platform"


def test_invalid_missing_owner_fixture_raises_validation_error() -> None:
    with pytest.raises(SkillOpsValidationError):
        SkillManifest.model_validate(_load_fixture("invalid_skill_missing_owner.yaml"))


def test_invalid_bad_status_fixture_raises_validation_error() -> None:
    with pytest.raises(SkillOpsValidationError):
        SkillManifest.model_validate(_load_fixture("invalid_skill_bad_status.yaml"))


def test_registry_entry_path_must_end_with_skill_yaml() -> None:
    with pytest.raises(SkillOpsValidationError):
        RegistrySkillEntry.model_validate(
            {"id": "valid-skill", "path": "skills/valid/manifest.yaml"}
        )


def test_validation_report_counts_errors_warnings_and_info() -> None:
    report = ValidationReport()
    report.add_error("error.code", "An error")
    report.add_warning("warning.code", "A warning")
    report.add_info("info.code", "Some info")

    assert report.has_errors
    assert report.error_count == 1
    assert report.warning_count == 1
    assert report.info_count == 1
