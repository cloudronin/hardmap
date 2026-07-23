"""Pebble P2 — the three-pole calibration RUN (prereg_v17). Measures reach_score for short(decoupled) / medium
(2-SAT) / long(2-affine) under BOTH pre-registered observables (corr, forcing) with the dpll sampler; the observable
that recovers the sealed ordering short<medium<long (non-overlapping intervals) is the qualified one. Then, for the
qualified observable: two-sampler concordance (dpll vs walksat) and the affine-exact ground-truth bias check on the
affine long pole. Writes results/landscape/reach_calibration.json.

Run: PYTHONPATH=... python foundry/dev/reach_calibrate.py
"""
import json

from foundry import reach as X

N, ALPHA, NINST, K = 16, 1.4, 8, 80
CONCORD_FLOOR = 0.10          # |reach_score(dpll) - reach_score(walksat)| must sit within this glitch floor
BIAS_FLOOR = 0.12             # |reach_score(dpll) - reach_score(affine_exact)| on the affine arm


def main():
    out = {"prereg": "v17", "n": N, "alpha": ALPHA, "n_instances": NINST, "sampler": "dpll", "observables": {}}
    print(f"three-pole calibration: n={N} alpha={ALPHA} n_instances={NINST}\n")

    for obs in ("corr", "forcing"):
        cal = X.three_pole_calibration(domain=(0, 1), n=N, alpha=ALPHA, observable=obs, sampler="dpll",
                                       n_instances=NINST, K=K)
        out["observables"][obs] = cal
        sc = cal["reach_scores"]
        print(f"[{obs}] short={sc['short']} medium={sc['medium']} long={sc['long']}  "
              f"ordered={cal['ordered_short_lt_medium_lt_long']} nonoverlap={cal['intervals_nonoverlapping']} "
              f"PASS={cal['PASS']}")
        print(f"      intervals: {cal['intervals']}")

    qualified = [o for o, c in out["observables"].items() if c["PASS"]]
    out["qualified_observable"] = qualified[0] if qualified else None
    print(f"\nqualified observable (recovers sealed ordering): {out['qualified_observable']}")

    if out["qualified_observable"]:
        obs = out["qualified_observable"]
        # two-sampler concordance (dpll vs walksat) on all three poles
        ws = X.three_pole_calibration(domain=(0, 1), n=N, alpha=ALPHA, observable=obs, sampler="walksat",
                                      n_instances=NINST, K=K)
        dp = out["observables"][obs]["reach_scores"]
        concord = {p: round(abs(dp[p] - ws["reach_scores"][p]), 4) for p in ("short", "medium", "long")}
        out["concordance_dpll_vs_walksat"] = {"deltas": concord, "floor": CONCORD_FLOOR,
                                              "within_floor": all(v <= CONCORD_FLOOR for v in concord.values()),
                                              "walksat_scores": ws["reach_scores"]}
        # affine-exact ground-truth bias check on the affine (long) pole
        exact_long = X.measure_reach((X.R_EQ,), (0, 1), N, ALPHA, observable=obs, sampler="affine_exact",
                                     n_instances=NINST, base_seed=808000 + 1, K=K)
        bias = round(abs(dp["long"] - exact_long["reach_score"]), 4)
        out["affine_exact_bias_check"] = {"dpll_long": dp["long"], "affine_exact_long": exact_long["reach_score"],
                                          "bias": bias, "floor": BIAS_FLOOR, "within_floor": bias <= BIAS_FLOOR}
        print(f"concordance dpll-vs-walksat deltas={concord} within_floor="
              f"{out['concordance_dpll_vs_walksat']['within_floor']}")
        print(f"affine-exact bias on long pole: {bias} (floor {BIAS_FLOOR}) within="
              f"{out['affine_exact_bias_check']['within_floor']}")
        out["VERDICT"] = ("QUALIFIED" if out["concordance_dpll_vs_walksat"]["within_floor"]
                          and out["affine_exact_bias_check"]["within_floor"] else "QUALIFIED_ORDERING_CHECK_SAMPLERS")
    else:
        # neither observable orders the poles -> pole-behavior diagnostic BEFORE any NOT-QUALIFIED call (prereg_v17)
        out["VERDICT"] = "ORDERING_FAILED_RUN_POLE_BEHAVIOR_DIAGNOSTIC"

    json.dump(out, open("foundry/foundry/results/landscape/reach_calibration.json", "w"), indent=2)
    print(f"\nVERDICT: {out['VERDICT']}")


if __name__ == "__main__":
    main()
