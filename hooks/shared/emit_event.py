#!/usr/bin/env python3
"""Append a JSON event to reports/events/events.jsonl."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Emit a SkillOps hook event.")
    parser.add_argument("--type", dest="event_type", help="Event type name.")
    parser.add_argument("--agent", help="Agent name.")
    parser.add_argument("--tool", help="Tool name.")
    parser.add_argument("--message", help="Human-readable message.")
    parser.add_argument("--data", help="Additional JSON object data.")
    parser.add_argument(
        "--output",
        default="reports/events/events.jsonl",
        help="Output JSONL path.",
    )
    return parser.parse_args()


def read_stdin_event() -> dict[str, Any]:
    if sys.stdin.isatty():
        return {}
    text = sys.stdin.read().strip()
    if not text:
        return {}
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("stdin JSON must be an object")
    return data


def main() -> int:
    args = parse_args()
    event = read_stdin_event()
    if args.event_type:
        event["type"] = args.event_type
    if args.agent:
        event["agent"] = args.agent
    if args.tool:
        event["tool"] = args.tool
    if args.message:
        event["message"] = args.message
    if args.data:
        extra = json.loads(args.data)
        if not isinstance(extra, dict):
            raise ValueError("--data must be a JSON object")
        event["data"] = extra
    event.setdefault("timestamp", datetime.now(UTC).isoformat())
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("a", encoding="utf-8") as file:
        file.write(json.dumps(event, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
