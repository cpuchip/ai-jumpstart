---
name: nightly-dream
description: The nightly dream — cross-session distillation of your own agent transcripts into durable improvements. Runs a deterministic miner over the day's sessions, clusters recurring friction by diagnostic signature, judges the top clusters against existing memory, and proposes evidence-cited changes; auto-applies only reversible additions, everything else waits for the human. Invoke nightly on a scheduler, or by hand after a heavy session ("run a dream over today").
---

# Dream — the nightly distillation

Karpathy's framing, built the house way: while awake we build context; sleep
distills it into weights. Sessions restart from zero — so the distillation
must be a *process we run*, not a hope. A deterministic health pass is one half: staleness, drift, linkrot, golden recall. The dream is the judgment half: what the transcripts show about HOW the work went, turned
into changes so tomorrow's sessions start smarter.

The dream never re-reads raw days. Evidence first, judgment second:

## The pass

1. **Mine.** `cd scripts/brain-v5 && python dream-mine.py --hours 24 --json C:/tmp/dream-digest.json`
   (widen `--hours` only when nights were missed). The digest clusters tool
   errors by diagnostic signature, plus denials, interrupts, retry loops.
2. **Join the deterministic pass.** If you also run a scheduled health check
   (staleness, drift, link rot, fixture failures), read its report — those
   findings are co-equal evidence with the transcript ones.
3. **Judge the top clusters** — ranked by `count × sessions` (cross-session
   beats loud-once). For at most ~8 clusters, follow the sample's session
   pointer back into the transcript ONLY where context is needed (grep near
   the quoted error; never read whole files). Ask of each: is this friction
   *recurring*, is it *preventable*, and is the prevention *durable* — a
   memory, a CLAUDE.md line, a tool fix, a skill amendment, a lint?
4. **Check existing memory first** (MEMORY.md + the named files). Three
   outcomes: already covered (note the memory failed to prevent it — that is
   its own finding about placement, not a reason to write a duplicate);
   covered but stale/wrong (propose the update); genuinely new (propose).
5. **Classify every proposal:**
   - **AUTO-SAFE — apply tonight:** new reference/feedback memories recording
     a recurring friction + its proven fix (append-only, evidence-cited,
     reversible); MEMORY.md index lines; typo/index repairs. Commit them.
     Write memories to whichever store your setup treats as canonical, and
     say in the report where they landed. LIVE-PROBE before re-raising a
     previously ruled item — window evidence may predate the fix, and a
     miner that filters files by mtime will happily re-report a bug you
     closed last week.
   - **WAIT AT THE HINGE:** CLAUDE.md/skill amendments, tool code changes,
     memory retractions, anything touching behavior or standing config.
     These go in the report, and a hinge card when any exist.
6. **Write the report** to `the report path your setup uses` (overwrite; git
   history keeps the nights): date, digest stats, numbered proposals — each
   with the cluster stats, ONE short transcript quote + session ref, the
   proposed change, and its class. Applied auto-safe items listed as applied.
7. **Close:** commit the report and any auto-safe changes (a dream that
   cannot commit is a dream nobody wakes up to); open a review card only if
   WAIT items exist; and **always leave a one-line note wherever your human
   actually looks in the morning** — a dashboard, a file they open, a message.
   A good quiet night must be visible, or silence and failure look identical
   from the kitchen. That last rule was learned the hard way: the first
   quiet night reported nothing, and read exactly like a night that never
   ran.

## Rails (non-negotiable)

- **Budget:** one digest read + at most ~8 transcript spelunks. An empty or
  thin digest = a one-line report and stop — no invented work.
- **The bar is recurrence, not annoyance.** One-off errors stay in the
  digest's history; only patterns (2+ occurrences or 2+ sessions, or one
  occurrence of a class that already has a memory) earn a proposal.
- **Never weaken a memory from transcript evidence alone** — transcripts show
  what happened, not what was ruled. Contradictions with a standing decision
  get a WAIT proposal quoting both sides: testimony beats inference, but a
  ruling outranks a bad night.
- **Privacy:** transcripts may contain secrets that leaked into output.
  Quotes in the report are minimal fragments; never quote credential-shaped
  strings — describe them ("a path-secret appeared in plaintext at ...").
- **The dream proposes; the hinge disposes.** Same law as everything else.
