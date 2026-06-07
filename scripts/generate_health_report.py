#!/usr/bin/env python3
"""Generate SkillOps health reports."""

import argparse
from pathlib import Path

from skillops_core.health import (
    generate_health_report,
    write_health_report_json,
    write_health_report_markdown,
)

_DEFAULT_ROOT = Path(__file__).resolve().parents[1]

parser = argparse.ArgumentParser(description="Generate SkillOps health reports.")
parser.add_argument(
    "--repo-root",
    type=Path,
    default=_DEFAULT_ROOT,
    help="Path to the repository root (default: inferred from script location).",
)
args = parser.parse_args()

root: Path = args.repo_root.resolve()
report = generate_health_report(root)
write_health_report_json(report, root / "reports/health/health-report.json")
write_health_report_markdown(report, root / "reports/health/health-report.md")
print(f"Generated health report with overall score {report.overall_score}")
