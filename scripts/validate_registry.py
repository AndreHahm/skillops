#!/usr/bin/env python3
"""Validate the SkillOps registry."""

import argparse
import sys
from pathlib import Path

from skillops_core.validation import validate_registry

_DEFAULT_ROOT = Path(__file__).resolve().parents[1]

parser = argparse.ArgumentParser(description="Validate the SkillOps registry.")
parser.add_argument(
    "--repo-root",
    type=Path,
    default=_DEFAULT_ROOT,
    help="Path to the repository root (default: inferred from script location).",
)
args = parser.parse_args()

repo_root: Path = args.repo_root.resolve()
if not repo_root.exists():
    print(f"error: repository root does not exist: {repo_root}", file=sys.stderr)
    sys.exit(1)

report = validate_registry(repo_root)
for finding in report.findings:
    print(f"{finding.level}: {finding.code}: {finding.message}")
sys.exit(1 if report.has_errors else 0)
