"""Tests for Phase 1 repository structure and CI foundation files."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
REQUIRED_DIRECTORIES = [
    "packages/skillops-core",
    "packages/skillops-cli",
    "schemas",
    "registry",
    "skills",
    "docs",
    "llm-wiki",
    "hooks",
    "mcp",
    "agents",
    "tests",
]
REQUIRED_ROOT_FILES = [
    "CLAUDE.md",
    "AGENTS.md",
    "README.md",
    "pyproject.toml",
]
ISSUE_TEMPLATES = [
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/ISSUE_TEMPLATE/skill_request.yml",
]
WRAPPER_SCRIPTS = [
    "scripts/validate_registry.py",
    "scripts/generate_health_report.py",
    "scripts/check_repository_structure.py",
]
PACKAGE_8_FILES = [
    ".github/workflows/ci.yml",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/ISSUE_TEMPLATE/skill_request.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    "justfile",
    "markdownlint.json",
    "scripts/validate_registry.py",
    "scripts/generate_health_report.py",
    "scripts/check_repository_structure.py",
    "docs/roadmap/phase-1-foundation.md",
    "README.md",
    "tests/test_ci_config.py",
    "tests/test_repository_structure.py",
]
LOWER_PYTHON_PATTERN = re.compile(
    r"(?i)(python-version:\s*[\"']?|python\s+)(?:2\.|3\.(?:[0-9]|1[0-2])(?:\D|$))"
)


def read_package_8_text() -> str:
    """Return combined text for Package 8 files that exist."""

    return "\n".join(
        (REPO_ROOT / path).read_text()
        for path in PACKAGE_8_FILES
        if (REPO_ROOT / path).exists()
    )


def test_required_phase_1_directories_exist() -> None:
    missing = [path for path in REQUIRED_DIRECTORIES if not (REPO_ROOT / path).is_dir()]
    assert missing == []


def test_required_root_files_exist() -> None:
    missing = [path for path in REQUIRED_ROOT_FILES if not (REPO_ROOT / path).is_file()]
    assert missing == []


def test_justfile_exists() -> None:
    assert (REPO_ROOT / "justfile").is_file()


def test_markdownlint_json_exists_and_is_valid_json() -> None:
    config_path = REPO_ROOT / "markdownlint.json"
    assert config_path.is_file()
    config = json.loads(config_path.read_text())
    assert config == {
        "default": True,
        "MD013": False,
        "MD033": False,
        "MD041": False,
    }


def test_github_issue_templates_exist() -> None:
    missing = [path for path in ISSUE_TEMPLATES if not (REPO_ROOT / path).is_file()]
    assert missing == []


def test_pull_request_template_exists() -> None:
    assert (REPO_ROOT / ".github/PULL_REQUEST_TEMPLATE.md").is_file()


def test_wrapper_scripts_exist() -> None:
    missing = [path for path in WRAPPER_SCRIPTS if not (REPO_ROOT / path).is_file()]
    assert missing == []


def test_repository_structure_script_exits_zero() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_repository_structure.py"],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Required Phase 1 repository structure exists." in result.stdout


def test_package_8_files_do_not_contain_stale_repository_name() -> None:
    stale_name = "agent" + "-skillops"
    assert stale_name not in read_package_8_text()


def test_package_8_files_do_not_introduce_lower_python_versions() -> None:
    assert not LOWER_PYTHON_PATTERN.search(read_package_8_text())
