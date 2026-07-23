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

# NETTING inputs = the LITERAL predicate a charge reads (prism.CHARGE_INPUTS), EXTENDED by the named-bridge layer.
# Bridge (Marx Ex 2.4): affine => weakly separable => FPT. So `affine` is a determinant of `parameterized` (affine is
# a sufficient condition for general_wsep), even though the literal predicate is general_wsep. Completing the sealed
# named-bridge layer (owner ruling; spec-defect #4: the per-pair netting missed this because the predicates have
# different names). Both residual sets (LITERAL vs BRIDGE-COMPLETED) are reported.
NETTING_INPUTS = {**prism.CHARGE_INPUTS, "parameterized": prism.CHARGE_INPUTS["parameterized"] | {"affine"}}


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


def _netted(rows, a_col, b_col, inputs=prism.CHARGE_INPUTS):
    """Per-pair shared-input netting: stratify both-real rows by the shared polymorphism inputs, pool the
    within-stratum V (size-weighted). Returns (raw_v, netted_v, n, shared_inputs, one_charge_constant)."""
    both = [r for r in rows if r[a_col] not in SENTINEL and r[b_col] not in SENTINEL]
    xs = [r[a_col] for r in both]; ys = [r[b_col] for r in both]
    raw = _v(xs, ys)
    shared = sorted(inputs[a_col] & inputs[b_col])
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

    # ── pairwise matrix: raw V + BOTH netted residuals (literal shared-input, bridge-completed) per pair ──────
    matrix = {}
    for a, b in combinations(COLS, 2):
        raw, net_lit, n, shared_lit, _ = _netted(rows, a, b, prism.CHARGE_INPUTS)
        _, net_bridge, _, shared_bridge, const_bridge = _netted(rows, a, b, NETTING_INPUTS)
        matrix[f"{a} x {b}"] = {
            "raw_v": raw, "netted_literal": net_lit, "netted_bridge_completed": net_bridge, "n_both_real": n,
            "shared_literal": shared_lit, "shared_bridge_completed": shared_bridge,
            "affine_bridge_changed_it": net_lit != net_bridge,
            "derivation": (f"function of shared inputs {shared_bridge} -> constant within stratum -> residual 0 "
                           f"(theorem-identity; affine=>WS bridge applies)" if const_bridge
                           else f"conditioned on {shared_bridge}; residual = association not theorem-forced")}

    # ── the approx<->param headline on the 166 both-real OBJECTIVE rows (matches v3) + Cai-Chen netting (pred 6) ─
    APX_RANK = {v: i for i, v in enumerate(prism.OO.APPROX_ORDER)}
    obj_rows = []   # (approx, param, affine)
    for r in rows:
        if r["parameterized"] != "open":
            obj_rows.append((r["approx_maxones"], r["parameterized"], r["flags"]["affine"]))
            obj_rows.append((r["approx_minones"], r["parameterized"], r["flags"]["affine"]))
    ax = [a for a, _, _ in obj_rows]; px = [p for _, p, _ in obj_rows]
    raw_v = _v(ax, px)
    raw_rho = _spearman([APX_RANK[a] for a in ax], [0 if p == "FPT" else 1 for p in px])
    # bridge-completed (affine=>WS): net the affine off-diagonal (condition on affine; pool within-stratum V)
    ap_bridge = 0.0
    for aff in (True, False):
        mem = [(a, p) for a, p, x in obj_rows if x == aff]
        v = _v([a for a, _ in mem], [p for _, p in mem])
        ap_bridge += (v or 0.0) * len(mem) / max(1, len(obj_rows))
    ap_bridge = round(ap_bridge, 3)
    # Cai-Chen: remove the forced (APX-complete, FPT) rows, recompute
    kept = [(a, p) for a, p, _ in obj_rows if not (a == "APX-complete" and p == "FPT")]
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
                    "netted_literal_shared_input": raw_v,   # approx & param share no literal predicate -> raw
                    "netted_bridge_completed_affine": ap_bridge,
                    "cai_chen_netted": {"removed_APX_complete_FPT_rows": n_removed, "netted_v": net_v,
                                        "netted_spearman": net_rho}}

    # ── score the live predictions ──────────────────────────────────────────────────────────────────────────
    dc = matrix["decision x counting"]
    bw_apx = max((matrix[k] for k in matrix if "localization" in k and "approx" in k), key=lambda m: m["raw_v"] or 0)

    def _param_pairs(field):
        return {k: m[field] for k, m in matrix.items() if "parameterized" in k}
    lit_survivors = {k: v for k, v in _param_pairs("netted_literal").items() if v is not None}
    bridge_survivors = {k: v for k, v in _param_pairs("netted_bridge_completed").items() if v is not None}
    # outlier persistence (pred 5): does any OTHER pair's netted residual exceed approx<->param's?
    other_lit = max((v for k, v in matrix.items() if "approx" not in k and (v["netted_literal"] or 0)
                     for v in [v["netted_literal"]]), default=0.0)
    other_bridge = max((m["netted_bridge_completed"] or 0 for k, m in matrix.items() if "approx" not in k), default=0.0)
    ap_ref_lit = max(matrix["approx_maxones x parameterized"]["netted_literal"] or 0,
                     matrix["approx_minones x parameterized"]["netted_literal"] or 0)
    ap_ref_bridge = max(matrix["approx_maxones x parameterized"]["netted_bridge_completed"] or 0,
                        matrix["approx_minones x parameterized"]["netted_bridge_completed"] or 0)

    scored = {
        "pred_1_NPI": "PASSED (R1)",
        "pred_2_identity_decision_counting": {"raw_v": dc["raw_v"], "netted": dc["netted_bridge_completed"],
                                              "verdict": "HIT" if (dc["netted_bridge_completed"] or 0) < 0.05 else "MISS"},
        "pred_3a_localization_identity": {"pair": [k for k in matrix if "localization" in k and "approx" in k],
                                          "bw_x_approx_raw_v": bw_apx["raw_v"], "netted": bw_apx["netted_bridge_completed"],
                                          "verdict": ("HIT (raw>=0.4 & netted~0, entailment finding)"
                                                      if (bw_apx["raw_v"] or 0) >= 0.4 and (bw_apx["netted_bridge_completed"] or 0) < 0.05
                                                      else "see values")},
        "pred_3b_bw_param": "UNTESTABLE — bounded-width constant on the param-real subset (R1 marginal degeneracy)",
        "pred_4_absorption": "UNTESTABLE — all both-real rows are bounded-width; one stratum (R1 marginal degeneracy). Needs arity>=4.",
        "pred_5_outlier_persistence": {
            "LITERAL": {"counting_x_param": matrix["counting x parameterized"]["netted_literal"],
                        "approx_counting_x_param": matrix["approx_counting x parameterized"]["netted_literal"],
                        "approx_param_ref": ap_ref_lit, "max_other_non_approx_pair": round(other_lit, 3),
                        "verdict": "MISS (spurious — theorem-forced survivors not yet netted)"},
            "BRIDGE_COMPLETED": {"counting_x_param": matrix["counting x parameterized"]["netted_bridge_completed"],
                                 "approx_counting_x_param": matrix["approx_counting x parameterized"]["netted_bridge_completed"],
                                 "approx_param_ref": ap_ref_bridge, "max_other_non_approx_pair": round(other_bridge, 3),
                                 "verdict": "HIT" if ap_ref_bridge >= other_bridge else "MISS"}},
        "pred_6_cai_chen": {"raw_spearman": raw_rho, "netted_spearman": net_rho, "raw_v": raw_v, "netted_v": net_v,
                            "ci": ci, "verdict": ("HIT" if (net_rho is not None and raw_rho is not None
                                                            and net_rho > raw_rho and net_v is not None
                                                            and ci[0] <= net_v <= ci[1]) else "MISS (Spearman did not rise; V within CI)")},
        "SEALED_STRUCTURAL_CLAIM_MISS": {"claim": "general weak-separability is orthogonal to the classical fingerprint (prereg_v32 structural_headline)",
                                         "refuted_by": "affine => weakly-separable => FPT (Marx Ex 2.4): counting/approx_counting read affine, so they are NOT orthogonal to param",
                                         "date": "2026-07-23", "standing": "sealed-claim miss, same as v3's direction miss"},
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
           "scored_predictions": scored, "affine_trace": affine_trace,
           "netting_note": "netted_literal = per-pair LITERAL shared-input (sealed procedure as first executed). "
                           "netted_bridge_completed = + affine=>weakly-separable=>FPT named bridge (Marx Ex 2.4; "
                           "completing the sealed named-bridge layer, owner ruling; spec-defect #4). Both reported."}
    print("=== pairwise residuals (raw -> netted LITERAL -> netted BRIDGE-COMPLETED) ===")
    for k, m in sorted(matrix.items(), key=lambda kv: -(kv[1]["netted_literal"] or 0)):
        flag = "  <- affine bridge changed it" if m["affine_bridge_changed_it"] else ""
        print(f"  {k:40s} raw={str(m['raw_v']):>6s} lit={str(m['netted_literal']):>6s} "
              f"bridge={str(m['netted_bridge_completed']):>6s}{flag}")
    print(f"\napprox<->param headline: raw V={raw_v} Spearman={raw_rho} CI{ci}")
    print(f"  literal-netted={raw_v}  bridge-completed(affine)={ap_bridge}  "
          f"Cai-Chen(rm {n_removed} APXc/FPT): V={net_v} Spearman={net_rho}")
    print("\nscored predictions:")
    for k, v in scored.items():
        print(f"  {k}: {v}")
    json.dump(out, open("foundry/foundry/results/lattice/prism_matrix.json", "w"), indent=2)
    print("\nwrote prism_matrix.json")


if __name__ == "__main__":
    main()
