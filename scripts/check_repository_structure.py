#!/usr/bin/env python3
"""Check that required Phase 1 files exist."""

import sys
from pathlib import Path

REQUIRED = [
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "pyproject.toml",
    "registry/skills.yaml",
    "schemas/skill.schema.json",
    "packages/skillops-core/pyproject.toml",
    "packages/skillops-cli/pyproject.toml",
    "hooks/shared/emit_event.py",
    "mcp/README.md",
]
missing = [path for path in REQUIRED if not (Path.cwd() / path).exists()]
if missing:
    print("Missing required files:")
    for path in missing:
        print(f"- {path}")
    sys.exit(1)
print("Required Phase 1 repository structure exists.")
