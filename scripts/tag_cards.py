"""Give every concept card a stable, human-readable id.

The caretaker needs a handle to say "this card changed"; the door and the
seeker need an anchor to jump to. Run it any time cards are added:

    python scripts/tag_cards.py

Idempotent — a card that already carries data-card is left exactly as it is,
so ids survive rewrites and the read-counters in the browser stay valid.
"""
import html
import re
import sys

F = "index.html"

CARD = re.compile(r'<details class="card"((?:\s+[a-zA-Z-]+="[^"]*")*)\s*>\s*<summary>\s*<b>(.*?)</b>', re.S)
SECTION = re.compile(r'<section id="([^"]+)"')

STOP = {"the", "a", "an", "and", "or", "of", "to", "in", "on", "vs", "&", "its", "how", "why", "what"}


def slug(text, limit=5):
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text).lower()
    words = [w for w in re.split(r"[^a-z0-9+]+", text) if w]
    keep = [w for w in words if w not in STOP] or words
    return "-".join(keep[:limit]) or "card"


def main():
    src = open(F, encoding="utf-8").read()

    # section boundaries, so a card's id names the layer it lives in
    bounds = [(m.start(), m.group(1)) for m in SECTION.finditer(src)]

    def section_at(pos):
        cur = "x"
        for start, sid in bounds:
            if start <= pos:
                cur = sid
            else:
                break
        return cur

    used, added = set(), 0
    for m in CARD.finditer(src):
        found = re.search(r'data-card="([^"]+)"', m.group(1) or "")
        if found:
            used.add(found.group(1))

    out, cursor = [], 0
    for m in CARD.finditer(src):
        attrs = m.group(1) or ""
        out.append(src[cursor:m.start()])
        cursor = m.end()
        if 'data-card="' in attrs:
            out.append(m.group(0))
            continue
        base = "%s-%s" % (section_at(m.start()), slug(m.group(2)))
        cid, n = base, 2
        while cid in used:
            cid, n = "%s-%d" % (base, n), n + 1
        used.add(cid)
        added += 1
        out.append(
            '<details class="card" id="%s" data-card="%s"%s>\n    <summary><b>%s</b>'
            % (cid, cid, attrs, m.group(2))
        )
    out.append(src[cursor:])
    new = "".join(out)

    if new != src:
        open(F, "w", encoding="utf-8").write(new)
    print("tag_cards: %d card(s) tagged, %d total" % (added, len(used)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
