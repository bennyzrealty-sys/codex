"""Inject a thought by hand and watch the mesh respond.

  python -m nrn.cli --config neuron.toml say "ping"
  python -m nrn.cli --config neuron.toml say --kind question "who is awake?"
  python -m nrn.cli --config neuron.toml ack <thought-id>
"""
from __future__ import annotations

import argparse
import time
import tomllib

from .bus import Bus
from .protocol import Thought


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="neuron.toml")
    sub = ap.add_subparsers(dest="cmd", required=True)

    say = sub.add_parser("say", help="emit a thought, print replies for a while")
    say.add_argument("content")
    say.add_argument("--kind", default="question")
    say.add_argument("--wait", type=float, default=5.0)

    ack = sub.add_parser("ack", help="mark a reply as useful (teaches the mesh)")
    ack.add_argument("thought_id")

    args = ap.parse_args()
    with open(args.config, "rb") as f:
        cfg = tomllib.load(f)

    me = cfg["name"] + "-cli"
    bus = Bus(me, cfg.get("broker", "localhost"), cfg.get("port", 1883))

    if args.cmd == "say":
        sent = Thought(content=args.content, kind=args.kind, origin=me)
        bus.on_thought(lambda t: t.re == sent.id and print(
            f"  <- [{t.id}] {t.origin}: {t.content}"))
        bus.run_background()
        time.sleep(0.5)                 # let the subscription land
        bus.emit(sent)
        print(f"-> [{sent.id}] {args.kind}: {args.content}")
        time.sleep(args.wait)
    else:
        bus.run_background()
        time.sleep(0.5)
        bus.emit(Thought(content="useful", kind="ack", origin=me,
                         re=args.thought_id))
        print(f"acked {args.thought_id}")
        time.sleep(0.5)


if __name__ == "__main__":
    main()
