"""NEXT.md — the stranger's front page, DERIVED from the artifacts that own the facts.

NOT A FOURTH HOME. The maptrail owns rulings, the methods thread owns reasoning, commits own sequence —
each fact in its right home, and this page duplicates none of them. It is the db pattern applied to the
to-do list: compiled, disposable, regenerable, and IF IT DISAGREES WITH ITS SOURCES, THE SOURCES ARE
RIGHT. Nothing may be written here that lives nowhere else, because a hand-edit would make it a place
where rulings hide.

LIFTED OUT OF `dev/` (2026-07-28) so the page is compiled by the library rather than by a script. The
dev entry point survives as a shim, because a test and a habit both point at it and neither is worth
breaking to make a point.

NO TIMESTAMP, NO COMMIT ID. A first version stamped `git log -1` into the page, which made it change
whenever HEAD moved even though nothing in its SOURCES had — a derived view drifting for reasons
unrelated to what it reports. Its own reproducibility test caught it.

IT NOW RECORDS ITS SOURCES, WHICH IT DID NOT BEFORE. The page claimed in prose to be a pure function of
its sources and gave a reader no way to check the claim. A source-hash block is safe in a page that must
regenerate byte-identically for exactly the reason the claim was true all along: a hash moves only when
its source moves.
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from . import freshness as F
from . import maptrail as M
from . import reservation as RES

SOURCES = ("maptrail.jsonl", "observatory_reservation.jsonl", "observatory.db")


def state(db: Path) -> dict:
    if not db.exists():
        return {}
    con = sqlite3.connect(db)
    q = lambda s: con.execute(s).fetchone()[0]                                    # noqa: E731
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


def compile_page(lat: Path, out: Path) -> dict:
    trail = lat / "maptrail.jsonl"
    items = M.open_items(trail)
    st = state(lat / "observatory.db")
    res = sorted(RES.reserved_rows(lat / "observatory_reservation.jsonl"))

    L = ["# NEXT — what is open, compiled from the artifacts", "",
         "**This file is DERIVED. Do not edit it.** Regenerate with `foundry next`.", "",
         "It duplicates no fact: the maptrail owns rulings, the methods thread owns reasoning, commits",
         "own sequence. If this page disagrees with its sources, **the sources are right.** Nothing may",
         "be recorded here that lives nowhere else — a hand-edit would make it a place where rulings",
         "hide, which is the failure it exists to prevent.", "",
         "This page carries no timestamp and no commit id: it is a pure function of its sources, so",
         "two compiles from the same artifacts are byte-identical. Provenance belongs to the commit",
         "that carries the file, not to a line inside it. The source hashes it was compiled from are",
         "recorded at the foot of the page, so the claim can be checked with `foundry fresh` rather",
         "than taken on trust.", "",
         "---", "", "## Open work, in declared order", ""]

    for it in items:
        L += [f"### {it.get('sequence')}. {it.get('title')}", "", f"{it.get('why')}", "",
              f"- key: `{it['opens']}`"]
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

    # THE SOURCE RECORD. Sorted keys, so the block is a pure function of the sources like everything
    # above it. This is what turns "trust me, it's derived" into `foundry fresh`.
    srcs = {n: F.sha(lat / n) for n in SOURCES if (lat / n).exists()}
    L += [f"{F.SOURCES_MARKER} {json.dumps(srcs, sort_keys=True)} -->", ""]

    out.write_text("\n".join(L) + "\n")
    return {"open_items": len(items), "sources": len(srcs), "reserved": len(res),
            "titles": [it.get("title") for it in items]}
