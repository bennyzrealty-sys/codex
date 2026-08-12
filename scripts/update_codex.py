"""The Codex caretaker.

Wakes every two days (06:00 UTC, see .github/workflows/refresh.yml) and does
exactly three things:

  1. writes new entries at the TOP of the live feed (updates.json) —
     append-only, nothing already there is ever edited or removed;
  2. refreshes Layer 04 (the Frontier) between its markers;
  3. where a finding genuinely changes material already taught below, edits
     that card and marks it `data-updated`, which the page renders as
     NEWLY UPDATED until the reader has opened it three times.

It fails safe in the strongest sense: unparseable output, a bad date, an
unknown card id or an image that does not exist all mean "skip that piece",
and a failure before any write means the site is left exactly as it was.
"""
import datetime
import json
import os
import re
import sys
import urllib.request

HTML = "index.html"
FEED = "updates.json"

MODEL = os.environ.get("CODEX_MODEL", "claude-sonnet-5")
MAX_ENTRIES = 6          # per sweep
MAX_CARD_EDITS = 6       # per sweep
DOMAINS = ("ai", "it", "hardware", "cyber")

TODAY = datetime.date.today()
today = TODAY.isoformat()
next_scan = (TODAY + datetime.timedelta(days=2)).isoformat() + " 06:00 UTC"


# ---------------------------------------------------------------- helpers
def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def card_index(html):
    """{card id: headline} for every concept card on the page."""
    out = {}
    for m in re.finditer(
        r'<details class="card" id="([^"]+)"[^>]*>\s*<summary><b>(.*?)</b><span>(.*?)</span>',
        html, re.S,
    ):
        out[m.group(1)] = re.sub(r"\s+", " ", "%s — %s" % (m.group(2), m.group(3))).strip()
    return out


def card_span(html, cid):
    """(start, end) of one card's full <details> block, or None."""
    open_at = html.find('<details class="card" id="%s"' % cid)
    if open_at < 0:
        return None
    close_at = html.find("</details>", open_at)
    if close_at < 0:
        return None
    return open_at, close_at + len("</details>")


def set_attr(tag, name, value):
    tag = re.sub(r'\s%s="[^"]*"' % re.escape(name), "", tag)
    return tag[:-1].rstrip() + ' %s="%s">' % (name, value.replace('"', "&quot;"))


def clean(s, limit=1200):
    s = re.sub(r"\s+", " ", str(s or "")).strip()
    return s[:limit]


# ---------------------------------------------------------------- the ask
def build_prompt(l4, cards, images):
    return """Today is %(today)s. You are the caretaker of The Operator's Codex — a personal
field manual for a solo operator in Sheffield running a Raspberry Pi 5 node, building
narrow AI agents, and moving toward NHS digital work.

Web-search for what genuinely changed in the last ~3 days across four fields:
  ai        — model releases (especially small/open-weight, Ollama-runnable), agent
              tooling, Anthropic/Claude and MCP releases, notable capability shifts
  it        — infrastructure, hosting, protocols, developer platforms, regulation
              affecting how software is built and shipped
  hardware  — Raspberry Pi news and firmware, silicon supply, accelerators, memory,
              anything that changes what a small board or a datacentre can do
  cyber     — actively-exploited vulnerabilities (CISA KEV), supply-chain incidents,
              notable breaches, defensive tooling, cryptography changes

Return ONLY a JSON object — no markdown fences, no prose around it — with these keys:

"entries": array of 2 to %(max_entries)d NEW feed items, each:
   {"id": "YYYY-MM-DD-short-slug",
    "date": "YYYY-MM-DD",              // the date of the development, not today
    "domain": "ai" | "it" | "hardware" | "cyber",
    "title": "a claim, not a topic — max ~70 chars",
    "oneline": "one clause of extra context",
    "plain":  "PLAIN VOICE: clear to a smart 13-year-old. No jargon unexplained. 60-110 words.",
    "tech":   "TECHNICAL VOICE: exact terminology, versions, numbers, CVE ids. 50-90 words.",
    "lands":  "WHERE IT LANDS: what this changes for a solo operator with one Pi, a few
               agents and an NHS ambition. Be concrete and specific. 60-110 words.",
    "tools":  ["3-6 tool or command names worth reaching for"],
    "toolnote": "optional single sentence about the tools",
    "art":    "one path from the allowed image list below",
    "artcap": "short caption for that image",
    "sources": [{"label":"publisher or title","url":"https://..."}]   // 1-3, real URLs only
   }

"layer04_html": the full replacement inner HTML for Layer 04 (the Frontier). Keep the
   exact two-voice card structure: <details class="card"><summary><b>Title</b><span>sub</span>
   </summary><p class="plain">…</p><p class="tech">…</p></details>. Update only facts that
   actually changed. Do not add id or data-card attributes — they are assigned separately.

"card_updates": array of 0 to %(max_edits)d edits to material already taught elsewhere in
   the Codex, ONLY where a finding this sweep genuinely changes what a card says:
   {"card": "<exact id from the card list below>",
    "note": "one short line naming what changed — shown under the NEWLY UPDATED mark",
    "plain": "optional full replacement for that card's plain voice",
    "tech":  "optional full replacement for that card's technical voice"}
   Leave this array empty rather than inventing a reason to touch a card.

"changelog_html": "<p><b>%(today)s</b> — what changed this sweep · source · action for
   Joe: none/consider/do</p>"

Rules that are not negotiable:
 - Never invent. If something is unconfirmed, say "unverified" and name the source.
 - Every source URL must be one you actually found in search results.
 - Plain voice never contains an unexplained acronym.
 - "lands" must say something an operator would act on, not a summary of the news.
 - Prefer 3-4 different domains over four items about the same story.

ALLOWED IMAGE PATHS (use only these):
%(images)s

EXISTING CARDS you may update (id — headline):
%(cards)s

CURRENT LAYER 04:
%(l4)s""" % {
        "today": today,
        "max_entries": MAX_ENTRIES,
        "max_edits": MAX_CARD_EDITS,
        "images": "\n".join("  " + i for i in images),
        "cards": "\n".join("  %s — %s" % (k, v) for k, v in cards.items()),
        "l4": l4,
    }


def ask(prompt):
    body = {
        "model": MODEL,
        "max_tokens": 16000,
        "tools": [{"type": "web_search_20250305", "name": "web_search"}],
        "messages": [{"role": "user", "content": prompt}],
    }
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(body).encode(),
        headers={
            "content-type": "application/json",
            "x-api-key": os.environ["ANTHROPIC_API_KEY"],
            "anthropic-version": "2023-06-01",
        },
    )
    data = json.loads(urllib.request.urlopen(req, timeout=900).read())
    text = "\n".join(b.get("text", "") for b in data["content"] if b.get("type") == "text")
    text = re.sub(r"```json|```", "", text).strip()
    return json.loads(text[text.index("{"): text.rindex("}") + 1])


# ---------------------------------------------------------------- applying
def valid_entry(e, images, seen_ids):
    try:
        if e["domain"] not in DOMAINS:
            return None
        datetime.date.fromisoformat(e["date"])
        if e["id"] in seen_ids or not re.match(r"^[0-9a-zA-Z._-]+$", e["id"]):
            return None
        for f in ("title", "plain", "tech", "lands"):
            if len(clean(e[f])) < 20:
                return None
        art = e.get("art") if e.get("art") in images else "images/update-%s.svg" % e["domain"]
        srcs = [
            {"label": clean(s.get("label"), 90), "url": s["url"]}
            for s in (e.get("sources") or [])
            if str(s.get("url", "")).startswith("https://")
        ][:3]
        return {
            "id": e["id"],
            "date": e["date"],
            "domain": e["domain"],
            "title": clean(e["title"], 140),
            "oneline": clean(e.get("oneline"), 160),
            "plain": clean(e["plain"]),
            "tech": clean(e["tech"]),
            "lands": clean(e["lands"]),
            "tools": [clean(t, 40) for t in (e.get("tools") or [])][:8],
            "toolnote": clean(e.get("toolnote"), 220),
            "art": art,
            "artcap": clean(e.get("artcap"), 160) or e["title"],
            "sources": srcs,
            "touches": [],
        }
    except Exception:
        return None


def apply_card_updates(html, updates, cards):
    """Rewrite a card's voices and stamp it as newly updated. Never structural."""
    done = []
    for u in updates[:MAX_CARD_EDITS]:
        cid = u.get("card")
        if cid not in cards:
            continue
        span = card_span(html, cid)
        if not span:
            continue
        start, end = span
        block = html[start:end]

        if u.get("plain") and "<p class=\"plain\">" in block:
            block = re.sub(r'<p class="plain">.*?</p>',
                           '<p class="plain">%s</p>' % clean(u["plain"], 1600),
                           block, count=1, flags=re.S)
        if u.get("tech") and "<p class=\"tech\">" in block:
            block = re.sub(r'<p class="tech">.*?</p>',
                           '<p class="tech">%s</p>' % clean(u["tech"], 1600),
                           block, count=1, flags=re.S)

        tag = re.match(r"<details[^>]*>", block).group(0)
        newtag = set_attr(set_attr(tag, "data-updated", today),
                          "data-updnote", clean(u.get("note"), 180))
        block = newtag + block[len(tag):]

        html = html[:start] + block + html[end:]
        done.append(cid)
    return html, done


def sane(html, before):
    """Refuse to write anything that lost structure."""
    return (
        "<!-- L4:START -->" in html
        and "<!-- L4:END -->" in html
        and "<!-- CHANGELOG:START -->" in html
        and html.count("<section id=") == before.count("<section id=")
        # Layer 04 is rewritten wholesale, so its card count may move a little;
        # anything larger than that is the model having eaten the page.
        and abs(html.count("</details>") - before.count("</details>")) <= 4
        and len(html) > len(before) * 0.9
    )


# ---------------------------------------------------------------- the run
def main():
    html = read(HTML)
    before = html
    feed = json.loads(read(FEED))
    cards = card_index(html)
    images = sorted(
        "images/" + n for n in os.listdir("images")
        if n.endswith((".svg", ".png", ".jpg"))
    )

    l4 = re.search(r"<!-- L4:START -->(.*?)<!-- L4:END -->", html, re.S).group(1)

    out = ask(build_prompt(l4, cards, images))

    # --- 1. the feed (append-only: existing entries are never touched)
    seen = {e["id"] for e in feed.get("entries", [])}
    fresh = []
    for e in (out.get("entries") or [])[:MAX_ENTRIES]:
        v = valid_entry(e, set(images), seen)
        if v:
            seen.add(v["id"])
            fresh.append(v)
    fresh.sort(key=lambda e: e["date"], reverse=True)

    # --- 2. Layer 04
    l4_new = out.get("layer04_html", "").strip()
    if len(l4_new) > 400 and l4_new.count("<details") >= 2:
        html = html.replace(l4, "\n" + l4_new + "\n")

    # --- 3. cards touched by this sweep
    html, touched = apply_card_updates(html, out.get("card_updates") or [], cards)

    # --- 4. the changelog
    entry = (out.get("changelog_html") or "").strip()
    if entry.startswith("<p>"):
        html = html.replace("<!-- CHANGELOG:START -->",
                            "<!-- CHANGELOG:START -->\n    " + entry, 1)

    # attribute each touched card back to the entry that caused it
    if fresh and touched:
        fresh[0]["touches"] = touched

    if not sane(html, before):
        print("caretaker: structural check failed — nothing written")
        return 0

    if fresh:
        feed["entries"] = fresh + feed.get("entries", [])
    feed["generated"] = today
    feed["next_scan"] = next_scan
    feed["cadence_days"] = 2

    with open(FEED, "w", encoding="utf-8") as fh:
        json.dump(feed, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    with open(HTML, "w", encoding="utf-8") as fh:
        fh.write(html)

    print("caretaker: %s — %d new feed entr%s, %d card(s) marked updated"
          % (today, len(fresh), "y" if len(fresh) == 1 else "ies", len(touched)))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:          # fail safe — never break the site
        print("caretaker: no update applied —", repr(exc))
        sys.exit(0)
