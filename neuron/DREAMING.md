# The house that dreams — architecture

**Plain voice.** Real brains don't learn while awake — waking life just
records. The learning happens at night: the day is replayed, the important
parts are moved into long-term memory, the noise is thrown away, and the
odd bits get turned over until they make sense. Give the node the same
trick. At 2 a.m., while the house sleeps, the Pi reads everything it heard
since sunrise, thinks about it slowly (slow is free at night), keeps what
matters, forgets what doesn't, and leaves a five-line note for breakfast.

**Technical voice.** A cron-driven organ (`organs/dreamer.py`) over the
neuron mesh's per-body SQLite: batch-read the last day of `thoughts`, run
staged offline inference (deterministic triage → model replay →
consolidation), write distilled facts to the `memories` table, prune stale
`thoughts` rows, and emit a morning brief as an ordinary `observation` on
the bus (plus Telegram, if configured). No new infrastructure: the dreamer
is just another body that happens to wake at night.

## Why it belongs on the mesh

The mesh already solves the hard parts. Every observation, question, and
answer of the day is already sitting in `memory.db` — the dreamer needs no
collectors. Distilled memories written via `memories` are already what
`recall()` serves to every waking mind — so **a dream tonight changes what
the mesh knows tomorrow**, with zero plumbing. And the brief is just a
thought: anything subscribed — your phone, another body, a future organ —
hears it the ordinary way.

## The four phases of a night

```
02:00 cron ──► 1 TRIAGE        deterministic, always works, no model needed
               2 REPLAY        the mind reads the day in chunks, slowly
               3 CONSOLIDATE   facts → memories table; stale thoughts pruned
               4 BRIEF         five lines, emitted on the bus + telegram
```

**1 · Triage (deterministic).** Counts by kind and origin; the day's
extremes (hottest CPU reading, lowest disk); who spoke and — as important —
who went silent. A body that said nothing all day is the anomaly a model
might not think to mention. Triage output is always produced, model or no
model: the dreamer degrades gracefully to a pocket notebook.

**2 · Replay (the mind).** The day's thoughts, in order, chunked to fit a
small model's context, each chunk prompted the same way: *what was
anomalous, what repeated, what almost happened, what deserves to be
remembered forever?* This is where "slow is fine" pays: a 3–4B model on
the Pi grinding for forty minutes costs nothing and nobody is waiting.
The dreamer uses the same pluggable minds as the daemon (`nrn/mind.py`) —
`ollama` is the natural night mind; `claude` is for nights you decide are
worth money; `rule` means phases 2 is skipped honestly.

**3 · Consolidate & forget.** Facts the replay judged durable are written
with `Memory.remember()` — keyed, timestamped, embedded when a model is
available. Then the forgetting, which is not a compromise but the point:
`thoughts` rows older than `retention_days` (default 30) are deleted.
Memories persist; raw traffic evaporates. A mesh that keeps everything
recalls nothing — relevance needs a quiet graveyard.

**4 · The brief.** Five lines, no more: the shape of the day, the anomaly,
the pattern, the suggestion, the thing consolidated. Written to
`morning-brief.md`, emitted as an `observation` thought (origin
`<name>-dreamer`), and pushed to Telegram when `TELEGRAM_BOT_TOKEN` /
`TELEGRAM_CHAT_ID` are set in the service environment. If the night was
truly empty the brief says so in one line — correct silence, like the
conductor's.

## Wiring

```toml
# neuron.toml
[dreamer]
mind = "ollama"                  # rule | ollama | claude
retention_days = 30
brief_path = "morning-brief.md"
# [dreamer.mind_options]
# model = "llama3.2:3b"
```

```cron
0 2 * * *  cd ~/codex/neuron && .venv/bin/python organs/dreamer.py --config neuron.toml
```

## Growth path

| Stage | Graft | What changes |
|-------|-------|--------------|
| D0 | cron + triage only (`mind = "rule"`) | A nightly pocket-notebook brief |
| D1 | `mind = "ollama"` | Real replay: anomalies and patterns, free |
| D2 | Embeddings in `Memory.embed()` | Dreams cluster by meaning, not keyword |
| D3 | Counterfactuals in the replay prompt | "What almost happened" gets teeth |
| D4 | Dream-to-dream memory | Tonight's dream reads last week's dreams; themes emerge |

The far end of this road is the Codex's Layer-08 caretaker and the
dreamer meeting in the middle: a house whose page, memory, and morning
voice are all written by what it lived through the day before.
