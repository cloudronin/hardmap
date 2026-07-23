"""Pebble P2b — point-to-set calibration. v22 REDESIGN #1: reach_score = signal at the FIXED radius r=2 (before the
finite-size collapse); ALL poles CONNECTED (kills the low-density small-component confound). Criterion honest to the
Boolean point-to-set DICHOTOMY: the affine/parity group reads HIGH, the bounded-width group reads LOW, non-overlapping
between groups, PARITY AT THE TOP (the exact inversion of corr). B1 population report + B2 verdict.

Run: PYTHONPATH=... python foundry/dev/pointset_calibrate.py
"""
import json
from itertools import product

from foundry import pointset as PS
from foundry import reach as X

R3_XOR = frozenset({(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)})

N, NINST, RADIUS = 16, 8, 2
# (label, relations, alpha, seed, group)
POLES = [
    ("parity (3-XOR)", (R3_XOR,), 0.6, 863000, "HIGH"),
    ("2-affine (equality)", (X.R_EQ,), 0.6, 864000, "HIGH"),
    ("2-SAT @0.9", (X.R_IMP,), 0.9, 862000, "LOW"),
    ("2-SAT @1.6", (X.R_IMP,), 1.6, 866000, "LOW"),
]


def main():
    out = {"prereg": "v22", "n": N, "n_instances": NINST, "reach_radius": RADIUS, "poles": {}}
    print(f"=== point-to-set calibration (v22): reach_score = signal @ r={RADIUS} ===")
    for name, rels, alpha, seed, grp in POLES:
        m = PS.measure_pointset(rels, (0, 1), N, alpha, n_instances=NINST, base_seed=seed, reach_radius=RADIUS)
        m["group"] = grp
        m["reach_interval"] = X.boot_interval(m["per_unit_reach"]) if len(m["per_unit_reach"]) >= 2 else (None, None)
        out["poles"][name] = m
        r2 = m["radii"].get(RADIUS, {})
        print(f"\n{name}  [{grp}]  alpha={alpha}  coset~{m['median_coset']} exact_frac={m['exact_fraction']}")
        print(f"   per-radius signal: {[(r, c['signal']) for r, c in m['radii'].items()]}")
        print(f"   reach_score(@r={RADIUS})={m['reach_score']} interval={m['reach_interval']} "
              f"(mean_buckets={r2.get('mean_buckets')}, measurable={r2.get('measurable')})")

    P = out["poles"]
    hi = {k: v for k, v in P.items() if v["group"] == "HIGH"}
    lo = {k: v for k, v in P.items() if v["group"] == "LOW"}
    hi_lows = [v["reach_interval"][0] for v in hi.values() if v["reach_interval"][0] is not None]
    lo_highs = [v["reach_interval"][1] for v in lo.values() if v["reach_interval"][1] is not None]
    groups_separate = bool(hi_lows and lo_highs and min(hi_lows) > max(lo_highs))
    parity = P["parity (3-XOR)"]["reach_score"]
    parity_top = parity is not None and parity == max(v["reach_score"] for v in P.values() if v["reach_score"] is not None)
    verdict = "QUALIFIED" if (groups_separate and parity_top) else "NOT_QUALIFIED_see_report"
    out["verdict"] = {"reach_scores": {k: v["reach_score"] for k, v in P.items()},
                      "HIGH_group_min_interval_low": min(hi_lows) if hi_lows else None,
                      "LOW_group_max_interval_high": max(lo_highs) if lo_highs else None,
                      "groups_separate": groups_separate, "parity_at_top": parity_top, "VERDICT": verdict}
    json.dump(out, open("foundry/foundry/results/landscape/pointset_calibration.json", "w"), indent=2)
    print(f"\n=== verdict ===\nreach_scores: {out['verdict']['reach_scores']}")
    print(f"HIGH group min-low={out['verdict']['HIGH_group_min_interval_low']}  "
          f"LOW group max-high={out['verdict']['LOW_group_max_interval_high']}  "
          f"separate={groups_separate}  parity_at_top={parity_top}")
    print(f"VERDICT: {verdict}")


if __name__ == "__main__":
    main()
