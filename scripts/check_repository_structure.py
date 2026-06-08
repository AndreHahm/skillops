#!/usr/bin/env python3
"""Check that required Phase 1 SkillOps repository paths exist."""

from __future__ import annotations

from pathlib import Path

REQUIRED_PATHS = [
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
    "CLAUDE.md",
    "AGENTS.md",
    "README.md",
    "pyproject.toml",
]

REPO_ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    """Print missing required paths and return a process exit code."""

    missing = [path for path in REQUIRED_PATHS if not (REPO_ROOT / path).exists()]
    if missing:
        print("Missing required Phase 1 repository paths:")
        for path in missing:
            print(f"- {path}")
        return 1

    print("Required Phase 1 repository structure exists.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
