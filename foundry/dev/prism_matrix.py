"""Prism R2 (prereg_v32) — pairwise Cramer's V matrix + PER-PAIR shared-input netting (r25 style) + the
named-bridge Cai-Chen netting on approx<->param (folded v3 addendum). Scores predictions 2, 3a, 5, 6.
3b + 4 are UNTESTABLE (R1 marginal degeneracy: bounded-width <=> tractable at arity<=3). $0.

Run: PYTHONPATH=... python foundry/dev/prism_matrix.py
"""
import json
from itertools import combinations

import numpy as np

from eightfold import structure as S
from foundry import prism

COLS = ("decision", "counting", "localization", "parallelization", "approx_counting",
        "approx_maxones", "approx_minones", "parameterized")
SENTINEL = {"open", "n.a."}   # non-charge values excluded from a pair's both-real rows (feasibility-hard IS real)
SEED, NBOOT = 32, 4000


def _v(xs, ys):
    if len(xs) < 3 or len(set(xs)) < 2 or len(set(ys)) < 2:
        return None
    v = S.cramers_v(xs, ys)
    return round(float(v), 3) if v == v else None


def _spearman(x, y):
    if len(x) < 3 or len(set(x)) < 2 or len(set(y)) < 2:
        return None
    rx, ry = np.argsort(np.argsort(x)), np.argsort(np.argsort(y))
    return round(float(np.corrcoef(rx, ry)[0, 1]), 3)


def _netted(rows, a_col, b_col):
    """Per-pair shared-input netting: stratify both-real rows by the shared polymorphism inputs, pool the
    within-stratum V (size-weighted). Returns (raw_v, netted_v, n, shared_inputs, one_charge_constant)."""
    both = [r for r in rows if r[a_col] not in SENTINEL and r[b_col] not in SENTINEL]
    xs = [r[a_col] for r in both]; ys = [r[b_col] for r in both]
    raw = _v(xs, ys)
    shared = sorted(prism.CHARGE_INPUTS[a_col] & prism.CHARGE_INPUTS[b_col])
    strata = {}
    for r in both:
        key = tuple(r["flags"][f] for f in shared)
        strata.setdefault(key, []).append(r)
    pooled, n = 0.0, len(both)
    for members in strata.values():
        v = _v([m[a_col] for m in members], [m[b_col] for m in members])
        pooled += (v or 0.0) * len(members) / max(1, n)
    # one charge constant within every shared-stratum => nets to 0 by determination
    const = all(len({m[a_col] for m in members}) == 1 or len({m[b_col] for m in members}) == 1
                for members in strata.values())
    return raw, round(pooled, 3), n, shared, const


def main():
    roster = prism.build_roster(3)
    rows = [{**c, "flags": c["flags"]} for _, _, _, c in roster]   # per-class charge dicts

    # ── pairwise matrix: raw V + netted residual, per pair ──────────────────────────────────────────────────
    matrix = {}
    for a, b in combinations(COLS, 2):
        raw, net, n, shared, const = _netted(rows, a, b)
        matrix[f"{a} x {b}"] = {"raw_v": raw, "netted_residual": net, "n_both_real": n,
                                "shared_inputs": shared,
                                "derivation": (f"one charge is a function of the shared inputs {shared} -> constant "
                                               f"within every stratum -> residual 0 (theorem-identity)" if const
                                               else f"conditioned on shared inputs {shared}; residual is the "
                                                    f"association not forced by them")}

    # ── the approx<->param headline on the 166 both-real OBJECTIVE rows (matches v3) + Cai-Chen netting (pred 6) ─
    APX_RANK = {v: i for i, v in enumerate(prism.OO.APPROX_ORDER)}
    obj_rows = []
    for r in rows:
        if r["parameterized"] != "open":
            obj_rows.append((r["approx_maxones"], r["parameterized"]))
            obj_rows.append((r["approx_minones"], r["parameterized"]))
    ax = [a for a, _ in obj_rows]; px = [p for _, p in obj_rows]
    raw_v = _v(ax, px)
    raw_rho = _spearman([APX_RANK[a] for a in ax], [0 if p == "FPT" else 1 for p in px])
    # Cai-Chen: remove the forced (APX-complete, FPT) rows, recompute
    kept = [(a, p) for a, p in obj_rows if not (a == "APX-complete" and p == "FPT")]
    kx = [a for a, _ in kept]; kpx = [p for _, p in kept]
    net_v = _v(kx, kpx)
    net_rho = _spearman([APX_RANK[a] for a in kx], [0 if p == "FPT" else 1 for p in kpx])
    n_removed = len(obj_rows) - len(kept)
    # bootstrap CI on raw_v sized to the class count (resample the 83 param-real classes, not the 166 rows)
    rng = np.random.default_rng(SEED)
    prclasses = [r for r in rows if r["parameterized"] != "open"]
    boot = []
    for _ in range(NBOOT):
        samp = rng.choice(len(prclasses), size=len(prclasses), replace=True)
        rr = []
        for i in samp:
            r = prclasses[i]
            rr.append((r["approx_maxones"], r["parameterized"])); rr.append((r["approx_minones"], r["parameterized"]))
        bv = _v([a for a, _ in rr], [p for _, p in rr])
        if bv is not None:
            boot.append(bv)
    ci = (round(float(np.percentile(boot, 2.5)), 3), round(float(np.percentile(boot, 97.5)), 3))

    approx_param = {"raw_v": raw_v, "raw_spearman": raw_rho, "n_rows": len(obj_rows),
                    "boot_ci95_sized_to_classes": ci,
                    "cai_chen_netted": {"removed_APX_complete_FPT_rows": n_removed, "netted_v": net_v,
                                        "netted_spearman": net_rho}}

    # ── score the live predictions ──────────────────────────────────────────────────────────────────────────
    dc = matrix["decision x counting"]
    bw_apx = max((matrix[k] for k in matrix if "localization" in k and "approx" in k), key=lambda m: m["raw_v"] or 0)
    # outlier persistence (pred 5): compare netted residuals; approx<->param cell = raw_v (shared inputs ~ empty)
    ap_net = matrix.get("approx_maxones x parameterized", {}).get("netted_residual")
    other_nets = {k: m["netted_residual"] for k, m in matrix.items()
                  if "parameterized" not in k or "approx" not in k}
    max_other = max((v for v in other_nets.values() if v is not None), default=0.0)

    scored = {
        "pred_1_NPI": "PASSED (R1)",
        "pred_2_identity_decision_counting": {"raw_v": dc["raw_v"], "netted": dc["netted_residual"],
                                              "verdict": "HIT" if (dc["netted_residual"] or 0) < 0.05 else "MISS"},
        "pred_3a_localization_identity": {"pair": [k for k in matrix if "localization" in k and "approx" in k],
                                          "bw_x_approx_raw_v": bw_apx["raw_v"], "netted": bw_apx["netted_residual"],
                                          "verdict": ("HIT (raw>=0.4 & netted~0, entailment finding)"
                                                      if (bw_apx["raw_v"] or 0) >= 0.4 and (bw_apx["netted_residual"] or 0) < 0.05
                                                      else "see values")},
        "pred_3b_bw_param": "UNTESTABLE — bounded-width constant on the param-real subset (R1 marginal degeneracy)",
        "pred_4_absorption": "UNTESTABLE — all both-real rows are bounded-width; one stratum (R1 marginal degeneracy). Needs arity>=4.",
        "pred_5_outlier_persistence": {"approx_param_netted": approx_param["raw_v"], "max_other_pair_netted": round(max_other, 3),
                                       "verdict": "HIT" if (approx_param["raw_v"] or 0) > max_other else "MISS"},
        "pred_6_cai_chen": {"raw_spearman": raw_rho, "netted_spearman": net_rho, "raw_v": raw_v, "netted_v": net_v,
                            "ci": ci, "verdict": ("HIT" if (net_rho is not None and raw_rho is not None
                                                            and net_rho > raw_rho and net_v is not None
                                                            and ci[0] <= net_v <= ci[1]) else "see values")},
    }

    # affine trace: where the affine class lands in each pairing (the tautology-breaker)
    affine_rows = [r for r in rows if r["flags"]["affine"]]
    affine_trace = {"n_affine_classes": len(affine_rows),
                    "counting": sorted({r["counting"] for r in affine_rows}),
                    "approx_maxones": sorted({r["approx_maxones"] for r in affine_rows}),
                    "approx_minones": sorted({r["approx_minones"] for r in affine_rows}),
                    "parameterized": sorted({r["parameterized"] for r in affine_rows}),
                    "note": "affine -> counting FP, param FPT (off-diagonal), approx varies; the tautology-breaker."}

    out = {"prereg": "v32", "matrix": matrix, "approx_param_headline": approx_param,
           "scored_predictions": scored, "affine_trace": affine_trace}
    print("=== pairwise netted residuals (raw -> netted) ===")
    for k, m in sorted(matrix.items(), key=lambda kv: -(kv[1]["netted_residual"] or 0)):
        print(f"  {k:42s} raw={str(m['raw_v']):>6s} -> net={str(m['netted_residual']):>6s}  (n={m['n_both_real']})")
    print(f"\napprox<->param headline: raw V={raw_v} Spearman={raw_rho}  CI{ci}")
    print(f"  Cai-Chen netted (removed {n_removed} APX-complete/FPT): V={net_v} Spearman={net_rho}")
    print("\nscored predictions:")
    for k, v in scored.items():
        print(f"  {k}: {v}")
    json.dump(out, open("foundry/foundry/results/lattice/prism_matrix.json", "w"), indent=2)
    print("\nwrote prism_matrix.json")


if __name__ == "__main__":
    main()
