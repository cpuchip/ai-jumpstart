# AI Jumpstart

**Point your AI assistant at this repository and it will set up — and practice — a
disciplined way of working with you.** Counsel before building, bounds before
delegation, verification before assertion, a journal before closing. Works with any
capable model: Claude, GPT, Gemini, or whatever comes next.

> **Sibling kit:** [working-with-ai](https://github.com/cpuchip/working-with-ai)
> is the full Claude-Code-native version of this discipline — fifty skills,
> agents, and a bilateral covenant, installable as a plugin. This repo is the
> on-ramp; that one is the toolshed.
>
> **Working with more than one machine, or more than one assistant?**
> [multiplayer-ai](https://github.com/cpuchip/multiplayer-ai) is the dance
> manual for a fleet: room norms, pairing, shared memory, and what agreement
> between assistants is actually worth.

**Governing files:** [GOVERNANCE.md](GOVERNANCE.md) explains the four documents
that govern the relationship — intent, covenant, identity, principles — what
each is for, where a given rule belongs, and why you should expect them to
diverge across machines rather than syncing them.

## Where to put it (read this before you clone)

These kits carry instruction files (`AGENTS.md`, `CLAUDE.md`) and hooks that an AI tool
loads by proximity: whatever folder you run the tool in, and the folders under it, become
its instructions. So **do not clone this repo, or its siblings, into the folder you work
in.** Cloned there, the kit's files take over your project's instructions and its hooks
run against a layout they were not written for; the result is a session that behaves
strangely from the first prompt. That has happened to a friend of ours, and moving the
folders was the whole fix.

Make a workspace folder with no git repository at its root, and clone the kits into an
`external_context/` folder inside it, beside your own projects:

```
workspace/                    <- untracked root: no .git here
  external_context/           <- reference kits, cloned; nothing of yours lives here
    ai-jumpstart/
    working-with-ai/          (optional, the Claude Code plugin)
    multiplayer-ai/           (optional, for more than one machine or assistant)
  my-project/                 <- your code, its own repository
  private-workspace/          <- optional: your memory and instructions, its own PRIVATE repo
```

```
mkdir -p workspace/external_context && cd workspace/external_context
git clone https://github.com/cpuchip/ai-jumpstart.git
git clone https://github.com/cpuchip/working-with-ai.git      # optional
git clone https://github.com/cpuchip/multiplayer-ai.git       # optional
cd ..
```

Run your AI tool from `workspace/` (or from `workspace/my-project/`), never from inside
`external_context/`. [WORKSPACE.md](WORKSPACE.md) explains the layout in full: one root,
walls by location rather than by `.gitignore`, and how to migrate an existing folder into
it. A multi-machine version of the same layout (each box its own facts, each assistant
its own charter) is being written and will land here when it has been lived.

## Quick start

1. With the kit cloned under `workspace/external_context/` as above, open your AI tool in
   `workspace/`.

2. Tell your AI assistant:

   > Read external_context/ai-jumpstart/AGENTS.md and follow it. This is our first
   > session.

3. That's it. The assistant will ask you what you're building, sharpen the vision with
   you, ask for its bounds, and propose the working files (`intent.md`, `covenant.md`,
   `journal/`, `active.md`) from the templates. Every session after that, it reads the
   memory first and closes the loop last — so the next session (or a different AI
   entirely) picks up where you left off instead of arriving as a stranger.

Many tools load instructions automatically if you place them where the tool looks —
`AGENTS.md` in the project root is an emerging convention; Claude Code reads
`CLAUDE.md`; Copilot reads `.github/copilot-instructions.md`. Symlink or copy
AGENTS.md there and the jumpstart becomes the standing way of working.

## What's in the kit

| File | What it is |
|---|---|
| [AGENTS.md](AGENTS.md) | The seed — instructions the assistant follows: first-session setup + the standing disciplines of every session |
| [PRACTICES.md](PRACTICES.md) | The nine practices and a coda, as checklists |
| [CYCLE.md](CYCLE.md) | The eleven-step creation cycle the practices come from |
| [templates/](templates/) | Starting points for `intent.md`, `covenant.md`, journal entries, and `active.md` |
| [DISCIPLINES.md](DISCIPLINES.md) | Optional heavier pack — council moments, cite-or-hedge, reversibility bias, the terms for when your assistant itself delegates, and verifying the deliverable where it lives. In A/B tests it moved smaller models measurably toward larger-model behavior |
| [WORKSPACE.md](WORKSPACE.md) | Optional layout guide for when you outgrow one folder — how to hold a durable memory, a reference corpus, and many code projects in one workspace without tangling their git histories. Walls by location, not `.gitignore` |
| [optional/](optional/) | Optional **Claude Code** automation — drop-in hooks (re-ground, close-the-loop, guard-destructive) + a usage statusline that make the disciplines self-enforcing, plus example skills (foreman, grindability, fan-out, study-it-out, and more) that encode a team's judgment once |

## Where this comes from

These practices were learned in real projects — a game built with a kid at the table,
a 230-million-token runaway, a fabricated quote caught by its own verification gate —
and written down in ***Beyond the Prompt: Discovering the Laws of Organized
Intelligence*** by Michael Stufflebeam ([source](https://github.com/cpuchip/scripture-book)).
The book is the why; this kit is the how, extracted so your AI can start practicing it
in the next five minutes.

Shared freely (MIT). Improvements welcome — especially reports of how different models
follow the seed, and where they drift.
