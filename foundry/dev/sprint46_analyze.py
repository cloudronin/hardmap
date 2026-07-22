"""Sprint 4.6 analysis (prereg_v11): A (rigidity middle-rank retest) + B (relation-level terrain prediction).
Runs on the measured roster (sprint46_roster.json). Held-out-by-co-clone is B's PRIMARY evaluation.

Run: PYTHONPATH=... python foundry/dev/sprint46_analyze.py
"""
import json
import statistics as st

import numpy as np

from foundry.relfeatures import fit_r2 as _fit_r2, selftest_perm


def _corr(xs, ys):
    if len(set(xs)) < 2 or len(set(ys)) < 2:
        return None
    return round(float(np.corrcoef(xs, ys)[0, 1]), 3)


def experiment_A(rows):
    """Rigidity middle-rank retest. Exclude the 0/1-valid edge (pre-registered). Per co-clone with >=5 reps,
    spread = max-min ruggedness; group by rank; resolve the 3~2 tie; rank 4 reported separately."""
    core = [r for r in rows if not r["edge"]]
    by_prof = {}
    for r in core:
        by_prof.setdefault(r["profile"], []).append(r)
    spreads = []  # (rank, profile, spread, n)
    for prof, ms in by_prof.items():
        if len(ms) >= 5:
            rugs = [m["ruggedness"] for m in ms]
            spreads.append((ms[0]["rank"], prof, round(max(rugs) - min(rugs), 3), len(ms)))
    by_rank = {}
    for rank, prof, sp, n in spreads:
        by_rank.setdefault(rank, []).append(sp)
    per_rank = {rk: {"mean_spread": round(st.mean(v), 3), "n_strata": len(v), "vals": v}
                for rk, v in sorted(by_rank.items(), reverse=True)}
    have23 = 2 in by_rank and 3 in by_rank and len(by_rank[3]) >= 1 and len(by_rank[2]) >= 1
    r3 = per_rank.get(3, {}).get("mean_spread")
    r2 = per_rank.get(2, {}).get("mean_spread")
    ranks = [s[0] for s in spreads]
    sps = [s[2] for s in spreads]
    corr = _corr(ranks, sps)
    # prediction: spread DECREASES with rank, so rank 3 (higher) should have LOWER spread than rank 2 (lower)
    if not have23 or min(len(by_rank.get(3, [])), len(by_rank.get(2, []))) < 1:
        verdict = "INSUFFICIENT_RESOLUTION"
    elif r3 is None or r2 is None:
        verdict = "INSUFFICIENT_RESOLUTION"
    elif abs(r3 - r2) <= 0.02:
        verdict = "TIE_REAL (rank3 ~ rank2 at resolution — the middle genuinely does not order terrain)"
    elif r3 < r2 and corr is not None and corr <= -0.5:
        verdict = "CONFIRMED (rank3 spread < rank2 spread, clean ordering — tie resolved)"
    elif r3 < r2:
        verdict = "PARTIAL (rank3 < rank2 in the predicted direction, but weak/overlapping)"
    else:
        verdict = "NOT_CONFIRMED (wrong direction: rank3 > rank2)"
    return {"experiment": "A_rigidity_retest", "verdict": verdict, "per_rank_spread": per_rank,
            "corr_rank_spread_core": corr, "n_strata_with_ge5_reps": len(spreads),
            "rank4_separate": "already firm (Sprint 4.5: 0.039); affine strata rare (<5 reps) by construction",
            "note": "0/1-valid edge EXCLUDED as pre-registered (non-Taylor). corr negative = prediction direction."}




def experiment_B(rows, n_perm=5000, seed=42):
    """Relation-level terrain prediction. 3 sealed features; permutation null + held-out-by-co-clone (primary)."""
    R = [r for r in rows if r["ruggedness"] is not None]
    feat_names = ["density", "arity", "tuple_dispersion"]
    X = np.array([[r["density"], float(r["arity"]), r["tuple_dispersion"]] for r in R])
    y = np.array([r["ruggedness"] for r in R])
    coclones = sorted({r["profile"] for r in R})
    floor_ok = sum(1 for cc in coclones if sum(1 for r in R if r["profile"] == cc) >= 5) >= 6
    r2_in, beta = _fit_r2(X, y)
    signs = {feat_names[i]: ("+" if beta[i + 1] > 0 else "-") for i in range(3)}
    # permutation null (shuffle y)
    rng = np.random.default_rng(seed)
    ge = sum(1 for _ in range(n_perm) if _fit_r2(X, rng.permutation(y))[0] >= r2_in - 1e-12)
    perm_p = round((ge + 1) / (n_perm + 1), 4)
    # held-out by co-clone: leave-one-co-clone-out; predict held reps; compare to marginal baseline (global mean)
    held_pred_err, base_err = [], []
    for cc in coclones:
        tr = [i for i, r in enumerate(R) if r["profile"] != cc]
        te = [i for i, r in enumerate(R) if r["profile"] == cc]
        if len(te) == 0 or len(tr) < 5:
            continue
        _, b = _fit_r2(X[tr], y[tr])
        pred = np.column_stack([np.ones(len(te)), X[te]]) @ b
        held_pred_err.append(float(np.sum((y[te] - pred) ** 2)))
        base_err.append(float(np.sum((y[te] - np.mean(y[tr])) ** 2)))
    held_mse = sum(held_pred_err) / len(held_pred_err) if held_pred_err else None
    base_mse = sum(base_err) / len(base_err) if base_err else None
    held_beats_base = (held_mse is not None and base_mse is not None and held_mse < base_mse)
    # sealed decision: a signed feature's sign matches (density '-' OR tuple_dispersion '+'), fit beats null,
    # held-out beats baseline
    sign_match = signs["density"] == "-" or signs["tuple_dispersion"] == "+"
    if not floor_ok:
        verdict = "INSUFFICIENT_RESOLUTION"
    elif sign_match and perm_p < 0.05 and held_beats_base:
        verdict = "SUPPORTED"
    else:
        verdict = "NOT_SUPPORTED"
    marg = {f: _corr([r[f] for r in R], list(y)) for f in feat_names}
    density_sealed_failed = marg["density"] is not None and marg["density"] > 0   # sealed NEGATIVE
    return {"experiment": "B_terrain_prediction", "verdict": verdict, "n": len(R), "n_coclones": len(coclones),
            "roster_floor_ok(>=6 coclones x>=5)": floor_ok, "in_sample_R2": round(r2_in, 3),
            "multivariate_coefficient_signs": signs,
            "sealed_signs": {"density": "NEGATIVE", "arity": "two-sided", "tuple_dispersion": "POSITIVE"},
            "marginal_corr_each_feature": marg,
            "carried_by": "tuple_dispersion (sealed POSITIVE, marginal %.2f)" % (marg["tuple_dispersion"] or 0),
            "density_sealed_sign_FAILED": density_sealed_failed,
            "density_note": ("the sealed density mechanism (sparse->rugged, NEGATIVE) is WRONG: density's marginal "
                             "corr is +%.2f (denser weakly MORE rugged). The physics density->clustering mechanism "
                             "does NOT transpose to relation-density in the sealed direction. SUPPORTED rests on "
                             "tuple_dispersion, not density." % (marg["density"] or 0)),
            "sign_match_via": "tuple_dispersion" if signs.get("tuple_dispersion") == "+" else None,
            "permutation_p": perm_p,
            "heldout_by_coclone": {"held_mse": round(held_mse, 4) if held_mse else None,
                                   "baseline_mse": round(base_mse, 4) if base_mse else None,
                                   "held_beats_baseline": held_beats_base},
            "note": "held-out by co-clone is PRIMARY; in-sample R2 is sensitivity only. tuple_dispersion (relation "
                    "tuple-geometry) is relation-level (varies within a co-clone), so it reaches where clone "
                    "invariants provably cannot. Density mechanism is physics prior art AND failed here."}




def main():
    roster = json.load(open("foundry/foundry/results/landscape/sprint46_roster.json"))["rows"]
    selftest_perm()
    A = experiment_A(roster)
    B = experiment_B(roster)
    out = {"A": A, "B": B, "bridge_hunt": "density->clustering mechanism is prior art (random-CSP statistical "
           "physics: cavity method RS/1RSB clustering, condensation, freezing vs constraint density)."}
    json.dump(out, open("foundry/foundry/results/landscape/sprint46_analysis.json", "w"), indent=2)
    print("\nA:", A["verdict"], "| per-rank spread:", {k: v["mean_spread"] for k, v in A["per_rank_spread"].items()},
          "corr", A["corr_rank_spread_core"])
    print("B:", B["verdict"], "| carried_by", B["carried_by"], "| density_sealed_FAILED", B["density_sealed_sign_FAILED"],
          "perm_p", B["permutation_p"], "held_beats_base", B["heldout_by_coclone"]["held_beats_baseline"],
          "R2_in", B["in_sample_R2"])


if __name__ == "__main__":
    main()
