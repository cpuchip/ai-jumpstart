# WORKSPACE — one root, many lifecycles

*How to hold a durable memory, a reference library, and many code projects in one
workspace without tangling their git histories. Optional, for when you outgrow a single
folder. Like everything in this kit, a real failure stands behind it.*

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

## Where the memory lives

This layout is the *where* for practices the kit already teaches. [Make It
Portable](PRACTICES.md) (Practice 5) says to write the work down in files beside the work;
the brain repo is where those files live. The [creation cycle](CYCLE.md)'s steps on
intent, covenant, and line-upon-line memory all point at that same private repo. The
layout adds no new practice — it gives the ones you have a clean house to run in.
