#!/usr/bin/env bash
# Run from the repo root ON THE PI to report ecosystem progress to the live Codex.
# usage: ./pi/log-progress.sh L1 current "watcher migrated, first run clean"
#        states: pending | current | done
set -e
LVL="$1"; STATE="$2"; NOTE="${3:-}"
python3 - "$LVL" "$STATE" "$NOTE" << 'PY'
import json, sys, datetime
lvl, state, note = sys.argv[1], sys.argv[2], sys.argv[3]
d = json.load(open("node-log.json"))
d["ladder"][lvl] = state
if state == "current":
    d["level"] = lvl; d["status"] = note[:60] if note else "in progress"
if state == "done" and d.get("level") == lvl:
    d["status"] = "complete — next rung"
d["entries"].insert(0, {"date": datetime.date.today().isoformat(),
                        "note": f"[{lvl} {state}] {note}"})
json.dump(d, open("node-log.json", "w"), indent=2, ensure_ascii=False)
PY
git add node-log.json
git commit -m "node: $LVL $STATE"
git push
echo "logged: $LVL $STATE — live on the Codex in ~1 minute"
