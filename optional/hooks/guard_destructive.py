#!/usr/bin/env python3
"""UserPromptSubmit hook: when the prompt contains destructive-operation
language, inject a confirm-before-irreversible reminder.

Operationalizes DISCIPLINES #4 (reversibility bias). Always safe: never raises,
never blocks. Install as a project hook — see optional/README.md.
"""
import json
import re
import sys

PATTERN = re.compile(
    r"rm\s+-rf|force[- ]?push|drop\s+(table|database)|reset\s+--hard|--no-verify|"
    r"docker\s+(system\s+|volume\s+|image\s+)?prune|delete\s+(all|everything)|"
    r"wipe|nuke|truncate|mkfs|dd\s+if=",
    re.IGNORECASE,
)
MSG = (
    "Destructive-operation language detected in the prompt. Covenant reminder: "
    "reversible-first — irreversible or outward-facing actions get explicit, "
    "per-instance confirmation, not assumed authorization carried over from a "
    "prior approval. Confirm the exact scope + target before executing. If this "
    "exact action was authorized in this prompt, proceed — but read carefully."
)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    text = data.get("prompt", "") or ""
    if PATTERN.search(text):
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit", "additionalContext": MSG}}))


main()
