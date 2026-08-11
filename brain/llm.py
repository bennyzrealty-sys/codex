"""Thin client for a local Ollama instance.

Two calls only: embed(text) and chat(system, user). Both go to 127.0.0.1 over
plain HTTP — there is no cloud dependency and no key. If Ollama isn't running,
you get one clear error instead of a stack trace.
"""
import requests

from config import OLLAMA_HOST, EMBED_MODEL, CHAT_MODEL


class OllamaError(RuntimeError):
    """Raised when the local model runtime can't be reached or errors."""


def _post(path, payload, timeout=120):
    url = f"{OLLAMA_HOST}{path}"
    try:
        r = requests.post(url, json=payload, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError as e:
        raise OllamaError(
            f"cannot reach Ollama at {OLLAMA_HOST} — start it with `ollama serve`"
        ) from e
    except requests.exceptions.HTTPError as e:
        raise OllamaError(f"Ollama returned {r.status_code} for {path}: {r.text[:200]}") from e


def embed(text):
    """Return the embedding vector for one piece of text."""
    data = _post("/api/embeddings", {"model": EMBED_MODEL, "prompt": text})
    return data["embedding"]


def chat(system, user):
    """Single-turn chat completion from the local model."""
    data = _post(
        "/api/chat",
        {
            "model": CHAT_MODEL,
            "stream": False,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        },
    )
    return data["message"]["content"]
