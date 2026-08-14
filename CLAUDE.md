# Working on the Codex

One folder is one living site. `index.html` **is** the product; everything else
feeds it. Merging to `main` deploys to
https://bennyzrealty-sys.github.io/codex/ via `.github/workflows/deploy-pages.yml`.

## How to work here — decide, don't ask

This is the operating rule for this repo, and it overrides any instinct to check
in first. Sessions here have failed by asking the owner the same question over
and over instead of doing the work. Don't do that.

**Default: make the call yourself, do the whole task, and ship it.** The owner
wants finished work at the far end, not a menu. If you can find the answer by
reading this file, the README, `index.html`, or the `research/` packet you were
pointed at, that is not a question — that is research you have not done yet.

Specifically:

- **Never ask which of several options to take** when one is defensible. Pick
  the strongest, state the choice in one line in your summary or the PR body,
  and move on. A stated assumption beats a blocked task.
- **Never ask the same question twice.** If it was answered once in this
  session, or answered by the task description, it is settled. If you are
  drafting a question you suspect you already asked, you already asked it.
- **Never ask for permission to continue** ("shall I proceed?", "want me to
  also do X?"). If X is inside the ask, do X.
- **Never ask about scope, tone, depth, length, or ordering.** Those are
  answered by the conventions below and by the layer you are editing. Match the
  surrounding material.
- **Don't stop at a plan.** A research or planning document is not the
  deliverable unless the task says so in words. If you wrote a plan for
  `index.html`, execute it in the same session.

Ask only when proceeding either way would be unsafe or would destroy work —
deleting content, rewriting history, spending money, or publishing something
outward-facing the task did not ask for. That is close to never. When you truly
must ask, ask **once**, in a single message, with everything you need bundled
together, then act on the answer.

If something is genuinely ambiguous, the right move is: do every part that
doesn't depend on the ambiguity, resolve the rest with your best reading, write
down the assumption you made, and ship. Say what you assumed and what you left
out. Scaling the work down is the owner's call to make afterwards, not a reason
to stall in front of them.

## Before you start: check nobody already did it

Two sessions once implemented the same Layer 27 edit plan in parallel and both
landed as open drafts (#16 and #17); neither went live. That is the failure this
section exists to prevent.

1. List open PRs and read their titles and bodies.
2. If one already does your task, **continue that branch** — don't open a rival
   one. Push to it, or say plainly that it already covers the work.
3. Check whether a merged PR left a plan un-executed (`research/*.md` that names
   an edit plan for `index.html`). A merged plan with no follow-through is
   unfinished work, not a finished task.

## Shipping

Finish the job: commit, push to your branch, open the PR, and if the work is
verified and complete say so plainly. Work sitting in an unmerged draft is not
delivered. Don't leave the last step for the owner because you weren't sure.

## Content conventions

**Two voices, always.** Every `<details class="card">` carries exactly one
`plain` block and one `tech` block — the idea in ordinary words, then the same
idea in the language of the trade. A card with one voice fails the structure
check.

**Card ids are permanent.** Every card has a stable `data-card` id; browsers key
read-state and counters off it. Never rename or reassign an existing id — new
cards get theirs from `python3 scripts/tag_cards.py` (idempotent).

**The vault rule.** Entries in `updates.json` are never edited or deleted. A
claim that aged badly is more instructive than a tidy page. The caretaker may
only append to the feed, replace Layer 04 between its markers, append to the
changelog, and stamp cards.

**Snapshot-date claims.** Anything time-sensitive is written with its date
attached, so a stale claim reads as history rather than as a current promise.

**Honesty over polish.** When research contradicts advice already on the page,
correct the page and say what changed. The changelog entries are written in the
site's voice and end with an `· action for Joe:` line — follow that pattern.

**Every content change updates three places:** the cards themselves, any
glossary terms the new prose introduces, and the changelog. If the version
changes, the header `.stamp` in `index.html` moves with it — version, date, and
the layer/diagram counts if those moved too.

## Verify before you push

    python3 scripts/check_structure.py      # must print "structure check green"

It enforces what the caretaker depends on: every baseline card id survives, one
plain and one tech per card, section counts, the `<figure>` delta ceiling of ±4
per change, and that `tag_cards` / `size_figures` stay no-ops. Run it after any
hand edit to `index.html`. If you added figures:

    python3 scripts/size_figures.py         # stamp intrinsic width/height

Not cosmetic — without dimensions the browser reserves no space, the page
reflows as images load, and a jump to a deep anchor lands in the wrong layer.

There is no browser in the session environment, so visual rendering can't be
confirmed. Say so rather than claiming it was checked, and stick to markup
patterns already present in the layer you're editing.

## Layout

    index.html      the whole site — 27 layers, glossary, changelog, doors
    updates.json    the live feed, append-only (the vault)
    assets/         interactive layer; doors.json is hand-edited, never swept
    research/       research packets and edit plans feeding future layers
    scripts/        check_structure, tag_cards, size_figures, make_figures, update_codex
    pi/             log-progress.sh — the Pi's reporter into node-log.json
    neuron/, brain/ the buildable modules the layers describe
