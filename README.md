# The Operator's Codex — publish kit

One folder = one living site: the guide (`index.html`), the node log
(`node-log.json`), the caretaker (`.github/workflows/refresh.yml` +
`scripts/update_codex.py`), and the Pi reporter (`pi/log-progress.sh`).

## Publish (one Claude Code session, from your phone)

Open Claude Code, give it this folder, and say:

> Create a public repo called `codex` on my GitHub, push these files to main,
> enable GitHub Pages (deploy from branch: main, root), and add a repository
> secret named ANTHROPIC_API_KEY — I'll paste the key when you ask.

Your link: **https://bennyzrealty-sys.github.io/codex/**
(Prefer your own domain? Import the repo into Vercel instead and point
`codex.homeberry.ai` at it — same files, zero changes.)

## Put it on your phone (online-only, as requested)

Open the link in Chrome → ⋮ menu → **Add to Home screen**. You get an app
icon; every open loads the live, freshly-updated page. No offline copy is
kept — if there's no signal, it simply waits, like any live thing.

## Prove the caretaker works

Repo → **Actions** → `refresh-codex` → **Run workflow**. Watch it search,
rewrite Layer 04, append the changelog, and redeploy. After that it wakes
itself every 2 days at 06:00 UTC.

## Teach the Pi to report (from day L0)

On the Pi, once Git and gh are set up (Layer 07, rung L0):

    gh repo clone bennyzrealty-sys/codex && cd codex
    ./pi/log-progress.sh L0 done "node booted, Tailscale up, SSD root"
    ./pi/log-progress.sh L1 current "migrating shift watcher"

Each line pushes a commit; the Node Log panel on your phone updates within
about a minute. The node literally writes its own diary.

## Safety notes

- The caretaker edits **only** Layer 04 and the changelog; any error means
  "change nothing" — the site can't be broken by a bad run.
- The API key lives in GitHub Secrets, never in the repo.
- `git log` of `node-log.json` is a permanent, dated history of the build.
