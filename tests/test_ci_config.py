"""Tests for the Phase 1 GitHub Actions CI workflow."""

from __future__ import annotations

import copy
import re
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
CI_WORKFLOW = REPO_ROOT / ".github/workflows/ci.yml"
PYTHON_VERSION_PATTERN = re.compile(r"python-version:\s*[\"']?(\d+(?:\.\d+)*)")
LOWER_PYTHON_PATTERN = re.compile(r"python-version:\s*[\"']?(?:2\.|3\.(?:[0-9]|1[0-2])(?:\D|$))")
FORBIDDEN_SCOPE_PATTERN = re.compile(
    r"\b(release|deploy|deployment|publish|pypi|ghcr|pages|marketplace)\b",
    re.IGNORECASE,
)
SECRET_PATTERN = re.compile(
    r"(?i)(api[_-]?key|access[_-]?token|secret[_-]?key|private[_-]?key|bearer\s+[a-z0-9])"
)


class GitHubActionsLoader(yaml.SafeLoader):
    """YAML loader that keeps GitHub Actions' `on` key as a string."""


GitHubActionsLoader.yaml_implicit_resolvers = copy.deepcopy(
    yaml.SafeLoader.yaml_implicit_resolvers
)
for first_char, resolvers in list(GitHubActionsLoader.yaml_implicit_resolvers.items()):
    GitHubActionsLoader.yaml_implicit_resolvers[first_char] = [
        (tag, regexp)
        for tag, regexp in resolvers
        if tag != "tag:yaml.org,2002:bool"
    ]


def load_workflow() -> dict[str, Any]:
    """Load the GitHub Actions workflow as YAML."""

    return yaml.load(CI_WORKFLOW.read_text(), Loader=GitHubActionsLoader)


def workflow_text() -> str:
    """Return the workflow text."""

    return CI_WORKFLOW.read_text()


def test_ci_workflow_exists() -> None:
    assert CI_WORKFLOW.exists()


def test_ci_workflow_yaml_is_valid() -> None:
    workflow = load_workflow()
    assert isinstance(workflow, dict)
    assert workflow["name"] == "CI"


def test_ci_workflow_runs_on_pull_requests() -> None:
    workflow = load_workflow()
    assert "pull_request" in workflow["on"]


def test_ci_workflow_runs_on_push_to_main() -> None:
    workflow = load_workflow()
    assert workflow["on"]["push"]["branches"] == ["main"]


def test_ci_workflow_uses_python_313() -> None:
    assert 'python-version: "3.13"' in workflow_text()


def test_ci_workflow_uses_uv() -> None:
    text = workflow_text()
    assert "astral-sh/setup-uv" in text
    assert "uv sync --all-packages --dev" in text


def test_ci_workflow_runs_required_checks() -> None:
    text = workflow_text()
    assert "uv run ruff check ." in text
    assert "uv run pytest" in text
    assert "uv run skillops validate" in text
    assert "uv run skillops health" in text
    assert "markdownlint" in text


def test_ci_workflow_uploads_health_report_artifacts() -> None:
    text = workflow_text()
    assert "actions/upload-artifact" in text
    assert "reports/health/health-report.json" in text
    assert "reports/health/health-report.md" in text
    assert "if-no-files-found: ignore" in text


def test_ci_workflow_does_not_contain_release_or_deployment_jobs() -> None:
    workflow = load_workflow()
    job_names = "\n".join(workflow.get("jobs", {}).keys())
    assert not FORBIDDEN_SCOPE_PATTERN.search(job_names)


def test_ci_workflow_does_not_reference_python_versions_lower_than_313() -> None:
    assert not LOWER_PYTHON_PATTERN.search(workflow_text())
    assert PYTHON_VERSION_PATTERN.findall(workflow_text()) == ["3.13"]


def test_ci_workflow_does_not_contain_secrets_or_real_tokens() -> None:
    assert not SECRET_PATTERN.search(workflow_text())
    assert "secrets." not in workflow_text()
