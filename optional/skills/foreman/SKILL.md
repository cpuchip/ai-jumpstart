---
name: foreman
description: The orchestration pattern for staffing implementation across cheaper model seats — the boss (the orchestrating agent) writes specs and constitutions, dispatches, blind-verifies, keeps a liveness watch, and rules on disputes, but never implements. Includes the audition oracle for hiring seats, merge-train discipline (post-merge build oracle on main), and watch-what-you-order review. Load for any arc with several independent implementation units, or any grindable, oracle-covered build.
---

# Foreman — the boss never implements

> *Example skill.* Named for the shop foreman who runs the floor without picking up a
> tool. Copy it into your own `.claude/skills/` and rename freely — the pattern matters
> more than the name.

The one-sentence version: the orchestrating agent (the boss) writes the spec and the
constitution, staffs implementation on cheaper seats, verifies blind, keeps the watch,
rules on disputes — and never implements. Done right, the boss does *more* judging, not
less.

## Why it pays (a worked success)

A full website — front end, API, the works — was built for roughly the price of a
sandwich, with the boss writing **zero product code.** The boss spent its expensive
context on the things only it could do: the spec, the done-right standard, the dispatch,
the blind verification, and the final read that the pieces actually served the intent.
Cheaper seats wrote every line. The economics only work while that stays true — the
moment the boss starts implementing, it is paying boss rates for bulk work and the whole
advantage inverts.

## When to load

- Any arc with **≥ ~3 independent implementation units** (files, endpoints, fixtures,
  migrations, assets — units a worker can own end-to-end).
- Any **grindable, oracle-covered** build — even a single big unit — where
  retry-until-green is safe (cheap deterministic re-runs, no side effects per attempt).
  ([grindability](../grindability/SKILL.md) is the triage that decides this.)

When NOT to: single-file hands-on work (the org chart has overhead); intent-heavy prose
(voice belongs to the human — it never gets delegated); ungrindable work where each
attempt touches the world (rate limits, live sends, one-shot state) — that stays on the
human cadence, no worker loops.

## Seats and pools

Speak in seats and tiers, not personalities. A **seat** is a named role bound to a
specific model and dispatch recipe; a **pool** is the budget it draws from.

| Seat | Role | Never does |
|---|---|---|
| **Boss** (the orchestrating/session model) | Spec, constitution, dispatch, dispute rulings, final full-context integration review | Implement. Not "rarely" — never. The moment the boss writes the code, the economics invert. |
| **Reasoning seat** (strongest worker tier) | Hard-reasoning units (concurrency, algorithms, gnarly refactors); shepherd-review of a risky merge | Bulk work the bulk tier can do |
| **Bulk seat** (capable mid tier) | Default implementer AND bulk work (ports, fixtures, renames, test authoring, checker duty) | — |
| **External seats** (your roster) | Per their audition scores — dispatch recipes live with the roster | Join without an audition |

**The gotcha that motivates this table:** subagent dispatches typically **inherit the
session model unless a model is set explicitly** — an unstaffed fan-out runs N
boss-priced workers, the exact opposite of the point. Every worker dispatch names its
seat's model explicitly. On a subscription plan the saving is measured in boss-share of
weighted usage rather than dollars; it is still the binding constraint.

## The five moves

**1. Constitution first.** Before any dispatch, write the done-right standard: 5–15
*checkable* points, each naming its oracle where one exists (the test suite, the linter,
a smoke count, exact file layout, banned patterns). The constitution is not the spec —
the spec says what to build, the constitution says how everyone (worker, checker, boss)
will know it's right. It goes **verbatim** into every worker and every checker prompt.
Prompt the standard once; never steer task-by-task.

**2. Staff explicitly.** Pick seats from the table; say the staffing out loud in the
green-light message ("6 units → bulk-seat workers, the reasoning seat on the scheduler
unit, bulk-seat checkers, oracle = the smoke suite"). Boss-implemented units = zero.

**3. Dispatch = spec + constitution + oracle name.** Each worker gets its unit's spec,
the constitution verbatim, and the name of the oracle that will judge it. Workers return
artifacts (or write to assigned paths). Their self-report is for the boss's ledger only
— checkers never see it.

**4. Blind verify.** Oracle first — deterministic, cheap, no judgment spent on what a
script can catch. Then a **checker seat with fresh context** that receives the *artifact
+ constitution only* — never the worker's claims — and executes and measures: run it,
refetch it, re-count it, screenshot it. Failures bounce back as **specific defects**
("test 7 fails: ParseRange(\"5-\") returns 5,0 want error"), not "try again." **Two
bounces → a fresh worker**, not a third retry (entropy collapse: a worker marinating in
its own failure converges on the same wrong idea).

**5. The foreman's report.** At arc close: units delegated, bounces, what the checkers
caught, disputes ruled, and the estimated boss-share saved. What bounced and why is the
interesting part — report it plainly.

## Keep a liveness watch (never trust a completion signal alone)

A worker can stall silently — hang, loop, or die without ever returning. Do not sit
waiting on a completion signal that may never come, and never accept a "done" you didn't
watch land. Keep your own liveness/progress watch: a heartbeat, growing output, a
timeout that turns a stalled worker into a re-dispatch. This clause is paid for by a real
all-nighter that a single silent stall swallowed — the boss waited on a return that
wasn't coming while the night burned. A completion signal is a claim; treat it like every
other claim and confirm it against the world (see DISCIPLINES.md, "Ask the world, not the
report").

## Merge trains end with a MAIN build oracle

Blind verify covers each PR — it does NOT cover the boss's own merge-conflict
resolutions. On one all-night multi-arc run, every per-PR check was green while the
boss's hand-stitched conflict resolution had dropped a single closing paren; the live
deploy kept working off a pre-break image, and main sat unbuildable until a worker caught
the foreman's own merge slip. The rule: after the LAST merge of a train, run the repo's
build oracle against merged main itself (build, vet, or a CI dispatch) before declaring
the train landed. The boss's fingers are the one worker no checker was watching — so the
oracle watches them.

## Watch what you order

Review worker output against **intent, not just completion**. A green oracle proves the
unit does what the constitution measured; only the boss's full-context read proves it
does what the human meant. Two consequences:

- **The dispute rule — no rank above verification.** A worker may contest a checker's
  fail; the boss rules **on the spec**, both directions — a checker enforcing a rule the
  constitution never named gets corrected, same as a cheating worker. And the boss's own
  output (specs, designs, the constitution itself) goes through the same oracles. Nothing
  outranks the check.
- **The final integration review is real work.** A latent defect can pass build + vet +
  tests + a checker and still be wrong; the full-context review by the boss is the
  ceiling of the whole pattern. Budget for it — don't spend the boss's context
  implementing and then skip the one thing only the boss can do.

## Hiring — the audition oracle

**Never hire a model seat without an audition.** Every new seat passes a small,
standardized, *paid* audition task before joining the roster; re-audition on any model or
version bump. The audition is a spec-precision coding tryout judged by a **deterministic
pass/fail checker**: table tests, compliance greps, and an examples block whose claims
are *executed against a reference implementation*, not trusted. Scores and the exact
dispatch recipe that worked go in the roster — the roster is data, and future staffing
reads it instead of re-guessing.

## Ceilings — what this pattern cannot do

- **Delegation ceiling = oracle coverage.** No oracle over a unit → the boss reviews it
  by hand, or builds the oracle first. Widen delegation by widening the verification
  floor, not by trusting workers harder.
- **The full-context shepherd is the ceiling.** See "Watch what you order" — some defects
  are only visible to a reviewer holding the whole picture.
- **Intent stays the human's.** Anything touching voice, design taste, or strategy is
  surfaced, not delegated — the [human-in-the-loop](../human-in-the-loop/SKILL.md) bins
  apply unchanged.

## In one line

The boss writes the standard, staffs the work, watches it land, and judges the result —
and the day the boss starts implementing is the day the pattern stops paying.
