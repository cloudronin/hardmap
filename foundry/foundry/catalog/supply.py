"""Supply — how many rows of a given kind exist, are built, are reserved, and remain.

WHY THIS IS MACHINERY AND NOT A SCRIPT. A supply number decides whether a held bet can revive on a
count or must convert to path-gated, and the previous number was quoted off a `reach_class` column that
had 51 rows on a superseded answer. A count that governs a disposition has to be recomputable on demand
from the current column, by anyone, without trusting that whoever ran it last ran it correctly.

THE POPULATION IS PARTITIONED, NOT FILTERED. Every row in the class lands in exactly one bucket —
built, reserved, excluded-at-birth, or available — and the buckets are asserted to sum to the total.
A filter that silently drops a row it does not recognise produces an undercount that looks like a
finding, which is the specific way a supply census can lie.

BUILT IS MEASURED THREE WAYS AND THEY MUST AGREE. Frames, panels, and catalog cells are independent
records of the same fact. If they disagree, the archive is inconsistent and the census refuses rather
than picking one — the disagreement is the finding, not an inconvenience to resolve.
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from . import maptrail as M
from . import reservation as RES


def _built_three_ways(con, lat: Path) -> tuple:
    frames = {r[0] for r in con.execute("SELECT DISTINCT problem_id FROM frames")}
    catalog = {r[0] for r in con.execute("SELECT DISTINCT problem_id FROM catalog")}
    panels, excluded = set(), {}
    for p in sorted(lat.glob("observatory_batch*_panels.json")):
        d = json.loads(p.read_text())
        panels |= {r["row"] for r in d["rows"]}
        for e in d.get("excluded_at_birth", []):
            excluded[e["row"]] = e.get("reason") or e.get("why") or "excluded at birth"
    return frames, panels, catalog, excluded


def census(lat: Path, family: str, reach_class: str) -> dict:
    """The partition, with its own consistency check."""
    con = sqlite3.connect(lat / "observatory.db")
    try:
        rows = {r[0] for r in con.execute(
            "SELECT problem_id FROM problems WHERE family=? AND reach_class=?", (family, reach_class))}
        frames, panels, catalog, excluded = _built_three_ways(con, lat)
    finally:
        con.close()

    disagree = sorted((rows & frames) ^ (rows & panels)) + sorted((rows & frames) ^ (rows & catalog))
    if disagree:
        raise RuntimeError(
            f"BUILT DISAGREES ACROSS RECORDS for {disagree[:5]} — frames, panels and catalog are "
            f"independent records of the same fact. A census cannot pick one; the disagreement is the "
            f"finding.")

    reserved = RES.reserved_rows(lat / "observatory_reservation.jsonl")
    built = rows & frames
    res = (rows & reserved) - built
    exc = (rows & set(excluded)) - built - res
    avail = rows - built - res - exc

    assert len(built) + len(res) + len(exc) + len(avail) == len(rows), "the partition does not close"
    return {
        "family": family, "reach_class": reach_class, "total": len(rows),
        "built": sorted(built), "reserved": sorted(res),
        "excluded_at_birth": {k: excluded[k] for k in sorted(exc)},
        "available": sorted(avail),
        "n_built": len(built), "n_reserved": len(res), "n_excluded": len(exc),
        "n_available": len(avail),
        "exhausted": not avail,
    }


def run(lat: Path, family: str, reach_class: str, out: Path | None = None,
        trail: Path | None = None) -> dict:
    c = census(lat, family, reach_class)
    doc = {
        "schema": "supply-census/v1",
        "STATUS": "COUNT — read off the CORRECTED reach_class column (the declared typing chain)",
        "column_provenance": (
            "reach_class as resolved by foundry.catalog.typing_chain over the declared supersession "
            "chain. The previous census read a column in which 51 rows carried a pre-adjudication "
            "answer; every one of those was REACH-subset narrowed to something more specific, so the "
            "old number was an OVERCOUNT and no supply figure may be quoted from it."),
        **c,
    }
    out = out or (lat / f"supply_census_{family}_{reach_class.lower().replace('-', '_')}.json")
    if trail:
        M.emit(trail, "annotation", key=f"supply:{family}:{reach_class}",
               family=family, reach_class=reach_class, total=c["total"],
               n_built=c["n_built"], n_reserved=c["n_reserved"], n_available=c["n_available"],
               exhausted=c["exhausted"], touches_no_measured_value=True,
               why="supply recount on the corrected typing column")
    out.write_text(json.dumps(doc, indent=1) + "\n")
    return doc
