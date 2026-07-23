"""Lattice v3 (prereg_v31) — the NATURAL population. Every non-trivial Boolean relation of arity <= 3,
symmetry-deduped up to coordinate permutation (charges are permutation-invariant), x {Min-Ones, Max-Ones}.
NO selection, NO stratification. Reports occupancy (primary) + Cramer's V with a bootstrap CI sized to the
SYMMETRY-CLASS count (not the raw row count), + Spearman direction, + full effective-n accounting. $0.

Run: PYTHONPATH=... python foundry/dev/lattice_v3.py
"""
import json
from collections import Counter
from itertools import permutations, product

import numpy as np

from eightfold import structure as S
from foundry import objective_oracles as OO

SEED, NBOOT = 31, 4000
APX_RANK = {v: i for i, v in enumerate(OO.APPROX_ORDER)}
PAR_RANK = {"FPT": 0, "W[1]": 1}


def all_relations(max_arity=3):
    for a in range(1, max_arity + 1):
        universe = list(product((0, 1), repeat=a))
        m = 2 ** a
        for mask in range(1, 2 ** m - 1):                       # non-empty, non-full
            yield a, frozenset(universe[i] for i in range(m) if (mask >> i) & 1)


def canonical(a, rel):
    """Canonical form under coordinate permutation (min over S_a of the permuted relation as a sorted tuple)."""
    best = None
    for sigma in permutations(range(a)):
        permuted = tuple(sorted(tuple(t[sigma[i]] for i in range(a)) for t in rel))
        if best is None or permuted < best:
            best = permuted
    return (a, best)


def spearman(x, y):
    if len(x) < 3 or len(set(x)) < 2 or len(set(y)) < 2:
        return None
    rx, ry = np.argsort(np.argsort(x)), np.argsort(np.argsort(y))
    return round(float(np.corrcoef(rx, ry)[0, 1]), 3)


def main():
    # symmetry-dedup
    seen, reps = set(), []
    n_raw = 0
    for a, rel in all_relations(3):
        n_raw += 1
        c = canonical(a, rel)
        if c not in seen:
            seen.add(c)
            reps.append((a, rel))
    n_classes = len(reps)

    rows = []
    for a, rel in reps:
        for obj in (OO.MAX_ONES, OO.MIN_ONES):
            apx, par = OO.charges([rel], obj)
            rows.append({"arity": a, "objective": obj, "approximation": apx, "parameterized": par})

    both = [r for r in rows if r["parameterized"] != "open"]
    profiles = sorted({(r["approximation"], r["parameterized"]) for r in both})
    grid = Counter((r["approximation"], r["parameterized"]) for r in both)

    xs = [r["approximation"] for r in both]
    ys = [r["parameterized"] for r in both]
    V = S.cramers_v(xs, ys)
    # direction (Spearman on ordinalized ranks)
    xr = [APX_RANK[r["approximation"]] for r in both]
    yr = [PAR_RANK[r["parameterized"]] for r in both]
    rho = spearman(xr, yr)

    # bootstrap CI sized to the number of independent rows (symmetry-class x objective both-real rows)
    rng = np.random.default_rng(SEED)
    idx = np.arange(len(both))
    boot = []
    for _ in range(NBOOT):
        s = rng.choice(idx, size=len(both), replace=True)
        bx = [both[i]["approximation"] for i in s]
        by = [both[i]["parameterized"] for i in s]
        vb = S.cramers_v(bx, by)
        if vb == vb:                                            # skip nan (degenerate resample)
            boot.append(vb)
    ci = (round(float(np.percentile(boot, 2.5)), 3), round(float(np.percentile(boot, 97.5)), 3)) if boot else None

    par_marginal = Counter(r["parameterized"] for r in both)
    n_profiles = len(profiles)
    uninformative = (ci is not None and ci[0] <= 0.0 and ci[1] >= 0.4)
    coupling_present = (ci is not None and ci[0] > 0.0)

    verdict = ("RESOLUTION-LIMITED — V's CI spans uninformative range given the effective-n" if uninformative
               else ("COUPLING PRESENT over the natural generated Boolean proxy universe" if coupling_present
                     else "NO COUPLING — V's CI includes 0 over the natural generated Boolean proxy universe"))

    out = {"prereg": "v31", "n_raw_relations": n_raw, "n_symmetry_classes": n_classes,
           "n_rows": len(rows), "n_both_real": len(both), "n_distinct_profiles": n_profiles,
           "param_marginal": dict(par_marginal),
           "occupancy": {f"{a} x {p}": c for (a, p), c in sorted(grid.items())},
           "cramers_v": V, "cramers_v_boot_ci95_sized_to_classes": ci, "spearman_direction": rho,
           "verdict": verdict,
           "effective_n_note": ("V's CI is bootstrapped over the %d symmetry-class both-real rows (independent "
                                "observations), NOT the %d raw arity<=3 relations." % (len(both), n_raw)),
           "scope": "natural coupling over the reachable PROXY universe (single-relation Boolean, 2 objectives); "
                    "population-scoped; comparable to 0.73 on the curated-vs-generated axis only.",
           "SEALED_PREDICTION_was": "present+positive, weaker than 0.73 (V~0.15-0.35), ~55% conf"}

    print(f"raw relations={n_raw}  symmetry-classes={n_classes}  rows={len(rows)}  both-real={len(both)}  "
          f"profiles={n_profiles}")
    print(f"param marginal: {dict(par_marginal)}")
    print(f"Cramer's V = {V}   boot CI95 (sized to {len(both)} class-rows) = {ci}   Spearman(direction) = {rho}")
    print(f"VERDICT: {verdict}")
    print("occupancy (approx x param):")
    for (a, p), c in sorted(grid.items()):
        print(f"  {a:28s} x {p:5s} : {c}")
    json.dump(out, open("foundry/foundry/results/lattice/lattice_v3_occupancy.json", "w"), indent=2)
    print("\nwrote lattice_v3_occupancy.json")


if __name__ == "__main__":
    main()
