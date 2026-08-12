"""Hebbian route-weighting: the mesh learns which neuron is good at what.

When an answer proves useful its asker emits an `ack`; every body hearing
the ack bumps the responder's score for that kind of thought. Scores decay
so old reputations fade. Paths that fire together wire together.
"""
from __future__ import annotations

import sqlite3
import time

SCHEMA = """
CREATE TABLE IF NOT EXISTS route_weights (
    responder TEXT,
    kind      TEXT,
    score     REAL DEFAULT 0,
    updated   REAL,
    PRIMARY KEY (responder, kind)
);
"""

HALF_LIFE_DAYS = 30.0


class Weights:
    def __init__(self, path: str = "memory.db"):
        self.db = sqlite3.connect(path)
        self.db.executescript(SCHEMA)

    def bump(self, responder: str, kind: str, amount: float = 1.0) -> None:
        now = time.time()
        new_score = self.score(responder, kind) + amount  # decayed + fresh credit
        self.db.execute(
            "INSERT OR REPLACE INTO route_weights (responder, kind, score, updated)"
            " VALUES (?,?,?,?)",
            (responder, kind, new_score, now),
        )
        self.db.commit()

    def score(self, responder: str, kind: str) -> float:
        row = self.db.execute(
            "SELECT score, updated FROM route_weights WHERE responder=? AND kind=?",
            (responder, kind),
        ).fetchone()
        if not row:
            return 0.0
        score, updated = row
        elapsed_halves = (time.time() - updated) / (HALF_LIFE_DAYS * 86400)
        return score * (0.5 ** elapsed_halves)

    def best(self, kind: str) -> tuple[str, float] | None:
        rows = self.db.execute(
            "SELECT responder, score, updated FROM route_weights WHERE kind=?",
            (kind,),
        ).fetchall()
        if not rows:
            return None
        ranked = sorted(
            ((r, s * 0.5 ** ((time.time() - u) / (HALF_LIFE_DAYS * 86400)))
             for r, s, u in rows),
            key=lambda x: -x[1],
        )
        return ranked[0]
