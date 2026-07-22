"""Sprint 4.6 roster build + terrain measurement (prereg_v11). Arity-3 full + arity-4 sampled, grouped by 6-flag
profile; measure ruggedness for a fixed-seed selection of representatives per profile spanning ranks 2,3,4 (+
0/1-valid edge). Coarse alpha_struct scan for throughput. Writes results/landscape/sprint46_roster.json.

Run: PYTHONPATH=... python foundry/dev/sprint46_roster.py
"""
import json
import random
import statistics as st
from itertools import combinations, product

from foundry import postlattice as PL
from foundry import solscape as S
from foundry.landscape_run import locate_alpha_struct
from foundry.rigidity import rigidity_rank

COARSE = [round(0.3 + 0.3 * i, 2) for i in range(14)]     # 0.3 .. 4.2, coarse (throughput)
N = {2: 20, 3: 18, 4: 16}


def profile(R):
    return tuple(n for n, ok in (("0v", PL.is_0valid((R,))), ("1v", PL.is_1valid((R,))),
                                 ("horn", PL.has_polymorphism((R,), PL.HORN)),
                                 ("dhorn", PL.has_polymorphism((R,), PL.DUAL_HORN)),
                                 ("bij", PL.has_polymorphism((R,), PL.BIJUNCTIVE)),
                                 ("aff", PL.has_polymorphism((R,), PL.AFFINE))) if ok)


def tuple_dispersion(R):
    ts = list(R)
    a = len(ts[0])
    if len(ts) < 2:
        return 0.0
    ds = [sum(1 for x, y in zip(ts[i], ts[j]) if x != y) / a
          for i in range(len(ts)) for j in range(i + 1, len(ts))]
    return round(st.mean(ds), 3)


def build_groups():
    groups = {}
    T3, T4 = list(product((0, 1), repeat=3)), list(product((0, 1), repeat=4))
    for k in (4, 5, 6, 7):
        for combo in combinations(T3, k):
            R = frozenset(combo)
            key = profile(R)
            if key:
                groups.setdefault(key, set()).add(R)
    rng = random.Random("4.6roster")
    for _ in range(6000):
        R = frozenset(rng.sample(T4, rng.randint(5, 13)))
        key = profile(R)
        if key:
            groups.setdefault(key, set()).add(R)
    return groups


def measure(R):
    a = len(next(iter(R)))
    n = N[a]
    a_struct, _ = locate_alpha_struct((R,), (0, 1), n, 660000, K=35, grid=COARSE)
    scores = []
    for frac in (0.7, 0.9):
        r = S.landscape_reading((R,), (0, 1), n, round(frac * a_struct, 3), base_seed=661000, K=35, n_instances=4)
        if r["pooled_score"] is not None:
            scores.append(r["pooled_score"])
    return (round(st.mean(scores), 3) if scores else None, a_struct)


def main():
    groups = build_groups()
    rng = random.Random("4.6select")
    # per rank, how many profiles/reps to measure (rank 4 rare -> take all; others capped)
    take_profiles = {4: 99, 3: 4, 2: 4, 0: 3}
    reps_per = {4: 3, 3: 6, 2: 6, 0: 5}
    rows = []
    for key, Rs in groups.items():
        rank, name, edge = rigidity_rank(key)
        rk = 0 if edge else rank
        if rk not in take_profiles:
            continue
        # deterministic profile selection: sort profiles by size desc, take the first take_profiles[rk]
        pass
    # group profiles by rank, pick the largest few per rank, then pick reps
    by_rank = {}
    for key, Rs in groups.items():
        rank, name, edge = rigidity_rank(key)
        rk = 0 if edge else rank
        by_rank.setdefault(rk, []).append((key, sorted(Rs, key=lambda R: (len(R), sorted(R)))))
    for rk, profs in by_rank.items():
        if rk not in take_profiles:
            continue
        profs = sorted(profs, key=lambda kv: -len(kv[1]))[:take_profiles[rk]]
        for key, Rs in profs:
            if len(Rs) < (5 if rk != 4 else 2):
                continue
            reps = Rs[:: max(1, len(Rs) // reps_per[rk])][:reps_per[rk]]
            for R in reps:
                rug, a_struct = measure(R)
                rows.append({"profile": "+".join(key), "rank": rk, "edge": rk == 0, "arity": len(next(iter(R))),
                             "n_tuples": len(R), "density": round(len(R) / 2 ** len(next(iter(R))), 3),
                             "tuple_dispersion": tuple_dispersion(R), "ruggedness": rug, "alpha_struct": a_struct,
                             "relation": sorted(tuple(t) for t in R)})
    json.dump({"n": len(rows), "rows": rows}, open("foundry/foundry/results/landscape/sprint46_roster.json", "w"), indent=2)
    ok = [r for r in rows if r["ruggedness"] is not None]
    print(f"measured {len(ok)}/{len(rows)} relations")
    from collections import Counter
    print("reps by rank:", dict(Counter(r["rank"] for r in ok)))
    print("profiles(>=5 reps) by rank:")
    prof_rank = {}
    for r in ok:
        prof_rank.setdefault((r["rank"], r["profile"]), 0)
        prof_rank[(r["rank"], r["profile"])] += 1
    for rk in sorted({k[0] for k in prof_rank}, reverse=True):
        ge5 = [p for (r, p), c in prof_rank.items() if r == rk and c >= 5]
        print(f"  rank {rk}: {ge5}")


if __name__ == "__main__":
    main()
