#!/usr/bin/env python3
"""Stop hook: if the session is ending with uncommitted changes, nudge to close
the loop (update active.md, write a journal entry, commit) before yielding.

Mirrors the covenant's "keep the memory, unprompted." Always safe: never raises,
never blocks. Install as a project hook — see optional/README.md.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
MSG = (
    "Session ending with uncommitted changes — substantive work happened. Close "
    "the loop before yielding: (1) update active.md (in-flight, decided, open "
    "questions); (2) add a journal/ entry (done / decided / learned / "
    "carry-forward); (3) commit. Covenant: keep the memory, unprompted. "
    "Work → memory → done. If this turn was conversational only, ignore."
)


def main():
    try:
        json.load(sys.stdin)
    except Exception:
        pass
    try:
        out = subprocess.run(
            ["git", "-C", str(ROOT), "status", "--porcelain"],
            capture_output=True, text=True, timeout=5,
        ).stdout.strip()
    except Exception:
        return
    if out:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "Stop", "additionalContext": MSG}}))


main()
