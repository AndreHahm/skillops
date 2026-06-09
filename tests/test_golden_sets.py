from __future__ import annotations

import json
import re
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
REQUIRED_CATEGORIES = {
    "happy_path",
    "edge_case",
    "invalid_input",
    "scope_creep",
    "safety_sensitive",
}
GOLDEN_SET_PATHS = {
    skill_id: ROOT / "evals" / "golden" / f"{skill_id}.yaml" for skill_id in CORE_SKILL_IDS
}
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$")
REAL_LOOKING_SECRET_RE = re.compile(
    r"(?i)(sk-[a-z0-9]{20,}|ghp_[a-z0-9]{20,}|xox[baprs]-[a-z0-9-]{20,}|"
    r"aws_secret_access_key\s*[:=]\s*[a-z0-9/+]{20,})"
)
# noinspection RegExpUnnecessaryNonCapturingGroup
LOCAL_USER_PATH_RE = re.compile(
    r"(?:/Users/[A-Za-z0-9._-]+|/home/[A-Za-z0-9._-]+|C:\\Users\\[A-Za-z0-9._-]+)"
)
PROHIBITED_CLAIMS = [
    "promptfoo execution is implemented",
    "deepeval execution is implemented",
    "production observability is implemented",
    "marketplace behavior is implemented",
    "dependency graph behavior is implemented",
    "self-improvement automation is implemented",
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


def _eval_suite_registry() -> dict[str, Any]:
    return _load_yaml(ROOT / "registry" / "eval-suites.yaml")


def _registered_core_skill_ids() -> set[str]:
    registry = _load_yaml(ROOT / "registry" / "skills.yaml")
    return {
        entry["id"]
        for entry in registry["skills"]
        if Path(entry["path"]).parts[:1] == ("skills",)
    }


def _all_golden_sets() -> dict[str, dict[str, Any]]:
    return {skill_id: _load_yaml(path) for skill_id, path in GOLDEN_SET_PATHS.items()}


def test_all_required_core_golden_set_files_exist() -> None:
    missing = [
        str(path.relative_to(ROOT)) for path in GOLDEN_SET_PATHS.values() if not path.is_file()
    ]
    assert missing == []


def test_all_core_golden_sets_validate_against_schema() -> None:
    validator = _golden_set_validator()
    for skill_id, path in GOLDEN_SET_PATHS.items():
        data = _load_yaml(path)
        validator.validate(data)
        assert data["skill_id"] == skill_id


def test_golden_sets_have_required_case_coverage_and_assertions() -> None:
    for skill_id, data in _all_golden_sets().items():
        cases = data["cases"]
        assert len(cases) >= 5, f"Skill '{skill_id}' must have at least 5 cases, found {len(cases)}"
        missing_categories = REQUIRED_CATEGORIES - {case["category"] for case in cases}
        assert not missing_categories, (
            f"Skill '{skill_id}' is missing required categories: {missing_categories}"
        )

        case_ids = [case["id"] for case in cases]
        duplicates = [cid for cid, count in Counter(case_ids).items() if count > 1]
        assert not duplicates, f"Skill '{skill_id}' has duplicate case IDs: {duplicates}"

        for case in cases:
            assert SLUG_RE.fullmatch(case["id"]), (
                f"Case ID '{case['id']}' in '{skill_id}' is not a valid slug"
            )
            assert case["input"].strip(), f"Case '{case['id']}' in '{skill_id}' has empty input"
            assert case["expected"]["contains"], (
                f"Case '{case['id']}' in '{skill_id}' has empty 'contains' assertions"
            )
            assert case["expected"]["not_contains"], (
                f"Case '{case['id']}' in '{skill_id}' has empty 'not_contains' assertions"
            )
            for reference in case["expected"].get("must_reference", []):
                assert reference.strip(), (
                    f"Case '{case['id']}' in '{skill_id}' has empty reference in 'must_reference'"
                )


def test_golden_set_skill_ids_correspond_to_registered_core_skills() -> None:
    registered_skill_ids = _registered_core_skill_ids()
    assert CORE_SKILL_IDS <= registered_skill_ids
    assert {data["skill_id"] for data in _all_golden_sets().values()} == CORE_SKILL_IDS


def test_eval_registry_references_all_core_golden_sets_once() -> None:
    suites = _eval_suite_registry()["eval_suites"]
    skill_counts = Counter(suite["skill_id"] for suite in suites)
    golden_sets_by_skill = {suite["skill_id"]: suite["golden_set"] for suite in suites}

    missing_skills = CORE_SKILL_IDS - set(skill_counts)
    extra_skills = set(skill_counts) - CORE_SKILL_IDS
    assert not missing_skills, f"Missing eval suites for core skills: {missing_skills}"
    assert not extra_skills, f"Unexpected eval suites for skills: {extra_skills}"

    duplicates = [sid for sid, count in skill_counts.items() if count > 1]
    assert not duplicates, f"Duplicate eval suites found for skills: {duplicates}"

    for skill_id in CORE_SKILL_IDS:
        expected_path = f"evals/golden/{skill_id}.yaml"
        assert golden_sets_by_skill[skill_id] == expected_path, (
            f"Expected golden set path '{expected_path}' for '{skill_id}', "
            f"got '{golden_sets_by_skill[skill_id]}'"
        )
        assert (ROOT / expected_path).is_file(), f"Golden set file not found: {expected_path}"


def test_eval_registry_does_not_reference_missing_promptfoo_or_deepeval_files() -> None:
    for suite in _eval_suite_registry()["eval_suites"]:
        promptfoo_config = suite.get("promptfoo_config")
        if promptfoo_config is not None:
            assert (ROOT / promptfoo_config).is_file(), (
                f"Promptfoo config file not found: {promptfoo_config}"
            )

        for deepeval_test in suite.get("deepeval_tests", []):
            assert (ROOT / deepeval_test).is_file(), (
                f"DeepEval test file not found: {deepeval_test}"
            )


def test_golden_sets_do_not_claim_future_runtime_systems_are_implemented() -> None:
    for path in GOLDEN_SET_PATHS.values():
        content = path.read_text(encoding="utf-8").lower()
        for claim in PROHIBITED_CLAIMS:
            assert claim not in content, f"Prohibited claim '{claim}' found in {path}"


def test_golden_sets_do_not_contain_real_looking_secrets_or_local_user_paths() -> None:
    for path in GOLDEN_SET_PATHS.values():
        content = path.read_text(encoding="utf-8")
        secret_match = REAL_LOOKING_SECRET_RE.search(content)
        assert secret_match is None, (
            f"Real-looking secret '{secret_match.group(0) if secret_match else ''}' found in {path}"
        )
        path_match = LOCAL_USER_PATH_RE.search(content)
        assert path_match is None, (
            f"Local user path '{path_match.group(0) if path_match else ''}' found in {path}"
        )
