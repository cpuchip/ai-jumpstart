#!/usr/bin/env python3
"""session-cost: token totals by category, wall time, and cost for a Claude Code session.

Tokens come from the transcript (message.usage per assistant turn, counted once per message.id).
Cost and API time come from the harness's statusline payload when statusline.py was run with
CLAUDE_STATUSLINE_DUMP=1 (<temp>/claude-statusline-<session_id>.json) and the session_id matches;
there is no public price table to compute from. Without the dump, cost reads n/a and /cost
in-session is the number.

Two views: the whole transcript (a resumed session's file goes back to its first day) and "this
run", windowed to the harness's own duration so it lines up with the harness cost.

Usage:
  python3 session-cost.py                 # newest transcript for this cwd
  python3 session-cost.py -f <path.jsonl>
  python3 session-cost.py --hook          # SessionEnd hook: reads the hook JSON on stdin, writes
                                          # <temp>/claude-session-cost-<sid>.txt and appends one
                                          # line to <temp>/claude-session-costs.log. SessionEnd
                                          # output is not displayed, so the file is the record.
"""
import glob, json, os, re, sys, tempfile, time

ROOT = None
CACHE = tempfile.gettempdir()


def newest_transcript():
    slug = re.sub(r"[\\/:]", "-", os.getcwd())  # the harness maps / \ : to -: "-home-x-proj" on Linux, "C--Users-x-proj" on Windows
    files = glob.glob(os.path.expanduser(f"~/.claude/projects/{slug}/*.jsonl"))
    return max(files, key=os.path.getmtime) if files else None


def span(sec):
    sec = int(max(0, sec)); h, r = divmod(sec, 3600); m, s = divmod(r, 60)
    return f"{h}h{m:02d}m" if h else f"{m}m{s:02d}s"


def summarize(path, since=None):
    seen, tot = set(), {"inp": 0, "cw": 0, "cr": 0, "out": 0, "turns": 0, "tools": 0, "user": 0}
    first = last = None; models = {}
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            ts = rec.get("timestamp")
            if since and ts and ts < since:
                continue
            if ts:
                first = first or ts; last = ts
            if rec.get("type") == "user" and not rec.get("isMeta"):
                c = (rec.get("message") or {}).get("content")
                if isinstance(c, str) or (isinstance(c, list) and c and c[0].get("type") == "text"):
                    tot["user"] += 1
            msg = rec.get("message") or {}
            for c in msg.get("content") or []:
                if isinstance(c, dict) and c.get("type") == "tool_use":
                    tot["tools"] += 1
            u, mid = msg.get("usage"), msg.get("id")
            if not u or not mid or mid in seen:
                continue
            seen.add(mid); tot["turns"] += 1
            models[msg.get("model", "?")] = models.get(msg.get("model", "?"), 0) + 1
            tot["inp"] += u.get("input_tokens", 0); tot["cw"] += u.get("cache_creation_input_tokens", 0)
            tot["cr"] += u.get("cache_read_input_tokens", 0); tot["out"] += u.get("output_tokens", 0)
    return tot, first, last, models


def harness_cost(sid):
    if not sid:
        return None
    try:
        d = json.load(open(os.path.join(CACHE, f"claude-statusline-{sid[:36]}.json")))
    except Exception:
        return None
    return d.get("cost") or None


def block(title, tot, first, last, models):
    total = tot["inp"] + tot["cw"] + tot["cr"] + tot["out"]
    def pct(n): return f"{100 * n / total:5.1f}%" if total else "   - "
    lines = [title,
             f"  turns {tot['turns']}  prompts {tot['user']}  tool calls {tot['tools']}  model(s) {', '.join(models) or '?'}"]
    if first and last:
        t0 = time.mktime(time.strptime(first[:19], "%Y-%m-%dT%H:%M:%S")); t1 = time.mktime(time.strptime(last[:19], "%Y-%m-%dT%H:%M:%S"))
        lines.append(f"  wall {span(t1 - t0)}  ({first[:16]}Z .. {last[:16]}Z)")
    lines += [f"  {'tokens':<14}{'count':>14}  share",
              f"  {'cache read':<14}{tot['cr']:>14,}  {pct(tot['cr'])}",
              f"  {'cache write':<14}{tot['cw']:>14,}  {pct(tot['cw'])}",
              f"  {'input':<14}{tot['inp']:>14,}  {pct(tot['inp'])}",
              f"  {'output':<14}{tot['out']:>14,}  {pct(tot['out'])}",
              f"  {'total':<14}{total:>14,}"]
    return lines


def render(path, sid=None):
    c = harness_cost(sid)
    tot, first, last, models = summarize(path)
    lines = block(f"session {sid or os.path.basename(path)[:36]} (whole transcript, resumes included)", tot, first, last, models)
    if c and c.get("total_duration_ms"):
        since = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(time.time() - c["total_duration_ms"] / 1000))
        rtot, rf, rl, rm = summarize(path, since)
        lines += [""] + block("this run (since the harness started)", rtot, rf, rl, rm)
        tot = rtot
    if c:
        lines.append(f"  cost ${c.get('total_cost_usd', 0):.2f}  api time {span(c.get('total_api_duration_ms', 0) / 1000)}  "
                     f"session {span(c.get('total_duration_ms', 0) / 1000)}  (harness)")
    else:
        lines.append("  cost n/a (run statusline.py with CLAUDE_STATUSLINE_DUMP=1, or /cost in-session)")
    return "\n".join(lines), tot, c


def main():
    args = sys.argv[1:]
    if "--hook" in args:
        try:
            h = json.load(sys.stdin)
        except Exception:
            h = {}
        path = h.get("transcript_path") or newest_transcript(); sid = h.get("session_id")
        if not path or not os.path.exists(path):
            return
        text, tot, c = render(path, sid)
        open(os.path.join(CACHE, f"claude-session-cost-{(sid or 'unknown')[:36]}.txt"), "w").write(text + "\n")
        with open(os.path.join(CACHE, "claude-session-costs.log"), "a") as f:
            f.write(f"{time.strftime('%Y-%m-%dT%H:%M')} {(sid or '?')[:8]} turns={tot['turns']} cr={tot['cr']} cw={tot['cw']} in={tot['inp']} out={tot['out']}"
                    + (f" cost=${c.get('total_cost_usd', 0):.2f}" if c else "") + "\n")
        print(text, file=sys.stderr)
        return
    path = args[args.index("-f") + 1] if "-f" in args else newest_transcript()
    if not path:
        sys.exit("no transcript found")
    sid = os.path.basename(path).rsplit(".", 1)[0]
    print(render(path, sid)[0])


main()
