#!/usr/bin/env python3
"""Compile NEXT.md — the stranger's front page, DERIVED from the artifacts that own the facts.

NOT A FOURTH HOME. The maptrail owns rulings, the methods thread owns reasoning, commits own sequence —
each fact in its right home, and this file duplicates none of them. It is the db pattern applied to the
to-do list: compiled, disposable, regenerable, and IF IT DISAGREES WITH ITS SOURCES, THE SOURCES ARE
RIGHT. Nothing may be written here that lives nowhere else, because a hand-edit would make it a place
where rulings hide.

WHY IT NEEDED AN OPENNESS SIGNAL FIRST. The trail records what happened, never what remains outstanding,
so "what is open" was an inference by a reader who knew the story. A generator over records that cannot
say what is open would be an inference layer wearing a compiler's clothes — so `open_item`/`discharge`
landed first and this reads their replay.
"""
import json, sqlite3, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from foundry.catalog import maptrail as M                                       # noqa: E402
from foundry.catalog import reservation as RES                                  # noqa: E402

LAT = ROOT / "foundry" / "results" / "lattice"
OUT = ROOT.parent / "NEXT.md"
TRAIL = LAT / "maptrail.jsonl"
DB = LAT / "observatory.db"


def state():
    if not DB.exists():
        return {}
    con = sqlite3.connect(DB)
    q = lambda s: con.execute(s).fetchone()[0]
    try:
        return {
            "problems": q("SELECT COUNT(*) FROM problems"),
            "catalog cells": q("SELECT COUNT(*) FROM catalog"),
            "frames": q("SELECT COUNT(*) FROM frames"),
            "frontier (reserved)": q("SELECT COUNT(*) FROM frontier WHERE released = 0"),
            "waves": q("SELECT COUNT(*) FROM waves"),
            "candidates enumerated": q("SELECT COUNT(*) FROM candidates"),
            "maptrail records": q("SELECT COUNT(*) FROM maptrail"),
            "descriptor version": q("SELECT descriptor_version FROM catalog LIMIT 1"),
        }
    finally:
        con.close()


# NO HEAD LINE, NO TIMESTAMP. A first version stamped `git log -1` into the page, which made it change
# whenever HEAD moved even though nothing in its SOURCES had — a derived view drifting for reasons
# unrelated to what it reports. Its own reproducibility test caught it. This is the loader's
# determinism law (no timestamps, no run ids, no environment capture) applied one layer up: the page
# is a pure function of the artifacts, and provenance belongs to the commit that carries the file.


def main() -> int:
    items = M.open_items(TRAIL)
    st = state()
    res = sorted(RES.reserved_rows(LAT / "observatory_reservation.jsonl"))

    L = ["# NEXT — what is open, compiled from the artifacts", "",
         "**This file is DERIVED. Do not edit it.** Regenerate with "
         "`python3 foundry/dev/build_next.py`.", "",
         "It duplicates no fact: the maptrail owns rulings, the methods thread owns reasoning, commits",
         "own sequence. If this page disagrees with its sources, **the sources are right.** Nothing may",
         "be recorded here that lives nowhere else — a hand-edit would make it a place where rulings",
         "hide, which is the failure it exists to prevent.", "",
         "This page carries no timestamp and no commit id: it is a pure function of its sources, so",
         "two compiles from the same artifacts are byte-identical. Provenance belongs to the commit",
         "that carries the file, not to a line inside it.", "",
         "---", "", "## Open work, in declared order", ""]

    for it in items:
        L.append(f"### {it.get('sequence')}. {it.get('title')}")
        L.append("")
        L.append(f"{it.get('why')}")
        L.append("")
        L.append(f"- key: `{it['opens']}`")
        for p in it.get("pointers") or []:
            L.append(f"- see: `{p}`")
        if it.get("reconstructed"):
            L.append("- *(opened by backfill — this item predates the openness signal)*")
        L.append("")

    L += ["---", "", "## State", ""]
    for k, v in st.items():
        L.append(f"- **{k}**: {v}")
    L += ["", f"- **reserved rows** ({len(res)}): " + ", ".join(f"`{r}`" for r in res), "",
          "---", "", "## How to close an item", "",
          "Discharge is a NEW maptrail record pointing at the original, never an edit — the same shape",
          "as the reservation ledger's reserve/release, so replay is the state:", "",
          "```python",
          "from foundry.catalog import maptrail as M",
          'M.discharge(TRAIL, "<item-key>", by="<commit or artifact>", note="...")',
          "```", "",
          "Then regenerate this file. An item vanishes from the page because the trail says it closed,",
          "never because someone deleted a line here.", ""]

    OUT.write_text("\n".join(L) + "\n")
    print(f"NEXT.md — {len(items)} open item(s), compiled from {TRAIL.name}")
    for it in items:
        print(f"   {it.get('sequence')}. {it.get('title')[:72]}")
    print(f"\n  wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
