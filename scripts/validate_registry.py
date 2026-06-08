#!/usr/bin/env python3
"""Validate the SkillOps registry for the current repository."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from skillops_core import validate_skills_registry
from skillops_core.errors import SkillOpsError

DEFAULT_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(description="Validate the SkillOps registry.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=DEFAULT_ROOT,
        help="Path to the repository root (default: inferred from script location).",
    )
    return parser.parse_args()


def main() -> int:
    """Run registry validation and return a process exit code."""

    args = parse_args()
    repo_root: Path = args.repo_root.resolve()
    if not repo_root.exists():
        print(f"error: repository root does not exist: {repo_root}", file=sys.stderr)
        return 1

    try:
        report = validate_skills_registry(repo_root)
    except SkillOpsError as exc:
        print(f"error: validation failed: {exc}", file=sys.stderr)
        return 1

    print("SkillOps registry validation summary:")
    print(f"- Errors: {report.error_count}")
    print(f"- Warnings: {report.warning_count}")
    print(f"- Info: {report.info_count}")

    if report.findings:
        print("Findings:")
        for finding in report.findings:
            skill = f" [{finding.skill_id}]" if finding.skill_id else ""
            path = f" ({finding.path})" if finding.path else ""
            print(f"- {finding.level}: {finding.code}{skill}{path}: {finding.message}")

    return 1 if report.has_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
