"""Deterministic smoke checks for SkillOps evaluation assets."""

from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema import exceptions as jsonschema_exceptions

from skillops_core.constants import DEFAULT_SKILLS_REGISTRY_PATH
from skillops_core.errors import SkillOpsFileNotFoundError, SkillOpsValidationError
from skillops_core.loaders import load_yaml
from skillops_core.models import ValidationReport
from skillops_core.validation import REQUIRED_CORE_SKILL_IDS

GOLDEN_SET_SCHEMA_PATH = Path("schemas/golden-set.schema.json")
EVAL_SUITE_SCHEMA_PATH = Path("schemas/eval-suite.schema.json")
EVAL_SUITE_REGISTRY_PATH = Path("registry/eval-suites.yaml")
ROOT_PROMPTFOO_CONFIG_PATH = Path("evals/promptfoo/promptfooconfig.yaml")
GOLDEN_SET_DIR = Path("evals/golden")

EVALUATION_DOC_PATHS = [
    Path("evals/README.md"),
    Path("evals/golden/README.md"),
    Path("evals/promptfoo/README.md"),
    Path("evals/deepeval/README.md"),
    Path("docs/evaluation/overview.md"),
    Path("docs/evaluation/ci-gate.md"),
    Path("docs/evaluation/skill-tdd.md"),
    Path("docs/evaluation/review-gates.md"),
    Path("llm-wiki/concepts/evaluation.md"),
    Path("llm-wiki/concepts/skill-tdd.md"),
]

FORBIDDEN_DOC_CLAIMS = [
    "full evaluation is implemented",
    "live llm evaluation is implemented",
    "llm-as-judge scoring is mandatory",
    "promptfoo cloud upload is implemented",
    "deepeval cloud login is implemented",
    "production observability is implemented",
    "production traces are implemented",
    "langfuse is integrated",
    "langfuse integration is implemented",
    "phoenix is integrated",
    "phoenix integration is implemented",
    "marketplace behavior is implemented",
    "self-improvement automation is implemented",
    "automatic skill patching is implemented",
]

SECRET_PATTERNS = [
    re.compile(r"sk-[a-z0-9]{20,}", re.IGNORECASE),
    re.compile(r"ghp_[a-z0-9]{20,}", re.IGNORECASE),
    re.compile(r"xox[baprs]-[a-z0-9-]{20,}", re.IGNORECASE),
    re.compile(r"aws_secret_access_key\s*=\s*['\"]?[a-z0-9/+=]{20,}", re.IGNORECASE),
]
# noinspection RegExpUnnecessaryNonCapturingGroup
LOCAL_USER_PATH_PATTERN = re.compile(
    r"(?:[A-Za-z]:\\Users\\[A-Za-z0-9._\- ]+|/(?:Users|home)/[A-Za-z0-9._-]+)"
)
TEXT_FILE_SUFFIXES = {".json", ".md", ".py", ".toml", ".yaml", ".yml"}


@dataclass(slots=True)
class EvaluationSmokeResult:
    """Summary of deterministic evaluation smoke checks."""

    report: ValidationReport = field(default_factory=ValidationReport)
    golden_sets_checked: int = 0
    eval_suites_checked: int = 0
    promptfoo_configs_checked: int = 0
    deepeval_files_checked: int = 0
    docs_checked: int = 0
    safety_files_checked: int = 0

    @property
    def passed(self) -> bool:
        """Return True when no blocking smoke errors were found."""

        return not self.report.has_errors


def _display_path(path: Path, repo_root: Path) -> str:
    try:
        return str(path.resolve().relative_to(repo_root.resolve()))
    except ValueError:
        return str(path)


def _repo_path(repo_root: Path, path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return repo_root / candidate


def _is_safe_repo_relative_path(value: str, repo_root: Path) -> bool:
    path = Path(value)
    if path.is_absolute():
        return False
    try:
        (repo_root / path).resolve().relative_to(repo_root.resolve())
    except ValueError:
        return False
    return True


def _load_json_schema(
    path: Path, repo_root: Path, result: EvaluationSmokeResult
) -> dict[str, Any] | None:
    display_path = _display_path(path, repo_root)
    if not path.exists():
        result.report.add_error(
            "eval_smoke.schema_missing", "Required schema is missing.", display_path
        )
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError, UnicodeDecodeError) as exc:
        result.report.add_error(
            "eval_smoke.schema_invalid_json",
            f"Required schema is not valid JSON: {exc}",
            display_path,
        )
        return None
    if not isinstance(data, dict):
        result.report.add_error(
            "eval_smoke.schema_not_mapping",
            "Required schema JSON must be an object.",
            display_path,
        )
        return None
    try:
        Draft202012Validator.check_schema(data)
    except jsonschema_exceptions.SchemaError as exc:
        result.report.add_error(
            "eval_smoke.schema_invalid",
            f"Required schema is not a valid JSON Schema: {exc.message}",
            display_path,
        )
        return None
    return data


def _load_yaml_mapping(
    path: Path, repo_root: Path, result: EvaluationSmokeResult
) -> dict[str, Any] | None:
    invalid_yaml = "eval_smoke.invalid_yaml"
    display_path = _display_path(path, repo_root)
    if not path.exists():
        result.report.add_error(
            "eval_smoke.file_missing", "Required file is missing.", display_path
        )
        return None
    try:
        data = load_yaml(path)
    except (SkillOpsValidationError, SkillOpsFileNotFoundError) as exc:
        result.report.add_error(
            invalid_yaml,
            f"YAML file is not parseable as a mapping: {exc}",
            display_path,
        )
        return None
    return data


def _validate_instance(
    validator,
    instance: dict[str, Any],
    path: Path,
    repo_root: Path,
    result: EvaluationSmokeResult,
    code: str,
) -> None:
    for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        result.report.add_error(
            code,
            f"Schema validation failed at {location}: {error.message}",
            _display_path(path, repo_root),
        )


def _validate_golden_sets(
    repo_root: Path,
    result: EvaluationSmokeResult,
    golden_validator,
) -> dict[str, Path]:
    golden_sets: dict[str, Path] = {}
    golden_dir = repo_root / GOLDEN_SET_DIR
    if not golden_dir.is_dir():
        result.report.add_error(
            "eval_smoke.golden_dir_missing",
            "Golden Set directory is missing.",
            str(GOLDEN_SET_DIR),
        )
        return golden_sets

    for path in sorted(golden_dir.glob("*.yaml")):
        data = _load_yaml_mapping(path, repo_root, result)
        if data is None:
            continue
        _validate_instance(
            golden_validator,
            data,
            path,
            repo_root,
            result,
            "eval_smoke.golden_set_invalid_schema",
        )
        skill_id = data.get("skill_id")
        if isinstance(skill_id, str):
            if skill_id in golden_sets:
                result.report.add_error(
                    "eval_smoke.duplicate_golden_set_skill_id",
                    f"Duplicate skill_id in golden sets: {skill_id}",
                    _display_path(path, repo_root),
                    skill_id,
                )
            else:
                golden_sets[skill_id] = path
        result.golden_sets_checked += 1
    return golden_sets


def _validate_promptfoo_config(path: Path, repo_root: Path, result: EvaluationSmokeResult) -> None:
    data = _load_yaml_mapping(path, repo_root, result)
    if data is None:
        return
    for key in ("prompts", "providers", "tests"):
        if key not in data:
            result.report.add_error(
                "eval_smoke.promptfoo_missing_key",
                f"Promptfoo config is missing required structural key: {key}",
                _display_path(path, repo_root),
            )
    result.promptfoo_configs_checked += 1


def _validate_deepeval_file(path: Path, repo_root: Path, result: EvaluationSmokeResult) -> None:
    display_path = _display_path(path, repo_root)
    if not path.exists():
        result.report.add_error(
            "eval_smoke.deepeval_missing", "DeepEval test file is missing.", display_path
        )
        return
    try:
        source = path.read_text(encoding="utf-8")
        ast.parse(source, filename=str(path))
    except (SyntaxError, OSError, UnicodeDecodeError) as exc:
        result.report.add_error(
            "eval_smoke.deepeval_invalid_python",
            f"DeepEval test file is not syntactically valid Python: {exc}",
            display_path,
        )
        return
    if "SKILLOPS_RUN_DEEPEVAL" not in source or "skipif" not in source:
        result.report.add_error(
            "eval_smoke.deepeval_not_guarded",
            "DeepEval runtime checks must be guarded by SKILLOPS_RUN_DEEPEVAL and pytest skipif.",
            display_path,
        )
    result.deepeval_files_checked += 1


def _validate_eval_suite_registry(
    repo_root: Path,
    result: EvaluationSmokeResult,
    eval_suite_validator,
    golden_sets_by_skill_id: dict[str, Path],
) -> None:
    registry_path = repo_root / EVAL_SUITE_REGISTRY_PATH
    registry = _load_yaml_mapping(registry_path, repo_root, result)
    if registry is None:
        return
    _validate_instance(
        eval_suite_validator,
        registry,
        registry_path,
        repo_root,
        result,
        "eval_smoke.eval_suite_registry_invalid_schema",
    )

    suites = registry.get("eval_suites")
    if not isinstance(suites, list):
        return

    suite_counts: dict[str, int] = {}
    seen_promptfoo_configs: set[Path] = set()
    seen_deepeval_files: set[Path] = set()
    for suite in suites:
        if not isinstance(suite, dict):
            continue
        skill_id = suite.get("skill_id")
        if isinstance(skill_id, str):
            suite_counts[skill_id] = suite_counts.get(skill_id, 0) + 1
        result.eval_suites_checked += 1

        golden_set = suite.get("golden_set")
        if isinstance(golden_set, str):
            if not _is_safe_repo_relative_path(golden_set, repo_root):
                result.report.add_error(
                    "eval_smoke.unsafe_reference",
                    "Eval suite golden_set reference must be a safe repository-relative path.",
                    str(EVAL_SUITE_REGISTRY_PATH),
                    skill_id if isinstance(skill_id, str) else None,
                )
            else:
                golden_path = _repo_path(repo_root, golden_set)
                if not golden_path.exists():
                    result.report.add_error(
                        "eval_smoke.golden_set_missing",
                        f"Referenced Golden Set is missing: {golden_set}",
                        str(EVAL_SUITE_REGISTRY_PATH),
                        skill_id if isinstance(skill_id, str) else None,
                    )
                elif (isinstance(skill_id, str) and
                      golden_sets_by_skill_id.get(skill_id) != golden_path):
                    result.report.add_error(
                        "eval_smoke.golden_set_skill_mismatch",
                        f"Eval suite Golden Set does not align with skill_id: {golden_set}",
                        str(EVAL_SUITE_REGISTRY_PATH),
                        skill_id,
                    )

        promptfoo_config = suite.get("promptfoo_config")
        if isinstance(promptfoo_config, str):
            if not _is_safe_repo_relative_path(promptfoo_config, repo_root):
                result.report.add_error(
                    "eval_smoke.unsafe_reference",
                    "Promptfoo config reference must be a safe repository-relative path.",
                    str(EVAL_SUITE_REGISTRY_PATH),
                    skill_id if isinstance(skill_id, str) else None,
                )
            else:
                promptfoo_path = _repo_path(repo_root, promptfoo_config)
                if promptfoo_path not in seen_promptfoo_configs:
                    seen_promptfoo_configs.add(promptfoo_path)
                    _validate_promptfoo_config(promptfoo_path, repo_root, result)

        deepeval_tests = suite.get("deepeval_tests")
        if isinstance(deepeval_tests, list):
            for deepeval_test in deepeval_tests:
                if not isinstance(deepeval_test, str):
                    continue
                if not _is_safe_repo_relative_path(deepeval_test, repo_root):
                    result.report.add_error(
                        "eval_smoke.unsafe_reference",
                        "DeepEval test reference must be a safe repository-relative path.",
                        str(EVAL_SUITE_REGISTRY_PATH),
                        skill_id if isinstance(skill_id, str) else None,
                    )
                else:
                    deepeval_path = _repo_path(repo_root, deepeval_test)
                    if deepeval_path not in seen_deepeval_files:
                        seen_deepeval_files.add(deepeval_path)
                        _validate_deepeval_file(deepeval_path, repo_root, result)

    for core_skill_id in sorted(REQUIRED_CORE_SKILL_IDS):
        count = suite_counts.get(core_skill_id, 0)
        if count != 1:
            result.report.add_error(
                "eval_smoke.core_skill_suite_count",
                f"Core skill must have exactly one eval suite; found {count}.",
                str(EVAL_SUITE_REGISTRY_PATH),
                core_skill_id,
            )

    skills_registry = _load_yaml_mapping(
        repo_root / DEFAULT_SKILLS_REGISTRY_PATH, repo_root, result
    )
    if skills_registry is not None:
        registered_ids = {
            entry.get("id")
            for entry in skills_registry.get("skills", [])
            if isinstance(entry, dict)
        }
        for skill_id in suite_counts:
            if skill_id not in registered_ids:
                result.report.add_error(
                    "eval_smoke.unregistered_skill",
                    "Eval suite references a skill that is not in registry/skills.yaml.",
                    str(EVAL_SUITE_REGISTRY_PATH),
                    skill_id,
                )


def _validate_docs(repo_root: Path, result: EvaluationSmokeResult) -> None:
    for relative_path in EVALUATION_DOC_PATHS:
        path = repo_root / relative_path
        if not path.exists():
            result.report.add_error(
                "eval_smoke.doc_missing",
                "Required evaluation documentation is missing.",
                str(relative_path),
            )
            continue
        try:
            content = path.read_text(encoding="utf-8").lower()
        except (OSError, UnicodeDecodeError) as exc:
            result.report.add_error(
                "eval_smoke.doc_read_error",
                f"Failed to read evaluation documentation: {exc}",
                str(relative_path),
            )
            continue
        for claim in FORBIDDEN_DOC_CLAIMS:
            if claim in content:
                result.report.add_error(
                    "eval_smoke.doc_overclaim",
                    f"Evaluation documentation overclaims future behavior: {claim}",
                    str(relative_path),
                )
        result.docs_checked += 1


def _iter_safety_scan_files(repo_root: Path) -> list[Path]:
    roots = [
        repo_root / ".github",
        repo_root / "docs",
        repo_root / "evals",
        repo_root / "llm-wiki",
        repo_root / "packages",
        repo_root / "registry",
        repo_root / "schemas",
        repo_root / "tests",
    ]
    files = [repo_root / "README.md", repo_root / "justfile", repo_root / "pyproject.toml"]
    for root in roots:
        if root.exists():
            files.extend(path for path in root.rglob("*") if path.is_file())
    return sorted(
        {path for path in files if path.suffix in TEXT_FILE_SUFFIXES or path.name == "justfile"}
    )


def _validate_safety_scan(repo_root: Path, result: EvaluationSmokeResult) -> None:
    for path in _iter_safety_scan_files(repo_root):
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        display_path = _display_path(path, repo_root)
        for pattern in SECRET_PATTERNS:
            match = pattern.search(content)
            if match is not None:
                result.report.add_error(
                    "eval_smoke.secret_like_value",
                    "Real-looking secret or token pattern found.",
                    display_path,
                )
        if LOCAL_USER_PATH_PATTERN.search(content):
            result.report.add_error(
                "eval_smoke.local_absolute_path",
                "Local absolute user path found.",
                display_path,
            )
        stale_project_name = "agent" + "-skillops"
        if stale_project_name in content.lower():
            result.report.add_error(
                "eval_smoke.stale_project_name",
                "Stale project name found.",
                display_path,
            )
        result.safety_files_checked += 1


def run_evaluation_smoke(repo_root: Path) -> EvaluationSmokeResult:
    """Run deterministic local smoke checks for Phase 2 evaluation assets."""

    repo_root = repo_root.resolve()
    result = EvaluationSmokeResult()

    golden_schema = _load_json_schema(repo_root / GOLDEN_SET_SCHEMA_PATH, repo_root, result)
    eval_suite_schema = _load_json_schema(repo_root / EVAL_SUITE_SCHEMA_PATH, repo_root, result)
    if golden_schema is None or eval_suite_schema is None:
        return result

    golden_validator = Draft202012Validator(golden_schema)
    eval_suite_validator = Draft202012Validator(eval_suite_schema)
    golden_sets_by_skill_id = _validate_golden_sets(repo_root, result, golden_validator)
    _validate_promptfoo_config(repo_root / ROOT_PROMPTFOO_CONFIG_PATH, repo_root, result)
    _validate_eval_suite_registry(repo_root, result, eval_suite_validator, golden_sets_by_skill_id)
    _validate_docs(repo_root, result)
    _validate_safety_scan(repo_root, result)
    return result
