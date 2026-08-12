"""The conductor — the repo organism's bloodstream.

Your repositories are organs in jars; this organ reads all of them nightly
and cross-pollinates: a utility in one proposed to another, a bug pattern in
one becoming a test in all, a parked idea surfacing where the hands to build
it now exist.

Run on the Pi (where `gh` is authenticated), nightly by cron:

  python organs/conductor.py --config ../neuron.toml           # dry-run
  python organs/conductor.py --config ../neuron.toml --emit    # thoughts on bus
  python organs/conductor.py --config ../neuron.toml --open-prs

Etiquette, enforced here: proposals are draft PRs, never merges; one PR per
idea; silence when there is nothing to say.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tomllib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from nrn.bus import Bus                     # noqa: E402
from nrn.protocol import Thought            # noqa: E402


def gh(*args: str) -> str:
    return subprocess.run(["gh", *args], capture_output=True, text=True,
                          check=True).stdout


def collect(repo: str) -> dict:
    """One repo's vital signs: commits, issues, TODOs, failing runs."""
    signs = {"repo": repo}
    signs["commits"] = gh("api", f"repos/{repo}/commits?per_page=10",
                          "--jq", "[.[].commit.message]")
    signs["issues"] = gh("api", f"repos/{repo}/issues?state=open&per_page=20",
                         "--jq", "[.[] | {title, body}]")
    signs["failed_runs"] = gh("api",
                              f"repos/{repo}/actions/runs?status=failure&per_page=5",
                              "--jq", "[.workflow_runs[].name]")
    # TODO(next): grep the tree for TODO/FIXME markers via the git trees API,
    # and pull each repo's README so the model knows what each organ is *for*.
    return signs


def think(organism: list[dict]) -> list[dict]:
    """One prompt over the whole organism -> a list of proposals.

    TODO(next): call a mind here. Options, in order of frugality:
      - `claude -p` if the Claude CLI is on the Pi
      - the API via nrn.mind.ClaudeMind
      - OllamaMind for a free (weaker) nightly pass
    The prompt to write: "Here are N repos' vital signs. Propose at most
    three cross-pollinations: something one repo has that another needs.
    For each: {from_repo, to_repo, title, rationale, sketch}. Say NOTHING
    if nothing is genuinely worth a PR."
    """
    print(json.dumps(organism, indent=2)[:2000])
    return []  # honest until the mind is wired


def emit(proposals: list[dict], cfg: dict) -> None:
    bus = Bus(cfg["name"] + "-conductor", cfg.get("broker", "localhost"))
    bus.run_background()
    for p in proposals:
        bus.emit(Thought(kind="proposal", origin=bus.name,
                         content=f"[{p['from_repo']} -> {p['to_repo']}] "
                                 f"{p['title']}: {p['rationale']}"))


def open_prs(proposals: list[dict]) -> None:
    for p in proposals:
        # TODO(next): branch, apply the sketch, push, then:
        # gh("pr", "create", "--repo", p["to_repo"], "--draft",
        #    "--title", p["title"], "--label", "cross-pollination",
        #    "--body", p["rationale"])
        print(f"would open draft PR on {p['to_repo']}: {p['title']}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="neuron.toml")
    ap.add_argument("--emit", action="store_true")
    ap.add_argument("--open-prs", action="store_true")
    args = ap.parse_args()
    with open(args.config, "rb") as f:
        cfg = tomllib.load(f)

    repos = cfg.get("conductor", {}).get("repos", [])
    if not repos:
        sys.exit("add repos to [conductor] in neuron.toml, e.g. "
                 'repos = ["bennyzrealty-sys/codex"]')

    organism = [collect(r) for r in repos]
    proposals = think(organism)
    if not proposals:
        print("nothing worth proposing tonight — correct silence")
        return
    if args.emit:
        emit(proposals, cfg)
    if args.open_prs:
        open_prs(proposals)


if __name__ == "__main__":
    main()
