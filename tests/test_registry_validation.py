from pathlib import Path
from shutil import copytree

from skillops_core.validation import validate_registry

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
