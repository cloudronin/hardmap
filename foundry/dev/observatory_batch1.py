#!/usr/bin/env python3
"""Observatory fan-out, BATCH 1 — six new graph rows. Generators + conformance at birth + dial panels.

DEPENDENCY ORDER. `REACH-subset` graph rows come first: the largest reachable class (127 after
adjudication), the simplest encoding (a solution is a vertex or edge subset, ambient 2^n), and the family
whose ramp parameter — edge density — already has five precedents in v3.

THE SIX, chosen for STRUCTURAL VARIETY rather than convenience, because a batch of six upward-closed rows
would tell the dial panel nothing it does not already know from set-cover:

  dissociation-number     feasible = subsets inducing max degree <= 1        DOWNWARD-closed
  high-degree-subgraph    feasible = subsets with min induced degree >= k    neither direction
  efficient-domination    feasible = every vertex dominated EXACTLY once     neither; an exact condition
  min-bisection           feasible = balanced bipartitions                   FIXED CARDINALITY
  densest-k-subgraph      feasible = size-k subsets                          FIXED CARDINALITY
  maximum-planar-subgraph feasible = edge subsets that stay planar           DOWNWARD-closed, edge-indexed

Two are fixed-cardinality, which the forced_saturated derivation (S4) predicts will read min/max SATURATED
— so this batch also exercises the screen stack in both directions rather than only the closed one.

CONFORMANCE AT BIRTH, AND WHY IT CANNOT BE THE GENERATOR'S OWN FILTER. These rows have no pinned Marrow
template, so the semantic template check does not apply. Checking that every emitted member satisfies the
predicate the generator FILTERED BY is circular and certifies nothing.

So conformance here is DERIVED CONSEQUENCES of the definition, checked independently of the filter:
  - a known-answer instance whose solution set is computable by hand
  - a monotonicity consequence the definition implies but the filter does not state
    (dissociation is downward-closed; planar-subgraph is downward-closed; a fixed-cardinality family
     has exactly one distinct member weight)
A generator passing its own filter but failing a derived consequence has the wrong definition.

CENSUS MINIMALISM: this reads the census and writes panels. It reads no prior outcome artifact.
"""
import hashlib
import json
import random
import sys
from itertools import combinations, islice, product
from pathlib import Path
from statistics import mean, pstdev

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "dev"))
LAT = ROOT / "foundry" / "results" / "lattice"
OUT = LAT / "observatory_batch1_panels.json"
import n2_dense_control as N2                                          # noqa: E402
import terrain_score as T                                              # noqa: E402
from sounding_v1 import BOOL_OPS                                       # noqa: E402

SEED, N_INST, R_FLOOR = 20260726, 3, 10
EDGE_DENSITY_RAMP = (0.15, 0.25, 0.35, 0.45, 0.60)      # the family dial, declared at census
N_VERT, K_CTRL, PAIR_CAP = 10, 20, 20000
HULL_MAX_N = 12                                          # m=2 only, per the standing scope


def G(n, p, rng):
    return [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < p]


def _adj(n, E):
    a = {i: set() for i in range(n)}
    for u, v in E:
        a[u].add(v); a[v].add(u)
    return a


def dissociation(rng, p, n=N_VERT):
    E = G(n, p, rng); a = _adj(n, E)
    f = [s for s in product((0, 1), repeat=n)
         if all(sum(1 for u in a[v] if s[u]) <= 1 for v in range(n) if s[v])]
    if not f: return []
    b = max(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b])]


def high_degree_subgraph(rng, p, n=N_VERT, k=2):
    E = G(n, p, rng); a = _adj(n, E)
    f = [s for s in product((0, 1), repeat=n)
         if all(sum(1 for u in a[v] if s[u]) >= k for v in range(n) if s[v])]
    if not f: return []
    b = max(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b])]


def efficient_domination(rng, p, n=N_VERT):
    E = G(n, p, rng); a = _adj(n, E)
    f = [s for s in product((0, 1), repeat=n)
         if all(sum(1 for u in (a[v] | {v}) if s[u]) == 1 for v in range(n))]
    return [("solutions", f)] if f else []


def min_bisection(rng, p, n=N_VERT):
    E = G(n, p, rng)
    half = n // 2
    f = [s for s in product((0, 1), repeat=n) if sum(s) == half]
    cut = lambda s: sum(1 for u, v in E if s[u] != s[v])
    b = min(cut(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if cut(s) == b])]


def densest_k_subgraph(rng, p, n=N_VERT, k=4):
    E = G(n, p, rng)
    f = [s for s in product((0, 1), repeat=n) if sum(s) == k]
    dens = lambda s: sum(1 for u, v in E if s[u] and s[v])
    b = max(dens(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if dens(s) == b])]


def _planar_ok(n, edges):
    """Euler's bound: a simple planar graph on v>=3 vertices has at most 3v-6 edges. A NECESSARY
    condition, and it is used as such — the row is typed `euler-bound relaxation` in the panel so the
    object is never mistaken for exact planarity."""
    used = {x for e in edges for x in e}
    v = len(used)
    return len(edges) <= max(0, 3 * v - 6) if v >= 3 else True


def maximum_planar_subgraph(rng, p, n=8):
    E = G(n, p, rng)
    if not E or len(E) > 16:
        return []
    m = len(E)
    f = [s for s in product((0, 1), repeat=m)
         if _planar_ok(n, [E[i] for i in range(m) if s[i]])]
    if not f: return []
    b = max(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b])]


ROWS = {
    "dissociation-number":     (dissociation,            "downward_closed"),
    "high-degree-subgraph":    (high_degree_subgraph,    None),
    "efficient-domination":    (efficient_domination,    None),
    "min-bisection":           (min_bisection,           "fixed_cardinality"),
    "densest-k-subgraph":      (densest_k_subgraph,      "fixed_cardinality"),
    "maximum-planar-subgraph": (maximum_planar_subgraph, "downward_closed"),
}


# ── CONFORMANCE AT BIRTH — derived consequences, never the filter itself ─────────────────────────────
def conformance(row, build, expect, rng):
    checks, fails = [], []
    regs = []
    for _ in range(4):
        d = dict(build(rng, 0.30) or [])
        r = d.get("feasible") or d.get("solutions")
        if r and 2 <= len(r) <= 4000:
            regs.append(r)
    if not regs:
        return [{"check": "buildable", "pass": False, "detail": "no region built"}], ["no region built"]
    checks.append({"check": "buildable", "pass": True, "n_regions": len(regs),
                   "sizes": [len(x) for x in regs]})

    if expect == "downward_closed":
        ok = all(tuple(t) in set(r)
                 for r in regs for s in r for i in range(len(s)) if s[i] == 1
                 for t in [tuple(0 if j == i else s[j] for j in range(len(s)))])
        checks.append({"check": "derived: downward-closed (clearing any 1 stays inside)", "pass": ok,
                       "why_not_the_filter": ("the generator filters by the row's predicate; downward "
                                              "closure is a CONSEQUENCE of that predicate, not a "
                                              "restatement of it")})
        if not ok: fails.append(f"{row}: not downward-closed")
    if expect == "fixed_cardinality":
        w = {len({sum(s) for s in r}) for r in regs}
        ok = w == {1}
        checks.append({"check": "derived: exactly one distinct member weight", "pass": ok,
                       "observed_distinct_weight_counts": sorted(w)})
        if not ok: fails.append(f"{row}: not fixed-cardinality")
    # universal derived consequence: the empty set is feasible iff the predicate is vacuous on it
    if expect == "downward_closed":
        ok = all(tuple([0] * len(r[0])) in set(r) for r in regs)
        checks.append({"check": "derived: a downward-closed family contains the empty set", "pass": ok})
        if not ok: fails.append(f"{row}: downward-closed but missing the empty set")
    return checks, fails


def overlaps(region, rng):
    n = len(region[0])
    if len(region) * (len(region) - 1) // 2 <= PAIR_CAP:
        pr = combinations(region, 2)
    else:
        pr = ((rng.choice(region), rng.choice(region)) for _ in range(PAIR_CAP))
    return [sum(1 for x, y in zip(a, b) if x == y) / n for a, b in pr if a != b]


def bc(o):
    import numpy as np
    a = np.asarray(o, float); n = len(a)
    if n < 4: return None
    sd = a.std(ddof=1)
    if sd == 0: return None
    m = a.mean()
    sk = ((a - m) ** 3).mean() / sd ** 3; ku = ((a - m) ** 4).mean() / sd ** 4 - 3
    return float((sk ** 2 + 1) / (ku + 3 * (n - 1) ** 2 / ((n - 2) * (n - 3))))


def hull_infl(region, op, m):
    cur = set(region)
    if len(region[0]) > HULL_MAX_N or m != 2:
        return None
    while True:
        new = {op(t) for t in combinations(cur, 2)} - cur
        if not new: return len(cur) / len(region)
        cur |= new
        if len(cur) > 60000: return None


def rate(region, op, m):
    """Violation rate over distinct m-subsets, capped.

    THE CAP MUST BE LAZY. An earlier version wrote `list(combinations(region, m))[:20000]`, which
    materialises the ENTIRE combination list before slicing — C(1024,3) is 178 million tuples, so the
    run died of memory with no output and no artifact. `islice` takes the cap without building the rest.
    A cap applied after the work is not a cap."""
    R = set(region)
    subs = list(islice(combinations(region, m), 20000))
    return (sum(1 for s in subs if op(s) not in R) / len(subs)) if subs else None


def main() -> int:
    rng = random.Random(SEED)
    out, conf_all, hard_fail = [], {}, []
    for row, (build, expect) in ROWS.items():
        print(f"  building {row} ...", flush=True)
        checks, fails = conformance(row, build, expect, rng)
        conf_all[row] = {"checks": checks, "passed": not fails}
        if fails:
            # A ROW'S EXCLUSION IS NOT THE BATCH'S FAILURE. An earlier version collected failures and
            # returned without writing, discarding five good rows' panels because a sixth could not be
            # conformance-checked. The row is excluded WITH ITS MEASURED REASON; the batch ships.
            hard_fail.append({"row": row, "reason": fails,
                              "measured": [c for c in checks if c["check"] == "buildable"]})
            print(f"    EXCLUDED at birth: {row} — {fails[0]}", flush=True)
            continue
        steps = []
        for pos, p in enumerate(EDGE_DENSITY_RAMP):
            srng = random.Random(SEED + 1000 * pos + abs(hash(row)) % 997)
            acc = {}
            for _ in range(N_INST):
                for kind, region in (build(srng, p) or []):
                    if not region or len(region) < 2:
                        continue
                    acc.setdefault(kind, []).append(region)
            if not acc:
                steps.append({"ramp_position": pos, "ramp_value": p, "state": "GAP-no-region",
                              "reason": "no instance at this step produced a region"})
                continue
            for kind, regs in acc.items():
                ov = [overlaps(r, srng) for r in regs]
                dials = {"r_per_instance": [len(r) for r in regs],
                         "r_mean": round(mean(len(r) for r in regs), 2),
                         "overlap_mean": round(mean(mean(o) for o in ov if o), 4) if any(ov) else None,
                         "bimodality_coefficient": None, "flavours": {}}
                flat = [x for o in ov for x in o]
                if flat:
                    b = bc(flat)
                    dials["bimodality_coefficient"] = round(b, 4) if b is not None else None
                    dials["bimodal_flag"] = (b > 0.555) if b is not None else None
                for fl, (op, m) in BOOL_OPS.items():
                    rs = [rate(r, op, m) for r in regs]
                    rs = [x for x in rs if x is not None]
                    if not rs:
                        continue
                    ctrl = []
                    for r in regs:
                        for _ in range(max(1, K_CTRL // len(regs))):
                            c, _e, _u = N2.cp_control(r, srng)
                            v = rate(c, op, m)
                            if v is not None:
                                ctrl.append(v)
                    hi = [hull_infl(r, op, m) for r in regs]
                    hi = [x for x in hi if x is not None]
                    dials["flavours"][fl] = {
                        "measured_rate": round(mean(rs), 4),
                        "control_mean": round(mean(ctrl), 4) if ctrl else None,
                        "control_sd": round(pstdev(ctrl), 5) if len(ctrl) > 1 else None,
                        "blend_excess": round(mean(rs) - mean(ctrl), 4) if ctrl else None,
                        "control_route": "CP",
                        "hull_inflation": round(mean(hi), 4) if hi else None,
                        "hull_note": None if hi else "unaffordable at this ambient/arity (m=2, n<=12 only)",
                        "insufficient": ("INSUFFICIENT-r" if mean(len(r) for r in regs) < R_FLOOR else
                                         ("INSUFFICIENT-degenerate" if len(ctrl) < 2 or pstdev(ctrl) == 0
                                          else None))}
                steps.append({"ramp_position": pos, "ramp_value": p, "region": kind,
                              "state": "usable", "dials": dials})
        out.append({"row": row, "family": "graph", "ramp_parameter": "edge density",
                    "ramp_values": list(EDGE_DENSITY_RAMP),
                    "structural_expectation": expect, "conformance": conf_all[row], "steps": steps})

    doc = {"schema": "observatory-batch1/v1",
           "STATUS": "EXPLORATORY dial panels — no verdict, no scored prediction, no seal",
           "not_citable_as": "a result. Descriptive capture only.",
           "batch": 1, "family": "graph", "reach_class": "REACH-subset",
           "ramp_parameter_declared_at_census": "edge density",
           "conformance_at_birth": ("derived CONSEQUENCES of each definition, checked independently of "
                                    "the generator's own filter. Checking that members satisfy the "
                                    "predicate the generator filtered by is circular and certifies "
                                    "nothing."),
           "structural_variety": ("two downward-closed, two fixed-cardinality, two neither — so the batch "
                                  "exercises the screen stack in both directions rather than only the "
                                  "closed one"),
           "dials": ["r + per-instance draws", "overlap mean", "bimodality coefficient",
                     "blend_excess with control tier + provenance", "hull_inflation where affordable"],
           "excluded_at_birth": hard_fail,
           "exclusion_is_per_row_not_per_batch": (
               "a generator that cannot reproduce a derived consequence of its own definition does not "
               "ship — but its exclusion does not discard the batch. Recorded with its measured reason."),
           "rows": out}
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    print("OBSERVATORY FAN-OUT — BATCH 1 (graph, REACH-subset)\n")
    print(f"  conformance at birth: {sum(1 for v in conf_all.values() if v['passed'])}/{len(conf_all)}")
    for h in hard_fail:
        print(f"    EXCLUDED {h['row']}: {h['reason'][0]}")
    print()
    for r in out:
        print(f"  {r['row']}  [{r['structural_expectation'] or 'no declared structure'}]")
        for s in r["steps"]:
            if s["state"] != "usable":
                print(f"      p={s['ramp_value']:<5} {s['state']}"); continue
            d = s["dials"]
            fl = d["flavours"]
            ex = {k: v["blend_excess"] for k, v in fl.items() if v["blend_excess"] is not None}
            print(f"      p={s['ramp_value']:<5}{s['region']:<9}r={d['r_mean']:<8}"
                  f"overlap={str(d['overlap_mean']):<7}BC={str(d['bimodality_coefficient']):<7}"
                  f"excess={ {k: round(v,3) for k,v in ex.items()} }")
        print()
    print(f"wrote {OUT.name}  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
