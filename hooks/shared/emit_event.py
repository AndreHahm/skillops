#!/usr/bin/env python3
"""Append a local JSON event to a JSONL file.

This Phase 1 helper is intentionally local-only. It reads optional JSON from
stdin, overlays supported CLI fields, adds a timestamp when needed, and appends
one event object per line. It never sends data to an external service.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

DEFAULT_OUTPUT = "reports/events/events.jsonl"


def parse_args() -> argparse.Namespace:
    """Parse supported event-emitter arguments."""
    parser = argparse.ArgumentParser(description="Emit a local SkillOps JSONL event.")
    parser.add_argument("--event", help="Event name.")
    parser.add_argument("--source", help="Event source.")
    parser.add_argument("--status", help="Event status.")
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root used to resolve relative output paths.",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help="Output JSONL path, relative to --repo-root unless absolute.",
    )
    return parser.parse_args()


def read_stdin_event() -> dict[str, Any]:
    """Read an optional JSON object from stdin."""
    if sys.stdin.isatty():
        return {}

    text = sys.stdin.read().strip()
    if not text:
        return {}

    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("stdin JSON must be an object")
    return data


def apply_cli_fields(event: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    """Overlay explicit CLI fields onto the event object."""
    merged = dict(event)
    for field in ("event", "source", "status"):
        value = getattr(args, field)
        if value is not None:
            merged[field] = value
    merged.setdefault("timestamp", datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"))
    return merged


def resolve_output_path(repo_root: str, output: str) -> Path:
    """Resolve the output path against the repository root when needed."""
    output_path = Path(output)
    if output_path.is_absolute():
        return output_path
    return Path(repo_root) / output_path


def append_event(event: dict[str, Any], output_path: Path) -> None:
    """Append one JSON object to the target JSONL file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(event, separators=(",", ":"), sort_keys=True) + "\n")


def main() -> int:
    """CLI entry point."""
    args = parse_args()
    output_path = resolve_output_path(args.repo_root, args.output)
    try:
        try:
            stdin_event = read_stdin_event()
        except (json.JSONDecodeError, ValueError) as err:
            print(f"Error: Invalid JSON input or structure: {err}", file=sys.stderr)
            return 1
        event = apply_cli_fields(stdin_event, args)
        append_event(event, output_path)
    except OSError as err:
        print(f"Error: Failed to write event to {output_path}: {err}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
