"""Index text/code files into the local vector store.

    python ingest.py                # index the whole Codex repo (default)
    python ingest.py ../notes docs  # index specific paths

Re-running is safe and cheap: chunk IDs are stable (sha1 of path + index), so an
edited file updates its chunks in place instead of duplicating them.
"""
import hashlib
import os
import sys

import chromadb

from config import CHROMA_PATH, COLLECTION, CHUNK_SIZE, CHUNK_OVERLAP, TEXT_EXT, SKIP_DIRS
from llm import embed, OllamaError


def chunk(text):
    """Split text into overlapping character windows."""
    step = max(1, CHUNK_SIZE - CHUNK_OVERLAP)
    pieces = [text[i:i + CHUNK_SIZE] for i in range(0, len(text), step)]
    return pieces or [""]


def iter_files(paths):
    for p in paths:
        if os.path.isfile(p):
            yield p
            continue
        for root, dirs, files in os.walk(p):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for f in files:
                if os.path.splitext(f)[1].lower() in TEXT_EXT:
                    yield os.path.join(root, f)


def main(paths):
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    col = client.get_or_create_collection(COLLECTION)

    n_files = n_chunks = 0
    for path in iter_files(paths):
        try:
            text = open(path, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        if not text.strip():
            continue

        ids, docs, embs, metas = [], [], [], []
        for i, c in enumerate(chunk(text)):
            if not c.strip():
                continue
            ids.append(hashlib.sha1(f"{path}:{i}".encode()).hexdigest())
            docs.append(c)
            embs.append(embed(c))          # local embedding, never leaves the box
            metas.append({"source": path, "chunk": i})

        if ids:
            col.upsert(ids=ids, documents=docs, embeddings=embs, metadatas=metas)
            n_files += 1
            n_chunks += len(ids)
            print(f"  {len(ids):3} chunks  {path}")

    print(f"done: {n_chunks} chunks from {n_files} files -> {CHROMA_PATH}")


if __name__ == "__main__":
    # Default target: the repo root (brain/ lives one level below it).
    default = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    targets = sys.argv[1:] or [default]
    try:
        main(targets)
    except OllamaError as e:
        sys.exit(f"error: {e}")
