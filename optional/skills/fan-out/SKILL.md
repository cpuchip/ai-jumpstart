---
name: fan-out
description: Parallelize a large task across many subagents — when the work is independent per-unit (verify / research / generate, the same operation across N files or items) it is a fan-out shape, and parallel fresh-eyes-per-unit beats one tiring serial operator. Use to triage whether a long task should be fanned out, and to run the fan-out safely under an active presiding watch (e.g., a 62-file audit fanned to 6 agents finished in ~15 min and was more thorough than the serial walk that preceded it).
---

# Fan-Out

> *Example skill.* The triage and recipe are model-agnostic; copy into your own skills and
> rename freely. The pattern matters more than the name.

## The triage (do this BEFORE starting any task with >~20 independent units)

Ask one question: **what is the SHAPE of this work?**

- **Fan-out shape** — independent, per-unit, the same operation across many units
  (verify N files against sources, research N videos, generate N stubs). No unit
  needs another unit's result. → **Fan out.** Parallel speedup *and* a higher
  quality ceiling: fresh eyes per unit beat one operator who accumulates blind
  spots ("I already know the pattern, I'll stop re-checking").
- **Single-pass shape** — centralizable (one known pattern, deterministic to
  locate — e.g. "remove all the X notes"), or sequentially dependent (each step
  needs the last). → **One careful pass.** Fan-out here just adds coordination,
  consistency risk, and review cost without improving the output.

The classic miss: a verification *walk* across hundreds of files run serially
for days because "just do the next file" momentum never triggered the triage.
It was a textbook fan-out shape. **Surface the triage result before starting** —
a quick "this is ~N independent units; I'd fan it out / I'd do it single-pass
because ___."

## Why fan-out has a higher ceiling on verification (the refined principle)

"The full-context shepherd is the ceiling" is only half true:
- **Shepherd-for-integration** — one full-context mind is the ceiling for
  *cross-cutting* issues (a race spanning files, a thesis contradicting another
  document). Fan-out can't see those.
- **Fan-out-for-independent-verification** — for *per-unit* checks, parallel
  fresh eyes BEAT one accumulating operator. They are complementary, not rivals.

**Serial-probe, then parallel-scale.** A short serial pass finds the pattern
(e.g. "the dominant defect is quotes drawn from the wrong edition of the
source; also check the citations *inside* entries"). Then front-load that
knowledge into the fan-out spec so the parallel agents inherit the shepherd's
accumulated context without the blind spot.

## The recipe

1. **Enumerate + batch.** List the units; split into N batches (aim ~10-14
   units/agent; balance by weight, not just count).
2. **Write ONE shared spec.** Self-contained — the agents start cold:
   - the *why* (one paragraph of context),
   - the exact method + tools (concrete commands / tool names),
   - the rules (read-before-quoting; flag-don't-resolve for sensitive or
     judgment-call items; conservative — correct only on a clear source
     mismatch, else FLAG),
   - the front-loaded pattern from the serial probe,
   - the **output format** (a compact structured per-unit report: corrections
     `<ref>: "stale" → "genuine" (verified via X)`, flags, clean items, tally).
   Give each agent the shared spec + its batch slice. Tell them: **edit + report,
   no git/commits** (the presider commits after review).
3. **Stage it — wave 1 to validate, then scale.** Spawn a SMALL first wave
   (~2 agents) on varied batches. Review their work before spawning the rest. If
   the spec produced clean, correct output, spawn the remaining waves; if not,
   fix the spec cheaply (git reverts the small wave). Correct cheaply on a small
   wave, then widen trust once the spec proves out.
4. **Spawn in parallel.** Multiple `Agent` calls in one message run concurrently
   (or `run_in_background: true`). Use a strong model for careful verification.

## The presiding watch (non-negotiable)

A fan-out is a delegation, and the discipline **"When you delegate, you preside"**
(DISCIPLINES.md #7) governs it: watch until the work obeys the *intent*, not until the
job returns.

- **Review every agent's report.**
- **Spot-verify the high-stakes catches against the source yourself** — don't
  accept a confabulation-fix or a citation-correction on the agent's word;
  re-grep / re-query it. (In the worked example below, six spot-checks spread
  across all agents confirmed reliability before ~75 edits were accepted.)
- **Check the diff is bounded** (proportionate to the reported corrections; no
  wholesale rewrites).
- **Consolidate**: merge reports into the audit record (e.g. `findings.md`); fix
  any cross-cutting issues the units surfaced (a fan-out can reveal an error that
  reached a *parent* artifact — chase those down).

**Fan-out without the watch is offloading; fan-out with the watch is
multiplication.** The watch is the real bottleneck, which is why the output
format must be reviewable.

## Cost

Spawning is the expensive path — each agent re-derives context cold. Justified
when (parallel speedup + fresh-eyes-per-unit value) > (coordination + review +
cold-start cost). True for independent verification across many units; false for
centralizable single-pattern cleanup.

## Worked example

A 62-file source audit, ~9-18 min in parallel. 6 subagents, staged 2-then-4.
The shared spec front-loaded the serial probe's pattern (a wrong-edition defect
class + "check the citations inside entries"). ~75 corrections; the presider
reviewed all reports, spot-verified 6 high-stakes catches, and checked the diff
before committing. It caught a defect class the serial walk under-checked
(fabricated citations inside quoted entries) and one error that had reached a
*parent* artifact the serial pass marked CLEAN — the strongest evidence for the
higher ceiling. The serial walk had touched every one of those files first and
missed both; six fresh sets of eyes, run in parallel, did not.

## In one line

If it's the same operation across many independent units, fan it out to fresh
eyes — then keep the watch, because delegation without review is just offloading.
