#!/usr/bin/env python3
"""Claude Code status line: model, context-window bar, and 5h/7d usage gauges.

Reads the statusline JSON on stdin (code.claude.com/docs/en/statusline).
Prints one line:  [Model] <bar> NN% ctx · 5h NN% ↻1h12m · 7d NN% ↻3d4h
(↻ = time until that rate-limit window resets, from rate_limits.*.resets_at)
Context bar color: green <50%, yellow 50-79%, red >=80%.

Drop-in for the ai-jumpstart workflow. Install globally (~/.claude/statusline.py)
so the gauge shows in every project — see optional/README.md.
"""
import json
import sys
import time


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

    try:
        d = json.load(sys.stdin)
    except Exception:
        print("[statusline: no input]")
        return

    parts = []

    model = (d.get("model") or {}).get("display_name")
    if model:
        parts.append(f"[{model}]")

    cw = d.get("context_window") or {}
    pct = cw.get("used_percentage")
    if pct is None:
        # null before the first API call and right after /compact
        parts.append("ctx —")
    else:
        p = max(0, min(100, int(pct)))
        bar = "▓" * (p // 10) + "░" * (10 - p // 10)
        color = "\033[32m" if p < 50 else "\033[33m" if p < 80 else "\033[31m"
        parts.append(f"{color}{bar} {p}% ctx\033[0m")

    rl = d.get("rate_limits") or {}
    now = time.time()
    for key, label in (("five_hour", "5h"), ("seven_day", "7d")):
        w = rl.get(key) or {}
        u = w.get("used_percentage")
        if u is None:
            continue
        s = f"{label} {int(u)}%"
        r = w.get("resets_at")  # unix epoch seconds; independently absent
        if r:
            dt = max(0, int(r - now))
            if dt >= 86400:
                t = f"{dt // 86400}d{(dt % 86400) // 3600}h"
            elif dt >= 3600:
                t = f"{dt // 3600}h{(dt % 3600) // 60}m"
            else:
                t = f"{dt // 60}m"
            s += f" ↻ {t}"
        parts.append(s)

    print(" · ".join(parts))


main()
