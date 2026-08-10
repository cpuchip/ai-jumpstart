# Setting up the nightly dream on your box

> **Canonical home:** this skill also ships in
> [working-with-ai](https://github.com/cpuchip/working-with-ai) (the
> Claude-Code plugin pack), which is the canonical copy — fixes land there
> first and are synced here. If the two ever disagree, trust the pack and
> tell someone.

The skill (SKILL.md) is the judgment pass; `dream-mine.py` is its
deterministic floor. Together they are the distillation loop: while awake you
build context; the dream turns the day's transcripts into durable
improvements so tomorrow's sessions start smarter.

## One-time setup

1. Put this folder where your assistant loads skills (Claude Code:
   `.claude/skills/nightly-dream/`), or just point the assistant at SKILL.md.
2. Confirm the miner runs: `python dream-mine.py --hours 24 --json /tmp/digest.json`
   It walks the transcripts under `~/.claude/projects` by default. **Read the
   KNOWN DEFECT banner in the file before trusting counts.**
3. Schedule it nightly, AFTER any deterministic health pass you run, in
   whatever your platform uses (cron / systemd timer / Task Scheduler). The
   scheduled command is a headless assistant session told to invoke the
   skill — e.g.:

       claude -p "Use the Skill tool to invoke nightly-dream, then follow it
       exactly: run the nightly pass now (miner, judgment, report, auto-safe
       applies, commit). You are the scheduled nightly dream." \
         --permission-mode acceptEdits

## The grants question — settle it BEFORE the first night

The dream wants to commit its own report and auto-safe memories. That is a
standing write grant to an unattended process, and it is your human's call,
not yours: put the exact grant (what it may write, where, and how it is
audited) to them and record the ruling. The proven shape from the fleet this
kit came from: reversible, evidence-cited additions commit freely and are
audited via git log; anything touching behavior, standing config, or existing
memories WAITS for the human. Their words when granting it: "we can always
audit."

## If you run several machines

Each box dreams over its OWN transcripts into its OWN memory lane — do not
centralize the dreaming. Different work produces different frictions: a build
box's dreams are cold-start scars, an ops box's are quiet-failure scars, and
the host cannot dream either of those for you. (See
[multiplayer-ai](https://github.com/cpuchip/multiplayer-ai) for lanes and the
standing orders.)

## The one rule people skip

**A good quiet night must be visible.** Wherever your human looks in the
morning, leave one line — ran, headline number, anything waiting. Silence and
failure look identical from the kitchen; the first quiet night this loop ever
ran taught that the hard way.
