# The Operator's Codex — publish kit

One folder = one living site: the guide (`index.html`), the live feed
(`updates.json`), the interactive layer (`assets/`), the node log
(`node-log.json`), the caretaker (`.github/workflows/refresh.yml` +
`scripts/update_codex.py`), and the Pi reporter (`pi/log-progress.sh`).

Your link: **https://bennyzrealty-sys.github.io/codex/**
(Prefer your own domain? Import the repo into Vercel instead and point
`codex.homeberry.ai` at it — same files, zero changes.)

## What the page does

- **23 layers**, every idea in two voices — plain, then technical.
- **The Latest** — a live feed across IT, AI, hardware and cyber security,
  swept **every 2 days**, each item in both voices with an illustration,
  where it lands on your setup, and the tools to reach for.
- **Double-click any word** and a door opens on it: both voices, an
  illustration, and the way back into the layer it came from.
- **Tap any diagram** for true full screen — pinch, pan, swipe, or `f` for
  the browser's own fullscreen.
- **Newly updated** marks on any card the caretaker touched, which stay
  until you have opened that card three times.
- Press `/` (or `⌘K`) to jump anywhere by name.

All motion is disabled automatically under `prefers-reduced-motion`.

## The 2-day cycle

`refresh.yml` fires on `0 6 */2 * *` — **06:00 UTC, every second day** — plus a
manual **Run workflow** button. One sweep does exactly three things:

1. **appends** new entries to the top of `updates.json`;
2. **rewrites** Layer 04 (the Frontier) between its markers;
3. **edits and marks** any existing card a finding genuinely changes, by
   setting `data-updated` / `data-updnote` on its stable `data-card` id.

The vault rule: entries already in `updates.json` are **never edited or
deleted**. A claim that aged badly is more instructive than a tidy page.

The caretaker fails safe at every step — a bad model response, an unknown card
id, a missing image or a failed structural check all mean "write nothing", so a
broken run can only ever be a no-op.

Set `CODEX_MODEL` in the workflow env to change which model does the sweep.

### Prove it works

Repo → **Actions** → `refresh-codex` → **Run workflow**. Watch it search, write
feed entries, rewrite Layer 04, mark any affected cards, and redeploy.

## Put it on your phone

Open the link in Chrome → ⋮ → **Add to Home screen**. You get an app icon;
every open loads the live, freshly-swept page.

## Maintenance tools

    python scripts/tag_cards.py      # give new cards stable ids (idempotent)
    python scripts/make_figures.py   # redraw every generated field diagram

`tag_cards.py` runs in CI after each sweep, because Layer 04 is rewritten
without ids. Ids are never reassigned, so the read-counters in your browser
survive every refresh.

## Teach the Pi to report (from day L0)

On the Pi, once Git and gh are set up (Layer 07, rung L0):

    gh repo clone bennyzrealty-sys/codex && cd codex
    ./pi/log-progress.sh L0 done "node booted, Tailscale up, SSD root"
    ./pi/log-progress.sh L1 current "migrating shift watcher"

Each line pushes a commit; the Node Log panel updates within about a minute.

## Safety notes

- The caretaker may only append to the feed, replace Layer 04, append to the
  changelog, and stamp cards. It cannot delete a layer or a feed entry.
- The API key lives in GitHub Secrets, never in the repo.
- `git log` of `node-log.json` and `updates.json` is a permanent, dated
  history of both the build and the field.
