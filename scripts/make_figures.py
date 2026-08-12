"""Draw the Codex's field diagrams.

Every figure in images/ that isn't a photograph is generated here, so the
palette, the type and the geometry stay one system no matter how many
layers get grafted on later.

    python scripts/make_figures.py          # writes images/*.svg

Existing hand-drawn figures are left alone — this only writes the names
listed in FIGURES.
"""
import os

W, H = 760, 420
INK, PANEL, PANEL2 = "#0d1219", "#151c26", "#1a2330"
BONE, DIM = "#e7e2d4", "#aab5c1"
GOLD, TEAL, EMBER = "#dfa32b", "#57b39c", "#cf6f57"
BLUE = "#9fb4d8"
MONO = "ui-monospace,monospace"

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images")


# ---------- primitives ----------------------------------------------------
def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def head(title, w=W, h=H):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
        'font-family="system-ui,-apple-system,sans-serif">\n'
        '  <rect width="%d" height="%d" fill="%s"/>\n'
        '  <text x="30" y="40" fill="%s" font-size="13" letter-spacing="3" '
        'font-family="%s">%s</text>\n' % (w, h, w, h, INK, GOLD, MONO, esc(title.upper()))
    )


def box(x, y, w, h, label="", sub="", stroke=DIM, fill=PANEL, r=9, size=13, op=".55"):
    s = '  <rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s" stroke="%s" stroke-opacity="%s"/>\n' % (
        x, y, w, h, r, fill, stroke, op)
    if label and sub:
        s += text(x + w / 2, y + h / 2 - 3, label, BONE, size, mid=True, weight="500")
        s += text(x + w / 2, y + h / 2 + 15, sub, DIM, size - 2, mid=True)
    elif label:
        s += text(x + w / 2, y + h / 2 + 5, label, BONE, size, mid=True, weight="500")
    return s


def text(x, y, t, fill=BONE, size=13, mid=False, mono=False, weight="400", anchor=None, op="1"):
    a = anchor or ("middle" if mid else "start")
    fam = ' font-family="%s"' % MONO if mono else ""
    return ('  <text x="%g" y="%g" fill="%s" fill-opacity="%s" font-size="%g" '
            'text-anchor="%s" font-weight="%s"%s>%s</text>\n'
            % (x, y, fill, op, size, a, weight, fam, esc(t)))


def arrow(x1, y1, x2, y2, color=TEAL, w=1.6, dash=None, op=".8"):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    ang = 0
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    hl = 7
    ax, ay = x2 - hl * math.cos(ang - 0.42), y2 - hl * math.sin(ang - 0.42)
    bx, by = x2 - hl * math.cos(ang + 0.42), y2 - hl * math.sin(ang + 0.42)
    return ('  <line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-opacity="%s" '
            'stroke-width="%g"%s/>\n'
            '  <polygon points="%g,%g %g,%g %g,%g" fill="%s" fill-opacity="%s"/>\n'
            % (x1, y1, x2, y2, color, op, w, d, x2, y2, ax, ay, bx, by, color, op))


def line(x1, y1, x2, y2, color=DIM, w=1, dash=None, op=".4"):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('  <line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-opacity="%s" '
            'stroke-width="%g"%s/>\n' % (x1, y1, x2, y2, color, op, w, d))


def chip(x, y, t, color=TEAL, w=None):
    w = w or (len(t) * 7.0 + 22)
    return ('  <rect x="%g" y="%g" width="%g" height="24" rx="12" fill="none" '
            'stroke="%s" stroke-opacity=".6"/>\n' % (x, y, w, color)
            + text(x + w / 2, y + 16, t, color, 11, mid=True, mono=True))


def caption(y, t, color=DIM, x=30, size=12):
    return text(x, y, t, color, size, mono=True)


def wrap(x, y, t, width, color=BONE, size=11, lh=15, mid=False, op="1"):
    """Plain <text> line-wrapping. foreignObject renders inconsistently
    outside browsers, and these figures must survive any renderer."""
    words, lines, cur = str(t).split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if len(trial) > width and cur:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return "".join(text(x, y + i * lh, ln, color, size, mid=mid, op=op)
                   for i, ln in enumerate(lines))


def tail():
    return "</svg>\n"


# ---------- the figures ---------------------------------------------------
def packet_journey():
    s = head("one click — the five things that happen before a page appears")
    stops = [
        ("you type", "a name", GOLD),
        ("DNS", "name → number", BLUE),
        ("TCP", "the handshake", TEAL),
        ("TLS", "the padlock", TEAL),
        ("HTTP", "the actual ask", GOLD),
    ]
    x = 30
    for i, (a, b, c) in enumerate(stops):
        s += box(x, 92, 122, 62, a, b, stroke=c)
        if i < 4:
            s += arrow(x + 122, 123, x + 140, 123, c)
        x += 140
    s += text(30, 190, "each stop can fail on its own — and each fails with its own accent", DIM, 12)
    fails = [
        ("typo, or a domain that never existed", GOLD, 30),
        ("NXDOMAIN · resolver unreachable · stale cache", BLUE, 170),
        ("connection refused · timeout · no route", TEAL, 310),
        ("certificate expired · name mismatch", TEAL, 450),
        ("404 · 500 · 429 too many requests", GOLD, 590),
    ]
    for t, c, fx in fails:
        s += line(fx + 60, 200, fx + 60, 216, c, op=".35")
        s += wrap(fx, 232, t, 20, c, 11, 15, op=".85")
    s += box(30, 306, 700, 76, stroke=EMBER, fill=PANEL2)
    s += text(48, 334, "the layer beneath the text", EMBER, 13, weight="600")
    s += text(48, 356, "TLS sends its hello in the clear — the cipher list is a fingerprint (JA4).", BONE, 12)
    s += text(48, 373, "Changing a header changes nothing one floor down. See the Deep Field.", DIM, 12)
    return s + tail()


def nat_tunnel():
    s = head("why your home server is unreachable — and the honest way in")
    s += text(30, 76, "the old way: punch a hole", EMBER, 14, weight="600")
    s += box(30, 96, 120, 54, "internet", "", stroke=EMBER)
    s += arrow(150, 123, 205, 123, EMBER)
    s += box(205, 96, 130, 54, "router / NAT", "port 22 open", stroke=EMBER)
    s += arrow(335, 123, 390, 123, EMBER)
    s += box(390, 96, 120, 54, "your Pi", "", stroke=EMBER)
    s += text(530, 112, "every scanner on earth", EMBER, 12)
    s += text(530, 130, "finds that hole in", DIM, 12)
    s += text(530, 148, "under an hour", DIM, 12)

    s += text(30, 208, "the modern way: no hole at all", TEAL, 14, weight="600")
    s += box(30, 228, 120, 54, "your phone", "", stroke=TEAL)
    s += box(390, 228, 120, 54, "your Pi", "", stroke=TEAL)
    s += box(190, 214, 150, 82, stroke=TEAL, fill=PANEL2)
    s += text(265, 246, "overlay mesh", TEAL, 13, mid=True, weight="500")
    s += text(265, 264, "WireGuard", DIM, 11, mid=True, mono=True)
    s += text(265, 280, "Tailscale / Nebula", DIM, 11, mid=True, mono=True)
    s += arrow(150, 255, 188, 255, TEAL)
    s += arrow(342, 255, 388, 255, TEAL)
    s += text(530, 244, "both ends dial out.", BONE, 12)
    s += text(530, 262, "the router opens nothing.", DIM, 12)
    s += text(530, 280, "identity, not address.", TEAL, 12)

    s += box(30, 326, 700, 60, stroke=DIM, fill=PANEL2)
    s += text(48, 352, "CGNAT (100.64.0.0/10) shares one public address across thousands of homes —", BONE, 12)
    s += text(48, 371, "so on many connections port-forwarding is not risky, it is simply impossible.", DIM, 12)
    return s + tail()


def linux_anatomy():
    s = head("the machine's own anatomy — what sits where on linux")
    s += box(30, 70, 700, 92, stroke=GOLD, fill=PANEL)
    s += text(48, 96, "userspace — everything you install and run", GOLD, 13, weight="600")
    apps = ["your python script", "ollama", "docker", "nginx", "sshd"]
    x = 48
    for a in apps:
        s += chip(x, 112, a, GOLD)
        x += len(a) * 7.0 + 34
    s += text(48, 152, "unprivileged · owns nothing it was not given", DIM, 11, mono=True)

    for i in range(5):
        s += arrow(120 + i * 130, 168, 120 + i * 130, 196, TEAL, 1.3, op=".55")
    s += text(392, 188, "syscalls — the only way through", TEAL, 11, mono=True, mid=True)

    s += box(30, 200, 700, 78, stroke=TEAL, fill=PANEL2)
    s += text(48, 226, "the kernel — the only code that touches the metal", TEAL, 13, weight="600")
    s += text(48, 250, "scheduler · memory · filesystems · network stack · drivers · permissions", BONE, 12)
    s += text(48, 268, "decides, every single time, whether a process may do the thing it asked", DIM, 11)

    s += box(30, 292, 700, 44, stroke=DIM, fill=PANEL)
    s += text(48, 320, "hardware — CPU · RAM · SSD · NIC · GPIO", BONE, 13)

    s += text(30, 366, "permissions, read once and never forgotten:", BONE, 12)
    perms = [("600", "secrets — only you", EMBER), ("644", "ordinary files", DIM),
             ("755", "things that run", TEAL), ("root", "avoid; use sudo", GOLD)]
    x = 30
    for a, b, c in perms:
        s += chip(x, 378, a + "  " + b, c)
        x += len(a + b) * 7.0 + 40
    return s + tail()


def schedule_loop():
    s = head("making something happen without you — the four clocks")
    rows = [
        ("cron", "0 6 */2 * *", "simplest. no logs, minimal PATH, no overlap guard.", GOLD, 78),
        ("systemd timer", "OnCalendar=", "journald logs, dependencies, restart policy.", TEAL, 152),
        ("CI schedule", "GitHub Actions", "runs on someone else's metal. free, but queued.", BLUE, 226),
        ("event / webhook", "on: push", "not a clock at all — it fires when reality does.", EMBER, 300),
    ]
    for name, code, note, col, y in rows:
        s += box(30, y, 168, 58, stroke=col)
        s += text(114, y + 26, name, col, 13, mid=True, weight="600")
        s += text(114, y + 44, code, DIM, 11, mid=True, mono=True)
        s += arrow(198, y + 29, 232, y + 29, col, op=".6")
        s += text(244, y + 34, note, BONE, 12)
    s += box(30, 366, 700, 40, stroke=EMBER, fill=PANEL2)
    s += text(48, 392, "the bite everyone takes once: a cron job runs in UTC, with no shell profile "
                       "and no PATH.", BONE, 12)
    return s + tail()


def store_shapes():
    s = head("six shapes of memory — pick by the question you will ask")
    cells = [
        ("relational", "postgres · sqlite", "rows, joins, transactions", TEAL),
        ("document", "mongo · json fields", "one blob per thing", BLUE),
        ("key–value", "redis · kv", "one lookup, no thinking", GOLD),
        ("vector", "chroma · pgvector", "nearest by meaning", TEAL),
        ("queue", "nats · sqs", "work waiting its turn", EMBER),
        ("object", "s3 · disk", "big files, cheap, slow", DIM),
    ]
    for i, (name, tools, use, col) in enumerate(cells):
        x = 30 + (i % 3) * 236
        y = 76 + (i // 3) * 128
        s += box(x, y, 216, 108, stroke=col)
        s += text(x + 16, y + 30, name, col, 14, weight="600")
        s += text(x + 16, y + 54, tools, BONE, 12, mono=True)
        s += text(x + 16, y + 78, use, DIM, 12)
    s += box(30, 336, 700, 62, stroke=GOLD, fill=PANEL2)
    s += text(48, 362, "on one 10-watt node: postgres with pgvector is five of these six at once —", BONE, 12)
    s += text(48, 381, "rows, JSON, key–value, vectors and a queue. Reach for a second store when it hurts.", DIM, 12)
    return s + tail()


def backup_321():
    s = head("3-2-1-1-0 — the only backup rule that survives contact")
    rules = [
        ("3", "copies of anything you would grieve", GOLD),
        ("2", "different kinds of media", TEAL),
        ("1", "copy off-site", BLUE),
        ("1", "copy offline or immutable", EMBER),
        ("0", "errors on a restore you actually tested", BONE),
    ]
    y = 84
    for n, t, c in rules:
        s += ('  <circle cx="60" cy="%g" r="21" fill="none" stroke="%s" stroke-opacity=".75"/>\n' % (y + 4, c))
        s += text(60, y + 11, n, c, 18, mid=True, weight="600")
        s += text(100, y + 11, t, BONE, 14)
        y += 58
    s += line(60, 108, 60, 314, DIM, dash="3 6", op=".3")
    s += box(430, 76, 300, 176, stroke=EMBER, fill=PANEL2)
    s += text(450, 104, "why the last two exist", EMBER, 13, weight="600")
    s += text(450, 130, "modern ransomware finds the", BONE, 12)
    s += text(450, 148, "backups first and encrypts them", BONE, 12)
    s += text(450, 166, "too — a synced copy is not a", BONE, 12)
    s += text(450, 184, "backup, it is a second victim.", BONE, 12)
    s += text(450, 214, "an untested backup is a rumour.", EMBER, 12)
    s += text(450, 232, "restore one thing, monthly.", DIM, 12)
    s += box(30, 336, 700, 60, stroke=TEAL)
    s += text(48, 362, "on the node: nightly pg_dump → SSD, weekly encrypted copy off-site,", BONE, 12)
    s += text(48, 381, "monthly restore-into-a-container drill. Ten minutes buys the whole rule.", DIM, 12)
    return s + tail()


def cia_triad():
    s = head("the three questions every security decision answers")
    pts = [(392, 130), (176, 268), (608, 268)]
    labels = [
        ("confidentiality", "only the right eyes", GOLD),
        ("integrity", "unchanged, and provably so", TEAL),
        ("availability", "there when needed", EMBER),
    ]
    s += ('  <polygon points="%g,%g %g,%g %g,%g" fill="none" stroke="%s" '
          'stroke-opacity=".3" stroke-width="1.4"/>\n'
          % (pts[0][0], pts[0][1], pts[1][0], pts[1][1], pts[2][0], pts[2][1], DIM))
    for (x, y), (name, sub, col) in zip(pts, labels):
        s += '  <circle cx="%g" cy="%g" r="30" fill="%s" stroke="%s" stroke-opacity=".85"/>\n' % (x, y, PANEL2, col)
        if y < 200:
            s += text(x, y - 48, name, col, 14, mid=True, weight="600")
            s += text(x, y - 30, sub, DIM, 12, mid=True)
        else:
            s += text(x, y + 52, name, col, 14, mid=True, weight="600")
            s += text(x, y + 70, sub, DIM, 12, mid=True)
    s += text(392, 214, "every control", BONE, 13, mid=True)
    s += text(392, 234, "trades one for another", DIM, 12, mid=True)
    s += box(30, 362, 700, 44, stroke=GOLD, fill=PANEL2)
    s += text(48, 382, "harden it and availability falls; copy it about and confidentiality spreads.", BONE, 12)
    s += text(48, 399, "There is no maximum — only a balance you chose on purpose, and wrote down.", DIM, 12)
    return s + tail()


def attack_path():
    s = head("how intrusions actually go — and where the cheap stops are")
    steps = [
        ("get in", "phished password", EMBER),
        ("hold on", "a scheduled task", EMBER),
        ("look around", "who else can I be?", GOLD),
        ("move sideways", "flat network", GOLD),
        ("take / break", "exfil, then encrypt", EMBER),
    ]
    x = 30
    for i, (a, b, c) in enumerate(steps):
        s += box(x, 82, 124, 60, a, b, stroke=c)
        if i < 4:
            s += arrow(x + 124, 112, x + 138, 112, c, op=".7")
        x += 138
    stops = [
        ("passkeys", TEAL), ("EDR + logs", TEAL), ("least privilege", TEAL),
        ("segmentation", TEAL), ("offline backups", TEAL),
    ]
    x = 30
    for t, c in stops:
        s += line(x + 62, 142, x + 62, 176, c, dash="3 5", op=".5")
        s += chip(x + 62 - (len(t) * 7.0 + 22) / 2, 178, t, c)
        x += 138
    s += text(30, 244, "the shape of the lesson", GOLD, 14, weight="600")
    s += text(30, 270, "None of these five steps is clever. Four of the five are stopped by things", BONE, 12)
    s += text(30, 290, "that cost nothing: a passkey, a non-admin account, a flat network broken in", BONE, 12)
    s += text(30, 310, "two, and a backup the attacker cannot reach. Sophistication is rarely the story.", BONE, 12)
    s += box(30, 332, 700, 62, stroke=EMBER, fill=PANEL2)
    s += text(48, 358, "dwell time — how long they sit inside before anyone notices — is measured", BONE, 12)
    s += text(48, 377, "in days now, not months. Detection has improved; the front door has not.", DIM, 12)
    return s + tail()


def patch_priority():
    s = head("what to patch first — three numbers, one decision")
    cols = [
        ("CVSS", "how bad if used", "0 – 10 severity", "thousands score 9+", GOLD),
        ("EPSS", "will it be used", "probability, 30 days", "most 9s never are", TEAL),
        ("KEV", "already being used", "CISA's exploited list", "this one, tonight", EMBER),
    ]
    x = 30
    for name, q, what, note, col in cols:
        s += box(x, 78, 216, 152, stroke=col)
        s += text(x + 108, 108, name, col, 16, mid=True, weight="600")
        s += text(x + 108, 134, q, BONE, 13, mid=True)
        s += text(x + 108, 162, what, DIM, 11, mid=True, mono=True)
        s += line(x + 30, 180, x + 186, 180, col, op=".3")
        s += text(x + 108, 204, note, DIM, 12, mid=True)
        x += 236
    s += box(30, 252, 700, 74, stroke=TEAL, fill=PANEL2)
    s += text(48, 280, "the rule that keeps a one-person estate sane", TEAL, 13, weight="600")
    s += text(48, 304, "Patch everything on KEV now. Then anything with high EPSS. Severity alone is a", BONE, 12)
    s += text(48, 322, "queue you will never finish — and finishing it was never the point.", DIM, 12)
    s += text(30, 360, "and the unglamorous truth beneath all three:", GOLD, 12)
    s += text(30, 384, "unattended-upgrades on the node closes more real doors than any dashboard.", BONE, 12)
    return s + tail()


def risk_tiers():
    s = head("the eu ai act — sorted by harm, not by cleverness")
    tiers = [
        ("unacceptable", "banned outright — social scoring, manipulation", EMBER, 120, 78),
        ("high risk", "employment · credit · essential services · health", GOLD, 300, 128),
        ("limited risk", "chatbots, deepfakes — you must say what it is", TEAL, 480, 178),
        ("minimal risk", "everything else — no new duty", DIM, 660, 228),
    ]
    for name, note, col, w, y in tiers:
        x = 392 - w / 2
        s += box(x, y, w, 44, stroke=col, fill=PANEL2 if col != DIM else PANEL)
        s += text(392, y + 21, name, col, 13, mid=True, weight="600")
        s += text(392, y + 37, note, DIM, 10.5, mid=True)
    s += text(392, 296, "plus separate duties for general-purpose models themselves", BONE, 12, mid=True)
    s += box(30, 318, 700, 80, stroke=TEAL)
    s += text(48, 344, "what it means for a solo operator", TEAL, 13, weight="600")
    s += text(48, 368, "Almost everything you build lands in the bottom two tiers. The moment an agent", BONE, 12)
    s += text(48, 386, "touches hiring, credit or clinical care, the paperwork is the product.", DIM, 12)
    return s + tail()


def context_engineering():
    s = head("context engineering — the real skill behind the prompt")
    slots = [
        ("system", "who it is, what it may not do", GOLD),
        ("tools", "the verbs it is allowed", TEAL),
        ("retrieved facts", "only what this task needs", TEAL),
        ("the ask", "one task, stated once", GOLD),
        ("format", "the shape of the answer", BLUE),
    ]
    y = 76
    for name, note, col in slots:
        s += box(30, y, 420, 44, stroke=col)
        s += text(48, y + 27, name, col, 13, weight="600")
        s += text(180, y + 27, note, BONE, 12)
        y += 54
    s += line(456, 84, 456, 328, DIM, dash="3 6", op=".35")
    s += box(476, 76, 254, 128, stroke=EMBER, fill=PANEL2)
    s += text(494, 102, "what fails", EMBER, 13, weight="600")
    s += text(494, 126, "stuffing everything in", BONE, 12)
    s += text(494, 146, "the whole document", DIM, 12)
    s += text(494, 166, "ten tasks in one breath", DIM, 12)
    s += text(494, 186, "chat history nobody pruned", DIM, 12)
    s += box(476, 216, 254, 112, stroke=TEAL)
    s += text(494, 242, "what works", TEAL, 13, weight="600")
    s += text(494, 266, "less, but exactly right", BONE, 12)
    s += text(494, 286, "examples over adjectives", DIM, 12)
    s += text(494, 306, "a schema, not a plea", DIM, 12)
    s += box(30, 344, 700, 54, stroke=GOLD, fill=PANEL2)
    s += text(48, 368, "the window is a desk, not a warehouse. Everything you put on it competes for", BONE, 12)
    s += text(48, 386, "attention with everything else — including the instruction that mattered.", DIM, 12)
    return s + tail()


def eval_loop():
    s = head("the loop that turns opinion into evidence")
    ring = [
        (392, 96, "write the case", "input + what good looks like", GOLD),
        (628, 216, "run it", "same input, every version", TEAL),
        (392, 336, "score it", "rule, rubric, or human", TEAL),
        (156, 216, "change one thing", "prompt, model, retrieval", GOLD),
    ]
    for x, y, a, b, c in ring:
        s += box(x - 108, y - 32, 216, 64, a, b, stroke=c)
    s += arrow(500, 118, 570, 186, TEAL, op=".6")
    s += arrow(614, 262, 520, 322, TEAL, op=".6")
    s += arrow(284, 336, 214, 268, GOLD, op=".6")
    s += arrow(170, 174, 268, 116, GOLD, op=".6")
    s += text(392, 210, "no vibes", BONE, 15, mid=True, weight="600")
    s += text(392, 232, "survive this loop", DIM, 12, mid=True)
    s += box(30, 376, 700, 30, stroke=EMBER, fill=PANEL2, r=8)
    s += text(48, 396, "twenty cases beat a thousand opinions — and they run in CI while you sleep.", BONE, 12)
    return s + tail()


def modalities():
    s = head("one architecture, five senses — where models grew hands")
    mods = [
        ("text", "read & write", "the original", GOLD),
        ("vision", "see images, screens, scans", "VLM · OCR is solved", TEAL),
        ("audio", "hear & speak", "ASR · TTS · real-time voice", BLUE),
        ("video", "watch & predict", "world models, still young", TEAL),
        ("action", "move & operate", "VLA · robots · computer use", EMBER),
    ]
    y = 74
    for name, what, note, col in mods:
        s += box(30, y, 700, 56, stroke=col)
        s += text(52, y + 34, name, col, 15, weight="600")
        s += text(172, y + 34, what, BONE, 13)
        s += text(392, y + 34, note, DIM, 12)
        y += 66
    s += box(30, 404 - 30, 700, 26, stroke=DIM, fill=PANEL2, r=8)
    s += text(48, 392, "all five are tokens in the end — which is why one architecture ate every field.",
              BONE, 12)
    return s + tail()


def chip_chokepoint():
    s = head("the funnel every ai chip on earth passes through")
    stages = [
        ("sand → wafer", "many suppliers", 700, DIM),
        ("EUV lithography", "one company: ASML", 520, GOLD),
        ("leading-edge fab", "essentially TSMC", 360, GOLD),
        ("HBM stacks", "three suppliers", 240, EMBER),
        ("advanced packaging", "the actual bottleneck", 150, EMBER),
    ]
    y = 76
    for name, note, w, col in stages:
        x = 392 - w / 2
        s += box(x, y, w, 46, stroke=col, fill=PANEL2)
        s += text(392, y + 22, name, col, 13, mid=True, weight="600")
        s += text(392, y + 38, note, DIM, 10.5, mid=True)
        y += 56
    s += arrow(392, 352, 392, 372, EMBER)
    s += text(392, 392, "every frontier model you have ever used", BONE, 13, mid=True)
    s += text(50, 200, "export", GOLD, 12, mono=True)
    s += text(50, 218, "controls", GOLD, 12, mono=True)
    s += text(50, 236, "bite here", DIM, 11, mono=True)
    s += line(112, 214, 224, 214, GOLD, dash="3 5", op=".45")
    return s + tail()


def cost_shape():
    s = head("where the money actually goes — and which way it moves")
    s += box(30, 76, 340, 150, stroke=GOLD)
    s += text(48, 104, "training — capex", GOLD, 14, weight="600")
    s += text(48, 130, "paid once, enormous, rare", BONE, 12)
    s += text(48, 152, "tens of thousands of GPUs", DIM, 12)
    s += text(48, 172, "communication-bound, not FLOP-bound", DIM, 12)
    s += text(48, 200, "you will never do this", EMBER, 12)
    s += box(390, 76, 340, 150, stroke=TEAL)
    s += text(408, 104, "inference — opex", TEAL, 14, weight="600")
    s += text(408, 130, "paid per token, forever", BONE, 12)
    s += text(408, 152, "memory-bandwidth-bound", DIM, 12)
    s += text(408, 172, "falls ~10× a year at equal quality", DIM, 12)
    s += text(408, 200, "this is your entire bill", TEAL, 12)
    s += box(30, 244, 700, 76, stroke=BLUE, fill=PANEL2)
    s += text(48, 270, "the three levers a solo operator actually pulls", BLUE, 13, weight="600")
    s += text(48, 294, "route cheap models to easy work · cache the prompt prefix · run the boring", BONE, 12)
    s += text(48, 312, "volume locally, where the marginal cost of a token is electricity.", DIM, 12)
    s += box(30, 336, 700, 62, stroke=EMBER)
    s += text(48, 362, "and the trap: reasoning models spend output tokens to think. A 3× better answer", BONE, 12)
    s += text(48, 381, "can cost 30× — which is fine for a decision and ruinous for a loop.", DIM, 12)
    return s + tail()


# ---------- feed banners --------------------------------------------------
def banner(kind, title, sub, col, motif):
    w, h = 760, 200
    s = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
         'font-family="system-ui,-apple-system,sans-serif">\n'
         '  <rect width="%d" height="%d" fill="%s"/>\n' % (w, h, w, h, INK))
    # motif: drifting constellation tuned per domain
    import math
    for i in range(motif):
        a = (i / float(motif)) * 6.283
        x = 620 + math.cos(a * 2.3) * 92
        y = 100 + math.sin(a * 1.7) * 64
        r = 2 + (i % 4)
        s += '  <circle cx="%.1f" cy="%.1f" r="%d" fill="%s" fill-opacity="%.2f"/>\n' % (
            x, y, r, col, 0.25 + (i % 5) * 0.13)
        if i:
            px = 620 + math.cos((i - 1) / float(motif) * 6.283 * 2.3) * 92
            py = 100 + math.sin((i - 1) / float(motif) * 6.283 * 1.7) * 64
            s += ('  <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                  'stroke-opacity=".16"/>\n' % (px, py, x, y, col))
    s += '  <rect x="0" y="0" width="6" height="%d" fill="%s"/>\n' % (h, col)
    s += text(38, 62, kind.upper(), col, 12, mono=True)
    s += '  <text x="38" y="106" fill="%s" font-size="30" font-weight="600" ' \
         'font-family="Fraunces,Georgia,serif">%s</text>\n' % (BONE, esc(title))
    s += text(38, 140, sub, DIM, 14)
    s += text(38, 172, "the operator's codex · live feed · refreshed every two days", DIM, 11, mono=True, op=".7")
    return s + tail()


FIGURES = {
    "packet-journey.svg": packet_journey,
    "nat-tunnel.svg": nat_tunnel,
    "linux-anatomy.svg": linux_anatomy,
    "schedule-loop.svg": schedule_loop,
    "store-shapes.svg": store_shapes,
    "backup-321.svg": backup_321,
    "cia-triad.svg": cia_triad,
    "attack-path.svg": attack_path,
    "patch-priority.svg": patch_priority,
    "risk-tiers.svg": risk_tiers,
    "context-engineering.svg": context_engineering,
    "eval-loop.svg": eval_loop,
    "modalities.svg": modalities,
    "chip-chokepoint.svg": chip_chokepoint,
    "cost-shape.svg": cost_shape,
    "update-ai.svg": lambda: banner("artificial intelligence", "AI", "models, agents, and the tools around them", TEAL, 26),
    "update-it.svg": lambda: banner("information technology", "IT", "the plumbing everything else stands on", BLUE, 22),
    "update-hardware.svg": lambda: banner("hardware & silicon", "Hardware", "chips, boards, memory and the machines that print them", GOLD, 24),
    "update-cyber.svg": lambda: banner("cyber security", "Cyber", "what is being broken, and what stops it", EMBER, 20),
}


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, fn in FIGURES.items():
        path = os.path.join(OUT, name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(fn())
    print("make_figures: wrote %d figures to %s" % (len(FIGURES), OUT))


if __name__ == "__main__":
    main()
