from pathlib import Path
from shutil import copytree

import yaml
from skillops_core.validation import validate_skill_manifest, validate_skills_registry

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).parent / "fixtures"


def _codes(report) -> set[str]:
    return {finding.code for finding in report.findings}


def _write_yaml(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def _copy_current_repo_registry_and_skills(tmp_path: Path) -> Path:
    copytree(ROOT / "registry", tmp_path / "registry")
    copytree(ROOT / "skills", tmp_path / "skills")
    return tmp_path


def test_validate_skill_manifest_returns_no_errors_for_valid_skill_with_skill_md(
    tmp_path: Path,
) -> None:
    manifest_path = tmp_path / "skill.yaml"
    manifest_path.write_text(
        (FIXTURES / "valid_skill.yaml").read_text(encoding="utf-8"), encoding="utf-8"
    )
    (tmp_path / "SKILL.md").write_text("# Valid Skill\n", encoding="utf-8")

    report = validate_skill_manifest(manifest_path, tmp_path)

    assert not report.has_errors


def test_validate_skill_manifest_detects_missing_skill_md(tmp_path: Path) -> None:
    manifest_path = tmp_path / "skill.yaml"
    manifest_path.write_text(
        (FIXTURES / "valid_skill.yaml").read_text(encoding="utf-8"), encoding="utf-8"
    )

    report = validate_skill_manifest(manifest_path, tmp_path)

    assert "skill_file.missing" in _codes(report)


def test_validate_skill_manifest_detects_invalid_manifest_schema() -> None:
    report = validate_skill_manifest(FIXTURES / "invalid_skill_bad_status.yaml", ROOT)

    assert "manifest.invalid_schema" in _codes(report)


def test_validate_skills_registry_succeeds_for_current_repository() -> None:
    report = validate_skills_registry(ROOT)

    assert not report.has_errors


def test_validate_skills_registry_detects_duplicate_skill_ids(tmp_path: Path) -> None:
    repo = _copy_current_repo_registry_and_skills(tmp_path)
    registry_path = repo / "registry" / "skills.yaml"
    registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
    registry["skills"].append(registry["skills"][0])
    _write_yaml(registry_path, registry)

    report = validate_skills_registry(repo)

    assert "registry.duplicate_skill_id" in _codes(report)


def test_validate_skills_registry_detects_missing_skill_path(tmp_path: Path) -> None:
    repo = _copy_current_repo_registry_and_skills(tmp_path)
    registry_path = repo / "registry" / "skills.yaml"
    registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
    registry["skills"][0]["path"] = "skills/missing-skill/skill.yaml"
    _write_yaml(registry_path, registry)

    report = validate_skills_registry(repo)

    assert "registry.skill_path_missing" in _codes(report)


def test_validate_skills_registry_detects_registry_manifest_id_mismatch(tmp_path: Path) -> None:
    repo = _copy_current_repo_registry_and_skills(tmp_path)
    manifest_path = repo / "skills" / "python-project-setup" / "skill.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest["id"] = "different-skill"
    _write_yaml(manifest_path, manifest)

    report = validate_skills_registry(repo)

    assert "registry.skill_id_mismatch" in _codes(report)


def test_validate_skills_registry_detects_missing_required_core_skill(tmp_path: Path) -> None:
    repo = _copy_current_repo_registry_and_skills(tmp_path)
    registry_path = repo / "registry" / "skills.yaml"
    registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
    registry["skills"] = [
        entry for entry in registry["skills"] if entry["id"] != "python-project-setup"
    ]
    _write_yaml(registry_path, registry)

    report = validate_skills_registry(repo)

    assert "registry.required_skill_missing" in _codes(report)


def test_validate_skills_registry_detects_unexpected_extra_skill(tmp_path: Path) -> None:
    repo = _copy_current_repo_registry_and_skills(tmp_path)
    extra_dir = repo / "skills" / "unexpected-skill"
    extra_dir.mkdir()
    manifest = yaml.safe_load((FIXTURES / "valid_skill.yaml").read_text(encoding="utf-8"))
    manifest["id"] = "unexpected-skill"
    _write_yaml(extra_dir / "skill.yaml", manifest)
    (extra_dir / "SKILL.md").write_text("# Unexpected Skill\n", encoding="utf-8")
    registry_path = repo / "registry" / "skills.yaml"
    registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
    registry["skills"].append(
        {"id": "unexpected-skill", "path": "skills/unexpected-skill/skill.yaml"}
    )
    _write_yaml(registry_path, registry)

    report = validate_skills_registry(repo)

    assert "registry.unexpected_skill" in _codes(report)
