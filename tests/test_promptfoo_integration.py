from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

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
PROMPTFOO_ROOT_CONFIG = ROOT / "evals" / "promptfoo" / "promptfooconfig.yaml"
PROMPTFOO_SKILL_DIR = ROOT / "evals" / "promptfoo" / "skills"
PROMPTFOO_DOC_PATHS = [
    ROOT / "evals" / "promptfoo" / "README.md",
    ROOT / "docs" / "evaluation" / "promptfoo.md",
    ROOT / "docs" / "evaluation" / "overview.md",
    ROOT / "docs" / "evaluation" / "skill-tdd.md",
    ROOT / "llm-wiki" / "concepts" / "evaluation.md",
    ROOT / "llm-wiki" / "concepts" / "skill-tdd.md",
]


def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict), path
    return data


def _golden_set(skill_id: str) -> dict[str, Any]:
    return _load_yaml(ROOT / "evals" / "golden" / f"{skill_id}.yaml")


def _skill_config_path(skill_id: str) -> Path:
    return PROMPTFOO_SKILL_DIR / f"{skill_id}.promptfooconfig.yaml"


def _skill_config(skill_id: str) -> dict[str, Any]:
    return _load_yaml(_skill_config_path(skill_id))


def _assertions(test: dict[str, Any], assertion_type: str) -> list[str]:
    values = []
    for assertion in test.get("assert", []):
        if assertion.get("type") == assertion_type:
            values.append(assertion.get("value"))
    return values


def test_promptfoo_root_and_skill_configs_exist_and_are_valid_yaml() -> None:
    assert PROMPTFOO_ROOT_CONFIG.is_file()
    _load_yaml(PROMPTFOO_ROOT_CONFIG)
    for skill_id in CORE_SKILL_IDS:
        path = _skill_config_path(skill_id)
        assert path.is_file(), path
        _load_yaml(path)


def test_root_promptfoo_config_is_local_smoke_only() -> None:
    config = _load_yaml(PROMPTFOO_ROOT_CONFIG)
    provider_ids = {provider["id"] for provider in config["providers"]}
    assert provider_ids == {"echo"}
    referenced_paths = {test["vars"]["promptfoo_config"] for test in config["tests"]}
    assert referenced_paths == {
        f"evals/promptfoo/skills/{skill_id}.promptfooconfig.yaml"
        for skill_id in CORE_SKILL_IDS
    }
    for referenced_path in referenced_paths:
        assert (ROOT / referenced_path).is_file()


def test_skill_promptfoo_configs_map_to_one_skill_and_required_categories() -> None:
    for skill_id in CORE_SKILL_IDS:
        config = _skill_config(skill_id)
        provider_ids = {provider["id"] for provider in config["providers"]}
        assert provider_ids == {"echo"}
        tests = config["tests"]
        assert len(tests) >= 5
        assert {test["metadata"]["skill_id"] for test in tests} == {skill_id}
        assert {test["metadata"]["category"] for test in tests} >= REQUIRED_CATEGORIES


def test_promptfoo_tests_align_with_golden_set_case_ids_and_categories() -> None:
    for skill_id in CORE_SKILL_IDS:
        golden_cases = {case["id"]: case for case in _golden_set(skill_id)["cases"]}
        config = _skill_config(skill_id)
        promptfoo_case_ids = {test["metadata"]["golden_case_id"] for test in config["tests"]}
        assert promptfoo_case_ids == set(golden_cases)
        for test in config["tests"]:
            metadata = test["metadata"]
            golden_case = golden_cases[metadata["golden_case_id"]]
            assert metadata["category"] == golden_case["category"]
            assert metadata["source_golden_set"] == f"evals/golden/{skill_id}.yaml"


def test_promptfoo_assertions_are_deterministic_and_derived_from_golden_sets() -> None:
    deterministic_types = {"contains", "not-contains", "regex", "not-regex", "is-json"}
    for skill_id in CORE_SKILL_IDS:
        golden_cases = {case["id"]: case for case in _golden_set(skill_id)["cases"]}
        for test in _skill_config(skill_id)["tests"]:
            assert test.get("assert"), test["description"]
            assert {assertion["type"] for assertion in test["assert"]} <= deterministic_types
            golden_case = golden_cases[test["metadata"]["golden_case_id"]]
            expected_contains = golden_case["expected"].get("contains", [])
            expected_not_contains = golden_case["expected"].get("not_contains", [])
            assert _assertions(test, "contains") == expected_contains
            if expected_not_contains:
                assert _assertions(test, "not-contains") == expected_not_contains


def test_registry_references_existing_promptfoo_configs_and_no_deepeval_files() -> None:
    registry = _load_yaml(ROOT / "registry" / "eval-suites.yaml")
    for suite in registry["eval_suites"]:
        assert suite["status"] == "draft"
        assert suite["deepeval_tests"] == []
        promptfoo_config = suite["promptfoo_config"]
        assert promptfoo_config == (
            f"evals/promptfoo/skills/{suite['skill_id']}.promptfooconfig.yaml"
        )
        assert (ROOT / promptfoo_config).is_file()


def test_promptfoo_configs_and_docs_do_not_commit_secrets_or_local_paths() -> None:
    files = [
        PROMPTFOO_ROOT_CONFIG,
        *[_skill_config_path(skill_id) for skill_id in CORE_SKILL_IDS],
        *PROMPTFOO_DOC_PATHS,
    ]
    secret_patterns = [
        re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
        re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9_./-]{12,}"),
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    ]
    local_path_patterns = [
        re.compile(r"/Users/[A-Za-z0-9._-]+"),
        re.compile(r"/home/[A-Za-z0-9._-]+"),
        re.compile(r"C:\\\\Users\\\\[A-Za-z0-9._-]+"),
    ]
    for path in files:
        content = path.read_text(encoding="utf-8")
        for pattern in secret_patterns + local_path_patterns:
            assert not pattern.search(content), path


def test_promptfoo_documentation_does_not_overclaim_future_behavior() -> None:
    prohibited_claims = [
        "deepeval execution is implemented",
        "production observability is implemented",
        "marketplace behavior is implemented",
        "self-improvement automation is implemented",
        "ci evaluation gate is implemented",
        "mandatory ci smoke evaluation gate is implemented",
    ]
    for path in PROMPTFOO_DOC_PATHS:
        content = path.read_text(encoding="utf-8").lower()
        for claim in prohibited_claims:
            assert claim not in content, path
