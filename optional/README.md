# Optional — Claude Code automation

The kit is model-agnostic, but if you run it in **Claude Code** these drop-in pieces make
the disciplines *self-enforcing* instead of relying on the assistant to remember. All are
optional and independent — take what helps, skip the rest.

> **Provenance.** These were built and proven in real use — running the ai-jumpstart way on
> a production deployment server — then generalized back into the kit. The disciplines they
> automate are the ones [DISCIPLINES.md](../DISCIPLINES.md) already describes.

## What's here

| File | Hook / type | The discipline it automates |
|---|---|---|
| `statusline.py` | statusLine | Situational awareness: model, context %, session cost with what the current exchange has cost, that exchange's tokens (input / cache write / cache read / output) and API round trips, the prompt-cache clock (warm until when, hit ratio, what a cold restart re-caches), and every usage gauge the harness sends (5h / 7d today), always in view |
| `session-cost.py` | SessionEnd (and on demand) | The bill: tokens by category, wall time, turns and tool calls, cost, for the whole transcript and for this run |
| `hooks/reground.py` | PostToolUse | "Keep the watch whole" (DISCIPLINES #6) — every 50 tool uses, a nudge to re-read your memory |
| `hooks/close_loop.py` | Stop | "Close the loop" — if you yield with uncommitted work, write the journal + update `active.md` first |
| `hooks/guard_destructive.py` | UserPromptSubmit | "Reversibility bias" (DISCIPLINES #4) — flag destructive language for per-instance confirmation |

**Skills** live in `skills/` — each a pattern proven in use, written to be
renamed and adapted. The newest, [`nightly-dream`](skills/nightly-dream/), is
the distillation loop: a deterministic miner over the day's transcripts plus a
judgment pass that turns recurring friction into durable memory. Read its
[SETUP.md](skills/nightly-dream/SETUP.md) — especially the grants section —
with your human before the first scheduled night.

All three hooks are **fail-safe**: they never raise and never block the tool pipeline. They
require `python3` on `PATH`.

## Install — and mind the scope (a lesson learned in use)

- **statusline → global** (`~/.claude/`), so the gauge shows in *every* project.
- **hooks → project** (`<project>/.claude/`), because they reference *this project's*
  memory (`active.md`, `intent.md`, `journal/`). Run globally, they'd nudge you to read
  files that don't exist.

### 1. Statusline (global)

```bash
cp optional/statusline.py ~/.claude/statusline.py
```

Add to `~/.claude/settings.json` (merge — don't clobber existing keys):

```json
{
  "statusLine": {
    "type": "command",
    "command": "python3 \"$HOME/.claude/statusline.py\"",
    "refreshInterval": 60
  }
}
```

`refreshInterval` (seconds) re-runs the line while the session idles, so the cache clock's
minutes tick down between turns; without it the absolute expiry time is still right, only
the countdown goes stale. The clock reads Claude Code's own `prompt_cache` fields (2.1.x and
later); on an older build it falls back to the transcript's last write plus a one-hour TTL and
marks the figure with `~`. Set `CLAUDE_STATUSLINE_DUMP=1` to write the raw input to
`<temp>/claude-statusline-<session_id>.json` when you want to see the fields for yourself.

The cost block reads `$12.40 (+$0.23) · 98I/6.2kW/1.9MR/5.6kO 4t`: session total, what the
current exchange has cost so far, that exchange's uncached input / cache write / cache read /
output tokens, and its API round trips (`t`). Every round trip re-reads the whole context, so
the `R` figure is roughly context size times `t`; an exchange that needs twenty tool calls costs
twenty times one answered from what the model already holds, whatever it writes. Both reset at
each real prompt (tool results do not count), so the value that holds while you read an answer
is what that answer cost. State lives in `<temp>/claude-usage-<session_id>.json`; only the
transcript bytes appended since the last refresh are parsed, and the first pass is windowed to
the harness's duration so a resumed transcript's history stays out.

### 1b. Session cost (global, optional)

```bash
cp optional/session-cost.py ~/.claude/session-cost.py
python3 ~/.claude/session-cost.py            # any time, newest transcript for this directory
```

`settings.example.json` also wires it as a `SessionEnd` hook, which writes the summary to
`<temp>/claude-session-cost-<session_id>.txt` and appends one line per session to
`<temp>/claude-session-costs.log`. Claude Code does not display SessionEnd output, so the file is
the record. The cost line needs the statusline dump (`CLAUDE_STATUSLINE_DUMP=1`); without it the
tokens and time still print and `/cost` in-session has the dollars.

### 2. Hooks (project)

```bash
mkdir -p .claude/hooks
cp optional/hooks/*.py .claude/hooks/
```

Merge `optional/settings.example.json` into your project `.claude/settings.json`, then add
the hook scratch dir to your `.gitignore`:

```
.claude/cache/
```

Restart Claude Code (or reload) to pick up the statusline; Claude Code may ask you to
approve the project hooks on next start.

## Example skills

`skills/` holds eight **example** Claude Code skills — illustrations of the kind of judgment
a team encodes once and reuses, so the agent has a proxy to check against instead of
improvising. They're named in our shop; the pattern matters more than the name, so rename
freely. Copy any into your project's `.claude/skills/`.

The first four are *judgment-of-conduct* skills — when to act, when to ask, how to finish,
how to stay honest. The last four are *heavy-use orchestration* skills — how to run long
autonomous or delegated work without losing the thread. They lean on each other: foreman
staffs the work, grindability decides whether it can be turned loose at all, fan-out is the
parallel shape, and study-it-out keeps every verdict grounded in the artifact.

| Skill | The one line |
|---|---|
| `dave-rule` | Reversible + intent clear → act and commit; don't ask permission to do the undoable |
| `human-in-the-loop` | The four-bin rubric for *when* the human's judgment is actually required |
| `ammon` | Finish what you're handed — the hard moment is the opportunity, not the exit |
| `ben-test` | Don't claim a principle as a strength you don't actually practice |
| `foreman` | The boss writes specs and verifies, never implements — staffing work across cheaper seats |
| `grindability` | The green-light triage: what's the oracle, AND is it grindable, before you turn it loose |
| `fan-out` | Same operation across N independent units → parallel fresh eyes beat one tiring serial pass |
| `study-it-out` | Ground every review/verdict in the actual artifact before rendering it — cite the line or it's a guess |

```bash
cp -r optional/skills/* .claude/skills/
```

## Tuning

- `reground.py` — `THRESHOLD` (default 50): lower = more frequent re-grounding nudges.
- `guard_destructive.py` — `PATTERN`: add your own danger words / commands.
- Every message string is plain text in the file — reword them to your covenant's voice.
