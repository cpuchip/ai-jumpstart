#!/usr/bin/env python3
"""Claude Code status line: model, context-window bar, prompt-cache clock, and usage gauges.

Reads the statusline JSON on stdin (code.claude.com/docs/en/statusline).
Prints one line:
  [Model] <bar> NN% ctx · 🔥 →16:42 (47m) hit 92% · 5h NN% ↻1h12m · 7d NN% ↻3d4h
(↻ = time until that rate-limit window resets, from rate_limits.*.resets_at)
Context bar color: green <50%, yellow 50-79%, red >=80%.

The cache clock reads Claude Code's own `prompt_cache` object (sent since 2.1.x): whether the
cached prefix is warm, when it expires, the session's hit ratio, and how many tokens a cold
restart would re-cache. The absolute expiry time is the number to trust while the line sits
idle; the minutes-left figure ticks only if you set `refreshInterval` in the statusLine
settings (see optional/README.md). On an older build without `prompt_cache`, the transcript's
last write plus CLAUDE_CACHE_TTL_MIN (default 60) stands in, marked with "~".

Every bucket in `rate_limits` is rendered, not just the two known ones, so a new window shows
up the day the harness sends it. Set CLAUDE_STATUSLINE_DUMP=1 to write the raw input to
<temp>/claude-statusline-<session_id>.json on each refresh when you want to see the fields yourself.

Drop-in for the ai-jumpstart workflow. Install globally (~/.claude/statusline.py)
so the gauge shows in every project — see optional/README.md.
"""
import json
import os
import sys
import tempfile
import time

CACHE_TTL_MIN = int(os.environ.get("CLAUDE_CACHE_TTL_MIN", "60"))
DUMP_ON = bool(os.environ.get("CLAUDE_STATUSLINE_DUMP"))  # one file per session in the temp dir

ESC = chr(27)
GREEN, YELLOW, RED, DIM, RESET = ESC + "[32m", ESC + "[33m", ESC + "[31m", ESC + "[2m", ESC + "[0m"

LABELS = {"five_hour": "5h", "seven_day": "7d"}


def span(seconds):
    dt = max(0, int(seconds))
    if dt >= 86400:
        return f"{dt // 86400}d{(dt % 86400) // 3600}h"
    if dt >= 3600:
        return f"{dt // 3600}h{(dt % 3600) // 60}m"
    return f"{dt // 60}m"


def ktok(n):
    try:
        n = int(n)
    except (TypeError, ValueError):
        return "?"
    return f"{n / 1000:.0f}k" if n >= 1000 else str(n)


def label_for(key):
    if key in LABELS:
        return LABELS[key]
    return key.replace("seven_day", "7d").replace("five_hour", "5h").replace("_", " ")[:14]


def clock_text(expires, now, hit=None, recache=None, approx=False):
    left = expires - now
    at = time.strftime("%H:%M", time.localtime(expires))
    mark = "~" if approx else ""
    if left <= 0:
        s = f"{DIM}❄ cache cold{mark} since {at}"
        if recache:
            s += f", recache {ktok(recache)}"
        return s + RESET
    color = GREEN if left > 20 * 60 else YELLOW if left > 5 * 60 else RED
    s = f"{color}🔥 →{at}{mark} ({span(left)})"
    if hit is not None:
        s += f" hit {int(round(hit * 100))}%"
    return s + RESET


def cache_clock(d, now):
    """The harness's prompt_cache object first; the transcript's last write as a fallback."""
    pc = d.get("prompt_cache")
    if isinstance(pc, dict) and pc.get("expires_at"):
        if pc.get("warm") is False:
            s = f"{DIM}❄ cache cold"
            if pc.get("last_miss_cause"):
                s += f" ({pc['last_miss_cause']})"
            if pc.get("recache_tokens_if_cold"):
                s += f", recache {ktok(pc['recache_tokens_if_cold'])}"
            return s + RESET
        s = clock_text(float(pc["expires_at"]), now, hit=pc.get("hit_ratio"),
                       recache=pc.get("recache_tokens_if_cold"))
        if pc.get("misses"):
            s += f" {DIM}({pc['misses']} miss){RESET}"
        return s
    tp = d.get("transcript_path")
    if not tp:
        return None
    try:
        last = os.path.getmtime(tp)
    except OSError:
        return None
    return clock_text(last + CACHE_TTL_MIN * 60, now, approx=True)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

    try:
        raw = sys.stdin.read()
        d = json.loads(raw)
    except Exception:
        print("[statusline: no input]")
        return

    if DUMP_ON:
        try:
            sid = str(d.get("session_id") or "unknown")[:36]
            with open(os.path.join(tempfile.gettempdir(), f"claude-statusline-{sid}.json"), "w", encoding="utf-8") as f:
                f.write(raw)
        except OSError:
            pass

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
        color = GREEN if p < 50 else YELLOW if p < 80 else RED
        parts.append(f"{color}{bar} {p}% ctx{RESET}")

    now = time.time()
    clock = cache_clock(d, now)
    if clock:
        parts.append(clock)

    rl = d.get("rate_limits") or {}
    known = [k for k in ("five_hour", "seven_day") if k in rl]
    others = sorted(k for k in rl if k not in LABELS)
    for key in known + others:
        w = rl.get(key) or {}
        if not isinstance(w, dict):
            continue
        u = w.get("used_percentage")
        if u is None:
            continue
        u = max(0, min(100, int(u)))
        color = GREEN if u < 50 else YELLOW if u < 80 else RED
        s = f"{color}{label_for(key)} {u}%{RESET}"
        r = w.get("resets_at")  # unix epoch seconds; independently absent
        if r:
            s += f" ↻ {span(r - now)}"
        parts.append(s)

    print(" · ".join(parts))


main()
