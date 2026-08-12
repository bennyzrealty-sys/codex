"""The trivial organ that proves the pattern: Pi vitals -> observations.

Run from cron every 10 minutes. Every future sense (mic, camera, SDR,
mmWave — Codex Layer 07 G3) enters the mesh exactly this way: read a
device, wrap a Thought, emit, exit.
"""
from __future__ import annotations

import argparse
import shutil
import sys
import time
import tomllib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from nrn.bus import Bus                     # noqa: E402
from nrn.protocol import Thought            # noqa: E402

TEMP = Path("/sys/class/thermal/thermal_zone0/temp")


def readings() -> list[str]:
    out = []
    if TEMP.exists():
        out.append(f"cpu temperature {int(TEMP.read_text()) / 1000:.1f}C")
    total, used, free = shutil.disk_usage("/")
    out.append(f"disk free {free / 1e9:.1f}GB of {total / 1e9:.1f}GB")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="neuron.toml")
    args = ap.parse_args()
    with open(args.config, "rb") as f:
        cfg = tomllib.load(f)

    bus = Bus(cfg["name"] + "-sensor", cfg.get("broker", "localhost"),
              cfg.get("port", 1883))
    bus.run_background()
    time.sleep(0.5)
    for line in readings():
        bus.emit(Thought(kind="observation", origin=bus.name, content=line))
        print(line)
    time.sleep(0.5)


if __name__ == "__main__":
    main()
