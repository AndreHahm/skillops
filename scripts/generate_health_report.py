#!/usr/bin/env python3
"""Generate SkillOps health reports."""

from pathlib import Path

from skillops_core.health import (
    generate_health_report,
    write_health_report_json,
    write_health_report_markdown,
)

root = Path.cwd()
report = generate_health_report(root)
write_health_report_json(report, root / "reports/health/health-report.json")
write_health_report_markdown(report, root / "reports/health/health-report.md")
print(f"Generated health report with overall score {report.overall_score}")
