from pathlib import Path
from shutil import copytree

import pytest as pt
from skillops_core import validation
from skillops_core.validation import validate_registry, validate_skill_manifest

ROOT = Path(__file__).resolve().parents[1]


def test_registry_validation_succeeds_current_repository() -> None:
    report = validate_registry(ROOT)
    assert not report.has_errors


def test_duplicate_skill_ids_are_detected(tmp_path: Path) -> None:
    copytree(ROOT / "registry", tmp_path / "registry")
    copytree(ROOT / "skills", tmp_path / "skills")
    registry_path = tmp_path / "registry" / "skills.yaml"
    registry_path.write_text(
        registry_path.read_text(encoding="utf-8")
        + "\n  - id: python-project-setup\n    path: skills/python-project-setup/skill.yaml\n",
        encoding="utf-8",
    )
    report = validate_registry(tmp_path)
    assert any(finding.code == "duplicate-skill-id" for finding in report.findings)


def test_missing_skill_md_is_detected(tmp_path: Path) -> None:
    copytree(ROOT / "registry", tmp_path / "registry")
    copytree(ROOT / "skills", tmp_path / "skills")
    (tmp_path / "skills" / "python-project-setup" / "SKILL.md").unlink()
    report = validate_registry(tmp_path)
    assert any(finding.code == "missing-skill-doc" for finding in report.findings)


def test_invalid_registry_yaml_is_detected(tmp_path: Path) -> None:
    (tmp_path / "registry").mkdir()
    (tmp_path / "registry" / "skills.yaml").write_text(": : invalid: yaml: [", encoding="utf-8")
    report = validate_registry(tmp_path)
    assert any(finding.code == "invalid-registry-yaml" for finding in report.findings)


def test_unreadable_registry_is_io_error(tmp_path: Path, monkeypatch: pt.MonkeyPatch) -> None:
    (tmp_path / "registry").mkdir()
    (tmp_path / "registry" / "skills.yaml").write_text("placeholder", encoding="utf-8")

    def _raise_os_error(path: Path) -> dict:  # type: ignore[return]
        raise OSError("permission denied")

    monkeypatch.setattr(validation, "load_yaml", _raise_os_error)
    report = validate_registry(tmp_path)
    assert any(finding.code == "io-error" for finding in report.findings)


def test_skill_manifest_io_error_is_detected(tmp_path: Path, monkeypatch: pt.MonkeyPatch) -> None:
    skill_yaml = tmp_path / "skill.yaml"
    skill_yaml.write_text("placeholder", encoding="utf-8")

    def _raise_os_error(path: Path) -> dict:  # type: ignore[return]
        raise OSError("permission denied")

    monkeypatch.setattr(validation, "load_yaml", _raise_os_error)
    report = validate_skill_manifest(skill_yaml, tmp_path)
    assert any(finding.code == "io-error" for finding in report.findings)


def test_skill_manifest_invalid_yaml_is_detected(tmp_path: Path) -> None:
    skill_yaml = tmp_path / "skill.yaml"
    skill_yaml.write_text(": : invalid: yaml: [", encoding="utf-8")
    report = validate_skill_manifest(skill_yaml, tmp_path)
    assert any(finding.code == "invalid-skill-yaml" for finding in report.findings)
