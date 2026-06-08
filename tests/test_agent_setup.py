from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

CLAUDE_SECTIONS = [
    "# CLAUDE.md",
    "## Project Mission",
    "## Repository Rules",
    "## Coding Standards",
    "## SkillOps Rules",
    "## Required Workflow",
    "## Testing Requirements",
    "## Documentation Requirements",
    "## Safety Rules",
    "## Preferred Commands",
    "## Out of Scope for Phase 1",
    "## Package Workflow",
]

AGENTS_SECTIONS = [
    "# AGENTS.md",
    "## Project Mission",
    "## Agent Responsibilities",
    "## Repository Structure",
    "## Package Boundaries",
    "## Skill Authoring Rules",
    "## Registry Rules",
    "## Validation Rules",
    "## Testing Rules",
    "## Documentation Rules",
    "## Pull Request Expectations",
    "## Self-Review Requirements",
    "## Safety Requirements",
]

LOWER_PYTHON_VERSION_PATTERN = re.compile(r"Python\s*(?:>=|==|~=|<=|<)?\s*3\.(?:[0-9]|1[0-2])\b")


def read_text(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_instruction_files_exist() -> None:
    assert (REPO_ROOT / "CLAUDE.md").is_file()
    assert (REPO_ROOT / "AGENTS.md").is_file()


def test_claude_contains_required_sections() -> None:
    content = read_text("CLAUDE.md")
    for section in CLAUDE_SECTIONS:
        assert section in content


def test_agents_contains_required_sections() -> None:
    content = read_text("AGENTS.md")
    for section in AGENTS_SECTIONS:
        assert section in content


def test_instruction_files_use_current_project_name_only() -> None:
    for path in ("CLAUDE.md", "AGENTS.md"):
        content = read_text(path)
        assert "skillops" in content
        stale_name = "agent" + "-skillops"
        assert stale_name not in content


def test_instruction_files_do_not_contain_todo() -> None:
    for path in ("CLAUDE.md", "AGENTS.md"):
        assert "TODO" not in read_text(path)


def test_instruction_files_do_not_reference_lower_python_versions() -> None:
    for path in ("CLAUDE.md", "AGENTS.md"):
        assert LOWER_PYTHON_VERSION_PATTERN.search(read_text(path)) is None


def test_claude_settings_example_is_valid_json() -> None:
    settings_path = REPO_ROOT / ".claude" / "settings.example.json"
    assert settings_path.is_file()
    data = json.loads(settings_path.read_text(encoding="utf-8"))
    assert data["project"] == "skillops"


def test_codex_and_agent_documentation_exists() -> None:
    required_paths = [
        ".codex/skills/README.md",
        ".codex/config/README.md",
        "agents/claude/README.md",
        "agents/codex/README.md",
    ]
    for path in required_paths:
        assert (REPO_ROOT / path).is_file()
