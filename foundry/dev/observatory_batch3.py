#!/usr/bin/env python3
"""Observatory fan-out, BATCH 3 — off `graph` for the first time, and the first batch with a frontier.

THE RESERVED ROWS HAVE NO GENERATOR IN THIS FILE. That is the enforcement, not an oversight. A guard that
forbids capturing a reserved row still requires the machinery to be capable of capturing it and trusted
not to; a batch that never learned how to build one cannot burn the ground by accident. The generators for
`nearest-codeword` and `weighted-interval-scheduling` get written when the frontier is released, against
predictions already hashed.

WHAT THIS BATCH IS SPENDING ITSELF ON. Three census-declared family ramps, none ever used, two of them
recorded in the census as "precedent: none yet". They govern 222 queued rows. If a declared ramp does not
move its family's regions, the census's ramp table is wrong and the fan-out has been building on it.

  d-hitting-set             subsets hitting every set            UPWARD-closed
  minimum-test-cover        test subsets separating every pair   UPWARD-closed
  max-coverage              exactly-k subfamilies                FIXED CARDINALITY
  subset-product            subsets under a product bound        DOWNWARD-closed
  generalized-subset-sum    signed subsets hitting a target      neither
  minimum-distance-code     nonzero messages of bounded weight   neither
"""
import hashlib
import json
import math
import sys
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "dev"))
LAT = ROOT / "foundry" / "results" / "lattice"
OUT = LAT / "observatory_batch3_panels.json"
LEDGER = LAT / "observatory_reservation.jsonl"
TRAIL = LAT / "maptrail.jsonl"
from foundry.catalog import capture as C                                        # noqa: E402
from foundry.catalog import maptrail as M                                       # noqa: E402
from foundry.catalog import reservation as RES                                  # noqa: E402
import n2_dense_control as N2                                                   # noqa: E402
from sounding_v1 import BOOL_OPS                                                # noqa: E402

SEED = 20260726
BATCH = 3


# ── optimization: constraints per ground-set element ────────────────────────────────────────────────
def d_hitting_set(rng, ratio, n=10, d=3):
    """Ground set = n elements; constraints = m sets that must be hit. Upward-closed: a superset of a
    hitting set hits."""
    m = max(1, round(ratio * n))
    sets = [tuple(sorted(rng.sample(range(n), rng.randint(2, d)))) for _ in range(m)]
    f = [s for s in product((0, 1), repeat=n) if all(any(s[i] for i in S) for S in sets)]
    if len(f) < 2:
        return []
    b = min(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b])]


def minimum_test_cover(rng, ratio, m=10):
    """Ground set = m tests; constraints = item pairs that must be separated. Upward-closed."""
    p = max(3, round((1 + math.sqrt(1 + 8 * ratio * m)) / 2))
    tests = [frozenset(i for i in range(p) if rng.random() < 0.5) for _ in range(m)]
    pairs = [(i, j) for i in range(p) for j in range(i + 1, p)]
    f = [s for s in product((0, 1), repeat=m)
         if all(any((i in tests[k]) != (j in tests[k]) for k in range(m) if s[k]) for i, j in pairs)]
    if len(f) < 2:
        return []
    b = min(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b])]


def max_coverage(rng, ratio, m=10, k=3):
    """Ground set = m candidate sets; constraints = universe elements. Region is every size-k
    subfamily, so the feasible side is fixed-cardinality by construction and the instance shows up
    only in which of them are optimal."""
    n = max(2, round(ratio * m))
    sets = [frozenset(i for i in range(n) if rng.random() < 0.4) for _ in range(m)]
    f = [s for s in product((0, 1), repeat=m) if sum(s) == k]

    def cov(s):
        u = set()
        for i in range(m):
            if s[i]:
                u |= sets[i]
        return len(u)
    b = max(cov(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if cov(s) == b])]


# ── number-theoretic: capacity fraction / value range ───────────────────────────────────────────────
def subset_product(rng, frac, n=11):
    """Subsets whose product stays under a capacity. Downward-closed: dropping a factor ≥ 1 can only
    shrink the product."""
    vals = [rng.randint(2, 9) for _ in range(n)]
    total = 1.0
    for v in vals:
        total *= v
    bound = total ** frac
    f = []
    for s in product((0, 1), repeat=n):
        p = 1.0
        for i in range(n):
            if s[i]:
                p *= vals[i]
        if p <= bound:
            f.append(s)
    if len(f) < 2:
        return []
    b = max(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b])]


def generalized_subset_sum(rng, frac, n=12):
    """Sign vectors with Σ ±aᵢ = t. The ramp is the VALUE RANGE: wider values spread the reachable
    sums and thin the solution set. Neither closure direction — an equality has no monotone side."""
    V = max(3, round(frac * 25))
    vals = [rng.randint(1, V) for _ in range(n)]
    s0 = tuple(rng.randint(0, 1) for _ in range(n))
    t = sum(vals[i] if s0[i] else -vals[i] for i in range(n))
    f = [s for s in product((0, 1), repeat=n)
         if sum(vals[i] if s[i] else -vals[i] for i in range(n)) == t]
    if len(f) < 2:
        return []
    b = max(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b])]


# ── algebraic: equations per unknown ────────────────────────────────────────────────────────────────
def _encode_weight(x, G, k, n):
    c = 0
    for j in range(n):
        b = 0
        for i in range(k):
            if x[i]:
                b ^= G[i][j]
        c += b
    return c


def minimum_distance_code(rng, dens, k=10):
    """Nonzero messages whose codeword weight stays under a bound. The ramp is code length per message
    bit — a longer code spreads weight and tightens a fixed-fraction bound."""
    n = max(k + 1, round(dens * k))
    G = [[rng.randint(0, 1) for _ in range(n)] for _ in range(k)]
    w = max(1, round(0.4 * n))
    f = [x for x in product((0, 1), repeat=k) if any(x) and _encode_weight(x, G, k, n) <= w]
    if len(f) < 2:
        return []
    b = min(_encode_weight(x, G, k, n) for x in f)
    return [("feasible", f), ("optimal", [x for x in f if _encode_weight(x, G, k, n) == b])]


# row → (builder, structural expectation, family, ramp values, what the family ramp is instantiated as)
OPT = (0.5, 1.0, 1.5, 2.0, 3.0)
NUM = (0.2, 0.35, 0.5, 0.65, 0.8)
ALG = (1.2, 1.5, 2.0, 2.5, 3.0)
ROWS = {
    "d-hitting-set":          (d_hitting_set, "upward_closed", "optimization", OPT,
                               "sets-to-hit per ground element"),
    "minimum-test-cover":     (minimum_test_cover, "upward_closed", "optimization", OPT,
                               "item-pairs to separate per test"),
    "max-coverage":           (max_coverage, "fixed_cardinality", "optimization", OPT,
                               "universe elements per candidate set"),
    "subset-product":         (subset_product, "downward_closed", "number-theoretic", NUM,
                               "capacity fraction of the full product"),
    "generalized-subset-sum": (generalized_subset_sum, None, "number-theoretic", NUM, "value range"),
    "minimum-distance-code":  (minimum_distance_code, None, "algebraic", ALG,
                               "code length per message bit"),
}


def main() -> int:
    cen = json.loads((LAT / "observatory_batch3_census.json").read_text())
    reserved = RES.reserved_rows(LEDGER)

    # ── the reservation, enforced three ways before a generator runs ────────────────────────────────
    leak = sorted(set(ROWS) & reserved)
    if leak:
        raise RuntimeError(f"FRONTIER LEAK — batch 3 defines generators for reserved row(s) {leak}")
    missing = sorted(set(cen["published"]) - set(ROWS))
    if missing:
        raise RuntimeError(f"census published {missing} but this batch has no generator for them")
    extra = sorted(set(ROWS) - set(cen["published"]))
    if extra:
        raise RuntimeError(f"batch defines {extra}, which the census did not publish")
    print(f"reservation honoured: {len(reserved)} row(s) withheld, no generator defined for any of "
          f"them — {', '.join(sorted(reserved))}\n")

    out, excluded = [], []
    ctrl = lambda region, rng: N2.cp_control(region, rng)[0]
    for row, (build, expect, fam, ramp, instantiates) in ROWS.items():
        print(f"  capturing {row} ...", flush=True)
        rec, ex = C.capture_row(row, build, expect, ramp, BOOL_OPS, SEED, ctrl)
        if ex:
            excluded.append(ex)
            print(f"    EXCLUDED at birth: {row} — {ex['reason'][0]}", flush=True)
        else:
            rec["family"] = fam
            rec["ramp_parameter"] = cen["families"][fam]["census_ramp"]
            rec["ramp_instantiated_as"] = instantiates
            out.append(rec)

    doc = {"schema": "observatory-batch3/v1",
           "STATUS": "EXPLORATORY dial panels — no verdict, no scored prediction, no seal",
           "not_citable_as": "a result. Descriptive capture only.",
           "batch": BATCH, "reach_class": "REACH-subset",
           "families": {f: cen["families"][f]["census_ramp"] for f in
                        sorted({v[2] for v in ROWS.values()})},
           "why_these_rows": cen["why_this_batch"],
           "frontier_reservation": {
               "reserved": sorted(reserved), "roster_sha256": cen["reservation"]["roster_sha256"],
               "note": ("reserved rows are not captured and have no generator in this file — the batch "
                        "cannot burn the ground because it never learned how to build it")},
           "pipeline": "foundry.catalog.capture — one implementation for every batch",
           "excluded_at_birth": excluded, "rows": out}
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    # ── maptrail, emitted HERE, at event time (Helm Kill 3) ─────────────────────────────────────────
    M.emit(TRAIL, "expansion", key=f"expansion:batch{BATCH}",
           artifact=OUT.name, sha256=hashlib.sha256(OUT.read_bytes()).hexdigest(),
           wave=None, rows_added=[r["row"] for r in out], n_rows=len(out),
           n_reserved=len(reserved), reservation_ledger=LEDGER.name,
           admission_authority="observatory fan-out, conformance-tested at birth; frontier reserved "
                               "per Helm §5 before capture")
    for e in excluded:
        M.emit(TRAIL, "exclusion", key=f"exclusion:batch{BATCH}:{e['row']}",
               problem=e["row"], batch=BATCH, reasons=e["reason"],
               authority="conformance at birth")
    M.emit(TRAIL, "annotation", key=f"annotation:batch{BATCH}:string-family-ramp",
           what=cen["flagged_for_ruling"]["why_it_does_not_apply"],
           problem=cen["flagged_for_ruling"]["problem"],
           disposition=cen["flagged_for_ruling"]["disposition"],
           touches_no_measured_value=True, authority="raised at batch 3 census, awaiting owner ruling")

    print(f"\nBATCH 3 — {len(out)} rows shipped, {len(excluded)} excluded at birth\n")
    for r in out:
        print(f"  {r['row']}  [{r['structural_expectation'] or 'no declared structure'}]  "
              f"{r['family']} / {r['ramp_instantiated_as']}")
        for s in r["steps"]:
            if s["state"] != "usable":
                print(f"      x={s['ramp_value']:<5} {s['state']}")
                continue
            d = s["dials"]
            ex2 = {k: round(v["blend_excess"], 3) for k, v in d["flavours"].items()
                   if v["blend_excess"] is not None}
            print(f"      x={s['ramp_value']:<5}{s['region']:<9}r={d['r_mean']:<8}"
                  f"ov={str(d['overlap_mean']):<7}BC={str(d['bimodality_coefficient']):<7}{ex2}")
        print()
    print(f"wrote {OUT.name}  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
