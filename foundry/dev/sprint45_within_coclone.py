"""Sprint 4.5 — within-co-clone replication (prereg_v8 gate). Does measured ruggedness cluster within a co-clone
(census roster survives for measured columns, coarse caveat) or scatter (measured columns need relation-level
sampling)?

Rigor fix: to guarantee representatives share a co-clone, ENUMERATE all non-trivial arity-3 Boolean relations,
group by the IDENTICAL 6-flag polymorphism profile the census uses (0valid,1valid,horn,dualhorn,bij,affine), and
measure 3 fixed-seed-chosen representatives within each tractable, satisfiable co-clone. Same profile => same
census charges => same census "co-clone"; so within-group ruggedness spread is the exact test.

Run: PYTHONPATH=... python foundry/dev/sprint45_within_coclone.py
"""
import json
import random
import statistics as st
from itertools import combinations, product

from foundry import ensemble as E
from foundry import landscape_run as LR
from foundry import postlattice as PL
from foundry import solscape as S

T3 = list(product((0, 1), repeat=3))                      # the 8 arity-3 tuples


def pkey(rels):
    flags = (("0v", PL.is_0valid(rels)), ("1v", PL.is_1valid(rels)), ("horn", PL.has_polymorphism(rels, PL.HORN)),
             ("dhorn", PL.has_polymorphism(rels, PL.DUAL_HORN)), ("bij", PL.has_polymorphism(rels, PL.BIJUNCTIVE)),
             ("aff", PL.has_polymorphism(rels, PL.AFFINE)))
    return tuple(n for n, ok in flags if ok)


def enumerate_coclones():
    """Group non-trivial arity-3 relations (4..7 tuples, so they constrain but stay satisfiable-rich) by profile."""
    groups = {}
    for k in (4, 5, 6, 7):
        for combo in combinations(T3, k):
            R = frozenset(combo)
            key = pkey((R,))
            if not key:                                   # skip NP-hard-region (no tractable polymorphism)
                continue
            groups.setdefault(key, []).append(R)
    return groups


def measure(R, n=18):
    a_struct, _ = LR.locate_alpha_struct((R,), (0, 1), n, 88000, K=35)
    scores = []
    for frac in (0.7, 0.9):
        r = S.landscape_reading((R,), (0, 1), n, round(frac * a_struct, 3), base_seed=88500, K=35, n_instances=4)
        if r["pooled_score"] is not None:
            scores.append(r["pooled_score"])
    return round(st.mean(scores), 3) if scores else None


def main():
    groups = enumerate_coclones()
    # keep tractable co-clones with >= 3 distinct representatives; pick 3 per group (fixed seed, no cherry-pick)
    rng = random.Random("sprint45")
    out = {}
    for key, members in sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        if len(members) < 3:
            continue
        reps = rng.sample(members, 3)
        rows = []
        for R in reps:
            rows.append({"relation": sorted(tuple(t) for t in R), "ruggedness": measure(R)})
        vals = [x["ruggedness"] for x in rows if x["ruggedness"] is not None]
        spread = round(max(vals) - min(vals), 3) if len(vals) > 1 else None
        out["+".join(key)] = {"profile": list(key), "n_relations_in_coclone": len(members),
                              "representatives": rows, "within_coclone_spread": spread}
        print(f"{'+'.join(key):22s} (n={len(members):3d})  reps={[x['ruggedness'] for x in rows]}  spread={spread}")
    spreads = [v["within_coclone_spread"] for v in out.values() if v["within_coclone_spread"] is not None]
    max_spread = max(spreads) if spreads else None
    verdict = "SCATTER" if (max_spread is not None and max_spread >= 0.15) else "CLUSTER"
    out["_verdict"] = {"max_within_coclone_spread": max_spread, "verdict": verdict, "n_coclones_tested": len(spreads),
                       "rule": "SCATTER if any co-clone's within-spread >= 0.15 (measured columns need relation-"
                               "level sampling); else CLUSTER (census roster survives with a coarse-class caveat)"}
    json.dump(out, open("foundry/foundry/results/landscape/sprint45_within_coclone.json", "w"), indent=2)
    print(f"\n{len(spreads)} co-clones tested; MAX within-co-clone spread = {max_spread}  ->  VERDICT: {verdict}")


if __name__ == "__main__":
    main()
