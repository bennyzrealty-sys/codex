"""Codex caretaker: refresh Layer 04 + changelog every 2 days. Fails safe: on any
problem it changes nothing, so the site never breaks."""
import os, re, json, datetime, urllib.request

F = "index.html"
html = open(F, encoding="utf-8").read()
l4 = re.search(r"<!-- L4:START -->(.*?)<!-- L4:END -->", html, re.S).group(1)
today = datetime.date.today().isoformat()

PROMPT = f"""Today is {today}. You are the caretaker of a personal AI study guide.
Web-search this watchlist for developments in the last ~3 days: new small/open-weight
model releases (Ollama-runnable), Raspberry Pi hardware/firmware news, Anthropic/Claude
and MCP releases, notable agentic-AI shifts, and NHS digital / clinical-safety updates.

Below is the current Layer 04 (Frontier) HTML. Update ONLY facts that changed; keep the
exact two-voice card structure (plain voice = clear to a smart 13-year-old; technical
voice = precise jargon). Never invent: unverified claims must say "unverified".

Return ONLY a JSON object, no markdown fences, with keys:
  "layer04_html": the full replacement inner HTML for Layer 04,
  "changelog_html": one <p><b>{today}</b> — what changed · source · action for Joe:
                    none/consider/do</p>

CURRENT LAYER 04:
{l4}"""

body = {
    "model": "claude-sonnet-4-6",
    "max_tokens": 8000,
    "tools": [{"type": "web_search_20250305", "name": "web_search"}],
    "messages": [{"role": "user", "content": PROMPT}],
}
req = urllib.request.Request(
    "https://api.anthropic.com/v1/messages",
    data=json.dumps(body).encode(),
    headers={"content-type": "application/json",
             "x-api-key": os.environ["ANTHROPIC_API_KEY"],
             "anthropic-version": "2023-06-01"},
)
try:
    data = json.loads(urllib.request.urlopen(req, timeout=600).read())
    text = "\n".join(b.get("text", "") for b in data["content"] if b.get("type") == "text")
    text = re.sub(r"```json|```", "", text).strip()
    out = json.loads(text[text.index("{"): text.rindex("}") + 1])
    html = html.replace(l4, "\n" + out["layer04_html"].strip() + "\n")
    html = html.replace("<!-- CHANGELOG:START -->",
                        "<!-- CHANGELOG:START -->\n    " + out["changelog_html"].strip())
    open(F, "w", encoding="utf-8").write(html)
    print("caretaker: updated", today)
except Exception as e:      # fail safe, never break the site
    print("caretaker: no update applied —", e)
