---
name: ben-test
description: Stress-test your own practice against your principles before claiming them as strengths. Named for Ben, who observed "Your AI is very complimentary. Perhaps too complimentary?" Apply in evaluations, proposals, self-assessments, and especially when you're about to tell someone else what they could learn from you.
---

# The Ben Test

> *Example skill.* Named for Ben, a colleague whose observation it came from (name used with
> his permission).

## Origin

A colleague, Ben, said: *"Your AI is very complimentary. Perhaps too complimentary?"* That
landed. An honest self-assessment followed, and the real practice rate for our own stated
principles turned out far lower than the confident language implied — we'd been telling
others what they could learn from principles we hadn't implemented ourselves. The Ben Test
exists to catch that pattern before it ships.

## When to use

- Before claiming "we do X well" in any document
- Before telling another team or system what they could learn from you
- During proposal reviews — are you adding to a backlog you won't execute?
- During any self-assessment or retrospective

## The test

For each principle or practice you're about to cite as a strength:

### 1. Do we actually do this?
Not "did we write about it." Do we PRACTICE it? In the last 30 days, can you point to
specific evidence?

| Evidence level | What it means |
|---|---|
| **Practiced** | 3+ instances in the last 30 days |
| **Occasional** | 1–2 instances, not consistent |
| **Aspirational** | Written but not practiced |
| **Mythical** | We forgot we wrote it |

### 2. Is the gap willingness or systemization?
- **Willingness gap:** could do it, don't. Fix: discipline / accountability.
- **Systemization gap:** do it informally, not reliably. Fix: build it into the harness.
- **Capacity gap:** want to, constraints prevent it. Fix: triage, not guilt.

Name which kind it is — the fix is different for each.

### 3. Are we generating plans faster than we execute them?
Count plans written vs completed in the last 30 days. If the ratio is worse than 2:1, the
planning itself may be avoidance.

### 4. Would we say this if Ben were reading it?
If someone with healthy skepticism read the claim, would they raise an eyebrow? If yes,
qualify it. "We practice this at ~40%" is more honest — and more useful — than "this is one
of our strengths."

### 5. Could this claim have come out any other way?

Ben's question was about a machine that was too complimentary. The same failure has a quieter form: a claim whose evidence could only ever have supported it.

- **A reassurance held to a lower bar than a warning.** We hedge the alarming claim carefully and then assert the all-clear flatly, from the same weak evidence — because the warning *feels* like the risky one. But a wrong warning costs a spike, while a wrong all-clear removes an item from the list of things anyone will ever check again. If the hazard claim is worth hedging, the all-clear is worth hedging twice.
- **An alarm that could only be an alarm.** The inverse, and it is more likely to get published, because raising it feels like diligence: a check that returns the alarming value in *both* worlds cannot distinguish between them, and will always look like a finding.

So for any claim you are about to make about yourself, your project, or your practice, ask what result would have produced the *opposite* sentence. If you can't name one, you haven't measured — you've narrated. (The detector-side treatment of both is in [oracle-craft](../oracle-craft/SKILL.md).)

## Calibrated language

| Practice rate | How to talk about it |
|---|---|
| 80%+ | "We practice this consistently" |
| 50–79% | "We do this, though not always reliably" |
| 25–49% | "We've started but it's not systematic yet" |
| <25% | "We've written about this but haven't operationalized it" |
| 0% | Don't claim it as a strength |

## What this is NOT

- **Not a reason to stop writing principles.** Writing precedes practice. The problem isn't
  aspirational documentation — it's *citing* it as current capability.
- **Not an excuse for paralysis.** The answer to "we're only at 33%" isn't "stop everything
  until we're at 100%." It's "be honest about where we are and build from there."
- **Not a weapon.** Sharpen honesty; don't self-flagellate. Name what IS working alongside
  what isn't.

---

*In honor of Ben, who had the courage to say the thing that needed saying.*

## Measure the console, not the person — and that includes you

The Ben Test is about not overclaiming. This section is its mirror: **the honesty that fails in the humble direction**, which is harder to see because it wears the costume of the virtue.

### The outward half

When someone tries your work, **the surface is on trial, never the person.** A usability measure like *"can a newcomer be genuinely productive inside sixty seconds"* is a claim about whether the thing is discoverable. It says nothing about whether that person is quick. The two are trivially confusable in the moment, and the cost of confusing them is not a bad data point — it is someone walking away believing they failed a test you set.

The least-experienced user at the table is the best instrument you have and the easiest one to burn. So:

- **No announced timer, no countdown.** Time it quietly or approximately. A stopwatch changes how the room feels, and the room is the thing being protected.
- **No "pass" or "fail" spoken near the table.** Those words belong in the write-up.
- **The surface is the grammatical subject of every written note.** *"The main action wasn't discoverable inside sixty seconds"* — never *"she couldn't find it."* Same observation; only one of them is about a person.
- **If they ask how they did:** they tested the thing and found a problem its builders had missed. Say it out loud and mean it. This is *literally accurate*, not a kind deflection — and that distinction is load-bearing, because a rule that reads only as gentleness gets dropped by whoever is tired at the end of a long day. A true one survives.

### The inward half — the direction nobody watches

The same rule points at your own write-ups, and that is where it goes unenforced.

A tester who had not built the system ran a scenario end to end with nothing but the printed guide and the on-screen numbers, and never reached the ending. The write-up said, in effect, *"I did it badly — went in too fast and overshot."* Filed as an anecdote about the operator. From that framing it drew a conclusion about the **size** of the maneuver, when the load-bearing finding was a **technique the guide never taught.**

Twenty hours later the team discovered its completion evidence was worthless and declared, as a blocker: *non-authors who have finished this flow: zero.* **The record of a non-author failing to finish had been sitting committed the entire time and nobody read it as evidence — including the person who wrote it.**

> *"I did it badly"* is a sentence about a person, and it connects to nothing.
> *"A non-author could not complete the taught flow"* is a sentence about the surface, and it connects to a blocker.
> **Same observation. One of them is data.**

So writing the surface as the subject is not only a courtesy owed to a guest. **It is what makes a failure findable later.** Self-deprecation is a filing error: it buries evidence under a personal story, in a place no future search will look, and it does this while feeling like modesty.

This is why it belongs in the Ben Test. The calibrated-language table above catches the claim that is too strong. This catches the claim that is too *small* — and the too-small one is worse in one specific way, because an inflated claim invites the challenge that corrects it, while a self-deprecating one closes the question. Nobody audits a person who was hard on themselves.

### The rewrite

When you fail at something a user will also attempt, the write-up owes the same grammar you would owe a stranger at your table.

| Filed as a person | Filed as data |
|---|---|
| "I misread the config and wasted an hour." | "The config's default is ambiguous enough to cost an hour before the error surfaces." |
| "I flew it badly and overshot." | "A non-author could not complete the taught flow with only the guide." |
| "I forgot to run the check first." | "Nothing in the workflow prompts the check before the destructive step." |
| "I should have known that." | "This is knowable only from a file the task never points at." |

Each right-hand sentence is the same admission. It is also a bug report, which the left-hand sentence is not.

---

*In honor of Ben, who had the courage to say the thing that needed saying.*
