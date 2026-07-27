#!/usr/bin/env python3
"""The maptrail's one-time import of history that predates the trail (Helm §7.1).

EVERY RECORD THIS WRITES CARRIES `reconstructed: true`. The program has real history — five frozen
artifacts, a 345-row census, an adjudication, two fan-out batches — and that history belongs in the trail.
But it was not emitted at event time, and Helm Kill 3 says an event that was not emitted at event time
halts the wave. The resolution the spec itself names: import it once, label every imported record, and
never let a reconstructed record masquerade as a live one.

EVERY VALUE IS DERIVED, NOT TRANSCRIBED. Hashes are recomputed from the bytes on disk and counts are read
out of the artifacts, because a backfill typed from a table in a paper is a hand-maintained list — the
exact species of object this program has repeatedly caught being wrong. If a hash here disagrees with the
paper, the bytes win and the disagreement is a finding.

Idempotent: re-running appends nothing, because every emit carries a stable key.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from foundry.catalog import maptrail as M                                       # noqa: E402

LAT = ROOT / "foundry" / "results" / "lattice"
ATLAS = ROOT.parent / "eightfold" / "eightfold" / "results" / "atlas"
TRAIL = LAT / "maptrail.jsonl"

FROZEN = [
    ("atlas.jsonl",     "the charge atlas, v1 — the founding canon"),
    ("atlas_v2.jsonl",  "v1 plus the Strata charge-applicability layer"),
    ("atlas_v3.jsonl",  "the broad expansion; the population most results run on"),
    ("anatomy_v1.jsonl", "the Structure Atlas — 345 natural rows, 4,072 Boolean"),
    ("anatomy_v2.jsonl", "v1 plus closure columns on the 28 rows that admit them"),
]


def main() -> int:
    n_before = len(M.read(TRAIL))
    print("MAPTRAIL BACKFILL — every record marked reconstructed: true\n")

    for name, what in FROZEN:
        p = ATLAS / name
        if not p.exists():
            print(f"  ABSENT {name} — skipped, and the absence is not silently a success")
            continue
        b = p.read_bytes()
        M.emit(TRAIL, "freeze", key=f"freeze:{name}", reconstructed=True,
               artifact=name, sha256=hashlib.sha256(b).hexdigest(),
               rows=sum(1 for x in b.decode().splitlines() if x.strip()), what=what,
               authority="frozen at hash and asserted by test on every run")
        print(f"  freeze     {name:<18} {hashlib.sha256(b).hexdigest()[:16]}")

    # ── the observatory's own history ───────────────────────────────────────────────────────────────
    cen = json.loads((LAT / "observatory_reach_census.json").read_text())
    M.emit(TRAIL, "annotation", key="annotation:reach-census", reconstructed=True,
           what="every atlas row typed for reachability; a TYPING, not a measurement",
           n_rows=cen["n_rows"], n_reachable=cen["n_reachable"],
           touches_no_measured_value=True,
           authority="observatory reach census, ramped-by-default amendment")
    print(f"  annotation reach census        {cen['n_rows']} rows, {cen['n_reachable']} reachable")

    adj = json.loads((LAT / "observatory_untyped_adjudication.json").read_text())
    M.emit(TRAIL, "annotation", key="annotation:untyped-adjudication", reconstructed=True,
           what="the STILL-UNTYPED residue adjudicated row by row",
           n_adjudicated=len(adj["adjudications"]), touches_no_measured_value=True,
           authority="observatory adjudication pass")
    print(f"  annotation adjudication        {len(adj['adjudications'])} rows retyped")

    for bp in sorted(LAT.glob("observatory_batch*_panels.json")):
        d = json.loads(bp.read_text())
        b = d.get("batch", bp.name)
        M.emit(TRAIL, "expansion", key=f"expansion:batch{b}", reconstructed=True,
               artifact=bp.name, sha256=hashlib.sha256(bp.read_bytes()).hexdigest(),
               wave=None, rows_added=[r["row"] for r in d["rows"]],
               n_rows=len(d["rows"]),
               admission_authority="observatory fan-out, conformance-tested at birth")
        print(f"  expansion  batch {b}               {len(d['rows'])} rows")
        for e in d.get("excluded_at_birth", []):
            M.emit(TRAIL, "exclusion", key=f"exclusion:batch{b}:{e['row']}", reconstructed=True,
                   problem=e["row"], batch=b, reasons=e["reason"],
                   authority="conformance at birth — a generator that cannot reproduce a derived "
                             "consequence of its own definition does not ship")
            print(f"  exclusion  {e['row']:<20} {e['reason'][0]}")

    cm = LAT / "catalog_v1_meta.json"
    if cm.exists():
        m = json.loads(cm.read_text())
        M.emit(TRAIL, "version", key="version:catalog-v1", reconstructed=True,
               schema=m["schema"], version=m["catalog_version"],
               descriptor_version=m["descriptor_version"], extractor_sha256=m["extractor_sha256"],
               law="F4 — a changed extraction rule is a NEW version, never an in-place edit")
        print(f"  version    catalog {m['catalog_version']}          descriptor@{m['descriptor_version']}")

    n = len(M.read(TRAIL))
    print(f"\n  {n - n_before} records appended, {n} in the trail")
    print(f"  all reconstructed: {all(r['reconstructed'] for r in M.read(TRAIL))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
