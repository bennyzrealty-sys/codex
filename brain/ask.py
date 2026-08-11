"""Ask your private brain a question.

    python ask.py "what did I decide about the shift watcher?"
    python ask.py                 # interactive loop (Ctrl-D to quit)

Retrieves the most relevant chunks from the local vector store and answers with
the local model, grounded strictly in what it retrieved. Fully offline: the only
network call is to Ollama on 127.0.0.1.
"""
import sys

import chromadb

from config import CHROMA_PATH, COLLECTION, TOP_K
from llm import embed, chat, OllamaError

SYSTEM = (
    "You are the operator's private assistant. Answer ONLY from the provided "
    "context. If the answer is not in the context, say so plainly rather than "
    "guessing. Cite the sources you used by their path."
)


def answer(col, question):
    res = col.query(
        query_embeddings=[embed(question)],
        n_results=TOP_K,
        include=["documents", "metadatas"],
    )
    docs = res["documents"][0]
    metas = res["metadatas"][0]
    if not docs:
        return "(the brain is empty — run `python ingest.py` first)", []

    context = "\n\n".join(
        f"[{m['source']}#{m['chunk']}]\n{d}" for d, m in zip(docs, metas)
    )
    reply = chat(SYSTEM, f"Context:\n{context}\n\nQuestion: {question}")
    sources = list(dict.fromkeys(m["source"] for m in metas))  # de-dup, keep order
    return reply, sources


def _print(reply, sources):
    print(reply)
    if sources:
        print("\nsources:", ", ".join(sources))


def main():
    col = chromadb.PersistentClient(path=CHROMA_PATH).get_or_create_collection(COLLECTION)

    if len(sys.argv) > 1:
        _print(*answer(col, " ".join(sys.argv[1:])))
        return

    print("brain ready — ask a question (Ctrl-D to quit)")
    while True:
        try:
            q = input("\n> ").strip()
        except EOFError:
            print()
            break
        if q:
            _print(*answer(col, q))


if __name__ == "__main__":
    try:
        main()
    except OllamaError as e:
        sys.exit(f"error: {e}")
