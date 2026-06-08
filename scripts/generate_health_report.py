#!/usr/bin/env python3
"""Generate SkillOps health report files for CI or local checks."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from skillops_core import generate_health_report
from skillops_core.errors import SkillOpsError
from skillops_core.health import write_health_report_json, write_health_report_markdown

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON_REPORT = Path("reports/health/health-report.json")
DEFAULT_MARKDOWN_REPORT = Path("reports/health/health-report.md")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(description="Generate SkillOps health reports.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=DEFAULT_ROOT,
        help="Path to the repository root (default: inferred from script location).",
    )
    parser.add_argument(
        "--json-path",
        type=Path,
        default=DEFAULT_JSON_REPORT,
        help="Path for the JSON health report, relative to the repository root by default.",
    )
    parser.add_argument(
        "--markdown-path",
        type=Path,
        default=DEFAULT_MARKDOWN_REPORT,
        help="Path for the Markdown health report, relative to the repository root by default.",
    )
    return parser.parse_args()


def resolve_output_path(path: Path, repo_root: Path) -> Path:
    """Resolve an output path relative to the repository root when needed."""

    return path if path.is_absolute() else repo_root / path


def main() -> int:
    """Generate health reports and return a process exit code."""

    args = parse_args()
    repo_root: Path = args.repo_root.resolve()
    if not repo_root.exists():
        print(f"error: repository root does not exist: {repo_root}", file=sys.stderr)
        return 1
    if not repo_root.is_dir():
        print(f"error: repository root is not a directory: {repo_root}", file=sys.stderr)
        return 1

    try:
        report = generate_health_report(repo_root)
        json_path = resolve_output_path(args.json_path, repo_root)
        markdown_path = resolve_output_path(args.markdown_path, repo_root)
        write_health_report_json(report, json_path)
        write_health_report_markdown(report, markdown_path)
    except SkillOpsError as exc:
        print(f"error: health report generation failed: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"error: could not write health report: {exc}", file=sys.stderr)
        return 1

    jsonpath = json_path.relative_to(repo_root) \
        if json_path.is_relative_to(repo_root) else json_path
    markdownpath = markdown_path.relative_to(repo_root) \
        if markdown_path.is_relative_to(repo_root) else markdown_path
    print("Generated SkillOps health reports:")
    print(f"- {jsonpath}")
    print(f"- {markdownpath}")
    print(f"Overall score: {report.overall_score}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
