#!/usr/bin/env python3
"""dream-mine — the deterministic floor of the nightly dream.

    python dream-mine.py [--hours 24] [--json PATH]

Walks every Claude Code session transcript under ~/.claude/projects modified
inside the window and extracts, with zero model judgment:

  * tool ERRORS — is_error tool_results, paired to their tool_use (tool name +
    input snippet), clustered by a normalized signature so "the same bite,
    seven times" reads as one line with a count instead of seven anecdotes;
  * permission DENIALS and user INTERRUPTIONS (each one is a place the human
    had to stop the machine — worth a look even when nothing "failed");
  * RETRY loops — the same normalized command erroring 2+ times in one
    session (retrying without a diagnosis is the anti-pattern; the cluster
    shows where it happened).

The digest feeds the judgment pass (the nightly-dream skill): the model reads
THIS instead of raw transcripts, follows the pointers back only where it
needs context, and proposes evidence-cited changes. Karpathy's "dreaming,"
made concrete: deterministic evidence first, judgment second, a human
before anything durable changes.

KNOWN DEFECT (found 2026-08-08, fix pending): the window filter selects
transcript FILES by mtime and then mines their whole history, so a long-lived
session re-reports old errors as if they were tonight's. Measured once at 221
reported vs 5 genuinely in-window. Until that is fixed, treat counts as an
upper bound and verify a cluster's timestamps before acting on it.

Why signatures normalize paths/numbers/uuids: an error that names a different
file each time is still the same wound. Clustering by raw text hides the
pattern; that hiding is exactly what a nightly pass exists to defeat.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from collections import defaultdict
from pathlib import Path

PROJECTS = Path.home() / ".claude" / "projects"


def norm_signature(text: str) -> str:
    """First meaningful line, with volatile tokens collapsed.

    'Exit code N' is boilerplate, not a signature — the first run collapsed
    132 of 171 errors into that one useless mega-cluster. The wound is named
    by the first DIAGNOSTIC line: prefer a line that looks like an error
    (Error/error:/fatal/Traceback/not recognized/No such/missing), else the
    first non-empty line after the exit-code banner."""
    lines = [l.strip() for l in (text or "").splitlines() if l.strip()]
    lines = [l for l in lines if not re.fullmatch(r"Exit code \d+", l)]
    line = ""
    for cand in lines:
        if re.search(r"error|fatal|traceback|not recognized|no such|missing|"
                     r"cannot|unable|denied|invalid|failed", cand, re.I):
            line = cand
            break
    if not line:
        line = lines[0] if lines else "Exit code (no output)"
    line = re.sub(r"[A-Za-z]:[\\/][^\s'\"]+", "<path>", line)
    line = re.sub(r"/[a-zA-Z0-9_./-]{8,}", "<path>", line)
    line = re.sub(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", "<uuid>", line)
    line = re.sub(r"\b\d+\b", "<n>", line)
    return line[:160]


def content_text(c) -> str:
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return " ".join(x.get("text", "") for x in c if isinstance(x, dict))
    return str(c)


def mine(hours: float):
    cutoff = time.time() - hours * 3600
    errors = defaultdict(lambda: {"count": 0, "tools": set(), "sessions": set(), "samples": []})
    denials = []
    interrupts = 0
    retry_clusters = defaultdict(set)   # (session, signature) -> occurrence count via list
    retry_counts = defaultdict(int)
    files_read = 0

    for proj in sorted(PROJECTS.iterdir()) if PROJECTS.is_dir() else []:
        if not proj.is_dir():
            continue
        for fp in proj.glob("*.jsonl"):
            if fp.stat().st_mtime < cutoff:
                continue
            files_read += 1
            session = f"{proj.name}/{fp.name}"
            tool_use = {}   # id -> (tool_name, input_snippet)
            try:
                fh = fp.open(encoding="utf-8", errors="replace")
            except OSError:
                continue
            with fh:
                for line in fh:
                    try:
                        d = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    msg = d.get("message")
                    if not isinstance(msg, dict):
                        continue
                    content = msg.get("content")
                    if not isinstance(content, list):
                        # a plain-string user message can still be an interrupt marker
                        if isinstance(content, str) and "[Request interrupted" in content:
                            interrupts += 1
                        continue
                    for c in content:
                        if not isinstance(c, dict):
                            continue
                        if c.get("type") == "tool_use":
                            snip = json.dumps(c.get("input", {}), ensure_ascii=False)[:180]
                            tool_use[c.get("id")] = (c.get("name", "?"), snip)
                        elif c.get("type") == "tool_result":
                            text = content_text(c.get("content"))
                            if "[Request interrupted" in text:
                                interrupts += 1
                            name, inp = tool_use.get(c.get("tool_use_id"), ("?", ""))
                            if c.get("is_error"):
                                low = text.lower()
                                if "user doesn't want" in low or "permission" in low and "denied" in low:
                                    denials.append({"session": session, "tool": name,
                                                    "snippet": text[:160]})
                                    continue
                                sig = norm_signature(text)
                                b = errors[sig]
                                b["count"] += 1
                                b["tools"].add(name)
                                b["sessions"].add(session)
                                if len(b["samples"]) < 3:
                                    b["samples"].append({
                                        "session": session, "tool": name,
                                        "input": inp, "error": text[:300]})
                                key = (session, sig)
                                retry_counts[key] += 1

    retries = [{"session": s, "signature": sig, "times": n}
               for (s, sig), n in sorted(retry_counts.items(), key=lambda kv: -kv[1])
               if n >= 2]
    clusters = sorted(
        ({"signature": sig, "count": b["count"], "tools": sorted(b["tools"]),
          "sessions": len(b["sessions"]), "samples": b["samples"]}
         for sig, b in errors.items()),
        key=lambda c: -c["count"])
    return {
        "window_hours": hours,
        "files_scanned": files_read,
        "total_errors": sum(c["count"] for c in clusters),
        "clusters": clusters,
        "denials": denials,
        "interrupts": interrupts,
        "retry_loops": retries,
    }


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--hours", type=float, default=24)
    ap.add_argument("--json", type=str, default="")
    args = ap.parse_args()

    digest = mine(args.hours)
    if args.json:
        Path(args.json).write_text(
            json.dumps(digest, indent=1, ensure_ascii=False), encoding="utf-8")

    print(f"dream-mine: {digest['files_scanned']} session file(s) in the last "
          f"{args.hours:g}h — {digest['total_errors']} tool error(s) in "
          f"{len(digest['clusters'])} cluster(s), {len(digest['denials'])} denial(s), "
          f"{digest['interrupts']} interrupt(s), {len(digest['retry_loops'])} retry loop(s)")
    for c in digest["clusters"][:20]:
        print(f"\n[{c['count']}x | {c['sessions']} session(s) | {','.join(c['tools'])}] {c['signature']}")
        s = c["samples"][0]
        print(f"    e.g. {s['error'][:150].replace(chr(10), ' ')}")
    if digest["retry_loops"]:
        print("\nRETRY LOOPS (same signature erroring 2+ times in one session):")
        for r in digest["retry_loops"][:10]:
            print(f"  {r['times']}x  {r['signature'][:110]}")
    if len(digest["clusters"]) > 20:
        print(f"\n(+{len(digest['clusters']) - 20} more clusters — see --json output)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
