# brain — your private, offline RAG

The Codex's **connectome** (Layer 11) and its **RAG memory** (Layer 14), made
real: a tiny retrieval setup that lets a *local* model answer questions about
*your* files — notes, repos, decisions — with nothing ever leaving the machine.

It is deliberately small: four Python files, two dependencies, one on-disk
vector store. Runs on your laptop and, more to the point, on the Pi.

## How it works

```
your files ──▶ ingest.py ──▶ [chunk] ──▶ [embed on Ollama] ──▶ ChromaDB (./store)
                                                                     │
your question ──▶ ask.py ──▶ [embed] ──▶ nearest-neighbour search ◀──┘
                                │
                                └─▶ top-k chunks ──▶ local LLM ──▶ grounded answer + sources
```

- **Embeddings and generation both run in [Ollama](https://ollama.com)** locally,
  so there is no API key and no egress (Codex Layer 12).
- **The vector store is ChromaDB on disk** (`brain/store/`, git-ignored). Because
  every vector is supplied explicitly, Chroma never downloads its own embedding
  model — the whole pipeline is offline after the models are pulled.

## Setup (once)

1. Install Ollama (`arm64` build works on the Pi): <https://ollama.com/download>
2. Pull the two models:
   ```bash
   ollama pull nomic-embed-text     # embeddings
   ollama pull llama3.2:3b          # generation (swap for any local chat model)
   ```
3. Install the Python deps:
   ```bash
   cd brain && pip install -r requirements.txt
   ```

## Use

```bash
# Index the whole Codex repo (default), or pass your own paths:
python ingest.py
python ingest.py ~/notes ~/second-brain

# Ask — one-shot or interactive:
python ask.py "what did I decide about the shift watcher?"
python ask.py
```

Re-run `ingest.py` whenever files change; IDs are stable, so edits update in
place instead of duplicating.

## Tuning

Everything is environment-overridable (see `config.py`) — no code edits needed:

| Variable | Default | Meaning |
|---|---|---|
| `BRAIN_CHAT_MODEL` | `llama3.2:3b` | local generation model |
| `BRAIN_EMBED_MODEL` | `nomic-embed-text` | local embedding model |
| `BRAIN_STORE` | `brain/store` | where the vectors live |
| `BRAIN_TOP_K` | `4` | chunks retrieved per question |
| `BRAIN_CHUNK_SIZE` / `BRAIN_CHUNK_OVERLAP` | `1000` / `150` | chunking (chars) |
| `OLLAMA_HOST` | `http://127.0.0.1:11434` | local runtime |

## Where this goes next

This is **v0.1 — one synapse**. The natural extensions, in order: have the
shift-watcher and other repos write their events in as memories (the Neural
Estate from Layer 11), add a nightly re-index (the "sleep"/consolidation job),
and later pair a LoRA-tuned base (your *voice*) with this retrieval (your
*facts*) for a private vertical model — exactly the loophole in Layer 14.
