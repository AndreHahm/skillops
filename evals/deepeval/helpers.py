"""Local helper utilities for SkillOps DeepEval skeleton tests.

These helpers intentionally keep Golden Sets as the canonical scenario source.
They provide deterministic Python checks and optional DeepEval test-case inputs
without importing DeepEval or contacting model providers.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
GOLDEN_ROOT = REPO_ROOT / "evals" / "golden"
REQUIRED_CATEGORIES = {
    "happy_path",
    "edge_case",
    "invalid_input",
    "scope_creep",
    "safety_sensitive",
}


@dataclass(frozen=True)
class ExpectedOutputChecks:
    """Deterministic output checks derived from one Golden Set case."""

    contains: tuple[str, ...]
    not_contains: tuple[str, ...]
    must_reference: tuple[str, ...]


def golden_set_path(skill_id: str) -> Path:
    """Return the conventional Golden Set path for a skill ID."""

    return GOLDEN_ROOT / f"{skill_id}.yaml"


def load_golden_set(skill_id: str) -> dict[str, Any]:
    """Load a Golden Set YAML document for a skill ID."""

    path = golden_set_path(skill_id)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TypeError(f"Golden Set must be a YAML mapping: {path}")
    if data.get("skill_id") != skill_id:
        raise ValueError(f"Golden Set {path} does not match skill_id {skill_id!r}")
    return data


def list_cases(golden_set: dict[str, Any]) -> list[dict[str, Any]]:
    """Return the cases from a Golden Set mapping."""

    cases = golden_set.get("cases", [])
    if not isinstance(cases, list):
        raise TypeError("Golden Set cases must be a list")
    return cases


def filter_cases(golden_set: dict[str, Any], category: str) -> list[dict[str, Any]]:
    """Return Golden Set cases matching one category."""

    return [case for case in list_cases(golden_set) if case.get("category") == category]


def categories(golden_set: dict[str, Any]) -> set[str]:
    """Return all categories represented by a Golden Set."""

    return {str(case.get("category")) for case in list_cases(golden_set)}


def build_expected_output_checks(case: dict[str, Any]) -> ExpectedOutputChecks:
    """Build deterministic output checks from a Golden Set case."""

    expected = case.get("expected", {})
    if not isinstance(expected, dict):
        raise TypeError("Golden Set case expected block must be a mapping")
    return ExpectedOutputChecks(
        contains=tuple(str(value) for value in expected.get("contains", [])),
        not_contains=tuple(str(value) for value in expected.get("not_contains", [])),
        must_reference=tuple(str(value) for value in expected.get("must_reference", [])),
    )


def assert_expected_output(output: str, checks: ExpectedOutputChecks) -> None:
    """Apply deterministic Golden Set assertions to local or captured output."""

    for phrase in checks.contains:
        assert phrase in output
    for phrase in checks.must_reference:
        assert phrase in output
    for phrase in checks.not_contains:
        assert phrase not in output


def deterministic_placeholder_output(case: dict[str, Any]) -> str:
    """Create a local placeholder output satisfying one case's positive checks."""

    checks = build_expected_output_checks(case)
    return "\n".join((*checks.contains, *checks.must_reference))


def to_deepeval_test_case_kwargs(case: dict[str, Any], actual_output: str) -> dict[str, str]:
    """Convert a Golden Set case into keyword arguments for DeepEval LLMTestCase."""

    return {
        "input": str(case.get("input", "")),
        "actual_output": actual_output,
        "expected_output": deterministic_placeholder_output(case),
    }
