---
name: grindability
description: The green-light triage for any long or autonomous work — ask "what's the oracle?" AND "is it grindable?" before committing to the shape. Use at the moment of green-lighting any overnight or unattended run, fan-out, "keep marching" arc, soak, migration walk, bulk verification, or agent-loop dispatch. Also triggers when sizing why an autonomous run underperformed. Companion to fan-out (the parallel shape) and foreman (the staffing pattern).
---

# grindability — the oracle's twin

> *Example skill.* The triage below is model-agnostic; copy it into your own skills and
> rename freely. The pattern matters more than the name.

**Verifiable isn't the bar — grindable is.** An oracle tells you *whether* an attempt
succeeded; grindability is whether you can afford *many attempts*: cheap, deterministic,
side-effect-free retries — a sandbox you can reset, a test you can rerun, a build you can
throw away. Autonomy compounds exactly where both hold. Where each attempt touches the
world (rate limits, live sites, sends, spends, one-shot state), no oracle quality makes
long unattended grinding safe. The canonical contrast: a test suite in a resettable
sandbox is grindable; a rate-limited live site is not — no matter how good the check.

## The two questions, asked together

1. **What's the oracle?** The deterministic check that says pass/fail without you
   (build/test/lint/diff/exit-code).
2. **Is it grindable?** Can attempt N+1 run immediately after attempt N failed, at ~zero
   cost, with no residue? (Reset-able sandbox · replayable input · idempotent target ·
   no external quota/party in the loop.)

## The four quadrants → what each green-lights

| | **oracled** | **no oracle** |
|---|---|---|
| **grindable** | ★ Let it run — autonomous goal loops, overnight runs, fan-out, retry-until-green. This is where autonomy compounds. | **Build the oracle first** — the detector is the actual first task; grinding without one just launders guesses. |
| **ungrindable** | Human-cadence checkpoints: act in small verified steps, surface between them. The oracle helps *judge* each step, but retries are expensive/dirty, so no unattended loops. (Deploys, live-DB migrations, anything where a probe against the live system is the only proof.) | Don't automate. Do it by hand with eyes on, or reshape the task until it moves quadrants. |

## Raising grindability is usually the real first task

Most "ungrindable" work is one artifact away from grindable — and building that artifact
beats grinding carefully:

- **Live system** → scratch container / disposable replica you can rebuild and replay
  against
- **One-shot state** → replay file / fixture / seeded world (e.g., a headless game
  driver replaying a recorded run)
- **External API with quotas** → recorded fixtures for the loop; the real call only at
  the final verify (the verify-on-the-real-path rule still applies to the *last* run)
- **Prod-only reproduction** → capture the failing input once, grind against the capture
- **Costly model calls** → grind the harness with a local/cheap model; the premium model
  only for the final pass

If no such artifact is buildable, that's the signal the work belongs on the human's
cadence — which is a scheduling fact, not a failure.

## The companion mechanism: entropy collapse

Long solo grinding degrades: an autoregressive model marinating in its own prior outputs
loses diversity (each attempt more like the last — the same wrong idea, retried politely).
The fix lives at the **prompt level, not the sampler**: fresh eyes per attempt (fan-out),
or **opposed mandates** (one attempt told to attack what the previous defended). This is
*why* council beats solo, and why the [fan-out](../fan-out/SKILL.md) skill's
fresh-context-per-unit shape out-performs one tiring serial operator on grindable work.

## Applying it (30 seconds at green-light)

1. Name the oracle. None? → building it is step 1 (or the work isn't autonomous yet).
2. Name the reset. "How do I cheaply undo/rerun attempt N?" No answer? → name the
   artifact that would create one, or drop to human-cadence checkpoints.
3. Pick the shape: grindable+oracled → autonomous loop / fan-out / overnight; add opposed
   mandates if attempts will iterate on each other.
4. Say the classification out loud in the green-light message — "grindable+oracled
   (sandbox X, oracle Y), letting it run" — so the shape is auditable.

## In one line

Before you turn anything loose, ask both questions together: what's the oracle, and can
it grind? Autonomy compounds only where both are yes.
