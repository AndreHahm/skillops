#!/usr/bin/env bash
set -euo pipefail
python hooks/shared/emit_event.py --type pre_tool_use --agent claude-code --tool "${1:-unknown}" --message "Claude pre-tool hook example"
