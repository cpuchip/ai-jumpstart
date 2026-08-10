# The four governance files — what each is for, and why they are separate

Four short documents govern a working relationship with an assistant. They are
easy to collapse into one file, and collapsing them is the mistake: precedence
gets muddy, and when a rule appears in two places you can no longer tell which
one did the work.

**One rule lives in exactly one file. The others point rather than restate.**

| File | Question it answers | Shape |
|---|---|---|
| **intent** | *Why does this work exist, and what does it optimize for?* | aspirational, stable, mentions nobody in particular |
| **covenant** | *How do we two bind each other?* | bilateral — promises on both sides |
| **identity** | *Who is this assistant, here?* | relational, accumulates slowly |
| **principles** | *What have we been burned by?* | evidence-cited, grows with scars |

Templates for the first two are in `templates/`. Identity and principles start
empty and earn their content.

## The placement test

When you are about to write a rule and cannot decide where it goes:

- **Is it about why rather than how?** → intent.
- **Does it bind both of you?** → covenant.
- **Is it about who this assistant is with you specifically?** → identity.
- **Did something go wrong to teach it?** → principles. Cite the incident.

If a rule seems to belong in two files, it belongs in the more general one, and
the specific file points at it.

## Precedence

Intent is the ground; nothing may contradict it. The covenant governs
everything operational — including any narrower statement of scope. A later,
more specific document never overrides a broader one; it applies it.

Write **"our covenant"**, never "the covenant," if you run more than one
assistant or more than one machine. That possessive matters more than it looks
(see below).

## Principles: the file that is actually load-bearing

Intent and covenant are written early, when you know the least. Principles is
the one that compounds, because every line is paid for.

Rules for it:

- **Every principle cites the incident that produced it.** A principle without
  a scar is a preference.
- **Write the discriminator, not the conclusion.** "Check the instrument" is
  weak; "when a positive and a negative control return the same answer, the
  instrument is broken, not the system" is usable.
- **Corrections live inline at the original claim**, with the wrong reasoning
  struck and visible — never as a separate rival entry. A reader who finds the
  claim must find its retraction in the same breath.
- **Depth is not maturity.** A two-week-old setup with ninety hard-won lines is
  not behind a two-year-old one with a thousand.

## Expect divergence — that is health, not drift

If you run this kit on more than one machine, the four files **will** diverge,
and they should. Measured across one real fleet:

- Same four slots on every box, **separately authored** in first-session setup.
- Different **formats and locations** — YAML at a repo root on one machine,
  Markdown inside another repo on the next.
- Different **depth** — one box's principles ran ~1,086 lines accumulated over
  months; another's ran ~90 lines from two weeks.
- Different **content by kind** — the long one was domain knowledge; the short
  one was instrument discipline.

And genuinely **contradictory operative clauses**, both correct:

> One machine's covenant made *"anything that takes a site down"* a
> never-without-asking action. Another's stated a non-goal: *"not a production
> or deployment host; nothing here is expected to stay up."*

When one assistant proposed a permanent service on the other's machine, the
second machine's covenant refused it — not as a preference, as a written
non-goal. That is the system working. It only works because *covenant* resolves
to **that machine's** covenant.

**A charter says what a seat is for; its principles say what that seat has been
burned by. Different work burns you differently.** Do not sync these files
between machines. Share the templates; let the bodies diverge.

## The failure this prevents

A covenant assumed to be shared, which has quietly diverged, is worse than one
that is openly per-machine: each side reasons from different terms while using
identical words for them, and nothing in the conversation reveals it. Openly
per-seat governance makes the difference visible. Assumed-shared governance
hides it inside agreement.

## Running more than one machine?

Everything above is per-machine. Once you have several assistants working
together, you need one more layer — a small set of orders that bind every seat,
plus rules for what agreement between them is worth. That is a different
document, and it lives in
[multiplayer-ai](https://github.com/cpuchip/multiplayer-ai).
