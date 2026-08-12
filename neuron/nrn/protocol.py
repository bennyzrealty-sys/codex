"""The Thought envelope — the mesh's only contract.

Any process that can produce and parse this JSON is a neuron,
whatever language or hardware it lives in. Resist adding fields.
"""
from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field, asdict

KINDS = ("observation", "question", "answer", "proposal", "ack")


@dataclass
class Thought:
    content: str
    kind: str = "observation"
    origin: str = "unknown"
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    re: str | None = None          # id of the thought this replies/acks to
    hops: list[str] = field(default_factory=list)
    ttl: int = 4                   # decremented on re-emission; 0 = do not forward
    ts: float = field(default_factory=time.time)
    sig: str | None = None         # reserved: per-body signature, unused on a trusted LAN

    def __post_init__(self):
        if self.kind not in KINDS:
            raise ValueError(f"unknown kind {self.kind!r}, expected one of {KINDS}")

    def reply(self, content: str, origin: str, kind: str = "answer") -> "Thought":
        return Thought(
            content=content,
            kind=kind,
            origin=origin,
            re=self.id,
            hops=self.hops + [origin],
            ttl=self.ttl - 1,
        )

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)

    @classmethod
    def from_json(cls, raw: str | bytes) -> "Thought":
        d = json.loads(raw)
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})
