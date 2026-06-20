#!/usr/bin/env python3
"""PostToolUse hook: per-session re-grounding nudge to prevent drift.

Counts tool uses per session (keyed by session_id) and, every THRESHOLD uses,
nudges the model to re-read the ai-jumpstart memory files. Per-session counters
live under the gitignored .claude/cache/ so concurrent sessions don't share one
counter and race on it. Always safe: never raises, never blocks the tool
pipeline; falls back to a single 'default' bucket if session_id is missing.

Operationalizes DISCIPLINES #6, "keep the watch whole." Install as a project
hook — see optional/README.md.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent  # .claude/hooks/ -> project root
THRESHOLD = 50
MSG = (
    "Re-grounding check: 50+ tool uses since the last refresh. Re-read active.md "
    "(the in-flight board), covenant.md, and intent.md, plus the most recent "
    "journal/ entry, before continuing. Are your current actions still aligned "
    "with the intent and within bounds? If you've drifted, course-correct now."
)


def counter_path(session_id):
    sid = re.sub(r"[^A-Za-z0-9-]", "", session_id or "") or "default"
    return ROOT / ".claude" / "cache" / f"reground-{sid}.txt"


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}
    path = counter_path(data.get("session_id", ""))
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            n = int(path.read_text(encoding="utf-8").strip())
        except (OSError, ValueError):
            n = 0
        n += 1
        if n >= THRESHOLD:
            path.write_text("0\n", encoding="utf-8")
            print(json.dumps({"hookSpecificOutput": {
                "hookEventName": "PostToolUse", "additionalContext": MSG}}))
        else:
            path.write_text(f"{n}\n", encoding="utf-8")
    except Exception:
        pass  # a counter must never break a tool call


main()
