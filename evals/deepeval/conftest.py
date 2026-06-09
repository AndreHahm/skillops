"""Pytest configuration for local DeepEval skeleton tests."""

from __future__ import annotations

import sys
from pathlib import Path

DEEPEVAL_DIR = Path(__file__).resolve().parent
if str(DEEPEVAL_DIR) not in sys.path:
    sys.path.insert(0, str(DEEPEVAL_DIR))
