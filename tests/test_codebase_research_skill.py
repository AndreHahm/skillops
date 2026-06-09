"""Structural checks for the Phase 2a codebase research skill."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "codebase-research"
SKILL_MD = SKILL_DIR / "SKILL.md"
SKILL_YAML = SKILL_DIR / "skill.yaml"
REPORT_DIR = ROOT / "reports" / "codebase-research"
REPORT_TEMPLATE = REPORT_DIR / "codebase-research-report.template.md"

REQUIRED_SECTIONS = (
    "# Codebase Research",
    "## Purpose",
    "## When to Use This Skill",
    "## When Not to Use This Skill",
    "## Inputs",
    "## Outputs",
    "## Research Workflow",
    "## Tool Guidance",
    "### Serena MCP",
    "### Repomix",
    "### graphify / Knowledge Graph Builders",
    "### code-review-graph",
    "## Research Report Format",
    "## Source Evidence Rules",
    "## Safety Rules",
    "## Anti-Patterns",
    "## Completion Checklist",
    "## Related Skills",
)

OPTIONAL_TOOL_TERMS = ("Serena", "Repomix", "graphify", "code-review-graph")
FORBIDDEN_IMPLEMENTED_CLAIMS = (
    "full Serena integration is implemented",
    "Repomix wrapper is implemented",
    "graphify adapter is implemented",
    "code-review-graph integration is implemented",
    "dependency graph product is implemented",
    "observability integration is implemented",
    "marketplace behavior is implemented",
    "self-improvement automation is implemented",
)
GENERATED_DUMP_PATTERNS = (
    "repomix-output",
    "repomix-full",
    "repository-context-dump",
    "codebase-dump",
    "knowledge-graph.db",
    "code-review-graph.db",
)
SECRET_PATTERNS = (
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"),
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"(?i)(api[_-]?key|token|secret)\s*[:=]\s*['\"][A-Za-z0-9_./+=-]{20,}['\"]"),
)
LOCAL_PATH_PATTERNS = (
    re.compile(r"/home/[A-Za-z0-9._-]+"),
    re.compile(r"/Users/[A-Za-z0-9._-]+"),
    re.compile(r"[A-Za-z]:\\Users\\[A-Za-z0-9._-]+"),
)


def _load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def _tracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return [ROOT / line for line in result.stdout.splitlines() if line]


def test_codebase_research_skill_files_exist() -> None:
    assert SKILL_DIR.is_dir()
    assert SKILL_MD.is_file()
    assert SKILL_YAML.is_file()


def test_codebase_research_manifest_validates_against_schema() -> None:
    schema = _load_yaml(ROOT / "schemas" / "skill.schema.json")
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(_load_yaml(SKILL_YAML))


def test_codebase_research_skill_is_registered() -> None:
    registry = _load_yaml(ROOT / "registry" / "skills.yaml")
    entries = registry["skills"]

    assert {entry["id"] for entry in entries} >= {"codebase-research"}
    assert any(
        entry == {
            "id": "codebase-research",
            "path": "skills/codebase-research/skill.yaml",
        }
        for entry in entries
    )


def test_codebase_research_skill_has_required_sections() -> None:
    skill_text = SKILL_MD.read_text(encoding="utf-8")

    for section in REQUIRED_SECTIONS:
        assert section in skill_text


def test_codebase_research_skill_documents_optional_tools_and_ci_boundary() -> None:
    skill_text = SKILL_MD.read_text(encoding="utf-8")
    lower_text = skill_text.lower()

    for term in OPTIONAL_TOOL_TERMS:
        assert term in skill_text
    assert "optional research aids" in lower_text
    assert "must not be required for baseline ci" in lower_text
    assert "unavailable serena setup must not block baseline repository validation" in lower_text
    assert "do not require code-review-graph for ci" in lower_text
    assert "do not implement the adapter in this skill package" in lower_text


def test_codebase_research_report_directory_and_template_exist() -> None:
    assert REPORT_DIR.is_dir()
    assert (REPORT_DIR / ".gitkeep").is_file()
    assert REPORT_TEMPLATE.is_file()


def test_no_large_generated_research_dumps_are_tracked() -> None:
    tracked_names = [str(path.relative_to(ROOT)) for path in _tracked_files()]

    for name in tracked_names:
        normalized = name.lower()
        assert not any(pattern in normalized for pattern in GENERATED_DUMP_PATTERNS)


def test_tracked_text_files_do_not_contain_real_looking_secrets_or_local_user_paths() -> None:
    offenders: list[str] = []
    for path in _tracked_files():
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".lock"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in (*SECRET_PATTERNS, *LOCAL_PATH_PATTERNS):
            if pattern.search(text):
                offenders.append(str(path.relative_to(ROOT)))
                break

    assert offenders == []


def test_documentation_does_not_claim_future_research_integrations_are_implemented() -> None:
    documentation_files = [
        *list((ROOT / "docs").rglob("*.md")),
        ROOT / "README.md",
        *list((ROOT / "llm-wiki").rglob("*.md")),
    ]
    combined_text = "\n".join(path.read_text(encoding="utf-8") for path in documentation_files)

    for claim in FORBIDDEN_IMPLEMENTED_CLAIMS:
        assert claim not in combined_text
