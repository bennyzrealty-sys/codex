#!/usr/bin/env python3
"""Merge gate for any change to index.html.

Replicates every structural invariant the caretaker (update_codex.py),
tag_cards.py and size_figures.py depend on, and proves a future caretaker
sweep would still pass against the current file. Run from the repo root:

    python3 scripts/check_structure.py [baseline-git-ref]

The baseline ref (default: origin/main) supplies the card-id set that must
survive — ids are stable forever because localStorage counters key on them.
Exits non-zero on the first broken invariant.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import update_codex  # noqa: E402  (main-guarded; import is side-effect free)

FAILED = []


def check(name, ok, detail=""):
    tag = "ok " if ok else "FAIL"
    print("  %s %s%s" % (tag, name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILED.append(name)


def git_show(ref, path):
    out = subprocess.run(
        ["git", "show", "%s:%s" % (ref, path)],
        cwd=ROOT, capture_output=True, text=True,
    )
    return out.stdout if out.returncode == 0 else None


def main():
    ref = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    base = git_show(ref, "index.html")

    print("card grammar (update_codex.card_index)")
    cards = update_codex.card_index(html)
    check("cards found", len(cards) > 0, "regex matched nothing")
    if base is not None:
        base_cards = update_codex.card_index(base)
        missing = sorted(set(base_cards) - set(cards))
        check(
            "every baseline card id survives (%d in %s)" % (len(base_cards), ref),
            not missing, "lost: %s" % ", ".join(missing[:8]),
        )
    else:
        print("  --  baseline %s unavailable; skipping id-survival check" % ref)

    print("per-card voice contract")
    bad_plain, bad_tech, nested = [], [], []
    for cid in cards:
        span = update_codex.card_span(html, cid)
        if not span:
            continue
        body = html[span[0]:span[1]]
        if len(re.findall(r'<p class="plain">', body)) != 1:
            bad_plain.append(cid)
        if len(re.findall(r'<p class="tech">', body)) != 1:
            bad_tech.append(cid)
        if body.count("<details") > 1:
            nested.append(cid)
    check("exactly one <p class=\"plain\"> per card", not bad_plain, ", ".join(bad_plain[:5]))
    check("exactly one <p class=\"tech\"> per card", not bad_tech, ", ".join(bad_tech[:5]))
    check("no nested <details> inside a card", not nested, ", ".join(nested[:5]))

    print("caretaker sane() against baseline")
    if base is not None:
        # sane() also enforces a length floor a legitimate commit may cross
        # (e.g. moving inline CSS out), so the pieces are checked individually;
        # the floor only matters within one caretaker run, proven below.
        check("L4 markers present", "<!-- L4:START -->" in html and "<!-- L4:END -->" in html)
        check("CHANGELOG markers present",
              "<!-- CHANGELOG:START -->" in html and "<!-- CHANGELOG:END -->" in html)
        check("<section id= count unchanged",
              html.count("<section id=") == base.count("<section id="),
              "%d vs %d" % (html.count("<section id="), base.count("<section id=")))
        check("</details> count within ±4 of baseline",
              abs(html.count("</details>") - base.count("</details>")) <= 4,
              "%d vs %d" % (html.count("</details>"), base.count("</details>")))

    print("simulated future sweep (L4 interior swapped wholesale)")
    l4 = re.search(r"<!-- L4:START -->(.*?)<!-- L4:END -->", html, re.S)
    check("L4 span locatable", bool(l4))
    if l4:
        dummy = "".join(
            '\n<details class="card" id="l4-dummy-%d" data-card="l4-dummy-%d">'
            "<summary><b>Dummy %d</b><span>sweep simulation</span></summary>"
            '<p class="plain">plain.</p><p class="tech">tech.</p></details>' % (i, i, i)
            for i in range(3)
        )
        swept = html[:l4.start(1)] + dummy + "\n" + html[l4.end(1):]
        check("sane() passes after a wholesale L4 rewrite", update_codex.sane(swept, html))
        check("card_index still parses every non-L4 card",
              set(update_codex.card_index(swept)) >= (set(cards) - set(update_codex.card_index(l4.group(1)))))

    print("sibling-script idempotency (tag_cards, size_figures)")
    dirty = subprocess.run(["git", "diff", "--quiet", "--", "index.html", "updates.json"], cwd=ROOT).returncode
    if dirty:
        print("  --  working tree already dirty for index.html/updates.json; running scripts anyway")
    before = html
    before_updates = (ROOT / "updates.json").read_text(encoding="utf-8")
    for script in ("tag_cards.py", "size_figures.py"):
        subprocess.run([sys.executable, "scripts/" + script], cwd=ROOT, capture_output=True)
    check("tag_cards + size_figures are no-ops",
          (ROOT / "index.html").read_text(encoding="utf-8") == before
          and (ROOT / "updates.json").read_text(encoding="utf-8") == before_updates)

    print("runtime DOM hooks")
    for needle, label in [
        ('id="nodelog"', "#nodelog"), ('id="nl-level"', "#nl-level"),
        ('id="nl-ladder"', "#nl-ladder"), ('id="nl-entries"', "#nl-entries"),
        ('id="path"', "#path"), ('id="pathcount"', "#pathcount"),
        ('id="pathreset"', "#pathreset"), ('id="feed"', "#feed"),
        ('id="lateststrip"', "#lateststrip"),
        ('id="filters"', "#filters"), ('id="pulsemeta"', "#pulsemeta"),
        ('id="updtally"', "#updtally"), ('id="doorcount"', "#doorcount"),
        ('class="sizer"', ".sizer"), ('id="gloss"', "#gloss"),
    ]:
        check(label + " present", needle in html)
    check('theme-color #0f141b', 'content="#0f141b"' in html)
    manifest = (ROOT / "manifest.json").read_text(encoding="utf-8")
    check("manifest colors intact", manifest.count("#0f141b") >= 2)

    print("feed domains (update_codex.DOMAINS ⇄ the filter chips ⇄ the art)")
    chips = set(re.findall(r'<button data-dom="([a-z]+)"', html))
    missing_chip = sorted(set(update_codex.DOMAINS) - chips)
    check("every caretaker domain has a filter chip", not missing_chip,
          "no chip for: %s" % ", ".join(missing_chip))
    # valid_entry() falls back to images/update-<domain>.svg, so a domain
    # without that file renders a broken image the first time it is used
    no_art = [d for d in update_codex.DOMAINS
              if not (ROOT / "images" / ("update-%s.svg" % d)).exists()]
    check("every caretaker domain has fallback art", not no_art,
          "no images/update-<d>.svg for: %s" % ", ".join(no_art))

    print("installable app (manifest / service worker / asset links)")
    man = json.loads(manifest)
    icons = man.get("icons", [])
    png = {(i.get("sizes"), i.get("purpose")) for i in icons
           if i.get("type") == "image/png"}
    check("manifest declares 192 and 512 raster icons",
          ("192x192", "any") in png and ("512x512", "any") in png)
    check("manifest declares a 512 maskable icon", ("512x512", "maskable") in png)
    for i in icons:
        check("icon file exists: %s" % i.get("src"), (ROOT / i.get("src", "")).exists())
    check("service worker present", (ROOT / "sw.js").exists())
    check("service worker is registered by the page", "sw.js" in
          (ROOT / "assets" / "codex.js").read_text(encoding="utf-8"))
    check("privacy policy present (Play requires a URL)", (ROOT / "privacy.html").exists())
    check(".nojekyll present (or /.well-known/ is never served)",
          (ROOT / ".nojekyll").exists())

    print()
    if FAILED:
        print("STRUCTURE CHECK FAILED: %s" % ", ".join(FAILED))
        return 1
    print("structure check green — caretaker-safe.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
