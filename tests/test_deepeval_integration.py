from __future__ import annotations

import ast
import importlib.util
import re
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEEPEVAL_DIR = ROOT / "evals" / "deepeval"
CORE_DEEPEVAL_TESTS = {
    "python-project-setup": DEEPEVAL_DIR / "test_python_project_setup.py",
    "skill-manifest-authoring": DEEPEVAL_DIR / "test_skill_manifest_authoring.py",
    "skill-registry-maintenance": DEEPEVAL_DIR / "test_skill_registry_maintenance.py",
    "skill-health-review": DEEPEVAL_DIR / "test_skill_health_review.py",
    "documentation-maintenance": DEEPEVAL_DIR / "test_documentation_maintenance.py",
}
REQUIRED_CATEGORIES = {
    "happy_path",
    "edge_case",
    "invalid_input",
    "scope_creep",
    "safety_sensitive",
}
DEEPEVAL_SUPPORT_FILES = [
    DEEPEVAL_DIR / "README.md",
    DEEPEVAL_DIR / "conftest.py",
    DEEPEVAL_DIR / "helpers.py",
]
DEEPEVAL_DOC_PATHS = [
    DEEPEVAL_DIR / "README.md",
    ROOT / "docs" / "evaluation" / "deepeval.md",
    ROOT / "docs" / "evaluation" / "overview.md",
    ROOT / "docs" / "evaluation" / "skill-tdd.md",
    ROOT / "llm-wiki" / "concepts" / "evaluation.md",
    ROOT / "llm-wiki" / "concepts" / "skill-tdd.md",
]
REAL_LOOKING_SECRET_RE = re.compile(
    r"(?i)(sk-[a-z0-9_-]{20,}|ghp_[a-z0-9]{20,}|xox[baprs]-[a-z0-9-]{20,}|"
    r"aws_secret_access_key\s*[:=]\s*[a-z0-9/+]{20,})"
)
# noinspection RegExpUnnecessaryNonCapturingGroup
LOCAL_USER_PATH_RE = re.compile(
    r"(?:/Users/[A-Za-z0-9._-]+|/home/[A-Za-z0-9._-]+|C:\\Users\\[A-Za-z0-9._-]+)"
)
PROHIBITED_NETWORK_MARKERS = [
    "requests.",
    "httpx.",
    "urllib.request",
    "socket.",
    "aiohttp.",
]
PROHIBITED_DOC_CLAIMS = [
    "production observability is implemented",
    "langfuse integration is implemented",
    "phoenix integration is implemented",
    "marketplace behavior is implemented",
    "self-improvement automation is implemented",
    "automatic patching is implemented",
    "ci evaluation gate is implemented",
]


def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict), path
    return data


def _import_python_file(path: Path) -> ModuleType:
    sys.path.insert(0, str(DEEPEVAL_DIR))
    try:
        spec = importlib.util.spec_from_file_location(f"_skillops_deepeval_{path.stem}", path)
        assert spec is not None
        assert spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        try:
            sys.path.remove(str(DEEPEVAL_DIR))
        except ValueError:
            pass


def test_deepeval_support_files_exist() -> None:
    for path in DEEPEVAL_SUPPORT_FILES:
        assert path.is_file(), path


def test_all_core_skill_deepeval_test_files_exist() -> None:
    for path in CORE_DEEPEVAL_TESTS.values():
        assert path.is_file(), path


def test_deepeval_python_files_are_valid_python() -> None:
    for path in [*DEEPEVAL_SUPPORT_FILES[1:], *CORE_DEEPEVAL_TESTS.values()]:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def test_deepeval_test_files_reference_expected_skill_and_golden_set() -> None:
    for skill_id, path in CORE_DEEPEVAL_TESTS.items():
        content = path.read_text(encoding="utf-8")
        assert f'SKILL_ID = "{skill_id}"' in content
        assert f'GOLDEN_SET_PATH = "evals/golden/{skill_id}.yaml"' in content
        assert "load_golden_set(SKILL_ID)" in content


def test_deepeval_test_files_are_guarded_against_mandatory_external_model_calls() -> None:
    for path in CORE_DEEPEVAL_TESTS.values():
        content = path.read_text(encoding="utf-8")
        assert "SKILLOPS_RUN_DEEPEVAL" in content
        assert "os.getenv" in content
        split_content = re.split(r"""pytest\.importorskip\(["']deepeval["']\)""", content)
        assert len(split_content) > 1, f"Missing pytest.importorskip('deepeval') guard in {path}"
        assert "from deepeval" not in split_content[0], (
            f"Import from deepeval must be after the importorskip guard in {path}"
        )
        assert "judge" in content.lower()
        for marker in PROHIBITED_NETWORK_MARKERS:
            assert marker not in content, path


def test_deepeval_test_files_import_without_live_credentials() -> None:
    for path in CORE_DEEPEVAL_TESTS.values():
        module = _import_python_file(path)
        assert module.DEEPEVAL_ENV_VAR == "SKILLOPS_RUN_DEEPEVAL"


def test_deepeval_helpers_align_with_all_golden_sets() -> None:
    helpers = _import_python_file(DEEPEVAL_DIR / "helpers.py")
    for skill_id in CORE_DEEPEVAL_TESTS:
        golden_set = helpers.load_golden_set(skill_id)
        assert golden_set["skill_id"] == skill_id
        assert helpers.REQUIRED_CATEGORIES <= helpers.categories(golden_set)
        happy_path_case = helpers.filter_cases(golden_set, "happy_path")[0]
        output = helpers.deterministic_placeholder_output(happy_path_case)
        helpers.assert_expected_output(
            output, helpers.build_expected_output_checks(happy_path_case)
        )


def test_registry_references_all_deepeval_tests_and_preserves_promptfoo_configs() -> None:
    registry = _load_yaml(ROOT / "registry" / "eval-suites.yaml")
    referenced = set()
    for suite in registry["eval_suites"]:
        skill_id = suite["skill_id"]
        assert suite["status"] == "draft"
        assert suite["promptfoo_config"] == (
            f"evals/promptfoo/skills/{skill_id}.promptfooconfig.yaml"
        )
        assert (ROOT / suite["promptfoo_config"]).is_file()
        relpath = CORE_DEEPEVAL_TESTS[skill_id].relative_to(ROOT).as_posix()
        assert suite["deepeval_tests"] == [relpath]
        for deepeval_path in suite["deepeval_tests"]:
            referenced.add(deepeval_path)
            assert (ROOT / deepeval_path).is_file()
    assert referenced == {path.relative_to(ROOT).as_posix() for path in
                          CORE_DEEPEVAL_TESTS.values()}


def test_deepeval_docs_exist_and_explain_guarded_local_usage() -> None:
    for path in DEEPEVAL_DOC_PATHS:
        assert path.is_file(), path
    combined = "\n".join(path.read_text(encoding="utf-8") for path in DEEPEVAL_DOC_PATHS)
    assert "SKILLOPS_RUN_DEEPEVAL=1" in combined
    assert "Golden Sets" in combined
    assert "Promptfoo" in combined
    assert "LLM-as-judge" in combined
    assert "optional" in combined.lower()


def test_deepeval_docs_do_not_overclaim_future_behavior() -> None:
    for path in DEEPEVAL_DOC_PATHS:
        content = path.read_text(encoding="utf-8").lower()
        for claim in PROHIBITED_DOC_CLAIMS:
            assert claim not in content, path


def test_deepeval_files_do_not_commit_secrets_or_local_absolute_user_paths() -> None:
    files = [*DEEPEVAL_SUPPORT_FILES, *CORE_DEEPEVAL_TESTS.values(), *DEEPEVAL_DOC_PATHS]
    for path in files:
        content = path.read_text(encoding="utf-8")
        assert not REAL_LOOKING_SECRET_RE.search(content), path
        assert not LOCAL_USER_PATH_RE.search(content), path


def test_deepeval_files_do_not_require_external_network_calls() -> None:
    for path in [*DEEPEVAL_SUPPORT_FILES, *CORE_DEEPEVAL_TESTS.values()]:
        content = path.read_text(encoding="utf-8")
        for marker in PROHIBITED_NETWORK_MARKERS:
            assert marker not in content, path
