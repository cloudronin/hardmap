#!/usr/bin/env python3
"""Sounding v1 — the qualified blend probe deployed on natural rows (prereg_v17, pilot S1).

WHAT THIS IS. Probe A, qualified on the Boolean roster, taken to the population it was built for: natural
problems, where closure anatomy is underivable for 317 of 345 rows. Named plainly in the seal: this is the
legitimate revival of Terroir-C's question on a NEW instrument and a NEW population. Nothing sealed shut is
reopened.

THE REAL COST, stated because it is the reason this is a pilot. Each row needs an instance GENERATOR and a
solution ENUMERATOR written by hand. That is per-row engineering and it does not amortise.

DESIGN LAWS, APPLIED FROM BIRTH (prereg_v17):
  1. DISTINCT m-SUBSETS ONLY. Blend operations are idempotent on repeats, so a repeat-bearing tuple cannot
     violate and a uniform-tuple rate is mechanically capped — its SHAPE forced by the denominator
     (methods 35). Every rate here is over distinct subsets and ships with r, the subset count, and the
     uniform cap for reference. The typed null is built in, not retrofitted.
  2. FIXED-LENGTH VECTOR ENCODING ONLY. Permutation-structured rows are `n.a.-encoding`, typed out.
  3. TWO REGIONS for optimization rows — FEASIBLE and OPTIMAL, measured separately, NEVER pooled. Feasible
     vertex covers are union-tolerant; optimal ones are not.
  4. ENSEMBLES DECLARED per row: family, parameters, sizes, seeds, counts. F2-typed throughout — a
     violation rate is a property of (problem, ensemble), never a worst-case charge.

S-1 IS THEOREM-FORCED ON CSP ROWS AND FEASIBLE REGIONS, and is sealed as calibration only: if Gamma is
closed under f then every instance's solution set is closed under f — that is what a polymorphism IS.
The OPTIMAL regions are not forced, and are the genuinely measured part.
"""
import hashlib
import json
import random
import sys
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
LAT = ROOT / "foundry" / "results" / "lattice"
OUT = LAT / "sounding_v1_results.json"
SEED = 20260726
MAX_SUBSETS = 20000          # exhaustive below this many distinct m-subsets, else sampled
N_INSTANCES = 12

# ── blend operations, per domain ──────────────────────────────────────────────────────────────────────
BOOL_OPS = {
    "majority": (lambda ts: tuple(1 if sum(c) >= 2 else 0 for c in zip(*ts)), 3),
    "minority": (lambda ts: tuple(c[0] ^ c[1] ^ c[2] for c in zip(*ts)), 3),
    "min":      (lambda ts: tuple(min(c) for c in zip(*ts)), 2),
    "max":      (lambda ts: tuple(max(c) for c in zip(*ts)), 2),
}
D3_OPS = {
    "median":    (lambda ts: tuple(sorted(c)[1] for c in zip(*ts)), 3),
    "maltsev3":  (lambda ts: tuple((c[0] - c[1] + c[2]) % 3 for c in zip(*ts)), 3),
    "min":       (lambda ts: tuple(min(c) for c in zip(*ts)), 2),
    "max":       (lambda ts: tuple(max(c) for c in zip(*ts)), 2),
}

# theorem-forced pairings: (row, region) -> {flavor: expected rate 0.0}. S-1's battery.
FORCED = {
    ("sat-2", "solutions"): ["majority"],
    ("horn-sat", "solutions"): ["min"],
    ("xor-sat", "solutions"): ["minority"],
    ("bipartiteness", "solutions"): ["minority"],
    ("vertex-cover", "feasible"): ["max"],        # a superset of a cover is a cover
    ("independent-set", "feasible"): ["min"],     # a subset of an independent set is independent
    ("clique", "feasible"): ["min"],
}


# ── generators + enumerators (the per-row engineering) ────────────────────────────────────────────────
def cnf_instances(n, m, k, mode, rng):
    cls = []
    for _ in range(m):
        vs = rng.sample(range(n), k)
        if mode == "horn":
            signs = [1] + [0] * (k - 1)
            rng.shuffle(signs)
            signs = [1 if i == signs.index(1) else 0 for i in range(k)] if 1 in signs else [0] * k
        elif mode in ("xor", "nae", "1in3"):
            signs = [rng.randint(0, 1) for _ in range(k)]
        else:
            signs = [rng.randint(0, 1) for _ in range(k)]
        cls.append((tuple(vs), tuple(signs)))
    return cls


def cnf_solutions(n, cls, mode):
    out = []
    for a in product((0, 1), repeat=n):
        ok = True
        for vs, sg in cls:
            vals = [a[v] for v in vs]
            if mode == "xor":
                if sum(vals) % 2 != (sum(sg) % 2):
                    ok = False
            elif mode == "nae":
                if len(set(vals)) == 1:
                    ok = False
            elif mode == "1in3":
                if sum(vals) != 1:
                    ok = False
            else:                                   # plain / horn clause
                if not any(vals[i] == sg[i] for i in range(len(vs))):
                    ok = False
            if not ok:
                break
        if ok:
            out.append(a)
    return out


def graph(n, p, rng):
    return [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < p]


def vc_sets(n, edges):
    feas = [s for s in product((0, 1), repeat=n) if all(s[i] or s[j] for i, j in edges)]
    if not feas:
        return [], []
    best = min(sum(s) for s in feas)
    return feas, [s for s in feas if sum(s) == best]


def is_sets(n, edges):
    feas = [s for s in product((0, 1), repeat=n) if all(not (s[i] and s[j]) for i, j in edges)]
    if not feas:
        return [], []
    best = max(sum(s) for s in feas)
    return feas, [s for s in feas if sum(s) == best]


def clique_sets(n, edges):
    E = {(min(a, b), max(a, b)) for a, b in edges}
    feas = [s for s in product((0, 1), repeat=n)
            if all((min(i, j), max(i, j)) in E for i in range(n) for j in range(i + 1, n) if s[i] and s[j])]
    best = max(sum(s) for s in feas)
    return feas, [s for s in feas if sum(s) == best]


def maxcut_sets(n, edges):
    feas = list(product((0, 1), repeat=n))                      # every bipartition is feasible
    def cut(s): return sum(1 for i, j in edges if s[i] != s[j])
    best = max(cut(s) for s in feas)
    return feas, [s for s in feas if cut(s) == best]


def col3_sets(n, edges):
    feas = [s for s in product((0, 1, 2), repeat=n) if all(s[i] != s[j] for i, j in edges)]
    return feas, feas


def subsetsum_sets(nums, target):
    feas = [s for s in product((0, 1), repeat=len(nums))
            if sum(v for v, b in zip(nums, s) if b) == target]
    return feas, feas


def partition_sets(nums):
    tot = sum(nums)
    feas = list(product((0, 1), repeat=len(nums)))
    def diff(s): return abs(2 * sum(v for v, b in zip(nums, s) if b) - tot)
    best = min(diff(s) for s in feas)
    return feas, [s for s in feas if diff(s) == best]


# ── the probe: distinct m-subsets only ────────────────────────────────────────────────────────────────
def violation(region, op, m, rng):
    """Rate over ALL-DISTINCT m-subsets. Repeats cannot violate an idempotent blend, so including them
    only inflates the denominator and forces the shape (methods 35)."""
    R = set(region)
    r = len(region)
    if r < m:
        return None, r, 0, None
    from math import comb
    total = comb(r, m)
    cap = 1.0
    for i in range(m):
        cap *= (r - i)
    cap /= r ** m
    if total <= MAX_SUBSETS:
        subs = combinations(range(r), m)
        n_used = total
    else:
        subs = (tuple(rng.sample(range(r), m)) for _ in range(MAX_SUBSETS))
        n_used = MAX_SUBSETS
    bad = sum(1 for idx in subs if op([region[i] for i in idx]) not in R)
    return bad / n_used, r, n_used, round(cap, 4)


ROWS = {
    "sat-2":            dict(fam="sat-csp", dom=2, kind="decision"),
    "sat-3":            dict(fam="sat-csp", dom=2, kind="decision"),
    "horn-sat":         dict(fam="sat-csp", dom=2, kind="decision"),
    "xor-sat":          dict(fam="sat-csp", dom=2, kind="decision"),
    "nae-sat":          dict(fam="sat-csp", dom=2, kind="decision"),
    "one-in-three-sat": dict(fam="sat-csp", dom=2, kind="decision"),
    "bipartiteness":    dict(fam="graph", dom=2, kind="decision"),
    "graph-3-coloring": dict(fam="graph", dom=3, kind="decision"),
    "vertex-cover":     dict(fam="graph", dom=2, kind="optimization"),
    "independent-set":  dict(fam="graph", dom=2, kind="optimization"),
    "clique":           dict(fam="graph", dom=2, kind="optimization"),
    "max-cut":          dict(fam="graph", dom=2, kind="optimization"),
    "subset-sum":       dict(fam="number-theoretic", dom=2, kind="decision"),
    "number-partitioning": dict(fam="number-theoretic", dom=2, kind="optimization"),
}


def regions_for(row, rng):
    """Returns [(region_name, [solution vectors])] for one generated instance, or [] if the instance is
    degenerate (empty region)."""
    if row in ("sat-2", "sat-3", "horn-sat", "xor-sat", "nae-sat", "one-in-three-sat"):
        k = {"sat-2": 2}.get(row, 3)
        mode = {"horn-sat": "horn", "xor-sat": "xor", "nae-sat": "nae",
                "one-in-three-sat": "1in3"}.get(row, "plain")
        n, m = 12, {"sat-2": 14, "xor-sat": 8}.get(row, 16)
        cls = cnf_instances(n, m, k, mode, rng)
        sol = cnf_solutions(n, cls, mode)
        return [("solutions", sol)] if sol else []
    if row == "bipartiteness":
        n = 10
        g = graph(n, 0.18, rng)
        sol = [s for s in product((0, 1), repeat=n) if all(s[i] != s[j] for i, j in g)]
        return [("solutions", sol)] if sol else []
    if row == "graph-3-coloring":
        n = 8
        f, o = col3_sets(n, graph(n, 0.35, rng))
        return [("solutions", f)] if f else []
    if row in ("vertex-cover", "independent-set", "clique", "max-cut"):
        n = 11
        g = graph(n, 0.35, rng)
        f, o = {"vertex-cover": vc_sets, "independent-set": is_sets,
                "clique": clique_sets, "max-cut": maxcut_sets}[row](n, g)
        return [("feasible", f), ("optimal", o)] if f and o else []
    if row == "subset-sum":
        nums = [rng.randint(1, 30) for _ in range(13)]
        tgt = sum(nums[i] for i in rng.sample(range(13), 5))
        f, o = subsetsum_sets(nums, tgt)
        return [("solutions", f)] if f else []
    if row == "number-partitioning":
        nums = [rng.randint(1, 40) for _ in range(12)]
        f, o = partition_sets(nums)
        return [("feasible", f), ("optimal", o)] if f and o else []
    return []


def main() -> int:
    rng = random.Random(SEED)
    rows_out = {}
    for row, meta in ROWS.items():
        ops = BOOL_OPS if meta["dom"] == 2 else D3_OPS
        acc = {}
        n_ok = 0
        for _ in range(N_INSTANCES):
            regs = regions_for(row, rng)
            if not regs:
                continue
            n_ok += 1
            for rname, region in regs:
                for fl, (op, m) in ops.items():
                    rate, r, nsub, cap = violation(region, op, m, rng)
                    if rate is None:
                        continue
                    d = acc.setdefault(rname, {}).setdefault(fl, {"rates": [], "r": [], "caps": []})
                    d["rates"].append(rate); d["r"].append(r); d["caps"].append(cap)
        prof = {}
        for rname, fls in acc.items():
            prof[rname] = {}
            for fl, d in fls.items():
                n = len(d["rates"])
                prof[rname][fl] = {
                    "mean_rate": round(sum(d["rates"]) / n, 4),
                    "max_rate": round(max(d["rates"]), 4),
                    "n_instances": n,
                    "mean_r": round(sum(d["r"]) / n, 1),
                    "mean_uniform_cap_for_reference": round(sum(d["caps"]) / n, 4),
                    "distinct_subsets_only": True}
        rows_out[row] = {"family": meta["fam"], "domain": meta["dom"], "kind": meta["kind"],
                         "n_instances_usable": n_ok, "profile": prof}
        print(f"  {row:<21} instances {n_ok:>3}  regions {list(prof)}")
    doc = {"schema": "sounding-v1/v1", "prereg": "prereg_v17", "seed": SEED,
           "F2_law": ("a violation rate is a property of (problem, ensemble). It NEVER impersonates a "
                      "worst-case charge."),
           "design_law_1": ("all rates over DISTINCT m-subsets only; r, subset count and the uniform-tuple "
                            "cap ship beside every rate so the deflator species cannot recur"),
           "design_law_3": "optimization rows report FEASIBLE and OPTIMAL regions separately, never pooled",
           "n_rows_attempted": len(ROWS),
           "rows": rows_out}
    OUT.write_text(json.dumps(doc, indent=1) + "\n")
    print(f"\nwrote {OUT.name}  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
