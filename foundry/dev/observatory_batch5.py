#!/usr/bin/env python3
"""Observatory fan-out, BATCH 5 — the first CONTRAST-DIAL capture, and three mis-typings found.

  minimum-common-string-partition   cut subsets of A that also partition B   CONTRAST-DIAL, upward-closed
  job-interval-selection            pairwise non-overlapping job subsets     DOWNWARD-closed
  biclique-cover                    subfamilies of candidate bicliques       UPWARD-closed

THE OTHER THREE ROSTERED ROWS HAVE NO SUBSET REGION AT ALL, and that is this batch's finding rather than
its failure. `min-sum-set-cover` scores an ORDERING of the sets; `cutwidth` scores a LINEAR LAYOUT;
`domatic-number` asks for a PARTITION into dominating sets. Each is typed REACH-subset in the census, and
none of them is a subset problem — their objects are permutations and partitions, which the census has
separate classes for.

I rostered them without checking their region formulations, and that is exactly how the mis-typing
surfaced: the roster was declared and hashed before the generators were written, so the check could not
be quietly skipped once it became inconvenient. Three of eight is a rate worth reporting, because the
REACH-subset queue is 127 rows and nothing has re-examined it since the census.

MCSP IMPORTS ITS GENERATOR FROM THE PILOT rather than copying it — the test-of-a-copy law. The row whose
ramp was amended and measured there must be built by the same code that measured it.
"""
import hashlib
import json
import sys
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "dev"))
LAT = ROOT / "foundry" / "results" / "lattice"
OUT = LAT / "observatory_batch5_panels.json"
LEDGER = LAT / "observatory_reservation.jsonl"
TRAIL = LAT / "maptrail.jsonl"
from foundry.catalog import capture as C                                        # noqa: E402
from foundry.catalog import maptrail as M                                       # noqa: E402
from foundry.catalog import reservation as RES                                  # noqa: E402
import mcsp_ramp_pilot as MP                                                    # noqa: E402
import n2_dense_control as N2                                                   # noqa: E402
from sounding_v1 import BOOL_OPS                                                # noqa: E402

SEED = 20260727
BATCH = 5
OPT = (0.5, 1.0, 1.5, 2.0, 3.0)
GRAPH = (0.15, 0.25, 0.35, 0.45, 0.60)
MCSP_LEVELS = (2, 6)


def job_interval_selection(rng, ratio, n=11):
    """Subsets of jobs whose chosen intervals pairwise do not overlap. Downward-closed; the ground set
    is the JOB set, held at n, so the ambient does not move with the dial."""
    T = max(3, round(n / ratio))
    iv = []
    for _ in range(n):
        a = rng.randrange(T)
        iv.append((a, min(T, a + rng.randint(1, 3))))
    def ok(s):
        idx = [i for i in range(n) if s[i]]
        return all(not (iv[i][0] < iv[j][1] and iv[j][0] < iv[i][1])
                   for i, j in combinations(idx, 2))
    f = [s for s in product((0, 1), repeat=n) if ok(s)]
    if len(f) < 2:
        return []
    b = max(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b])]


def biclique_cover(rng, p, n=6, m=11):
    """Subfamilies of a FIXED candidate set of bicliques that together cover every edge. Upward-closed.
    The candidate count is held at m so the ground set does not move with edge density."""
    E = {(i, j) for i in range(n) for j in range(n) if i < j and rng.random() < p}
    if not E:
        return []
    cands = []
    for _ in range(m):
        L = {i for i in range(n) if rng.random() < 0.5}
        R = {i for i in range(n) if i not in L and rng.random() < 0.6}
        cands.append({(min(a, b), max(a, b)) for a in L for b in R if a != b} & E)
    f = []
    for s in product((0, 1), repeat=m):
        cov = set()
        for i in range(m):
            if s[i]:
                cov |= cands[i]
        if cov == E:
            f.append(s)
    if len(f) < 2:
        return []
    b = min(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b])]


ROWS = {
    "minimum-common-string-partition": (lambda rng, k: MP.mcsp(rng, k), "upward_closed", "string",
                                        MCSP_LEVELS, "alphabet size at fixed string length",
                                        "CONTRAST-DIAL"),
    "job-interval-selection": (job_interval_selection, "downward_closed", "optimization", OPT,
                               "jobs per time slot", "RAMPED"),
    "biclique-cover": (biclique_cover, "upward_closed", "graph", GRAPH,
                       "edge density of the ground graph", "RAMPED"),
}

# Rostered, then found to have no subset region. Recorded as TYPINGS, not as build failures.
MISTYPED = {
    "min-sum-set-cover": ("the objective scores an ORDERING of the sets — cost is the sum over elements "
                          "of the position at which each is first covered. The subfamily that covers is "
                          "just set-cover, which is already built; the min-sum question is not a subset "
                          "question at all."),
    "cutwidth": ("the object is a LINEAR LAYOUT of the vertices and the cost is the maximum edge cut "
                 "across a position. Vertex subsets do not encode a layout; this belongs to the "
                 "permutation class."),
    "domatic-number": ("asks for a PARTITION of the vertices into as many dominating sets as possible. "
                       "A single dominating set is the already-built `dominating-set` row; the domatic "
                       "question lives over partitions."),
}


def main() -> int:
    cen = json.loads((LAT / "observatory_batch5_census.json").read_text())
    reserved = RES.reserved_rows(LEDGER)
    leak = sorted(set(ROWS) & reserved)
    if leak:
        raise RuntimeError(f"FRONTIER LEAK — batch 5 defines generators for reserved row(s) {leak}")
    covered = set(ROWS) | set(MISTYPED)
    missing = sorted(set(cen["published"]) - covered)
    if missing:
        raise RuntimeError(f"census published {missing} with neither a generator nor a mis-typing")
    print(f"reservation honoured: {len(reserved)} row(s) withheld across all batches\n")

    out, excluded = [], []
    ctrl = lambda region, rng: N2.cp_control(region, rng)[0]
    for row, reason in MISTYPED.items():
        if row not in cen["published"]:
            continue
        excluded.append({"row": row, "kind": "mis-typed", "reason": [reason],
                         "census_class": "REACH-subset",
                         "belongs_to": ("REACH-permutation" if row in ("min-sum-set-cover", "cutwidth")
                                        else "a partition class the census does not yet have")})
        print(f"  MIS-TYPED: {row} — no subset region", flush=True)

    for row, (build, expect, fam, ramp, inst, mode) in ROWS.items():
        print(f"  capturing {row} [{mode}] ...", flush=True)
        rec, ex = C.capture_row(row, build, expect, ramp, BOOL_OPS, SEED, ctrl, capture_mode=mode)
        if ex:
            excluded.append({**ex, "kind": "conformance"})
            print(f"    EXCLUDED at birth: {row} — {ex['reason'][0]}", flush=True)
        else:
            rec["family"] = fam
            rec["ramp_parameter"] = cen["families"][fam]["census_ramp"]
            rec["ramp_instantiated_as"] = inst
            out.append(rec)

    doc = {"schema": "observatory-batch5/v1",
           "STATUS": "EXPLORATORY dial panels — no verdict, no scored prediction, no seal",
           "not_citable_as": "a result. Descriptive capture only.",
           "batch": BATCH, "reach_class": "REACH-subset",
           "families": {f: cen["families"][f]["census_ramp"] for f in
                        sorted({v[2] for v in ROWS.values()})},
           "why_these_rows": cen["why_this_batch"],
           "first_contrast_dial_capture": "minimum-common-string-partition, levels |Sigma| in {2, 6}",
           "mistyping_rate": f"{len(MISTYPED)} of {cen['n_roster']} rostered rows have no subset region",
           "frontier_reservation": {"reserved_this_batch": sorted(cen["reservation"]["reserved"]),
                                    "roster_sha256": cen["reservation"]["roster_sha256"]},
           "pipeline": "foundry.catalog.capture — one implementation for every batch",
           "excluded_at_birth": excluded, "rows": out}
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    M.emit(TRAIL, "expansion", key=f"expansion:batch{BATCH}",
           artifact=OUT.name, sha256=hashlib.sha256(OUT.read_bytes()).hexdigest(),
           wave=None, rows_added=[r["row"] for r in out], n_rows=len(out),
           n_reserved=len(cen["reservation"]["reserved"]), reservation_ledger=LEDGER.name,
           first_contrast_dial="minimum-common-string-partition",
           admission_authority="observatory fan-out, conformance-tested at birth")
    for e in excluded:
        M.emit(TRAIL, "exclusion", key=f"exclusion:batch{BATCH}:{e['row']}",
               problem=e["row"], batch=BATCH, reasons=e["reason"], kind=e.get("kind"),
               authority=("census mis-typing found at build" if e.get("kind") == "mis-typed"
                          else "conformance at birth"))

    print(f"\nBATCH 5 — {len(out)} rows shipped, {len(excluded)} excluded "
          f"({len(MISTYPED)} mis-typed, {len(excluded) - len(MISTYPED)} conformance)\n")
    for r in out:
        print(f"  {r['row']}  [{r['capture_mode']}]  {r['family']} / {r['ramp_instantiated_as']}")
        for s in r["steps"]:
            if s["state"] != "usable":
                print(f"      x={s['ramp_value']:<5} {s['state']}")
                continue
            d = s["dials"]
            ex2 = {k: round(v["blend_excess"], 3) for k, v in d["flavours"].items()
                   if v["blend_excess"] is not None}
            print(f"      x={str(s['ramp_value']):<5}{s['region']:<9}r={d['r_mean']:<8}"
                  f"ov={str(d['overlap_mean']):<7}BC={str(d['bimodality_coefficient']):<7}{ex2}")
        print()
    print(f"wrote {OUT.name}  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
