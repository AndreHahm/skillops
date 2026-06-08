from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
MCP_EXAMPLES = [
    REPO_ROOT / "mcp" / "serena.example.json",
    REPO_ROOT / "mcp" / "linear.example.json",
    REPO_ROOT / "mcp" / "filesystem.example.json",
]
REQUIRED_KEYS = {"name", "purpose", "enabled", "configuration", "security"}
SECRET_PATTERNS = [
    "sk" + "-",
    "ghp" + "_",
    "xoxb" + "-",
    "BEGIN PRIVATE" + " KEY",
    "REPLACE" + "_WITH_REAL",
    "password123",
]
USER_PATH_PATTERNS = ["/" + "home/", "/" + "Users/", "C:" + "\\"]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_mcp_examples_exist_and_are_valid_json() -> None:
    for path in MCP_EXAMPLES:
        assert path.is_file()
        assert isinstance(load_json(path), dict)


def test_mcp_examples_have_required_shape_and_are_disabled() -> None:
    for path in MCP_EXAMPLES:
        data = load_json(path)
        assert REQUIRED_KEYS <= data.keys()
        assert data["enabled"] is False
        assert isinstance(data["configuration"], dict)
        assert isinstance(data["security"], dict)


def test_mcp_examples_do_not_contain_realistic_secrets_or_user_paths() -> None:
    for path in MCP_EXAMPLES:
        content = path.read_text(encoding="utf-8")
        for pattern in SECRET_PATTERNS:
            assert pattern not in content
        for pattern in USER_PATH_PATTERNS:
            assert pattern not in content


def test_mcp_readme_exists_and_states_examples_only() -> None:
    readme = REPO_ROOT / "mcp" / "README.md"
    assert readme.is_file()
    content = readme.read_text(encoding="utf-8").lower()
    assert "example configs only" in content
