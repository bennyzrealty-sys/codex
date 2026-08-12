"""The neuron loop: hear → recall → consider → emit.

Run one of these on every body:  python -m nrn.daemon --config neuron.toml
"""
from __future__ import annotations

import argparse
import logging
import tomllib

from .bus import Bus
from .memory import Memory
from .mind import build as build_mind
from .protocol import Thought
from .weights import Weights

log = logging.getLogger("nrn")


class Neuron:
    def __init__(self, cfg: dict):
        self.name = cfg["name"]
        self.memory = Memory(cfg.get("memory", "memory.db"))
        self.weights = Weights(cfg.get("memory", "memory.db"))
        self.mind = build_mind(cfg.get("mind", "rule"), self.name,
                               **cfg.get("mind_options", {}))
        self.bus = Bus(self.name, cfg.get("broker", "localhost"),
                       cfg.get("port", 1883))
        self.bus.on_thought(self.hear)

    def hear(self, t: Thought) -> None:
        if self.memory.seen(t.id):
            return                      # the mesh echoes; a neuron doesn't
        self.memory.store(t)

        if t.kind == "ack":             # learning: credit the acked responder
            answered = self.memory.db.execute(
                "SELECT origin, kind FROM thoughts WHERE id=?", (t.re,)
            ).fetchone()
            if answered:
                self.weights.bump(answered[0], answered[1])
                log.info("weight++ %s (%s)", answered[0], answered[1])
            return

        if t.ttl <= 0 or self.name in t.hops:
            return                      # exhausted, or we already touched it

        recalled = self.memory.recall(t.content)
        response = self.mind.consider(t, recalled)
        if response:
            reply = t.reply(response, origin=self.name)
            self.memory.store(reply)
            self.bus.emit(reply)
            log.info("%s -> %s: %s", t.origin, self.name, response[:80])

    def run(self) -> None:
        log.info("neuron %r awake, mind=%s", self.name,
                 type(self.mind).__name__)
        self.bus.run_forever()


def main() -> None:
    ap = argparse.ArgumentParser(description="run one neuron")
    ap.add_argument("--config", default="neuron.toml")
    args = ap.parse_args()
    with open(args.config, "rb") as f:
        cfg = tomllib.load(f)
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(name)s %(message)s")
    Neuron(cfg).run()


if __name__ == "__main__":
    main()
