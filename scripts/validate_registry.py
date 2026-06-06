#!/usr/bin/env python3
"""Validate the SkillOps registry."""

import sys
from pathlib import Path

from skillops_core.validation import validate_registry

report = validate_registry(Path.cwd())
for finding in report.findings:
    print(f"{finding.level}: {finding.code}: {finding.message}")
sys.exit(1 if report.has_errors else 0)
