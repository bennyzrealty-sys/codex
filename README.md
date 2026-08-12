# The Operator's Codex — publish kit

One folder = one living site: the guide (`index.html`), the live feed
(`updates.json`), the interactive layer (`assets/`), the offline copy
(`sw.js` + `manifest.json`), the node log (`node-log.json`), the caretaker
(`.github/workflows/refresh.yml` + `scripts/update_codex.py`), and the Pi
reporter (`pi/log-progress.sh`).

Your link: **https://bennyzrealty-sys.github.io/codex/**
(Prefer your own domain? Import the repo into Vercel instead and point
`codex.homeberry.ai` at it — same files, zero changes.)

## What the page does

- **26 layers**, every idea in two voices — plain, then technical.
- **The suggested path** — the layer numbers are the order they were *written*;
  the path panel in the header is the order to *read* them, in six stages. It
  ticks each stop once you have genuinely spent time in it (kept on-device only,
  with a reset button).
- **The Latest** — a live feed across IT, AI, hardware, cyber security and
  **markets**, swept **every 2 days**, each item in both voices with an
  illustration, where it lands on your setup, and the tools to reach for.
  The three newest items are lifted into the header, and every feed card
  closes with a link into the layer that teaches the ground it stands on —
  the news is the hook, the curriculum is the thing.
- **The Atlas** — the page opens as a full-height hero, then the 26 layers
  as a bento grid of stage-tinted tiles: diagram thumbnails, live card
  counts, and read-state ticks fed by the same on-device progress the path
  uses. At desk widths cards flow two abreast inside every layer, an opened
  card spreads its two voices side by side, and a fixed minimap of every
  layer rides the left edge.
- **Double-click any word** and a door opens *at the word*: an iris wipe, a
  starfield tinted by the term's world (minds / wires / silicon / shields /
  craft / the wider world), then a room with both voices, an illustration,
  an authored "why it matters" line, the way back into the layers — and
  neighboring doors, so you can walk from term to term. The metadata lives
  in `assets/doors.json` (world, why, kin, art per term; hand-edited, never
  touched by the caretaker).
- **Tap any diagram** for true full screen — pinch, pan, swipe, or `f` for
  the browser's own fullscreen.
- **Newly updated** marks on any card the caretaker touched, which stay
  until you have opened that card three times.
- **The glossary is the door's showroom** — every term is clickable, with a
  sift-as-you-type filter and an A–Z jump row.
- Press `/` (or `⌘K`) to jump anywhere by name.

All motion is disabled automatically under `prefers-reduced-motion`.

Structural invariants the caretaker depends on are enforced by
`scripts/check_structure.py` — run it after any hand edit to `index.html`.

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

Open the link in Chrome → ⋮ → **Install app**. You get an app icon, a
standalone window with no address bar, and — because `sw.js` caches the
shell, the typefaces and every diagram — **the whole Codex readable with no
signal**. The feed is fetched network-first, so it is current whenever there
is signal and legible when there is not.

Nothing about you leaves the device; `privacy.html` says so in full, and the
typefaces are served from `assets/fonts/` rather than Google's CDN precisely
so that stays true.

### Adding a fifth thing to the feed

The feed's domains live in exactly one place — `DOMAINS` in
`scripts/update_codex.py`. Adding one means four small edits, and
`check_structure.py` fails if you forget any of them:

1. add it to `DOMAINS` and to the search brief in `build_prompt`;
2. add a `<button data-dom="…">` chip in `#live` (the renderer counts chips
   from the DOM, so no JS change is needed);
3. add `images/update-<domain>.svg` — `valid_entry` falls back to it, so
   without the file the first entry renders a broken image
   (`make_figures.py` draws it: one line in `FIGURES`);
4. add the domain tint (`.dom.<domain>`) in `assets/codex.css`, and the
   layer it funnels into (`TAUGHT_IN`) in `assets/codex.js`.

### Getting it into the Play Store

The blocker is not the app, it is the URL. A Trusted Web Activity verifies
against `https://<origin>/.well-known/assetlinks.json` at the **origin root**,
and `bennyzrealty-sys.github.io/codex/` is a project path — the root belongs
to a different repository. Either move to a custom domain (recommended) or
serve the asset links from a `bennyzrealty-sys.github.io` repo. The file and
the full explanation are in `.well-known/`; `.nojekyll` is what makes GitHub
Pages serve that directory at all.

Once the domain is settled:

    npx @bubblewrap/cli init --manifest https://<origin>/manifest.json
    npx @bubblewrap/cli build

Bubblewrap prints the SHA-256 signing fingerprint that goes into
`assetlinks.json`. A Play developer account is $25 once, and personal
accounts carry a closed-testing requirement (roughly 12 testers for 14
continuous days) before production — start that clock early, it is calendar
time, not work.

## Maintenance tools

    python scripts/tag_cards.py      # give new cards stable ids (idempotent)
    python scripts/size_figures.py   # stamp every figure with its intrinsic size
    python scripts/make_figures.py   # redraw every generated field diagram

`tag_cards.py` and `size_figures.py` both run in CI after each sweep — Layer 04
is rewritten without ids, and any new feed image needs its dimensions recorded.
Ids are never reassigned, so the read-counters in your browser survive every
refresh.

`size_figures.py` is not cosmetic: without width/height the browser reserves no
space for a lazy image, the page reflows as it loads, and a jump to a deep
anchor lands you in the wrong layer.

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
