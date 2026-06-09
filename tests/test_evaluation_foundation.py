from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CORE_SKILL_IDS = {
    "python-project-setup",
    "skill-manifest-authoring",
    "skill-registry-maintenance",
    "skill-health-review",
    "documentation-maintenance",
}
GOLDEN_SET_PATHS = {
    skill_id: ROOT / "evals" / "golden" / f"{skill_id}.yaml" for skill_id in CORE_SKILL_IDS
}
EVALUATION_DOC_PATHS = [
    ROOT / "evals" / "README.md",
    ROOT / "evals" / "golden" / "README.md",
    ROOT / "evals" / "promptfoo" / "README.md",
    ROOT / "evals" / "deepeval" / "README.md",
    ROOT / "evals" / "redteam" / "README.md",
    ROOT / "docs" / "evaluation" / "overview.md",
    ROOT / "docs" / "evaluation" / "golden-sets.md",
    ROOT / "docs" / "evaluation" / "review-gates.md",
    ROOT / "docs" / "evaluation" / "skill-tdd.md",
    ROOT / "llm-wiki" / "concepts" / "evaluation.md",
    ROOT / "llm-wiki" / "concepts" / "skill-tdd.md",
]


def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def _load_json_schema(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    Draft202012Validator.check_schema(data)
    return data


def _golden_set_validator():
    return Draft202012Validator(_load_json_schema(ROOT / "schemas" / "golden-set.schema.json"))


def _eval_suite_validator():
    return Draft202012Validator(_load_json_schema(ROOT / "schemas" / "eval-suite.schema.json"))


def _eval_suite_registry() -> dict[str, Any]:
    return _load_yaml(ROOT / "registry" / "eval-suites.yaml")


def test_evaluation_directory_structure_exists() -> None:
    expected_directories = [
        ROOT / "evals",
        ROOT / "evals" / "golden",
        ROOT / "evals" / "promptfoo",
        ROOT / "evals" / "deepeval",
        ROOT / "evals" / "redteam",
    ]
    expected_files = [
        ROOT / "evals" / "README.md",
        ROOT / "evals" / "golden" / "README.md",
        ROOT / "evals" / "promptfoo" / "README.md",
        ROOT / "evals" / "deepeval" / "README.md",
        ROOT / "evals" / "redteam" / "README.md",
        ROOT / "evals" / "redteam" / "phase-2-redteam-seeds.yaml",
    ]
    assert all(path.is_dir() for path in expected_directories)
    assert all(path.is_file() for path in expected_files)


def test_all_core_golden_set_files_exist() -> None:
    assert all(path.is_file() for path in GOLDEN_SET_PATHS.values())


def test_evaluation_schemas_exist_and_are_valid_json_schema() -> None:
    _load_json_schema(ROOT / "schemas" / "golden-set.schema.json")
    _load_json_schema(ROOT / "schemas" / "eval-suite.schema.json")


def test_golden_sets_validate_against_schema_and_cover_core_skills() -> None:
    validator = _golden_set_validator()
    seen_skill_ids = set()

    for skill_id, path in GOLDEN_SET_PATHS.items():
        data = _load_yaml(path)
        validator.validate(data)
        seen_skill_ids.add(data["skill_id"])
        assert data["skill_id"] == skill_id
        categories = {case["category"] for case in data["cases"]}
        assert "happy_path" in categories
        assert categories & {"edge_case", "invalid_input", "scope_creep"}
        case_ids = [case["id"] for case in data["cases"]]
        assert len(case_ids) == len(set(case_ids))

    assert seen_skill_ids == CORE_SKILL_IDS


def test_eval_suite_registry_validates_against_schema() -> None:
    _eval_suite_validator().validate(_eval_suite_registry())


def test_each_core_skill_has_exactly_one_eval_suite_entry() -> None:
    suites = _eval_suite_registry()["eval_suites"]
    skill_id_counts = Counter(suite["skill_id"] for suite in suites)
    assert set(skill_id_counts) == CORE_SKILL_IDS
    assert all(count == 1 for count in skill_id_counts.values())


def test_eval_suites_reference_existing_golden_sets_and_registered_skills() -> None:
    registered_skill_ids = {
        entry["id"] for entry in _load_yaml(ROOT / "registry" / "skills.yaml")["skills"]
    }
    for suite in _eval_suite_registry()["eval_suites"]:
        assert suite["skill_id"] in registered_skill_ids
        golden_set = ROOT / suite["golden_set"]
        assert golden_set.is_file()
        golden_data = _load_yaml(golden_set)
        assert golden_data["skill_id"] == suite["skill_id"]


def test_eval_suites_do_not_reference_missing_promptfoo_or_deepeval_files() -> None:
    for suite in _eval_suite_registry()["eval_suites"]:
        promptfoo_config = suite["promptfoo_config"]
        assert promptfoo_config is None
        for deepeval_path in suite["deepeval_tests"]:
            assert (ROOT / deepeval_path).is_file()
        assert suite["deepeval_tests"] == []
        assert suite["status"] in {"planned", "draft"}


def test_evaluation_docs_do_not_claim_future_execution_or_observability() -> None:
    prohibited_claims = [
        "skillops now evaluates skills with promptfoo",
        "skillops now evaluates skills with deepeval",
        "promptfoo execution is implemented",
        "deepeval execution is implemented",
        "production observability is implemented",
        "marketplace behavior is implemented",
        "dependency graph behavior is implemented",
        "self-improvement automation is implemented",
    ]
    for path in EVALUATION_DOC_PATHS:
        assert path.is_file(), f"Required documentation file does not exist: {path}"
        content = path.read_text(encoding="utf-8").lower()
        for claim in prohibited_claims:
            assert claim not in content, path


def test_no_future_runtime_behavior_files_were_added() -> None:
    assert sorted(
        p.name for p in (ROOT / "evals" / "promptfoo").iterdir() if not p.name.startswith(".")
    ) == ["README.md"]
    assert sorted(
        p.name for p in (ROOT / "evals" / "deepeval").iterdir() if not p.name.startswith(".")
    ) == ["README.md"]
    assert not (ROOT / "packages" / "skillops-cli" / "src" / "skillops_cli" / "eval.py").exists()
    assert not (ROOT / "registry" / "marketplace.yaml").exists()
    assert not (ROOT / "registry" / "dependency-graph.yaml").exists()
    assert not (ROOT / "registry" / "self-improvement.yaml").exists()
