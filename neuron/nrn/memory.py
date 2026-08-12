"""Per-body memory: every thought seen, recallable.

Keyword recall today; the schema stores an embedding blob from day one so
upgrading to vector recall never means migrating data.
"""
from __future__ import annotations

import sqlite3
import time

from .protocol import Thought

SCHEMA = """
CREATE TABLE IF NOT EXISTS thoughts (
    id      TEXT PRIMARY KEY,
    ts      REAL,
    origin  TEXT,
    kind    TEXT,
    re      TEXT,
    content TEXT,
    vec     BLOB
);
CREATE TABLE IF NOT EXISTS memories (
    key     TEXT PRIMARY KEY,
    ts      REAL,
    content TEXT,
    vec     BLOB
);
"""


class Memory:
    def __init__(self, path: str = "memory.db"):
        self.db = sqlite3.connect(path)
        self.db.executescript(SCHEMA)

    def seen(self, thought_id: str) -> bool:
        row = self.db.execute(
            "SELECT 1 FROM thoughts WHERE id = ?", (thought_id,)
        ).fetchone()
        return row is not None

    def store(self, t: Thought) -> None:
        self.db.execute(
            "INSERT OR IGNORE INTO thoughts (id, ts, origin, kind, re, content, vec)"
            " VALUES (?,?,?,?,?,?,?)",
            (t.id, t.ts, t.origin, t.kind, t.re, t.content, self.embed(t.content)),
        )
        self.db.commit()

    def remember(self, key: str, content: str) -> None:
        """Distilled, durable facts — what the dream cycle writes."""
        self.db.execute(
            "INSERT OR REPLACE INTO memories (key, ts, content, vec) VALUES (?,?,?,?)",
            (key, time.time(), content, self.embed(content)),
        )
        self.db.commit()

    def recall(self, query: str, limit: int = 5) -> list[str]:
        """Keyword recall over both tables, newest first."""
        like = f"%{query}%"
        rows = self.db.execute(
            "SELECT content, ts FROM thoughts WHERE content LIKE ? "
            "UNION ALL SELECT content, ts FROM memories WHERE content LIKE ? "
            "ORDER BY ts DESC LIMIT ?",
            (like, like, limit),
        ).fetchall()
        return [r[0] for r in rows]

    def embed(self, text: str) -> bytes | None:
        """Hook for vector recall (N-stage upgrade).

        When a body has an embedding model (e.g. Ollama's nomic-embed-text),
        return the vector packed as bytes here and add a cosine search to
        recall(). Until then, None is honest.
        """
        return None
