"""Guarded DeepEval skeleton tests for the skill-manifest-authoring skill."""

from __future__ import annotations

import os

import pytest
from helpers import (
    REQUIRED_CATEGORIES,
    assert_expected_output,
    build_expected_output_checks,
    categories,
    deterministic_placeholder_output,
    filter_cases,
    golden_set_path,
    list_cases,
    load_golden_set,
    to_deepeval_test_case_kwargs,
)

SKILL_ID = "skill-manifest-authoring"
GOLDEN_SET_PATH = "evals/golden/skill-manifest-authoring.yaml"
DEEPEVAL_ENV_VAR = "SKILLOPS_RUN_DEEPEVAL"


def test_golden_set_loaded_for_skill_manifest_authoring() -> None:
    golden_set = load_golden_set(SKILL_ID)

    assert str(golden_set_path(SKILL_ID)).endswith(GOLDEN_SET_PATH)
    assert golden_set["skill_id"] == SKILL_ID
    assert list_cases(golden_set)


def test_required_categories_for_skill_manifest_authoring() -> None:
    golden_set = load_golden_set(SKILL_ID)

    assert REQUIRED_CATEGORIES <= categories(golden_set)


def test_deterministic_placeholder_output_for_skill_manifest_authoring() -> None:
    golden_set = load_golden_set(SKILL_ID)
    case = filter_cases(golden_set, "happy_path")[0]
    checks = build_expected_output_checks(case)
    output = deterministic_placeholder_output(case)

    assert_expected_output(output, checks)


@pytest.mark.skipif(
    os.getenv(DEEPEVAL_ENV_VAR) != "1",
    reason="Set SKILLOPS_RUN_DEEPEVAL=1 to run optional DeepEval construction smoke tests.",
)
def test_optional_deepeval_llm_test_case_construction_for_skill_manifest_authoring() -> None:
    # Future packages can replace this placeholder with captured system output.
    # This smoke test only constructs a DeepEval test case and performs local
    # deterministic assertions; it does not call a model provider or judge.
    pytest.importorskip("deepeval")
    from deepeval.test_case import LLMTestCase

    golden_set = load_golden_set(SKILL_ID)
    case = filter_cases(golden_set, "happy_path")[0]
    output = deterministic_placeholder_output(case)
    deepeval_kwargs = to_deepeval_test_case_kwargs(case, output)
    test_case = LLMTestCase(**deepeval_kwargs)

    assert test_case.input == deepeval_kwargs["input"]
    assert test_case.actual_output == output
    assert_expected_output(output, build_expected_output_checks(case))
