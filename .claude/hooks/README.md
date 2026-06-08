# Claude Code Hook Notes

Hook examples live in `hooks/claude/`.

Do not store secrets in hooks. Phase 1 hook telemetry is local-only and writes example JSONL events through `hooks/shared/emit_event.py`. Observability backend integration is out of scope for Phase 1.
