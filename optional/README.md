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
| `statusline.py` | statusLine | Situational awareness — model, context %, and the 5h / 7d usage gauges, always in view |
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
    "command": "python3 \"$HOME/.claude/statusline.py\""
  }
}
```

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
