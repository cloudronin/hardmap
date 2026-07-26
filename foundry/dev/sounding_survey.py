#!/usr/bin/env python3
"""Sounding — SURVEY. Matched-null excess readings on every row with a working generator.

EXPLORATORY. NO SCORED PREDICTIONS. DESCRIPTIVE ONLY.
This is not a study and carries no sealed bet. It is a measured column with full provenance, produced
because the tooling exists and the readings are cheap. Nothing here may be cited as a result; anything
that catches the eye goes to `sounding-survey-banked-questions.md` for a later design to pose properly.

THE STATISTIC (design from the v3 spec, used as METHOD without its sealed predictions):
    excess = rate_measured - mean(rate_control)
where each control is a uniform random subset of the SAME ambient space D^n at the SAME cardinality r.
Every row carries its own size-matched control, so the reading is scale-free by construction — which is
what round 2's failure showed was needed, region size being semantics rather than nuisance.

RAW DIFFERENCE, not z-score: the control mean is empirically flat across a 60x range of r (0.81-0.91)
while the control SD varies 20x, so standardising would divide by the one quantity still tracking region
size. The standardized value ships beside it, unscored, so the rejected choice stays visible.

WHY THESE EXTRA ROWS. `dominating-set`, `exact-cover-x3c` and `three-dimensional-matching` are EXCLUDED
from Marrow's closure columns — their constraint scopes are unbounded-arity, so no fixed finite template
exists to take polymorphisms of. The probe does not care: it enumerates solutions directly. These rows are
the demonstration that this instrument reaches where closure anatomy cannot.
"""
import hashlib
import json
import random
import sys
from itertools import combinations, product
from math import comb, log
from pathlib import Path
from statistics import mean, pstdev

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "dev"))
sys.path.insert(0, str(ROOT.parent / "eightfold"))
from sounding_v1 import BOOL_OPS, D3_OPS, violation                              # noqa: E402
from sounding_v2 import ROWS as FLEET_ROWS, regions_for as fleet_regions, FORCED  # noqa: E402
from sounding_v1 import graph                                                     # noqa: E402
from eightfold import atlas as A                                                  # noqa: E402

LAT = ROOT / "foundry" / "results" / "lattice"
OUT = LAT / "sounding_survey_readings.json"
SEED, N_INST, K_CONTROL, CTRL_CAP = 20260726, 8, 40, 1500
INSUFFICIENT_R = 10

# ── cheap additions, all EXCLUDED from Marrow's closure columns (unbounded-arity scopes) ──────────────
def dominating_sets(n, edges):
    adj = {i: {i} for i in range(n)}
    for a, b in edges:
        adj[a].add(b); adj[b].add(a)
    feas = [s for s in product((0, 1), repeat=n)
            if all(any(s[u] for u in adj[v]) for v in range(n))]
    if not feas:
        return [], []
    best = min(sum(s) for s in feas)
    return feas, [s for s in feas if sum(s) == best]


def exact_cover_sets(n_elems, sets3):
    feas = []
    for s in product((0, 1), repeat=len(sets3)):
        cov = {}
        ok = True
        for i, b in enumerate(s):
            if b:
                for e in sets3[i]:
                    cov[e] = cov.get(e, 0) + 1
                    if cov[e] > 1:
                        ok = False; break
            if not ok:
                break
        if ok and len(cov) == n_elems:
            feas.append(s)
    return feas, feas


def matching3d_sets(triples, n_each):
    feas = []
    for s in product((0, 1), repeat=len(triples)):
        used = [set(), set(), set()]
        ok = True
        for i, b in enumerate(s):
            if b:
                for d in range(3):
                    if triples[i][d] in used[d]:
                        ok = False; break
                    used[d].add(triples[i][d])
            if not ok:
                break
        if ok:
            feas.append(s)
    if not feas:
        return [], []
    best = max(sum(s) for s in feas)
    return feas, [s for s in feas if sum(s) == best]


EXTRA = {
    "dominating-set": ("graph", 2, "opt"),
    "exact-cover-x3c": ("sat-csp", 2, "solutions"),
    "three-dimensional-matching": ("optimization", 2, "opt"),
}
MARROW_EXCLUDED = set(EXTRA)


def extra_regions(row, rng):
    if row == "dominating-set":
        n = 11
        f, o = dominating_sets(n, graph(n, 0.28, rng))
        return [("feasible", f), ("optimal", o)] if f and o else []
    if row == "exact-cover-x3c":
        n_e = 9
        sets3 = [tuple(rng.sample(range(n_e), 3)) for _ in range(14)]
        f, _ = exact_cover_sets(n_e, sets3)
        return [("solutions", f)] if f else []
    if row == "three-dimensional-matching":
        k = 4
        tri = [(rng.randrange(k), rng.randrange(k), rng.randrange(k)) for _ in range(13)]
        f, o = matching3d_sets(tri, k)
        return [("feasible", f), ("optimal", o)] if f and o else []
    return []


def control_profile(r, n, dom, op, m, rng):
    """K uniform random subsets of D^n at cardinality r — matched on BOTH r and n."""
    N = dom ** n
    if r >= N:
        return None, None
    vals = []
    for _ in range(K_CONTROL):
        idx = rng.sample(range(N), r)
        S = []
        for x in idx:
            v = []
            for _ in range(n):
                v.append(x % dom); x //= dom
            S.append(tuple(reversed(v)))
        rate, _, _, _ = violation(S, op, m, rng)
        if rate is not None:
            vals.append(rate)
    if not vals:
        return None, None
    return mean(vals), pstdev(vals)


def main() -> int:
    v3 = {e.problem_id: e for e in A.load_atlas(
        str(ROOT.parent / "eightfold" / "eightfold" / "results" / "atlas" / "atlas_v3.jsonl"))}
    def dec(p): return next((c.value for c in v3[p].charges if c.charge == "decision"), "n.a.")

    rng = random.Random(SEED)
    allrows = dict(FLEET_ROWS); allrows.update(EXTRA)
    readings, skipped = [], []
    for row, (fam, dom, kind) in allrows.items():
        ops = BOOL_OPS if dom == 2 else D3_OPS
        acc = {}
        for _ in range(N_INST):
            regs = extra_regions(row, rng) if row in EXTRA else fleet_regions(row, rng)
            if not regs:
                continue
            for rname, region in regs:
                if not region:
                    continue
                n_amb = len(region[0])
                for fl, (op, m) in ops.items():
                    rate, r, nsub, cap = violation(region, op, m, rng)
                    if rate is None:
                        continue
                    d = acc.setdefault((rname, fl), {"rates": [], "r": [], "n": [], "nsub": [], "cap": []})
                    d["rates"].append(rate); d["r"].append(r); d["n"].append(n_amb)
                    d["nsub"].append(nsub); d["cap"].append(cap)
        for (rname, fl), d in acc.items():
            r_m, n_m = round(mean(d["r"]), 1), int(round(mean(d["n"])))
            measured = mean(d["rates"])
            cmu, csd = control_profile(int(round(r_m)), n_m, dom, ops[fl][0], ops[fl][1], rng)
            rec = {"row": row, "family": fam, "decision": dec(row), "domain": dom,
                   "region": rname, "flavor": fl,
                   "measured_rate": round(measured, 4),
                   "control_mean": round(cmu, 4) if cmu is not None else None,
                   "control_sd": round(csd, 5) if csd is not None else None,
                   "excess": round(measured - cmu, 4) if cmu is not None else None,
                   "standardized_excess_UNSCORED": (round((measured - cmu) / csd, 2)
                                                    if cmu is not None and csd else None),
                   "r": r_m, "ambient_n": n_m, "ambient_size": dom ** n_m,
                   "distinct_subsets_used": int(round(mean(d["nsub"]))),
                   "uniform_tuple_cap_for_reference": round(mean(d["cap"]), 4),
                   "n_instances": len(d["rates"]), "control_draws": K_CONTROL,
                   "theorem_forced": fl in FORCED.get((row, rname), set()),
                   "marrow_excluded_row": row in MARROW_EXCLUDED,
                   "insufficient": "INSUFFICIENT-r" if r_m < INSUFFICIENT_R else None}
            if cmu is None:
                skipped.append({"row": row, "region": rname, "flavor": fl,
                                "why": "region size >= ambient space; no size-matched control exists"})
            else:
                readings.append(rec)

    doc = {"schema": "sounding-survey/v1",
           "STATUS": "EXPLORATORY SURVEY — NO SCORED PREDICTIONS, NO SEALED BET, DESCRIPTIVE ONLY",
           "not_citable_as": ("a result. Nothing here was predicted in advance and nothing here is scored. "
                              "Anything of interest is banked in sounding-survey-banked-questions.md for a "
                              "later design to pose properly."),
           "method": ("excess = measured rate - mean(control), where each control is a uniform random "
                      "subset of the SAME ambient space at the SAME cardinality. Raw difference, not "
                      "z-score: the control mean is empirically flat across r while the control SD varies "
                      "20x, so standardising would divide by the quantity still tracking region size."),
           "provenance": {"seed": SEED, "instances_per_row": N_INST, "control_draws_per_reading": K_CONTROL,
                          "control_subset_cap": CTRL_CAP, "measured_subset_cap": 20000,
                          "distinct_subsets_only": True, "insufficient_r_floor": INSUFFICIENT_R},
           "n_readings": len(readings), "n_rows": len({x["row"] for x in readings}),
           "n_marrow_excluded_rows": len({x["row"] for x in readings if x["marrow_excluded_row"]}),
           "skipped": skipped,
           "readings": readings}
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    rows = sorted({x["row"] for x in readings})
    print(f"SOUNDING SURVEY — {len(readings)} readings over {len(rows)} rows "
          f"({doc['n_marrow_excluded_rows']} Marrow-excluded)\n")
    print(f"{'row':<27}{'dec':<5}{'region':<10}{'flavor':<10}{'meas':>8}{'ctrl':>8}{'excess':>9}{'r':>8}")
    for x in sorted(readings, key=lambda z: (z["row"], z["region"], z["flavor"])):
        mark = " F" if x["theorem_forced"] else ("  !" if x["insufficient"] else "")
        print(f"{x['row']:<27}{x['decision']:<5}{x['region']:<10}{x['flavor']:<10}"
              f"{x['measured_rate']:>8.4f}{x['control_mean']:>8.4f}{x['excess']:>+9.4f}{x['r']:>8.1f}{mark}")
    print(f"\nwrote {OUT.name}  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
