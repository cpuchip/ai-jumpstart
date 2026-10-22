# WORKSPACE — one root, many lifecycles

*How to hold a durable memory, a reference library, and many code projects in one
workspace without tangling their git histories. Optional, for when you outgrow a single
folder, and for the later day you weigh a second agent or a second machine. Like everything in this kit, a real failure stands behind it.*

The rest of the kit assumes one project in one folder. Once you work across several — a
few apps, a pile of reference material, and an assistant whose memory you want to keep —
you hit a structural problem the single-folder setup doesn't have. This file describes
the layout that solves it. It is model-agnostic and git-only; nothing here is specific to
any one assistant.

## The problem: three lifecycles, one history

Put a brain, a reference library, and your code projects in one repository and you have
jammed three things with opposite git needs into a single history:

- **Instructions and memory** — your intent, your covenant, your journal, the skills you
  have tuned — want *private* version history. You want to diff them and walk them back,
  but never publish them.
- **Reference material** — the corpus you read against, downloaded docs, material that
  was never yours to publish — wants *no git at all*. It is large, it churns, and it
  isn't yours to ship.
- **Code projects** want their *own* identities. Some public, some private, each with its
  own remote, its own release cadence, its own contributors.

One history cannot serve all three. So you reach for `.gitignore`, and now a
hand-maintained denylist is the only thing standing between "private" and "published."
Every `git add -A` is a bet that the list is still complete. Miss one line and private
content lands in a public commit, where deleting it later doesn't remove it — it lives in
history until you rewrite the whole thing.

That is not hypothetical. The workspace these practices came from committed material into
a public history that a single wrong `add` had swept in, and un-leaking it took **two
full history rewrites**: one to scrub the public repo, one to move the true history
somewhere private. The denylist hadn't failed dramatically. It had quietly fallen one
line behind the tree, which is what a denylist does eventually.

## The layout: walls by location, not policy

The fix is topological. Stop asking a list what to hide. Make an **untracked root** hold
**tracked sub-repos**, so anything that shouldn't be in a repo simply isn't inside one:

```
workspace/                  ← UNTRACKED root (no .git here, ever)
  AGENTS.md / CLAUDE.md     ← base instructions; assistants walk parent dirs, so
                              every session in any subfolder inherits these
  private-workspace/        ← THE BRAIN: its own PRIVATE git repo
    AGENTS.md               ← extends the base; memory, skills, journal, specs
  context/                  ← reference material: untracked by location —
  external_context/           no rules needed; it simply cannot leak
  projects/                 ← independent repos, each its own git identity
    my-app/    (public)
    my-notes/  (private)
```

The root has no `.git`, ever. It is a plain directory that happens to contain
repositories. The brain is one private repo. Each project is its own repo with its own
remote. The reference folders are tracked by nothing — not because a rule excludes them,
but because there is no repository at that level to include them.

## Why it works

- **Each lifecycle gets its native git posture.** The brain keeps private history; each
  project keeps its own public-or-private identity and release cadence; the corpus keeps
  none. Nothing is forced to share a history with something whose needs are opposite.
- **The corpus needs no `.gitignore`, and sits at one stable path.** It lives outside
  every repository boundary, so there is nothing to exclude it *from* — and every
  project, session, and git worktree reaches it at the same path. A folder no repo can
  see needs no rule to stay unseen.
- **A leak now takes a deliberate act, not a forgotten one.** To publish private content
  you would have to copy it *into* a repo on purpose. The failure mode inverts: from
  "forgot to exclude" (silent, easy) to "explicitly included" (visible, hard). That is
  the whole point — walls you can't forget to build, because they are made of location
  rather than vigilance.
- **Memory persists while every project stays clean.** Your assistant's journal, intent,
  and tuned skills live in the brain repo and survive across every session and every
  project you touch. The projects themselves carry none of that weight; they hold code
  and nothing else.
- **One base instruction can govern all of it.** Many assistants load their instructions
  by walking up the directory tree from wherever they are working (Claude Code does this
  for `CLAUDE.md`), so a single base file at the root is inherited by every session in
  every subfolder, and a subfolder's own file *extends* it — the root carries what's true
  everywhere, the brain and each project narrow it. Where a tool only reads one fixed
  location, symlink or copy the base there, the same move the [README](README.md)
  describes for placing `AGENTS.md` where your assistant looks.

## Migrating an existing workspace

You don't need a big-bang move. Every step is reversible until the moment you re-home the
brain:

1. **Stand up the brain repo first.** Create `private-workspace/`, move your instructions,
   memory, journal, and skills into it, and give it a *private* remote. Nothing published,
   everything backed up.
2. **Move projects out one at a time.** Each project is already, or becomes, its own repo;
   a plain move (or `git mv`) preserves its history. There's no coupling and no rush — do
   them as you touch them.
3. **Leave reference material where it lands.** Drop `context/`, `external_context/`, and
   any corpus at the root, then delete the `.gitignore` lines that used to hide them.
   They're outside every repo now, so those rules are dead weight.
4. **The root never gets a `.git`.** If you ever catch yourself about to run `git init` at
   the workspace root, stop — that single command is the exact move this layout exists to
   prevent.

## One agent or many: decide before you add the second one

Everything above assumes one assistant, in one workspace, on one machine. Most people never
need more than that, and the kit is complete without the rest of this file. What follows is
for the day you consider a second agent or a second machine, written so you can judge the
trade for yourself. The vocabulary: a **box** is a machine; a **seat** is one running
assistant session with a named role; a **room** is the shared channel the seats talk in.

**The signals that you have outgrown one seat.** Any one of these is a reason to think about
it; two together are a reason to act:

- The work splits into independent units a second worker could own end to end, and a
  deterministic check (a test suite, a linter, a diff against a known answer) can judge each
  unit without you reading it. Work without that check does not get cheaper with more
  hands; it gets more expensive to review.
- A job has to keep running after your laptop closes, so it needs a box that stays on.
- A job needs hardware the first box lacks: a GPU, more memory, a second disk.
- One session keeps switching between unrelated projects, and its memory and context pay
  for every switch.

**What the second seat costs, measured in the house this kit came from.** The work itself
was never the expense. Coordination was. One night of agents broadcasting to the whole room
by default, with ordinary politeness (acknowledgments, confirmations, restating a finding
back to its author), consumed close to a quarter of a week's compute budget, and every one
of those seats was doing its job well. The norms that fixed it are five short rules
(address one recipient; silence is acknowledgment; paste the artifact and three lines, not
prose; close once and go dark; claim a shared thing before touching it), published as the
[room-norms skill in working-with-ai](https://github.com/cpuchip/working-with-ai/blob/main/skills/room-norms/SKILL.md).
Two more costs arrive with the second seat whether or not it has a room. Somebody has to be
the foreman: the seat that writes the spec, dispatches, verifies blind and rules on disputes,
and never implements, because the moment the foreman writes the code the economics invert
([foreman skill](https://github.com/cpuchip/working-with-ai/blob/main/skills/foreman/SKILL.md)).
And a shared checkout becomes a hazard: on this house's tree one `git stash` swept every
seat's uncommitted edits, and three seats then committed other seats' files under their own
messages. The rule that came out of it is to commit by explicit path only
(`git commit -m "..." -- <your files>`), never stash, never `git add -A`, and merge rather
than rebase when the remote has moved.

**A recommendation, not a rule.** Stay with one seat until two of the signals hold and you
have the deterministic check for the work you would hand off. Then add a second seat on the
same box before you add a second box, because the second box breaks something the second
seat does not, and that is the next section.

## The second machine: three layers, each fact in exactly one place

The layout earlier in this file puts one base instruction file at the untracked root and
lets every subfolder extend it. That held for a year on one machine. It failed on the first
day a second machine joined, and the failure is worth describing because it is quiet.

The second box was Linux. The root file it inherited said Windows 11, Git Bash, Windows-style
paths for inline Python, and listed six folders the new box did not have. The session-start
hook handed the new seat another seat's charter and called it "your post". Touching a file
inside the brain repo pulled the first machine's house rules into context by proximity (the
assistant loads any instruction file it finds near a file it reads), including an order to
write memory into a repository the new box only mirrored. A shared script carried the first
machine's absolute path, so on the new box every git query hit a missing directory and it
printed "clean" over an unpushed commit. None of this raised an error. The assistant followed
rules written for a different machine with full confidence, which is the failure mode to
design against: every instruction a seat loads has to be true on that box, true for that
seat, and consistent with everything else it loads.

The fix is to sort every fact into one of three layers and keep each fact in exactly one:

| Layer | What lives there | One file or source |
|---|---|---|
| **Universal** | the base covenant and intent, the standing orders, what each space *is* (never whether it is present) | versioned root files, in one repo every box checks out |
| **Box** | OS and shell, what is checked out here, which corpora are present, hardware, the agent's OS user, rules that only apply on this machine | `box.md` at that box's root, one per machine |
| **Seat** | the seat's charter (its post, what it may do unasked), its lane, its chat identity | rendered per seat at session start from a record, never copied from another seat |

The root of each box then holds a two-line glue file (`@<repo>/root/AGENTS.md` and
`@box.md`) plus that box's `box.md`:

```
workspace/                    <- untracked root on EVERY box
  AGENTS.md / CLAUDE.md       <- two-line glue: imports the universal file and box.md
  box.md                      <- THIS machine: OS, shell, what is present, hardware, its rules
  fleet/root/AGENTS.md        <- the universal file, versioned, identical on every box
  private-workspace/          <- the brain, as before
```

Four rules fall out of the table. No file states a fact from a lower layer (the universal
file loses "Windows 11" and gains `@box.md`; the space map says what each folder is *if
present*). Hooks point at files and say whose they are; they never restate a count, a size
or a charter, because every restated copy goes stale on its own schedule (ours said "the
five orders" for three weeks after there were six). The root is rendered from versioned
files, so drift between boxes is a `git diff` and not a surprise. And the layers get an
oracle: a check that runs on each box, goes red on a box fact in a universal file, a missing
`box.md`, or an absent folder the instructions claim is present, and went red before the
fix landed and green after.

Two measured details that will bite anyone who builds this with Claude Code. An
`@`-import inside a *symlinked* instruction file resolves relative to the link's target, so
a shared root file that says `@box.md` hands every box the same `box.md`; the glue file has
to be a plain file per box. And a missing `@`-imported file is dropped silently, which is
why the oracle has to exist. The proximity problem (another box's nested instruction files
loading when you touch its tree) is closed with Claude Code's `claudeMdExcludes` setting,
measured on 2.1.283: the nested file loaded on every read without it and never with it.

On the OS user: one agent user per box by default (`claude` on the Linux boxes), with
your own account left alone, and a separate user only for a seat that holds a secret
the other seats must not read. The wall goes where the secret is, which is the same
principle as the untracked root.

## The lessons, in the order they were paid for

- **Box facts in a universal file** are the first thing a second machine breaks, and the
  break is silent. Sort by layer before the second box, not after.
- **A restated fact is a second copy with its own expiry.** Hooks and helper text point;
  they do not repeat.
- **Instruction files load by proximity.** Reading one file in another box's tree can pull
  that box's house rules into the seat. Exclude foreign trees explicitly.
- **A mirror pulled at session start is stale by the afternoon** in a session that runs for
  days. Freshness is per read, not per start.
- **Recall fails before recording does.** One seat's in-flight board reached two thousand
  lines, and a fact written at line 3104 was never recalled; a compaction summary later
  invented a measurement. Keep the board lean, move closed work to a journal, and re-ground
  from files after every compaction.
- **A shared script with one machine's path is a blind instrument.** It reports "clean" on
  a box where it could not look. Derive paths from the script's own location.
- **Shared checkout, explicit paths.** Never stash, never add everything, merge rather than
  rebase.
- **The room is the expense.** Direct address, silence as acknowledgment, claims before
  touching shared things. Measure the coordination cost; it is the one that grows with the
  number of seats, which is exactly the number you added seats to increase.
- **Every layer needs an oracle that has been seen red.** A grounding check that has never
  failed is an opinion about the layout, not a measurement of it.

The sequence these came in is the argument for the order of this file: walls by location
first, one seat until the signals say otherwise, a second seat before a second box, and the
three layers before the second box's first session. The companion book for the room side
(norms, pairing machines without secrets in flight, presiding over seats) is
[multiplayer-ai](https://github.com/cpuchip/multiplayer-ai).

## Where the memory lives

This layout is the *where* for practices the kit already teaches. [Make It
Portable](PRACTICES.md) (Practice 5) says to write the work down in files beside the work;
the brain repo is where those files live. The [creation cycle](CYCLE.md)'s steps on
intent, covenant, and line-upon-line memory all point at that same private repo. The
layout adds no new practice — it gives the ones you have a clean house to run in.

## A law for anything standing

When you add a standing system to this house — a memory store, a watcher, an always-on
helper — design its resting metabolism to zero: it should cost nothing while idle, ride
work that was already happening, and bill per use, never per hour. In a four-generation
lineage of memory systems, every one that had to be fed died when its feeder got tired
or its food got expensive; the survivor was the humble file, which eats nothing. The
corollary: trust follows the read-path — a new system wins by making the surface people
already read better, never by demanding they migrate.
