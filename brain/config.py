"""brain — configuration.

Everything here is environment-overridable, so the same code runs unchanged on
your laptop and on the Pi. Nothing in this module reaches the network except the
local Ollama host below — no cloud, no API key, no egress (Codex Layer 12).
"""
import os

# Local Ollama runtime. Talks to 127.0.0.1 only.
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")

# Models — pull each once with `ollama pull <name>`.
EMBED_MODEL = os.environ.get("BRAIN_EMBED_MODEL", "nomic-embed-text")
CHAT_MODEL = os.environ.get("BRAIN_CHAT_MODEL", "llama3.2:3b")

# On-disk, persistent vector store (Codex Layer 14's "connectome").
CHROMA_PATH = os.environ.get(
    "BRAIN_STORE", os.path.join(os.path.dirname(os.path.abspath(__file__)), "store")
)
COLLECTION = os.environ.get("BRAIN_COLLECTION", "second-brain")

# Chunking + retrieval knobs.
CHUNK_SIZE = int(os.environ.get("BRAIN_CHUNK_SIZE", "1000"))       # characters
CHUNK_OVERLAP = int(os.environ.get("BRAIN_CHUNK_OVERLAP", "150"))  # characters
TOP_K = int(os.environ.get("BRAIN_TOP_K", "4"))

# File types worth indexing. Everything else is skipped.
TEXT_EXT = {
    ".md", ".txt", ".rst", ".py", ".js", ".ts", ".json", ".yml", ".yaml",
    ".html", ".css", ".sh", ".toml", ".ini", ".cfg",
}

# Directories never worth walking into.
SKIP_DIRS = {".git", "node_modules", "store", "__pycache__", ".venv", "venv"}
