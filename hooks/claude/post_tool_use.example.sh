#!/usr/bin/env bash
set -euo pipefail

python hooks/shared/emit_event.py \
  --event claude.post_tool_use \
  --source claude-code \
  --status completed
