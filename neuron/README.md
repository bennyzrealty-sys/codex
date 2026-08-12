# neuron — a nervous system for the house

**Plain voice.** Stop calling the Pi a computer; demote it to a *neuron*.
Every device you own — Pi, laptop, the old phone in a drawer — runs the same
tiny daemon: a local memory, a small local mind, and a shared *synapse bus*
they all publish to. A **thought** is a message any neuron may pick up,
enrich, and re-emit. Answers are whatever the traffic converges on. The
intelligence lives in the wiring, not in any box — so the brain grows by
grafting on another £30 neuron, never by replacing anything.

**Technical voice.** MQTT pub/sub (`mosquitto` on the Pi) carrying a small
JSON `Thought` envelope; per-node SQLite memory; pluggable "mind" backends
(rule-based → Ollama → Claude API); Hebbian route-weighting so the mesh
learns which node is good at what; specialised **organs** (long-running
agents) ride the same bus — the first one is the *conductor*, which reads
all your repos nightly and cross-pollinates them.

## Anatomy

```
neuron/
├── nrn/                  the daemon every body runs
│   ├── protocol.py       the Thought envelope (the mesh's only contract)
│   ├── bus.py            MQTT synapse — publish/subscribe thoughts
│   ├── memory.py         SQLite: everything seen, recallable
│   ├── mind.py           pluggable: RuleMind | OllamaMind | ClaudeMind
│   ├── weights.py        Hebbian scores: which neuron proved useful at what
│   ├── daemon.py         the loop: hear → recall → consider → emit
│   └── cli.py            inject a thought by hand, watch replies
├── organs/
│   ├── conductor.py      the repo organism — cross-repo cross-pollination
│   └── sensor.py         example body: Pi temperature/disk → observations
├── systemd/neuron.service
├── neuron.toml.example
└── install.sh            Pi bootstrap (mosquitto + venv + systemd)
```

## Quickstart — two bodies, first synapse

On the **Pi** (this is the broker + first neuron):

```bash
cd neuron && ./install.sh          # mosquitto, venv, systemd service
```

On the **laptop** (second neuron, pointing at the Pi):

```bash
cd neuron
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
cp neuron.toml.example neuron.toml   # set name = "laptop", broker = "<pi-ip>"
.venv/bin/python -m nrn.daemon --config neuron.toml
```

Then from either machine:

```bash
.venv/bin/python -m nrn.cli --config neuron.toml say "ping"
```

…and the *other* body answers `pong from <its name>`. That round-trip is the
whole idea in miniature: a thought left one skull and came back improved.

## Growing the brain

| Stage | Graft | What changes |
|-------|-------|--------------|
| N0 | Two bodies, RuleMind | The wiring works; thoughts travel |
| N1 | `mind = "ollama"` on the Pi | The mesh can genuinely think, offline, free |
| N2 | `organs/sensor.py` on a timer | The mesh has senses; observations flow unprompted |
| N3 | `organs/conductor.py` nightly | Your repos join the organism (see ARCHITECTURE.md) |
| N4 | Weights steering routing | The mesh has learned who is good at what |

## Leaving home

This folder is deliberately self-contained. The day it deserves its own
repository:

```bash
git subtree split --prefix=neuron -b neuron-standalone
# then push that branch to a fresh repo called "neuron"
```

Nothing in here imports from the rest of the Codex.
