"""Tests for the Phase 2 evaluation CI smoke gate."""

from __future__ import annotations

import ast
import copy
import re
import shutil
from pathlib import Path
from typing import Any

import yaml
from skillops_cli.main import app
from skillops_core.eval_smoke import run_evaluation_smoke
from typer.testing import CliRunner

ROOT = Path(__file__).resolve().parents[1]
CI_WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"
JUSTFILE = ROOT / "justfile"
SMOKE_COMMAND = "uv run skillops eval --smoke"
runner = CliRunner()

SECRET_PATTERNS = [
    re.compile(r"sk-[a-z0-9]{20,}", re.IGNORECASE),
    re.compile(r"ghp_[a-z0-9]{20,}", re.IGNORECASE),
    re.compile(r"xox[baprs]-[a-z0-9-]{20,}", re.IGNORECASE),
    re.compile(r"aws_secret_access_key\s*=\s*['\"]?[a-z0-9/+=]{20,}", re.IGNORECASE),
]
LOCAL_USER_PATH_PATTERN = re.compile(
    r"(?:[A-Za-z]:\\Users\\[A-Za-z0-9._\- ]+|/(?:Users|home)/[A-Za-z0-9._-]+)"
)
FORBIDDEN_DOC_CLAIMS = [
    "production observability is implemented",
    "langfuse is integrated",
    "langfuse integration is implemented",
    "phoenix is integrated",
    "phoenix integration is implemented",
    "marketplace behavior is implemented",
    "self-improvement automation is implemented",
    "automatic skill patching is implemented",
]


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


def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def _workflow() -> dict[str, Any]:
    data = yaml.load(CI_WORKFLOW.read_text(encoding="utf-8"), Loader=GitHubActionsLoader)
    assert isinstance(data, dict)
    return data


def _workflow_text() -> str:
    return CI_WORKFLOW.read_text(encoding="utf-8")


def _copy_smoke_fixture(tmp_path: Path) -> Path:
    fixture_root = tmp_path / "repo"
    for relative in [
        "schemas",
        "registry",
        "evals",
        "docs/evaluation",
        "llm-wiki/concepts",
        ".github",
    ]:
        source = ROOT / relative
        target = fixture_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, target)
    for relative in ["README.md", "justfile", "pyproject.toml"]:
        target = fixture_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, target)
    return fixture_root


def test_eval_smoke_cli_command_exists_and_runs() -> None:
    result = runner.invoke(app, ["eval", "--smoke", "--repo-root", str(ROOT)])

    assert result.exit_code == 0
    assert "SkillOps Evaluation Smoke Check" in result.output
    assert "Evaluation smoke check completed" in result.output
    assert "Golden sets: 5 checked" in result.output
    assert "Eval suites: 5 checked" in result.output
    assert "Promptfoo configs: 6 checked" in result.output
    assert "DeepEval files: 5 checked" in result.output


def test_eval_command_requires_smoke_flag() -> None:
    result = runner.invoke(app, ["eval", "--repo-root", str(ROOT)])

    assert result.exit_code == 1
    assert "Only deterministic smoke evaluation is available" in result.output


def test_eval_smoke_fails_on_missing_required_reference(tmp_path: Path) -> None:
    fixture_root = _copy_smoke_fixture(tmp_path)
    registry_path = fixture_root / "registry" / "eval-suites.yaml"
    registry = _load_yaml(registry_path)
    registry["eval_suites"][0]["golden_set"] = "evals/golden/missing-python-project-setup.yaml"
    registry_path.write_text(yaml.safe_dump(registry, sort_keys=False), encoding="utf-8")

    result = run_evaluation_smoke(fixture_root)

    assert not result.passed
    assert any(
        finding.code == "eval_smoke.golden_set_missing" for finding in result.report.findings
    )


def test_ci_references_evaluation_smoke_and_phase_1_validation() -> None:
    text = _workflow_text()

    assert "Evaluation smoke check" in text
    assert SMOKE_COMMAND in text
    assert "uv run skillops validate" in text
    assert "uv run pytest" in text
    assert "uv run ruff check ." in text
    assert "uv run skillops health" in text


def test_justfile_has_eval_smoke_target() -> None:
    text = JUSTFILE.read_text(encoding="utf-8")

    assert "eval-smoke:" in text
    assert SMOKE_COMMAND in text


def test_ci_safety_boundaries_for_evaluation_gate() -> None:
    workflow = _workflow()
    text = _workflow_text().lower()

    assert "schedule" not in workflow["on"]
    assert "skillops_run_deepeval" not in text
    assert "secrets." not in text
    assert "api_key" not in text
    assert "langfuse" not in text
    assert "phoenix" not in text
    assert "promptfoo cloud" not in text
    assert "deepeval login" not in text
    assert "release" not in "\n".join(workflow.get("jobs", {}).keys()).lower()
    assert "deploy" not in "\n".join(workflow.get("jobs", {}).keys()).lower()
    assert "promptfoo" not in text or "promptfoo" not in text.split("actions/upload-artifact")[-1]
    assert "deepeval" not in text or "deepeval" not in text.split("actions/upload-artifact")[-1]


def test_promptfoo_config_references_are_parseable() -> None:
    registry = _load_yaml(ROOT / "registry" / "eval-suites.yaml")
    promptfoo_paths = {ROOT / "evals" / "promptfoo" / "promptfooconfig.yaml"}
    promptfoo_paths.update(ROOT / suite["promptfoo_config"] for suite in registry["eval_suites"])

    for path in promptfoo_paths:
        data = _load_yaml(path)
        assert isinstance(data.get("prompts"), list)
        assert isinstance(data.get("providers"), list)
        assert isinstance(data.get("tests"), list)


def test_deepeval_test_references_are_valid_and_guarded() -> None:
    registry = _load_yaml(ROOT / "registry" / "eval-suites.yaml")

    for suite in registry["eval_suites"]:
        for relative_path in suite["deepeval_tests"]:
            path = ROOT / relative_path
            source = path.read_text(encoding="utf-8")
            ast.parse(source, filename=str(path))
            assert "SKILLOPS_RUN_DEEPEVAL" in source
            assert "skipif" in source


def test_docs_mention_ci_smoke_gate_without_future_phase_overclaims() -> None:
    docs = [
        ROOT / "docs" / "evaluation" / "ci-gate.md",
        ROOT / "docs" / "evaluation" / "overview.md",
        ROOT / "docs" / "evaluation" / "skill-tdd.md",
        ROOT / "docs" / "evaluation" / "review-gates.md",
        ROOT / "evals" / "README.md",
        ROOT / "llm-wiki" / "concepts" / "evaluation.md",
        ROOT / "llm-wiki" / "concepts" / "skill-tdd.md",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in docs)

    assert "skillops eval --smoke" in combined
    assert "production observability is planned for phase 4" in combined
    assert "marketplace behavior is planned for phase 5" in combined
    assert "self-improvement automation is planned for phase 6" in combined
    for claim in FORBIDDEN_DOC_CLAIMS:
        assert claim not in combined


def test_no_real_looking_secrets_local_paths_or_stale_project_names_in_text_files() -> None:
    roots = [
        ROOT / ".github",
        ROOT / "docs",
        ROOT / "evals",
        ROOT / "llm-wiki",
        ROOT / "packages",
        ROOT / "registry",
        ROOT / "schemas",
        ROOT / "tests",
    ]
    files = [ROOT / "README.md", ROOT / "justfile", ROOT / "pyproject.toml"]
    for root in roots:
        files.extend(path for path in root.rglob("*") if path.is_file())

    stale_project_name = "agent" + "-skillops"
    for path in sorted(set(files)):
        text_suffixes = {".json", ".md", ".py", ".toml", ".yaml", ".yml"}
        if path.suffix not in text_suffixes and path.name != "justfile":
            continue
        content = path.read_text(encoding="utf-8")
        for pattern in SECRET_PATTERNS:
            assert pattern.search(content) is None, path
        assert LOCAL_USER_PATH_PATTERN.search(content) is None, path
        assert stale_project_name not in content.lower(), path
