# Architecture — intelligence as traffic

## 1. The one contract: the Thought

Everything on the mesh is a `Thought` (see `nrn/protocol.py`): a small JSON
envelope with an id, an origin, a kind, free-text content, a hop trail, and a
TTL. Kinds:

- `observation` — something a body sensed ("cpu 71°C", "repo X test failed")
- `question`    — a request for the mesh ("what changed in the repos today?")
- `answer`      — a reply, always referencing the question's id (`re`)
- `proposal`    — an actionable suggestion (the conductor's currency)
- `ack`         — "that answer was useful"; the raw material of learning

The envelope is the *only* coupling between bodies. Any language, any device,
any decade can join the mesh by speaking it. Resist adding fields.

## 2. The synapse bus

`mosquitto` on the Pi; topics:

- `neuron/thoughts` — every thought, broadcast; each daemon filters locally
- `neuron/presence/<name>` — retained heartbeats, so bodies know each other

Broadcast-then-filter is deliberate: at household scale the traffic is tiny,
and it means no central router decides who *may* think about what. Curiosity
is free.

Security posture: the broker binds to the LAN / Tailscale interface only.
Nothing secret rides the bus — thoughts are observations and text, never
credentials. A body that needs a secret reads it from its own environment.

## 3. Minds

`nrn/mind.py` defines one method: `consider(thought, recalled) -> str | None`.
Returning `None` means "I have nothing to add" — the most common and most
correct output. Backends:

- **RuleMind** — regex/table lookups. Zero cost, always on. Handles `ping`,
  presence questions, and anything you teach it. Never underestimate it:
  most reflexes in real nervous systems are exactly this.
- **OllamaMind** — a small local model (3–4B) via `localhost:11434`. Free,
  private, slow-is-fine. The Pi's night brain.
- **ClaudeMind** — the API, for thoughts explicitly tagged worth money.
  A frugality gate in the daemon decides; the default answer is no.

The point of the plug: *the mesh does not care where thinking happens.* A
body upgrades its mind and nobody else changes a line.

## 4. Memory

Per-body SQLite (`memory.db`): every thought seen, plus a `memories` table
for distilled facts. Recall is keyword-first (LIKE), with an embedding hook
left open (`memory.embed()`) for when a body has a model to embed with —
the schema stores vectors as blobs from day one, so upgrading recall never
means migrating data.

Memory is deliberately **per-body**, not shared. Bodies remember what passed
through *them*; the mesh's shared memory is the traffic itself plus whatever
the dream cycle (Codex Layer 07, "the house that dreams") chooses to
consolidate. This mirrors the biology and avoids a single corruptible store.

## 5. Learning: Hebbian weights

`nrn/weights.py` keeps a table `(responder, kind) -> score`. When a body's
question gets an answer it uses, it emits an `ack`; every body hearing the
ack bumps the responder's score for that kind. Scores decay slowly.

What this buys, cheaply: **the mesh learns which neuron is good at what**
without anyone designing a routing table. Later (N4) the daemon can consult
weights before spending mind-cycles: "the laptop always answers code
questions better — stay quiet unless it's silent." Paths that fire together
wire together; that's the whole trick.

## 6. Organs — specialised bodies

An organ is just a process that speaks Thought but has a job beyond
reflexes. It needs no special permission — the mesh can't tell an organ
from a neuron, which is exactly right.

### The conductor (the repo organism)

`organs/conductor.py`, run nightly by cron on the Pi. Your repositories are
organs in jars; the conductor is the bloodstream between them.

1. **Collect** — for each repo in its config: recent commits, open issues,
   TODO/FIXME markers, failing workflow runs (via `gh`).
2. **Think** — one prompt over the *whole* organism: what does repo A have
   that repo B needs? what bug pattern in A should become a test in B? what
   idea parked in A's notes can B now build?
3. **Emit** — findings become `proposal` thoughts on the bus (so the mesh —
   and you, via any subscribed body — see them), and, with `--open-prs`,
   draft pull requests labelled `cross-pollination`.

Etiquette is enforced in code: proposals are drafts, never merges; one PR
per idea; silence when there is nothing to say. `--dry-run` is the default.

### The dreamer (the house that dreams)

`organs/dreamer.py`, cron at 02:00 — the mesh's sleep cycle. It replays the
day's thoughts from this body's memory, consolidates the durable parts into
the `memories` table (which `recall()` serves to every waking mind — so a
dream tonight changes what the mesh knows tomorrow), prunes stale raw
traffic, and emits a five-line morning brief on the bus. Full architecture
in `DREAMING.md`. This is also who writes `Memory.remember()` in anger —
the consolidation path §4 promised.

### The sensor

`organs/sensor.py` — the trivial organ that proves the pattern: reads Pi
temperature and disk headroom, emits `observation` thoughts. Ten lines of
job, same envelope. Every future sense (mic, camera, SDR, mmWave — Codex
Layer 07 G3) enters the mesh exactly this way.

## 7. What is deliberately absent

- **No orchestrator.** Nothing assigns work. Convergence comes from traffic.
- **No shared database.** The bus is the only common surface.
- **No auth between bodies (yet).** The trust boundary is the LAN/Tailnet.
  When a body leaves the house, that's the day to add per-body keys —
  signed thoughts slot into the envelope's `sig` field without breaking anyone.
- **No cleverness in the protocol.** The envelope stays dumb so the minds
  can get smart.
