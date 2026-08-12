"""The house that dreams — nightly replay, consolidation, and a morning brief.

Real brains learn offline: the day is replayed, the durable parts move to
long-term memory, the noise evaporates. This organ gives the node the same
trick. Run from cron at 02:00 (see DREAMING.md):

  python organs/dreamer.py --config neuron.toml

Phases: TRIAGE (deterministic, always works) -> REPLAY (the mind, chunked)
-> CONSOLIDATE & FORGET -> BRIEF (file + bus + optional Telegram).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import tomllib
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from nrn.bus import Bus                     # noqa: E402
from nrn.memory import Memory               # noqa: E402
from nrn.mind import build as build_mind    # noqa: E402
from nrn.protocol import Thought            # noqa: E402

DAY = 86400

REPLAY_PROMPT = (
    "You are the night mind of a small household mesh, replaying part of "
    "one day's traffic. Below are thoughts in order (kind | origin | text).\n"
    "\n{chunk}\n\n"
    "Report ONLY things worth keeping, one per line:\n"
    "  ANOMALY: <something off, once>\n"
    "  PATTERN: <something that repeated meaningfully>\n"
    "  REMEMBER: <a durable fact the mesh should know from now on>\n"
    "  SUGGEST: <one concrete action for the operator>\n"
    "If this chunk holds nothing worth keeping, reply exactly PASS."
)


def gather(memory: Memory, since: float) -> list[tuple]:
    """The day's traffic, oldest first: (ts, origin, kind, content)."""
    return memory.db.execute(
        "SELECT ts, origin, kind, content FROM thoughts"
        " WHERE ts >= ? ORDER BY ts", (since,),
    ).fetchall()


def triage(rows: list[tuple], known_bodies: set[str]) -> list[str]:
    """Deterministic notebook: shape of the day, extremes, silences."""
    if not rows:
        return ["a silent day: no thoughts crossed the mesh"]
    kinds = Counter(r[2] for r in rows)
    talkers = Counter(r[1] for r in rows)
    lines = [
        f"{len(rows)} thoughts from {len(talkers)} bodies "
        f"({', '.join(f'{k}:{n}' for k, n in kinds.most_common())})",
        f"busiest body: {talkers.most_common(1)[0][0]} "
        f"({talkers.most_common(1)[0][1]} thoughts)",
    ]
    silent = known_bodies - set(talkers)
    if silent:
        lines.append(f"silent all day (worth a look): {', '.join(sorted(silent))}")
    return lines


def replay(rows: list[tuple], mind, chunk_size: int = 60) -> list[str]:
    """The mind reads the day in chunks; slow is free at night."""
    findings: list[str] = []
    for i in range(0, len(rows), chunk_size):
        chunk = "\n".join(f"{k} | {o} | {c}" for _, o, k, c in
                          rows[i:i + chunk_size])
        prompt = REPLAY_PROMPT.format(chunk=chunk)
        answer = mind.consider(
            Thought(content=prompt, kind="question", origin="dreamer"), [])
        if answer:
            findings += [ln.strip() for ln in answer.splitlines()
                         if ln.strip() and ln.strip() != "PASS"]
    return findings


def consolidate(findings: list[str], memory: Memory, retention_days: int,
                now: float) -> int:
    """Durable facts into long-term memory; stale raw traffic forgotten."""
    kept = 0
    for line in findings:
        if line.upper().startswith("REMEMBER:"):
            fact = line.split(":", 1)[1].strip()
            memory.remember(f"dream-{int(now)}-{kept}", fact)
            kept += 1
    memory.db.execute(
        "DELETE FROM thoughts WHERE ts < ?", (now - retention_days * DAY,))
    memory.db.commit()
    return kept


def compose_brief(triage_lines: list[str], findings: list[str],
                  kept: int) -> str:
    """Five lines, no more. An empty night earns one honest line."""
    picks = [ln for ln in findings
             if ln.split(":")[0].upper() in ("ANOMALY", "PATTERN", "SUGGEST")]
    lines = triage_lines[:2] + picks[:2]
    if kept:
        lines.append(f"consolidated {kept} new memor{'y' if kept == 1 else 'ies'}")
    return "\n".join(f"- {ln}" for ln in lines[:5])


def deliver(brief: str, cfg: dict, dcfg: dict) -> None:
    Path(dcfg.get("brief_path", "morning-brief.md")).write_text(
        f"# Morning brief — {time.strftime('%d %b %Y')}\n\n{brief}\n")
    bus = Bus(cfg["name"] + "-dreamer", cfg.get("broker", "localhost"),
              cfg.get("port", 1883))
    bus.run_background()
    time.sleep(0.5)
    bus.emit(Thought(kind="observation", origin=bus.name,
                     content=f"morning brief:\n{brief}"))
    time.sleep(0.5)

    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat = os.environ.get("TELEGRAM_CHAT_ID")
    if token and chat:
        data = urllib.parse.urlencode(
            {"chat_id": chat, "text": f"🌙 morning brief\n{brief}"}).encode()
        urllib.request.urlopen(
            f"https://api.telegram.org/bot{token}/sendMessage", data,
            timeout=30)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="neuron.toml")
    ap.add_argument("--since-hours", type=float, default=24.0)
    args = ap.parse_args()
    with open(args.config, "rb") as f:
        cfg = tomllib.load(f)
    dcfg = cfg.get("dreamer", {})
    now = time.time()

    memory = Memory(cfg.get("memory", "memory.db"))
    rows = gather(memory, now - args.since_hours * 3600)
    known = {r[0] for r in memory.db.execute(
        "SELECT DISTINCT origin FROM thoughts").fetchall()}

    triage_lines = triage(rows, known)

    mind = build_mind(dcfg.get("mind", "rule"), cfg["name"] + "-dreamer",
                      **dcfg.get("mind_options", {}))
    findings = replay(rows, mind) if rows else []

    kept = consolidate(findings, memory, dcfg.get("retention_days", 30), now)
    brief = compose_brief(triage_lines, findings, kept)
    deliver(brief, cfg, dcfg)
    print(brief)


if __name__ == "__main__":
    main()
