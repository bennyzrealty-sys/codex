"""Stamp every figure with its intrinsic size.

Without width/height the browser reserves no space for a lazy-loaded image,
so the page reflows as you scroll and a jump to a deep anchor lands you in
the wrong layer. The attributes cost nothing — CSS still sizes the image
with width:100%;height:auto — but they give the browser the aspect ratio up
front, so the layout is stable before a single byte of image arrives.

    python scripts/size_figures.py

Idempotent: existing width/height attributes are refreshed from the file on
disk, so redrawing a diagram at a new size fixes the page automatically.
"""
import json
import os
import re
import struct
import sys

F = "index.html"
FEED = "updates.json"
IMG = re.compile(r'<img\s+([^>]*?)src="(images/[^"]+)"([^>]*?)>')


def svg_size(path):
    head = open(path, encoding="utf-8", errors="ignore").read(2000)
    m = re.search(r'viewBox="\s*[\d.+-]+\s+[\d.+-]+\s+([\d.]+)\s+([\d.]+)', head)
    if m:
        return int(float(m.group(1))), int(float(m.group(2)))
    w = re.search(r'\swidth="(\d+)', head)
    h = re.search(r'\sheight="(\d+)', head)
    return (int(w.group(1)), int(h.group(1))) if w and h else None


def png_size(path):
    with open(path, "rb") as fh:
        head = fh.read(26)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", head[16:24])


def jpg_size(path):
    with open(path, "rb") as fh:
        if fh.read(2) != b"\xff\xd8":
            return None
        while True:
            b = fh.read(1)
            while b and b != b"\xff":
                b = fh.read(1)
            marker = fh.read(1)
            while marker == b"\xff":
                marker = fh.read(1)
            if not marker:
                return None
            if marker[0] in range(0xC0, 0xCF) and marker[0] not in (0xC4, 0xC8, 0xCC):
                fh.read(3)
                h, w = struct.unpack(">HH", fh.read(4))
                return w, h
            size = struct.unpack(">H", fh.read(2))[0]
            fh.seek(size - 2, 1)


def size_of(path):
    if not os.path.exists(path):
        return None
    low = path.lower()
    try:
        if low.endswith(".svg"):
            return svg_size(path)
        if low.endswith(".png"):
            return png_size(path)
        if low.endswith((".jpg", ".jpeg")):
            return jpg_size(path)
    except Exception:
        return None
    return None


def main():
    src = open(F, encoding="utf-8").read()
    stamped, skipped = 0, []

    def fix(m):
        nonlocal stamped
        pre, path, post = m.group(1), m.group(2), m.group(3)
        dims = size_of(path)
        if not dims:
            skipped.append(path)
            return m.group(0)
        attrs = re.sub(r'\s(?:width|height)="[^"]*"', "", pre + post).strip()
        stamped += 1
        return '<img %s src="%s" width="%d" height="%d">' % (
            attrs.replace('  ', ' '), path, dims[0], dims[1])

    out = IMG.sub(fix, src)
    if out != src:
        open(F, "w", encoding="utf-8").write(out)

    # the live feed renders its own <img> tags from JSON, so stamp those too
    feed_n = 0
    if os.path.exists(FEED):
        feed = json.load(open(FEED, encoding="utf-8"))
        changed = False
        for e in feed.get("entries", []):
            dims = size_of(e.get("art", "")) if e.get("art") else None
            if dims and (e.get("artw"), e.get("arth")) != dims:
                e["artw"], e["arth"] = dims
                changed = True
                feed_n += 1
        if changed:
            with open(FEED, "w", encoding="utf-8") as fh:
                json.dump(feed, fh, indent=2, ensure_ascii=False)
                fh.write("\n")

    print("size_figures: %d figure(s) and %d feed image(s) stamped%s"
          % (stamped, feed_n,
             ", skipped: " + ", ".join(sorted(set(skipped))) if skipped else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
