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
HEATHER = "#b79ad8"          # the fifth feed domain — market & money
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


def render_path():
    s = head("html to pixels — the six steps behind every page")
    steps = [
        ("parse", "HTML → DOM tree", GOLD),
        ("style", "CSS → CSSOM", BLUE),
        ("layout", "where everything sits", TEAL),
        ("paint", "what colour each pixel is", TEAL),
        ("composite", "stack the layers", GOLD),
    ]
    x = 30
    for i, (a, b, c) in enumerate(steps):
        s += box(x, 78, 124, 62, a, "", stroke=c)
        s += wrap(x + 62, 152, b, 18, DIM, 11, 14, mid=True)
        if i < 4:
            s += arrow(x + 124, 109, x + 138, 109, c, op=".7")
        x += 138
    s += box(30, 200, 700, 74, stroke=EMBER, fill=PANEL2)
    s += text(48, 226, "the two that cost you", EMBER, 13, weight="600")
    s += text(48, 250, "Changing size or position redoes layout for everything after it (reflow).", BONE, 12)
    s += text(48, 268, "Changing only colour or opacity skips to paint — which is why animations", DIM, 12)
    s += text(48, 286, "should move transform and opacity, and nothing else.", DIM, 12)
    s += box(30, 306, 700, 76, stroke=TEAL)
    s += text(48, 332, "the blocking rule", TEAL, 13, weight="600")
    s += text(48, 356, "CSS blocks rendering; a plain <script> blocks parsing. Hence defer, async,", BONE, 12)
    s += text(48, 374, "and putting width/height on images so nothing jumps when they arrive.", DIM, 12)
    return s + tail()


def test_shape():
    s = head("what to test, how much, and what each kind catches")
    tiers = [
        ("end-to-end", "a real user path, start to finish", "few · slow · brittle", 240, EMBER, 78),
        ("integration", "two real parts actually talking", "some · medium", 420, GOLD, 148),
        ("unit", "one function, no world attached", "many · instant · cheap", 620, TEAL, 218),
    ]
    for name, what, cost, w, col, y in tiers:
        x = 392 - w / 2
        s += box(x, y, w, 58, stroke=col, fill=PANEL2)
        s += text(392, y + 25, name, col, 14, mid=True, weight="600")
        s += text(392, y + 44, what + "   ·   " + cost, DIM, 11.5, mid=True)
    s += box(30, 296, 700, 46, stroke=BLUE)
    s += text(48, 316, "the fourth kind nobody names: a test that reproduces the bug you just fixed.", BONE, 12)
    s += text(48, 334, "It is the only test guaranteed to be worth writing.", DIM, 12)
    s += box(30, 354, 700, 46, stroke=TEAL, fill=PANEL2)
    s += text(48, 374, "for agents, the pyramid inverts: the model is not deterministic, so the unit", BONE, 12)
    s += text(48, 392, "layer is thin and the eval set (Layer 21) does the heavy lifting.", DIM, 12)
    return s + tail()


def confusion():
    s = head("the four boxes every detector lives in")
    cells = [
        ("true positive", "caught it", 250, 88, TEAL),
        ("false positive", "cried wolf", 460, 88, GOLD),
        ("false negative", "missed it", 250, 168, EMBER),
        ("true negative", "correctly quiet", 460, 168, DIM),
    ]
    for name, sub, x, y, col in cells:
        s += box(x, y, 200, 72, stroke=col, fill=PANEL2)
        s += text(x + 100, y + 32, name, col, 13, mid=True, weight="600")
        s += text(x + 100, y + 52, sub, DIM, 11.5, mid=True)
    s += text(350, 76, "actually true", DIM, 11, mono=True, mid=True)
    s += text(560, 76, "actually false", DIM, 11, mono=True, mid=True)
    s += text(240, 128, "flagged", DIM, 11, mono=True, anchor="end")
    s += text(240, 208, "not flagged", DIM, 11, mono=True, anchor="end")
    s += text(30, 106, "precision", TEAL, 13, weight="600")
    s += wrap(30, 126, "of what you flagged, how much was real", 22, DIM, 11, 15)
    s += text(30, 176, "recall", EMBER, 13, weight="600")
    s += wrap(30, 196, "of what was real, how much you caught", 22, DIM, 11, 15)
    s += box(30, 264, 700, 62, stroke=GOLD, fill=PANEL2)
    s += text(48, 290, "you cannot have both — where you set the threshold trades one for the other,", BONE, 12)
    s += text(48, 308, "and which one matters depends entirely on the cost of each mistake.", DIM, 12)
    s += box(30, 340, 700, 60, stroke=EMBER)
    s += text(48, 366, "the base rate trap: at 1-in-1,000 prevalence, a 99%-accurate test flags", BONE, 12)
    s += text(48, 384, "ten false alarms for every real find. Accuracy alone is close to meaningless.", DIM, 12)
    return s + tail()


def cloud_shapes():
    s = head("three depths of rented computer — and who is left holding it")
    cols = [
        ("IaaS", "a bare machine", "you patch the OS,\nthe runtime, the app", GOLD),
        ("PaaS", "a place to put code", "they patch below,\nyou own the app", TEAL),
        ("SaaS", "finished software", "you own the config\nand the data only", BLUE),
    ]
    x = 30
    for name, what, who, col in cols:
        s += box(x, 78, 216, 150, stroke=col)
        s += text(x + 108, 110, name, col, 17, mid=True, weight="600")
        s += text(x + 108, 136, what, BONE, 12.5, mid=True)
        s += line(x + 30, 152, x + 186, 152, col, op=".3")
        for i, ln in enumerate(who.split("\n")):
            s += text(x + 108, 176 + i * 17, ln, DIM, 11.5, mid=True)
        x += 236
    s += text(30, 256, "the shared responsibility line moves — the liability does not", GOLD, 13, weight="600")
    s += box(30, 272, 700, 56, stroke=EMBER, fill=PANEL2)
    s += text(48, 296, "Whatever the provider secures, your data, your access control and your", BONE, 12)
    s += text(48, 314, "misconfiguration remain yours. Almost every cloud breach is that last one.", DIM, 12)
    s += box(30, 342, 700, 58, stroke=TEAL)
    s += text(48, 366, "the three bills that surprise people", TEAL, 13, weight="600")
    s += text(48, 388, "egress per gigabyte · an idle thing nobody turned off · logs charged by volume", BONE, 12)
    return s + tail()


def adoption_gap():
    s = head("everyone adopted — almost nobody shipped")
    s += text(30, 78, "organisations that say they use AI agents", DIM, 12)
    s += box(30, 88, 553, 48, stroke=TEAL, fill=PANEL2)
    s += text(48, 118, "79% — adopted", TEAL, 16, weight="600")
    s += line(583, 88, 583, 136, DIM, 1, "4 4", op=".35")

    s += text(30, 172, "organisations running agents in production, doing real work", DIM, 12)
    s += box(30, 182, 77, 48, stroke=GOLD, fill=PANEL2)
    s += text(40, 212, "11%", GOLD, 15, weight="600")
    s += line(107, 206, 570, 206, EMBER, 1, "5 5", op=".5")
    s += text(580, 200, "the gap", EMBER, 13, weight="600")
    s += text(580, 218, "is plumbing", DIM, 12)

    s += text(30, 268, "what stops the other 68% — cited blockers, largest first", BONE, 12)
    for i, (t, c) in enumerate([("integration with existing systems  ~46%", EMBER),
                                ("permissions, auth & data access", GOLD),
                                ("no evals, so nobody can prove it works", BLUE),
                                ("model capability", TEAL)]):
        s += chip(30 + (i % 2) * 366, 282 + (i // 2) * 34, t, c, 350)

    s += box(30, 352, 700, 52, stroke=GOLD, fill=PANEL2)
    s += text(48, 376, "None of the blockers are intelligence. They are auth, permissions, evals, rollback —", BONE, 12)
    s += text(48, 394, "which is why a solo operator with working plumbing is ahead of most enterprises.", DIM, 12)
    return s + tail()


def commit_vs_push():
    s = head("committed is saved · pushed is safe")
    s += ('  <rect x="30" y="76" width="392" height="188" rx="10" fill="%s" stroke="%s" '
          'stroke-opacity=".7" stroke-dasharray="6 5"/>\n' % (PANEL, EMBER))
    s += text(48, 100, "the session's workshop — disposable", EMBER, 13, weight="600")
    s += box(48, 118, 150, 56, "your edits", "in the working tree", stroke=DIM)
    s += arrow(198, 146, 246, 146, GOLD)
    s += text(222, 138, "commit", GOLD, 10, mid=True, mono=True)
    s += box(246, 118, 156, 56, "8aa47a0", "saved — but only here", stroke=GOLD)
    s += text(48, 202, "close the session and this whole box is shredded:", BONE, 12)
    s += text(48, 222, "the commit that never left never existed.", EMBER, 12, weight="600")
    s += text(48, 246, "\"one thing goes with the container: 8aa47a0 is unpushed\"", DIM, 11, mono=True)

    s += arrow(422, 146, 486, 146, TEAL, 2)
    s += text(454, 136, "git push", TEAL, 11, mid=True, mono=True)
    s += text(454, 172, "~10 s", DIM, 11, mid=True, mono=True)
    s += box(486, 76, 244, 188, stroke=TEAL, fill=PANEL2)
    s += text(504, 104, "GitHub · origin/main", TEAL, 13, weight="600")
    s += text(504, 132, "durable", BONE, 12)
    s += text(504, 152, "shared with your other agents", DIM, 12)
    s += text(504, 172, "survives every container", DIM, 12)
    s += text(504, 206, "branches are free —", BONE, 12)
    s += text(504, 224, "park a backup/ branch", DIM, 12)
    s += text(504, 242, "before any history surgery", DIM, 12)

    s += box(30, 286, 700, 58, stroke=GOLD, fill=PANEL2)
    s += text(48, 310, "the reflex worth building", GOLD, 13, weight="600")
    s += text(48, 332, "Say \"push\" before you say anything else. Ten seconds beats an afternoon of work.", BONE, 12)
    s += text(30, 378, "the same shape underneath: ephemeral compute · shared state · stale notes · default-deny egress · metered everything", DIM, 11, mono=True)
    return s + tail()


def caretaker_loop():
    s = head("the caretaker — one sweep, every two days")
    steps = [
        ("wake", "0 6 */2 * *", GOLD),
        ("search", "the watchlist", BLUE),
        ("write", "feed · layer 04", TEAL),
        ("commit", "one dated entry", TEAL),
        ("redeploy", "same link, fresh", GOLD),
    ]
    x = 30
    for i, (a, b, c) in enumerate(steps):
        s += box(x, 92, 122, 62, a, b, stroke=c)
        if i < 4:
            s += arrow(x + 122, 123, x + 140, 123, c)
        x += 140
    s += line(691, 154, 691, 186, GOLD, 1.2, "4 4", op=".5")
    s += line(691, 186, 91, 186, GOLD, 1.2, "4 4", op=".5")
    s += arrow(91, 186, 91, 156, GOLD, 1.2)
    s += text(392, 204, "and the page under your home-screen link is newer than when you looked", DIM, 11, mid=True, mono=True)

    s += box(30, 226, 340, 122, stroke=TEAL, fill=PANEL2)
    s += text(48, 252, "what one sweep may change", TEAL, 13, weight="600")
    s += text(48, 276, "append to the live feed (never edit, never delete)", BONE, 11.5)
    s += text(48, 296, "replace the Frontier layer between its markers", BONE, 11.5)
    s += text(48, 316, "append one dated changelog entry", BONE, 11.5)
    s += text(48, 336, "mark a touched card newly updated", BONE, 11.5)

    s += box(390, 226, 340, 122, stroke=EMBER, fill=PANEL2)
    s += text(408, 252, "what it may never do", EMBER, 13, weight="600")
    s += text(408, 276, "delete a feed entry or remove a layer", BONE, 11.5)
    s += text(408, 296, "touch any layer outside the markers", BONE, 11.5)
    s += text(408, 316, "invent a fact — unverified is written as such", BONE, 11.5)
    s += text(408, 336, "half-finish: any error at all writes nothing", BONE, 11.5)

    s += text(30, 382, "a bad run can only ever be a no-op — which is why the loop is allowed to run unattended", GOLD, 12)
    return s + tail()


def graveyard_test():
    s = head("the graveyard test — apply it to your own idea")
    s += text(392, 74, "does the next model release make this stronger, or redundant?", BONE, 14, mid=True, weight="600")
    s += box(30, 96, 340, 220, stroke=EMBER)
    s += text(48, 124, "redundant — absorbed by the next release", EMBER, 12.5, weight="600")
    dead = ["\"prompt engineer\" as a job title", "thin wrappers around someone else's model",
            "AI-text detectors (never worked, still sold)", "fine-tune a model per company",
            "the vector-database gold rush", "\"bigger models are all you need\"",
            "chatbots as the product"]
    for i, d in enumerate(dead):
        s += text(48, 152 + i * 22, "·  " + d, DIM, 11.5)

    s += box(390, 96, 340, 220, stroke=TEAL)
    s += text(408, 124, "stronger — compounds with every release", TEAL, 12.5, weight="600")
    alive = ["data only you have", "evals only you wrote", "distribution — the people who trust you",
             "the domain workflow you actually know", "judgement about what to automate",
             "reliability: auth, rollback, audit trail", "a node you own outright"]
    for i, a in enumerate(alive):
        s += text(408, 152 + i * 22, "·  " + a, BONE, 11.5)

    s += box(30, 332, 700, 68, stroke=GOLD, fill=PANEL2)
    s += text(48, 358, "early is not the same as wrong", GOLD, 13, weight="600")
    s += text(48, 380, "2023's autonomous-agent toys looped in circles. The idea was right; the reliability wasn't.", BONE, 12)
    return s + tail()


def paradigm_pivots():
    s = head("how the thinking turned — and where you came in")
    y = 150
    s += line(50, y, 720, y, DIM, 1.2, op=".35")
    stops = [
        ("hand-written rules", "experts wrote every rule", "pre-2012", DIM),
        ("learn from examples", "the deep-learning turn", "2012", BLUE),
        ("one giant model, steered", "pretrain, then align", "2018–23", TEAL),
        ("make it think longer", "reasoning at answer-time", "2024–25", GOLD),
        ("wire it into real systems", "the integration era", "2025–26", EMBER),
    ]
    for i, (name, sub, when, c) in enumerate(stops):
        x = 74 + i * 154
        s += '  <circle cx="%g" cy="%g" r="9" fill="%s" stroke="%s"/>\n' % (x, y, PANEL2, c)
        s += text(x, y - 30, when, c, 11.5, mid=True, mono=True)
        s += wrap(x, y + 34, name, 17, BONE, 12, 15, mid=True)
        s += wrap(x, y + 74, sub, 20, DIM, 11, 14, mid=True)
    s += text(686, y - 52, "you are here", EMBER, 12, mid=True, weight="600")
    s += line(686, y - 44, 686, y - 40, EMBER, 1.2, op=".6")

    s += box(30, 250, 700, 72, stroke=GOLD, fill=PANEL2)
    s += text(48, 274, "the craft pivoted with it", GOLD, 13, weight="600")
    s += text(48, 296, "clever prompts → curated context   ·   impressive demos → boring evals", DIM, 11.5)
    s += text(48, 314, "\"which model is smartest\" → \"who can wire one into a real system safely\"", BONE, 11.5)

    s += box(30, 330, 700, 70, stroke=TEAL)
    s += text(48, 356, "the frontier question changed shape", TEAL, 13, weight="600")
    s += text(48, 378, "from \"can it?\" to \"can it be trusted, audited and afforded — repeatedly?\"", BONE, 12)
    return s + tail()


def leak_paths():
    s = head("five ways a secret leaves the building")
    rows = [
        ("staff paste it into an unapproved chatbot", "biggest by volume", "an approved tool that is actually good", TEAL),
        ("a webpage hides instructions your agent obeys", "indirect injection", "egress allowlist · least-privilege tools", GOLD),
        ("the model repeats a fragment of its training", "extraction", "never train on what you cannot publish", BLUE),
        ("patient interrogation lifts the system prompt", "prompt & key disclosure", "keys never live in the prompt", EMBER),
        ("a key is committed to a repo", "history remembers forever", "secret scanning · short-lived scoped tokens", TEAL),
    ]
    s += text(30, 76, "the route out", DIM, 11.5, mono=True)
    s += text(430, 76, "the control that closes it", DIM, 11.5, mono=True)
    for i, (route, kind, fix, c) in enumerate(rows):
        y = 92 + i * 54
        s += box(30, y, 350, 44, stroke=c)
        s += text(44, y + 20, route, BONE, 11.5)
        s += text(44, y + 36, kind, c, 10.5, mono=True)
        s += arrow(382, y + 22, 424, y + 22, c, 1.4)
        s += box(430, y, 300, 44, stroke=DIM)
        s += wrap(444, y + 20, fix, 42, DIM, 11.5, 15)

    s += box(30, 366, 700, 40, stroke=GOLD, fill=PANEL2)
    s += text(48, 392, "Notice the pattern: every leak is words tricking a word-machine, or humans being human.", BONE, 12)
    return s + tail()


def neural_estate():
    s = head("your repos as one organism — the vocabulary, mapped")
    nodes = [(96, 108, "bennyz"), (222, 92, "shift-watcher"), (96, 200, "thiri"), (232, 196, "second-brain")]
    for x, y, name in nodes:
        s += '  <circle cx="%g" cy="%g" r="26" fill="%s" stroke="%s" stroke-opacity=".8"/>\n' % (x, y, PANEL2, TEAL)
        s += text(x, y + 46, name, DIM, 10.5, mid=True, mono=True)
    for x, y, _ in nodes:
        s += line(x, y, 178, 288, TEAL, 1, "3 4", op=".45")
    s += box(108, 268, 140, 46, "the Pi", "always on", stroke=GOLD)
    s += text(178, 340, "brainstem · reflexes", GOLD, 10.5, mid=True, mono=True)
    s += text(178, 362, "£366 · ~10 watts", DIM, 10.5, mid=True, mono=True)

    pairs = [("neuron", "a repo", TEAL), ("firing", "an event it emits", TEAL),
             ("axon", "webhook / repository_dispatch", BLUE),
             ("brainstem", "the Pi — always on, runs the reflexes", GOLD),
             ("connectome", "the shared vector store, where traces live", BLUE),
             ("sleep", "the nightly job that consolidates the day", EMBER)]
    s += text(360, 78, "the metaphor, and the engineering underneath it", DIM, 11.5, mono=True)
    for i, (a, b, c) in enumerate(pairs):
        y = 106 + i * 30
        s += text(360, y, a, c, 12.5, weight="600")
        s += text(452, y, b, BONE, 11.5)
    s += text(360, 300, "engineering name: event-driven architecture", DIM, 11.5, mono=True)
    s += text(360, 320, "with choreography — standard practice.", DIM, 11.5, mono=True)

    s += box(30, 356, 700, 48, stroke=GOLD, fill=PANEL2)
    s += text(48, 380, "v0.1 is one synapse: shift-watcher fires → second-brain logs it → Telegram tells you.", BONE, 12)
    s += text(48, 398, "Build one synapse before dreaming the whole brain. That is also how brains did it.", DIM, 12)
    return s + tail()


def node_ladder():
    W2, H2 = 760, 460
    s = head("the ladder — the box never changes, its responsibility does", W2, H2)
    rungs = [
        ("L0", "first light", "reachable, safe, yours", DIM),
        ("L1", "the proving week", "one unattended job for 7 days", BLUE),
        ("L2", "the orchestrator", "it directs rented intelligence", TEAL),
        ("L3", "Meera's body", "one memory every project reads", TEAL),
        ("L4", "the local mind", "private inference, free per use", GOLD),
        ("L5", "the conglomerate", "operations dept of 3 businesses", EMBER),
    ]
    base, step_w, rise = 394, 118, 38
    for i, (lv, name, sub, c) in enumerate(rungs):
        x = 30 + i * step_w
        h = 44 + i * rise
        y = base - h
        s += box(x, y, 108, h, stroke=c, fill=PANEL2 if i else PANEL)
        s += text(x + 54, base - 16, lv, c, 15, mid=True, weight="600", mono=True)
        # the label sits above its own rung, so short rungs never overflow
        s += wrap(x + 54, y - 56, name, 17, BONE, 11.5, 14, mid=True)
        s += wrap(x + 54, y - 30, sub, 18, DIM, 10.5, 13, mid=True)
    s += line(30, base + 4, 730, base + 4, DIM, 1, op=".3")
    s += text(30, base + 30, "watts at every rung: about ten", GOLD, 12)
    s += text(392, base + 30, "what changes is trust, not hardware", BONE, 12, mid=True)
    s += text(730, base + 30, "headcount: zero", EMBER, 12, anchor="end")
    s += text(30, 76, "each rung is only allowed to start once the one below it has run boringly for a week", DIM, 11.5, mono=True)
    return s + tail()


def pi_grafts():
    W2, H2 = 760, 460
    s = head("the pi 5 is not an appliance — it is a socket", W2, H2)
    s += box(276, 176, 208, 118, stroke=GOLD, fill=PANEL2)
    s += text(380, 212, "Raspberry Pi 5 · 16GB", GOLD, 13, mid=True, weight="600")
    s += text(380, 236, "the exposed PCIe lane", BONE, 12, mid=True)
    s += text(380, 258, "first Pi to offer its spine", DIM, 11, mid=True)
    s += text(380, 274, "to strangers", DIM, 11, mid=True)

    grafts = [
        (30, 78, "G1 · NVMe spine", "M.2 HAT+ — storage stops being the bottleneck", TEAL, 1),
        (500, 78, "G2 · silicon retina", "Hailo 26 TOPS — camera brains, NOT chat models", TEAL, 1),
        (30, 180, "G3 · new senses", "mic · SDR · LoRa · mmWave · air quality", BLUE, 1),
        (500, 180, "G4 · borrowed brain", "llama.cpp RPC — the house pools its RAM", BLUE, 1),
        (30, 300, "G5 · brainstem + cortex", "Wake-on-LAN a mini PC only for hard thoughts", GOLD, 1),
        (500, 300, "G6 · the forbidden graft", "eGPU over Oculink — warranty-void, patched kernels", EMBER, 0),
    ]
    for x, y, name, what, c, solid in grafts:
        if solid:
            s += box(x, y, 230, 76, stroke=c)
        else:
            s += ('  <rect x="%g" y="%g" width="230" height="76" rx="9" fill="%s" stroke="%s" '
                  'stroke-opacity=".7" stroke-dasharray="5 4"/>\n' % (x, y, PANEL, c))
        s += text(x + 14, y + 28, name, c, 12.5, weight="600")
        s += wrap(x + 14, y + 48, what, 34, DIM, 11, 14)
        if x < 276:
            s += arrow(260, y + 38, 274, 216 if y > 200 else 200, c, 1.3, op=".55")
        else:
            s += arrow(498, y + 38, 486, 216 if y > 200 else 200, c, 1.3, op=".55")

    s += box(30, 396, 700, 48, stroke=GOLD, fill=PANEL2)
    s += text(48, 420, "survival organs first: a UPS HAT so a power cut is a journal entry instead of amnesia,", BONE, 12)
    s += text(48, 438, "and the RTC battery (pennies) so the node keeps true time offline. Boring grafts matter first.", DIM, 12)
    return s + tail()


def coherence_stack():
    s = head("why editing a header fools nobody — the floors beneath the text")
    floors = [
        ("what you edited", "User-Agent: Mozilla/5.0 …", "one line of text, free to change", EMBER),
        ("HTTP/2 frames", "header order · settings · window sizes", "chosen by your library, not by you", GOLD),
        ("the TLS hello", "cipher list · extensions · curves · GREASE", "sent in the clear, before any header", TEAL),
        ("TCP / IP", "TTL · timestamps · the return address", "the network's own accent", BLUE),
    ]
    y = 72
    for i, (name, detail, note, c) in enumerate(floors):
        h = 74 if i == 2 else 56

        s += box(30, y, 700, h, stroke=c, fill=PANEL2 if i == 2 else PANEL)
        s += text(48, y + 24, name, c, 12.5, weight="600")
        s += text(190, y + 24, detail, BONE, 11.5, mono=True)
        s += text(190, y + 43, note, DIM, 11)
        if i == 0:
            s += text(714, y + 24, "the only floor you can edit  ✎", EMBER, 11, anchor="end")
        if i == 2:
            s += text(190, y + 63, "the firewall reads this floor first — before a single header exists",
                      TEAL, 11.5, weight="600")
        y += h + 8

    s += box(30, 348, 700, 56, stroke=GOLD, fill=PANEL2)
    s += text(48, 372, "detection wins on coherence, not on a better hash", GOLD, 13, weight="600")
    s += text(48, 394, "A browser's four floors agree with each other. A script wearing a browser's hat does not.", BONE, 12)
    return s + tail()


def four_pillars():
    s = head("the four floors beneath the map — two to study, two to build")
    cols = [
        ("Pillar 1", "the network floor", "JA3/JA4 — the handshake\ntell, one floor below\nthe headers you edit", "study", TEAL),
        ("Pillar 2", "the IP layer", "datacentre vs residential\nvs mobile — and why\nreputation collapses", "study", BLUE),
        ("Pillar 3", "searchable memory", "a vector store on the\nSSD: facts you own,\nretrieved by meaning", "build", GOLD),
        ("Pillar 4", "the right always-on", "not serverless, not a\nlaptop — a box with no\ntimeout, no cold start", "build", EMBER),
    ]
    x = 30
    for tag, name, body, mode, c in cols:
        s += box(x, 76, 166, 196, stroke=c)
        s += text(x + 14, 104, tag, c, 11.5, mono=True)
        s += wrap(x + 14, 130, name, 18, BONE, 13, 17)
        for i, ln in enumerate(body.split("\n")):
            s += text(x + 14, 178 + i * 17, ln, DIM, 11)
        s += chip(x + 14, 234, mode, c, 74)
        x += 178

    s += box(30, 292, 700, 52, stroke=GOLD, fill=PANEL2)
    s += text(48, 316, "Pillars 1 and 2 you study so you can read a defence honestly — and so you never mistake", BONE, 12)
    s += text(48, 334, "a spoofed header for anonymity. Pillars 3 and 4 you build; both are already in your hands.", DIM, 12)
    s += box(30, 356, 700, 46, stroke=TEAL)
    s += text(48, 384, "the 10-second wall is why: serverless dies mid-job, the edge forgets, the Pi just keeps going.", BONE, 12)
    return s + tail()


def secret_ladder():
    s = head("where a key lives — worst to best")
    rungs = [
        ("hardcoded in the code", "in git history forever · travels with every clone and fork", EMBER),
        ("a .env file on the box", "out of the repo — but readable by anything that gets on the box", GOLD),
        ("platform env vars / secret manager", "injected at start · never committed · rotatable in one place", TEAL),
        ("short-lived scoped token, minted per job", "expires before it can be traded · scoped to one task", TEAL),
    ]
    for i, (name, why, c) in enumerate(rungs):
        y = 280 - i * 62
        s += box(30, y, 470, 52, stroke=c, fill=PANEL2 if i == 3 else PANEL)
        s += text(46, y + 22, name, c, 12.5, weight="600")
        s += text(46, y + 40, why, DIM, 11)
        s += text(512, y + 32, ("worst" if i == 0 else "better" if i == 1 else "good" if i == 2 else "best"),
                  c, 11.5, mono=True)
    s += arrow(586, 288, 586, 84, TEAL, 1.4, op=".6")
    s += text(600, 190, "each rung shortens", BONE, 11.5)
    s += text(600, 208, "the blast radius of", DIM, 11.5)
    s += text(600, 226, "one leaked string", DIM, 11.5)

    s += box(30, 342, 700, 60, stroke=GOLD, fill=PANEL2)
    s += text(48, 366, "the kettle and the plug socket", GOLD, 13, weight="600")
    s += text(48, 388, "The same kettle works in Sheffield and Kottayam — only the socket changes. Rotate on the day someone leaves.", BONE, 11.5)
    return s + tail()


def idor():
    s = head("the bug behind most \"hacks\" — signed in, never checked")
    s += text(30, 76, "your own request", TEAL, 12.5, weight="600")
    s += box(30, 92, 300, 52, stroke=TEAL)
    s += text(46, 116, "GET /api/orders/1041", BONE, 12.5, mono=True)
    s += text(46, 134, "Authorization: your token", DIM, 11, mono=True)
    s += arrow(330, 118, 372, 118, TEAL)
    s += box(372, 84, 178, 68, stroke=DIM, fill=PANEL2)
    s += text(461, 108, "signed in?  yes", TEAL, 12, mid=True, mono=True)
    s += text(461, 130, "is it yours?  not asked", EMBER, 12, mid=True, mono=True)
    s += arrow(550, 118, 592, 118, TEAL)
    s += text(600, 122, "your order", BONE, 12)

    s += text(30, 194, "the same request with one digit changed", EMBER, 12.5, weight="600")
    s += box(30, 210, 300, 52, stroke=EMBER)
    s += text(46, 234, "GET /api/orders/1042", BONE, 12.5, mono=True)
    s += text(46, 252, "Authorization: your token", DIM, 11, mono=True)
    s += arrow(330, 236, 372, 236, EMBER)
    s += box(372, 202, 178, 68, stroke=DIM, fill=PANEL2)
    s += text(461, 226, "signed in?  yes", TEAL, 12, mid=True, mono=True)
    s += text(461, 248, "is it yours?  still not", EMBER, 12, mid=True, mono=True)
    s += arrow(550, 236, 592, 236, EMBER)
    s += text(600, 232, "somebody", EMBER, 12)
    s += text(600, 250, "else's order", EMBER, 12)

    s += box(30, 292, 340, 108, stroke=BLUE)
    s += text(48, 318, "two different questions", BLUE, 13, weight="600")
    s += text(48, 342, "authentication — who are you?", BONE, 11.5)
    s += text(48, 362, "authorisation — what may you touch?", BONE, 11.5)
    s += text(48, 384, "most systems ask the first and assume the second", DIM, 11)

    s += box(390, 292, 340, 108, stroke=TEAL, fill=PANEL2)
    s += text(408, 318, "the fix is usually one clause", TEAL, 13, weight="600")
    s += text(408, 342, "…WHERE id = 1042 AND owner = caller", BONE, 11.5, mono=True)
    s += text(408, 366, "scope every read and write by the caller —", DIM, 11.5)
    s += text(408, 386, "and log the ones that come back empty.", DIM, 11.5)
    return s + tail()


def breach_clock():
    s = head("the 72-hour clock — it starts when you become aware")
    s += line(60, 150, 700, 150, DIM, 1.2, op=".35")
    stops = [
        ("hour 0", "you become aware", "a log, a report, a stranger's email", EMBER),
        ("hours 1–24", "assess", "whose data · what risk to them", GOLD),
        ("by hour 72", "tell the regulator", "even if the picture is incomplete", TEAL),
        ("without delay", "tell the people", "if the risk to them is high", BLUE),
    ]
    for i, (when, what, detail, c) in enumerate(stops):
        x = 110 + i * 180
        s += '  <circle cx="%g" cy="%g" r="9" fill="%s" stroke="%s"/>\n' % (x, 150, PANEL2, c)
        s += text(x, 122, when, c, 11.5, mid=True, mono=True)
        s += wrap(x, 184, what, 18, BONE, 12.5, 15, mid=True)
        s += wrap(x, 210, detail, 22, DIM, 11, 14, mid=True)

    s += box(30, 254, 340, 92, stroke=EMBER)
    s += text(48, 280, "why the clock is brutal", EMBER, 13, weight="600")
    s += text(48, 304, "It runs from awareness, not from", BONE, 11.5)
    s += text(48, 322, "understanding. A partial report on time", BONE, 11.5)
    s += text(48, 340, "beats a complete one on day five.", DIM, 11.5)

    s += box(390, 254, 340, 92, stroke=TEAL, fill=PANEL2)
    s += text(408, 280, "what makes it survivable", TEAL, 13, weight="600")
    s += text(408, 304, "an audit trail written before the day", BONE, 11.5)
    s += text(408, 322, "you need it: what happened, in what", BONE, 11.5)
    s += text(408, 340, "order, and who or what did it.", DIM, 11.5)

    s += text(30, 380, "If you can answer that in minutes you have a problem. If you cannot, you have a crisis —", BONE, 12)
    s += text(30, 400, "because now you must assume the worst about everything you cannot account for.", DIM, 12)
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
    "render-path.svg": render_path,
    "test-shape.svg": test_shape,
    "confusion.svg": confusion,
    "cloud-shapes.svg": cloud_shapes,
    "adoption-gap.svg": adoption_gap,
    "commit-vs-push.svg": commit_vs_push,
    "caretaker-loop.svg": caretaker_loop,
    "graveyard-test.svg": graveyard_test,
    "paradigm-pivots.svg": paradigm_pivots,
    "leak-paths.svg": leak_paths,
    "neural-estate.svg": neural_estate,
    "node-ladder.svg": node_ladder,
    "pi-grafts.svg": pi_grafts,
    "coherence-stack.svg": coherence_stack,
    "four-pillars.svg": four_pillars,
    "secret-ladder.svg": secret_ladder,
    "idor.svg": idor,
    "breach-clock.svg": breach_clock,
    "update-ai.svg": lambda: banner("artificial intelligence", "AI", "models, agents, and the tools around them", TEAL, 26),
    "update-it.svg": lambda: banner("information technology", "IT", "the plumbing everything else stands on", BLUE, 22),
    "update-hardware.svg": lambda: banner("hardware & silicon", "Hardware", "chips, boards, memory and the machines that print them", GOLD, 24),
    "update-cyber.svg": lambda: banner("cyber security", "Cyber", "what is being broken, and what stops it", EMBER, 20),
    "update-market.svg": lambda: banner("market & money", "Markets", "who is paying, what it costs, and where the money moved", HEATHER, 23),
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
