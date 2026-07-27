#!/usr/bin/env python3
"""Observatory fan-out, BATCH 7 — and a lexicon false-positive caught at the generator.

Four rows ship. Two do not, and their reasons differ in a way worth keeping apart:

  planar-vertex-deletion            no AFFORDABLE EXACT planarity test at this scale
  lex-first-maximal-independent-set LEXICON FALSE POSITIVE — matched "independent set", but the
                                    lex-first MIS is UNIQUE given an order, so the row has a unique
                                    answer, not a region

The second is the more useful. Lexicon v2 read 53.5% of the class and its stopping rule already says
the remainder gets hand adjudication; this shows the MATCHED portion also needs a region check, because
a phrase can be present and the object still not be a subset region.
"""
import hashlib, json, sys
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "dev"))
LAT = ROOT / "foundry" / "results" / "lattice"
OUT = LAT / "observatory_batch7_panels.json"
LEDGER = LAT / "observatory_reservation.jsonl"
TRAIL = LAT / "maptrail.jsonl"
from foundry.catalog import capture as C                                        # noqa: E402
from foundry.catalog import maptrail as M                                       # noqa: E402
from foundry.catalog import reservation as RES                                  # noqa: E402
import n2_dense_control as N2                                                   # noqa: E402
from sounding_v1 import BOOL_OPS                                                # noqa: E402

SEED = 20260727
BATCH = 7
NG = 9
GRAPH = (0.15, 0.25, 0.35, 0.45, 0.60)
OPT = (0.5, 1.0, 1.5, 2.0, 3.0)


def G(n, p, rng):
    return [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < p]


def total_dominating_set(rng, p, n=NG):
    """Every vertex must have a NEIGHBOUR in S — itself does not count. Upward-closed."""
    E = G(n, p, rng)
    adj = {i: set() for i in range(n)}
    for u, v in E:
        adj[u].add(v); adj[v].add(u)
    if any(not adj[v] for v in range(n)):
        return []
    f = [s for s in product((0, 1), repeat=n) if all(any(s[u] for u in adj[v]) for v in range(n))]
    if len(f) < 2:
        return []
    b = min(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b])]


def _disjoint_packing(cands, m):
    f = [s for s in product((0, 1), repeat=m)
         if all(not (cands[i] & cands[j])
                for i, j in combinations([k for k in range(m) if s[k]], 2))]
    if len(f) < 2:
        return []
    b = max(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b])]


def triangle_packing(rng, p, n=NG, m=11):
    """Subsets of a FIXED candidate triangle list that are pairwise vertex-disjoint. Downward-closed;
    the ground set is the candidate list, held at m, so the ambient does not move with density."""
    E = set(G(n, p, rng))
    tri = [frozenset(c) for c in combinations(range(n), 3)
           if all(tuple(sorted(e)) in E for e in combinations(c, 2))]
    if len(tri) < 2:
        return []
    cands = [tri[i % len(tri)] for i in range(m)]
    return _disjoint_packing(cands, m)


def cycle_packing(rng, p, n=NG, m=11):
    """Same shape on 4-cycles. Downward-closed, ground set fixed at m."""
    E = set(G(n, p, rng))
    cyc = []
    for c in combinations(range(n), 4):
        a, b, cc, d = c
        if all(tuple(sorted(e)) in E for e in ((a, b), (b, cc), (cc, d), (a, d))):
            cyc.append(frozenset(c))
    if len(cyc) < 2:
        return []
    cands = [cyc[i % len(cyc)] for i in range(m)]
    return _disjoint_packing(cands, m)


def quadratic_knapsack(rng, ratio, n=11):
    """Item subsets under a capacity. Downward-closed; the quadratic part is the OBJECTIVE, so the
    feasible region is an ordinary knapsack region and `ratio` instantiates capacity tightness."""
    w = [rng.randint(1, 9) for _ in range(n)]
    cap = sum(w) / (1.0 + ratio)
    f = [s for s in product((0, 1), repeat=n)
         if sum(w[i] for i in range(n) if s[i]) <= cap]
    if len(f) < 2:
        return []
    val = [[rng.randint(0, 5) for _ in range(n)] for _ in range(n)]
    def q(s):
        idx = [i for i in range(n) if s[i]]
        return sum(val[i][j] for i, j in combinations(idx, 2))
    b = max(q(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if q(s) == b])]


ROWS = {
    "total-dominating-set": (total_dominating_set, "upward_closed", "graph", GRAPH,
                             "edge density of the ground graph"),
    "triangle-packing":     (triangle_packing, "downward_closed", "graph", GRAPH,
                             "edge density of the ground graph"),
    "cycle-packing":        (cycle_packing, "downward_closed", "graph", GRAPH,
                             "edge density of the ground graph"),
    "quadratic-knapsack":   (quadratic_knapsack, "downward_closed", "optimization", OPT,
                             "capacity tightness per item"),
}

NOT_BUILT = {
    "planar-vertex-deletion": {
        "kind": "no-affordable-exact-test",
        "reason": ("the region is vertex subsets whose removal leaves a PLANAR graph, and no exact "
                   "planarity test is affordable at enumeration scale here. The available shortcuts "
                   "(the |E| <= 3n-6 bound) are NECESSARY, not sufficient — using one would silently "
                   "admit non-planar residues and mis-define the row rather than approximate it.")},
    "lex-first-maximal-independent-set": {
        "kind": "lexicon-false-positive",
        "reason": ("matched L4-subset on the phrase 'independent set', but the LEX-FIRST maximal "
                   "independent set is UNIQUE given a vertex order. The row has a unique answer, not "
                   "a region — it belongs to REGIONLESS-unique-answer. The lexicon read a real phrase "
                   "in a real encoding and still got the object wrong, because presence of a "
                   "subset-shaped noun does not make the certificate a subset.")},
}


def main() -> int:
    cen = json.loads((LAT / "observatory_batch7_census.json").read_text())
    reserved = RES.reserved_rows(LEDGER)
    leak = sorted(set(ROWS) & reserved)
    if leak:
        raise RuntimeError(f"FRONTIER LEAK — batch 7 defines generators for reserved row(s) {leak}")
    covered = set(ROWS) | set(NOT_BUILT)
    missing = sorted(set(cen["published"]) - covered)
    if missing:
        raise RuntimeError(f"census published {missing} with neither a generator nor a reason")
    print(f"reservation honoured: {len(reserved)} row(s) withheld across all batches\n")

    out, excluded = [], []
    ctrl = lambda region, rng: N2.cp_control(region, rng)[0]
    for row, info in NOT_BUILT.items():
        if row not in cen["published"]:
            continue
        excluded.append({"row": row, "kind": info["kind"], "reason": [info["reason"]]})
        print(f"  NOT BUILT [{info['kind']}]: {row}", flush=True)

    for row, (build, expect, fam, ramp, inst) in ROWS.items():
        print(f"  capturing {row} ...", flush=True)
        rec, ex = C.capture_row(row, build, expect, ramp, BOOL_OPS, SEED, ctrl)
        if ex:
            excluded.append({**ex, "kind": "conformance"})
            print(f"    EXCLUDED at birth: {row} — {ex['reason'][0]}", flush=True)
        else:
            rec["family"] = fam
            rec["ramp_parameter"] = cen["families"][fam]["census_ramp"]
            rec["ramp_instantiated_as"] = inst
            out.append(rec)

    doc = {"schema": "observatory-batch7/v1",
           "STATUS": "EXPLORATORY dial panels — no verdict, no scored prediction, no seal",
           "batch": BATCH, "reach_class": "REACH-subset",
           "families": {f: cen["families"][f]["census_ramp"] for f in
                        sorted({v[2] for v in ROWS.values()})},
           "why_these_rows": cen["why_this_batch"],
           "lexicon_false_positive": ("lex-first-maximal-independent-set matched L4-subset on a real "
                                      "phrase and is still not a subset region — the MATCHED portion "
                                      "of the lexicon needs a region check too"),
           "frontier_reservation": {"reserved_this_batch": sorted(cen["reservation"]["reserved"]),
                                    "roster_sha256": cen["reservation"]["roster_sha256"]},
           "pipeline": "foundry.catalog.capture — one implementation for every batch",
           "excluded_at_birth": excluded, "rows": out}
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    M.emit(TRAIL, "expansion", key=f"expansion:batch{BATCH}",
           artifact=OUT.name, sha256=hashlib.sha256(OUT.read_bytes()).hexdigest(),
           rows_added=[r["row"] for r in out], n_rows=len(out),
           n_reserved=len(cen["reservation"]["reserved"]),
           admission_authority="observatory fan-out; roster vetted before hashing")
    for e in excluded:
        M.emit(TRAIL, "exclusion", key=f"exclusion:batch{BATCH}:{e['row']}",
               problem=e["row"], batch=BATCH, reasons=e["reason"], kind=e.get("kind"),
               authority="build-time finding")

    print(f"\nBATCH 7 — {len(out)} rows shipped, {len(excluded)} excluded\n")
    for r in out:
        print(f"  {r['row']}  [{r['structural_expectation'] or '—'}]")
        for s in r["steps"]:
            if s["state"] != "usable":
                print(f"      x={s['ramp_value']:<5} {s['state']}"); continue
            d = s["dials"]
            ex2 = {k: round(v["blend_excess"], 3) for k, v in d["flavours"].items()
                   if v["blend_excess"] is not None}
            print(f"      x={str(s['ramp_value']):<5}{s['region']:<9}r={d['r_mean']:<8}{ex2}")
        print()
    print(f"wrote {OUT.name}  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
