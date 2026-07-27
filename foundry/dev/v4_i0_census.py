#!/usr/bin/env python3
"""V4 I-phase — the screen-survival census. THE GATE. No survey, no readings, no seal.

WHY THIS RUNS BEFORE ANYTHING IS RECRUITED. N1's findings recorded that its secondary was unaskable: two of
three region kinds had ZERO decision-easy readings, because the P-labelled rows in those kinds
(max-flow, min-spanning-tree, reachability-stcon, matching) had all been removed upstream by the standing
screens. That was "not fixable by re-analysis". V4's answer is to make screen-survival an ADMISSION
CRITERION, verified on pilot instances before a row joins the ramp.

THE SCREEN STACK, dry-run per (row, region kind, flavour):
  1. theorem_forced        — the join's CLOSED direction: the pinned template's polymorphisms
  2. forced_saturated      — the join's SECOND direction: S1-S5 (methods 40)
  3. INSUFFICIENT-r        — r < 10, the pre-declared floor
  4. INSUFFICIENT-degenerate — no varying control at either ladder rung
A (row, region) pair SURVIVES if at least one flavour clears all four.

THE FLOOR, from the spec and evaluated here rather than argued past:
    the N5 master needs >= 4 easy rows surviving in EACH of `feasible` and `optimal`.
Below that, N5 stays gated and THE CENSUS IS THE FINDING — and the finding would be a real one:
**forced flavours are much of what easiness MEANS**, so easy rows' regions may be intrinsically
screen-mortal, and that is a fact about where the hardness contrast can ever be asked.

RECRUITMENT IS BLIND OTHERWISE. Candidates are chosen on label coverage and screen survival only. No
geometry is consulted — no excess, no violation rate, no hull. This file reads no outcome artifact.
"""
import hashlib
import json
import random
import sys
from itertools import combinations, product
from pathlib import Path
from statistics import pstdev

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "dev"))
LAT = ROOT / "foundry" / "results" / "lattice"
AT = ROOT.parent / "eightfold" / "eightfold" / "results" / "atlas"
OUT = LAT / "v4_i0_census.json"
import sounding_v3_survey as S3                                        # noqa: E402
import sounding_v2 as S2                                               # noqa: E402
import n2_dense_control as N2                                          # noqa: E402
import terrain_score as T                                              # noqa: E402
from sounding_v1 import BOOL_OPS                                       # noqa: E402

SEED, N_PILOT, R_FLOOR = 20260726, 4, 10

# ── THE DIAL-AFFORDABILITY ADMISSION RULE, declared HERE and never mid-run (amendment, item 1) ────────
# hull_inflation is exact-only and m=2-only per the standing V4 scope. |hull| <= 2^n bounds every closure
# round, so affordability is decidable from the ENCODING ALONE, before any region exists:
#     m=2 admits ambient dimension n <= 12   (C(4096,2) = 8.4M, inside a 10M round budget)
#     m=3 would need n <= 8, which no realistic budget lifts — hence m=2 only.
# overlap and its bimodality coefficient are O(r^2 * n) with a pair cap and are affordable everywhere.
HULL_MAX_N_M2 = 12
DIALS = ("blend_excess", "overlap", "bimodality_coefficient", "r", "hull_inflation", "n4_property_flags")

# ── candidate generators. Each returns [(region_kind, region)]. New ones are born with a conformance
#    obligation (below) and are marked `new`. Existing ones are reused, never reimplemented.
def interval_scheduling(rng, n=11):
    """Feasible = pairwise-compatible interval subsets; optimal = max cardinality. P by greedy."""
    iv = []
    for _ in range(n):
        a = rng.randrange(0, 18); iv.append((a, a + rng.randrange(2, 7)))
    ok = lambda s: all(not (iv[i][0] < iv[j][1] and iv[j][0] < iv[i][1])
                       for i, j in combinations([k for k, b in enumerate(s) if b], 2))
    f = [s for s in product((0, 1), repeat=n) if ok(s)]
    if not f:
        return []
    best = max(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == best])]


def bipartite_matching(rng, nl=4, nr=4):
    """Feasible = matchings in a random bipartite graph; optimal = maximum. P by Hopcroft-Karp."""
    edges = [(a, b) for a in range(nl) for b in range(nr) if rng.random() < 0.45]
    if not edges:
        return []
    m = len(edges)
    ok = lambda s: len({e[0] for i, e in enumerate(edges) if s[i]}) == sum(s) and \
                   len({e[1] for i, e in enumerate(edges) if s[i]}) == sum(s)
    f = [s for s in product((0, 1), repeat=m) if ok(s)]
    if not f:
        return []
    best = max(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == best])]


def unit_knapsack(rng, n=12):
    """Unit weights, capacity k: feasible = subsets of size <= k, optimal = size exactly k. Poly."""
    k = rng.randrange(3, 7)
    f = [s for s in product((0, 1), repeat=n) if sum(s) <= k]
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == k])]


def two_colouring(rng, n=10, p=0.28):
    """Proper 2-colourings of a random graph; solutions region. P."""
    E = [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < p]
    f = [s for s in product((0, 1), repeat=n) if all(s[a] != s[b] for a, b in E)]
    return [("solutions", f)] if f else []


CANDIDATES = {
    # row                     builder                                    decision  new?
    "interval-scheduling":   (lambda r: interval_scheduling(r),          "P",      True),
    "bipartite-matching":    (lambda r: bipartite_matching(r),           "P",      True),
    "unit-knapsack":         (lambda r: unit_knapsack(r),                "P",      True),
    "two-colouring":         (lambda r: two_colouring(r),                "P",      True),
    "horn-sat":              (lambda r: S3.sat(r, 2.0, 3, "horn"),       "P",      False),
    "bipartiteness":         (lambda r: S2.regions_for("bipartiteness", r), "P",   False),
    "matching":              (lambda r: S2.regions_for("matching", r),   "P",      False),
    "min-spanning-tree":     (lambda r: S2.regions_for("min-spanning-tree", r), "P", False),
    "reachability-stcon":    (lambda r: S2.regions_for("reachability-stcon", r), "P", False),
    "max-flow":              (lambda r: S2.regions_for("max-flow", r),   "P",      False),
    "sat-2":                 (lambda r: S3.sat(r, 1.0, 2, "plain"),      "P",      False),
    "xor-sat":               (lambda r: S3.sat(r, 0.7, 3, "xor"),        "P",      False),
    "sharp-monotone-2sat":   (lambda r: S3.monotone2(r, 1.3),            "P",      False),
}

SEMILATTICE = ("min", "max")
MONOTONE_OBJECTIVE = {"interval-scheduling": "subset cardinality (maximised)",
                      "bipartite-matching": "edge-set cardinality (maximised)",
                      "unit-knapsack": "item count (maximised)",
                      "matching": "edge-set cardinality (maximised)",
                      "min-spanning-tree": "total edge weight (minimised)"}


def closed(region, op, m):
    R = set(region)
    if len(region) < m:
        return None
    tot = 0
    for t in combinations(region, m):
        tot += 1
        if op(t) not in R:
            return False
        if tot > 200000:
            break
    return True


def saturated(region, op, m):
    """Every non-trivial blend leaves — the forced_saturated direction, measured not asserted."""
    R = set(region)
    if len(region) < m:
        return None
    n = 0
    for t in combinations(region, m):
        if op(t) in R:
            return False
        n += 1
        if n > 50000:
            break
    return True


def control_varies(region, op, m, rng):
    vals = []
    for _ in range(10):
        c, _e, _u = N2.cp_control(region, rng)
        v = _rate(c, op, m)
        if v is not None:
            vals.append(v)
    return len(vals) > 1 and pstdev(vals) > 0


def _rate(region, op, m):
    R = set(region)
    subs = list(combinations(region, m))[:20000]
    return (sum(1 for s in subs if op(s) not in R) / len(subs)) if subs else None


def main() -> int:
    rng = random.Random(SEED)
    rows_out = []
    for row, (build, decision, is_new) in CANDIDATES.items():
        per_kind = {}
        conf = None
        for _ in range(N_PILOT):
            try:
                regs = dict(build(rng) or [])
            except Exception as e:
                per_kind["__error__"] = str(e); break
            for kind, region in regs.items():
                if not region or len(region) < 2:
                    continue
                d = per_kind.setdefault(kind, {"sizes": [], "flavours": {}, "n": len(region[0])})
                d["sizes"].append(len(region))
                d["n"] = len(region[0])
                for fl, (op, m) in BOOL_OPS.items():
                    if len(region) < m:
                        continue
                    st = d["flavours"].setdefault(fl, {"closed": 0, "saturated": 0, "open": 0,
                                                       "below_r_floor": 0, "no_control": 0, "clear": 0})
                    if len(region) < R_FLOOR:
                        st["below_r_floor"] += 1; continue
                    c = closed(region, op, m)
                    s_ = saturated(region, op, m)
                    if c:
                        st["closed"] += 1; continue
                    if s_:
                        st["saturated"] += 1; continue
                    st["open"] += 1
                    if not control_varies(region, op, m, rng):
                        st["no_control"] += 1; continue
                    st["clear"] += 1
        # ambient dimension is a property of the ENCODING, read off a pilot region, not of any outcome
        amb_n = None
        for kind, d in per_kind.items():
            if kind != "__error__" and d["sizes"]:
                amb_n = None
                break
        entry = {"row": row, "decision": decision, "new_generator": is_new, "regions": {},
                 "dial_affordability": {}}
        for kind, d in per_kind.items():
            if kind == "__error__":
                entry["build_error"] = d; continue
            surv = [fl for fl, st in d["flavours"].items() if st["clear"] >= max(1, N_PILOT // 2)]
            entry["regions"][kind] = {
                "ambient_dimension_n": d.get("n"),
                "hull_inflation_affordable_m2": (d.get("n") is not None and d["n"] <= HULL_MAX_N_M2),
                "overlap_affordable": True,
                "pilot_sizes": d["sizes"],
                "median_size": sorted(d["sizes"])[len(d["sizes"]) // 2] if d["sizes"] else None,
                "per_flavour": d["flavours"],
                "surviving_flavours": surv,
                "SURVIVES": bool(surv)}
        rows_out.append(entry)

    # ── the floor, evaluated ────────────────────────────────────────────────────────────────────────
    easy = [e for e in rows_out if e["decision"] == "P"]
    feas = [e["row"] for e in easy if e["regions"].get("feasible", {}).get("SURVIVES")]
    opt = [e["row"] for e in easy if e["regions"].get("optimal", {}).get("SURVIVES")]
    soln = [e["row"] for e in easy if e["regions"].get("solutions", {}).get("SURVIVES")]
    floor_ok = len(feas) >= 4 and len(opt) >= 4

    doc = {"schema": "v4-i0-census/v1",
           "STATUS": "I-PHASE GATE — no survey, no readings, no seal. Reads no outcome artifact.",
           "why": ("N1's secondary was unaskable because two of three region kinds had zero "
                   "decision-easy readings — the P-labelled rows there had been removed upstream by the "
                   "standing screens. V4 makes screen-survival an ADMISSION CRITERION, verified on pilot "
                   "instances before a row joins the ramp."),
           "dial_affordability_rule_declared_here": {
               "hull_inflation": f"exact-only, m=2 only, ambient dimension n <= {HULL_MAX_N_M2}. "
                                 f"|hull| <= 2^n bounds every closure round, so this is decidable from "
                                 f"the ENCODING ALONE before any region exists — the selection is "
                                 f"designed, not discovered. m=3 would need n <= 8 and no realistic "
                                 f"budget lifts it.",
               "overlap_and_bimodality": "O(r^2 n) with a pair cap; affordable at every step",
               "dials": list(DIALS),
               "absence_is_a_record": ("where a dial is unaffordable at a step, that is recorded with "
                                       "its reason — the three-state vocabulary applies to dials too")},
           "typing_boundary": ("cited charges are FIXED ROW LABELS, never ramp-varying quantities. Only "
                               "measured ensemble-typed dials move along a ramp. Nothing here or "
                               "downstream may suggest a charge changes with hardness — that is the F2 "
                               "category error."),
           "screen_stack": ["theorem_forced (closed direction)", "forced_saturated (S1-S5)",
                            f"INSUFFICIENT-r (r < {R_FLOOR})", "INSUFFICIENT-degenerate (no varying control)"],
           "survival_rule": f"a (row, region) pair survives if >= 1 flavour clears all four screens on at "
                            f"least {max(1, N_PILOT//2)} of {N_PILOT} pilot instances",
           "N5_FLOOR": {"required": ">= 4 easy rows surviving in EACH of feasible and optimal",
                        "easy_rows_tested": len(easy),
                        "surviving_feasible": feas, "n_feasible": len(feas),
                        "surviving_optimal": opt, "n_optimal": len(opt),
                        "surviving_solutions": soln, "n_solutions": len(soln),
                        "FLOOR_CLEARS": floor_ok},
           "rows": rows_out}
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    print("V4 I-PHASE — SCREEN-SURVIVAL CENSUS (the gate)\n")
    print(f"  {'row':<22}{'dec':<5}{'new':<5}{'region':<11}{'med |R|':>8}  surviving flavours")
    for e in rows_out:
        if "build_error" in e:
            print(f"  {e['row']:<22}BUILD ERROR: {e['build_error'][:48]}"); continue
        for kind, d in sorted(e["regions"].items()):
            mark = "yes" if d["SURVIVES"] else "NO"
            print(f"  {e['row']:<22}{e['decision']:<5}{'new' if e['new_generator'] else '-':<5}"
                  f"{kind:<11}{str(d['median_size']):>8}  {mark:<4}"
                  f"{','.join(d['surviving_flavours']) if d['surviving_flavours'] else '(none)'}")
    print(f"\n  THE N5 FLOOR — needs >= 4 easy rows in EACH of feasible and optimal")
    print(f"    feasible : {len(feas)}  {feas}")
    print(f"    optimal  : {len(opt)}  {opt}")
    print(f"    solutions: {len(soln)}  {soln}   (not a floor requirement; recorded)")
    print(f"\n  FLOOR {'CLEARS — N5 can be built on this population' if floor_ok else 'DOES NOT CLEAR'}")
    print(f"\nwrote {OUT.name}  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
