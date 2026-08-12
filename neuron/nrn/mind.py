"""Pluggable minds. One method: consider(thought, recalled) -> str | None.

Returning None means "nothing to add" — the most common and most correct
output. The mesh does not care where thinking happens; a body upgrades its
mind and nobody else changes a line.
"""
from __future__ import annotations

import json
import os
import re
import urllib.request

from .protocol import Thought


class RuleMind:
    """Reflexes. Zero cost, always on. Teach it your own reflexes over time."""

    def __init__(self, name: str):
        self.name = name
        self.rules: list[tuple[re.Pattern, str]] = [
            (re.compile(r"^ping$", re.I), f"pong from {name}"),
            (re.compile(r"^who is (awake|online)\??$", re.I),
             f"{name} is awake"),
        ]

    def consider(self, t: Thought, recalled: list[str]) -> str | None:
        if t.kind not in ("question", "observation"):
            return None
        for pattern, response in self.rules:
            if pattern.search(t.content.strip()):
                return response
        return None


class OllamaMind:
    """A small local model via Ollama. Free, private, slow-is-fine."""

    def __init__(self, name: str, model: str = "llama3.2:3b",
                 host: str = "http://localhost:11434"):
        self.name, self.model, self.host = name, model, host

    def consider(self, t: Thought, recalled: list[str]) -> str | None:
        if t.kind != "question":
            return None
        context = "\n".join(recalled) or "(no relevant memories)"
        prompt = (
            f"You are {self.name}, one neuron in a small household mesh. "
            f"Relevant local memories:\n{context}\n\n"
            f"Question on the mesh: {t.content}\n"
            "Answer briefly if your memories genuinely help; "
            "otherwise reply exactly PASS."
        )
        req = urllib.request.Request(
            f"{self.host}/api/generate",
            data=json.dumps({"model": self.model, "prompt": prompt,
                             "stream": False}).encode(),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            answer = json.load(resp)["response"].strip()
        return None if answer == "PASS" or not answer else answer


class ClaudeMind:
    """The API, for thoughts explicitly worth money. Requires ANTHROPIC_API_KEY.

    The frugality gate lives in the daemon, not here: this mind only ever
    sees thoughts the daemon already decided deserve it.
    """

    def __init__(self, name: str, model: str = "claude-haiku-4-5"):
        self.name, self.model = name, model
        self.key = os.environ.get("ANTHROPIC_API_KEY", "")

    def consider(self, t: Thought, recalled: list[str]) -> str | None:
        if not self.key or t.kind != "question":
            return None
        body = {
            "model": self.model,
            "max_tokens": 512,
            "messages": [{"role": "user", "content":
                          f"Memories: {recalled}\n\nQuestion: {t.content}\n"
                          "Answer briefly, or reply exactly PASS."}],
        }
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json",
                     "x-api-key": self.key,
                     "anthropic-version": "2023-06-01"},
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            answer = json.load(resp)["content"][0]["text"].strip()
        return None if answer == "PASS" else answer


def build(kind: str, name: str, **kw):
    return {"rule": RuleMind, "ollama": OllamaMind, "claude": ClaudeMind}[kind](name, **kw)
