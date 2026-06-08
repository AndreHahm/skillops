from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EMITTER = REPO_ROOT / "hooks" / "shared" / "emit_event.py"
HOOK_SCRIPTS = [
    REPO_ROOT / "hooks" / "claude" / "pre_tool_use.example.sh",
    REPO_ROOT / "hooks" / "claude" / "post_tool_use.example.sh",
]
UNSAFE_COMMANDS = ["rm -rf /", "sudo rm", "mkfs", "shutdown", "reboot"]
SECRET_PATTERNS = ["sk-", "ghp_", "xoxb-", "BEGIN PRIVATE KEY", "REPLACE_WITH_REAL"]


def read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_emit_event_script_exists() -> None:
    assert EMITTER.is_file()


def test_emit_event_writes_jsonl_from_cli_args(tmp_path: Path) -> None:
    output = tmp_path / "events" / "events.jsonl"
    subprocess.run(
        [
            sys.executable,
            str(EMITTER),
            "--event",
            "package6_test",
            "--source",
            "pytest",
            "--status",
            "ok",
            "--output",
            str(output),
        ],
        check=True,
        cwd=REPO_ROOT,
    )

    events = read_jsonl(output)
    assert len(events) == 1
    assert events[0]["event"] == "package6_test"
    assert events[0]["source"] == "pytest"
    assert events[0]["status"] == "ok"
    assert "timestamp" in events[0]


def test_emit_event_merges_stdin_json_with_cli_args(tmp_path: Path) -> None:
    output = tmp_path / "merged.jsonl"
    subprocess.run(
        [
            sys.executable,
            str(EMITTER),
            "--event",
            "cli_override",
            "--status",
            "completed",
            "--output",
            str(output),
        ],
        input=json.dumps({"event": "stdin_event", "source": "stdin_source", "extra": "kept"}),
        text=True,
        check=True,
        cwd=REPO_ROOT,
    )

    event = read_jsonl(output)[0]
    assert event["event"] == "cli_override"
    assert event["source"] == "stdin_source"
    assert event["status"] == "completed"
    assert event["extra"] == "kept"
    assert "timestamp" in event


def test_claude_hook_examples_exist_and_are_safe() -> None:
    for script in HOOK_SCRIPTS:
        assert script.is_file()
        content = script.read_text(encoding="utf-8")
        assert "set -euo pipefail" in content
        assert "hooks/shared/emit_event.py" in content
        for pattern in SECRET_PATTERNS:
            assert pattern not in content
        for command in UNSAFE_COMMANDS:
            assert command not in content
