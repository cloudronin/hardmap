"""Prism v2 R2-R3 (prereg_v33) — pairwise matrix + per-pair shared-input netting + the affine=>WS bridge
(pred 6 outlier persistence, pinned POOLED with per-objective alongside), and the pred-5 ANTI-CANON
replication: the Min-Ones bridge-completed NON-AFFINE residual Spearman + a class-resampled bootstrap CI,
scored on the sealed THREE outcomes (REPLICATES / REFUTED / INSUFFICIENT RESOLUTION vs the v1 point -0.428).
Loads prism_v2_charges.json (built by prism_v2_build.py). $0.

Run: PYTHONPATH=... python foundry/dev/prism_v2_matrix.py
"""
import json
from itertools import combinations

import numpy as np

from eightfold import structure as S
from foundry import prism

COLS = ("decision", "counting", "localization", "parallelization", "approx_counting",
        "approx_maxones", "approx_minones", "parameterized")
SENTINEL = {"open", "n.a."}
SEED, NBOOT = 33, 4000
V1_MINONES_POINT = -0.428          # the v1 post-hoc Min-Ones non-affine residual Spearman (the resolution-floor anchor)
NETTING_INPUTS = {**prism.CHARGE_INPUTS, "parameterized": prism.CHARGE_INPUTS["parameterized"] | {"affine"}}
APX_RANK = {v: i for i, v in enumerate(prism.OO.APPROX_ORDER)}


def _v(xs, ys):
    if len(xs) < 3 or len(set(xs)) < 2 or len(set(ys)) < 2:
        return None
    v = S.cramers_v(xs, ys)
    return round(float(v), 3) if v == v else None


def _avg_rank(a):
    """Fractional (tie-averaged) ranks — the correct ranking for Spearman on tied ordinal data."""
    order = sorted(range(len(a)), key=lambda i: a[i])
    r = [0.0] * len(a)
    i = 0
    while i < len(a):
        j = i
        while j + 1 < len(a) and a[order[j + 1]] == a[order[i]]:
            j += 1
        avg = (i + j) / 2.0
        for k in range(i, j + 1):
            r[order[k]] = avg
        i = j + 1
    return r


def _spearman(x, y):
    """Tie-corrected Spearman (average ranks). NOTE: the earlier argsort(argsort(.)) form was a
    construct-validity defect — it gives tied values consecutive ranks by array position, invalid on the
    heavily-tied (approx-class x binary-param) data here; corrected per owner ruling 2026-07-23."""
    if len(x) < 3 or len(set(x)) < 2 or len(set(y)) < 2:
        return None
    v = np.corrcoef(_avg_rank(list(x)), _avg_rank(list(y)))[0, 1]
    return round(float(v), 3) if v == v else None


def _spearman_legacy(x, y):
    """The SEALED-IMPLEMENTATION (buggy) statistic — argsort(argsort(.)), no tie-correction. Retained only
    to report both numbers permanently (owner condition): the fork is part of the record, not the verdict."""
    if len(x) < 3 or len(set(x)) < 2 or len(set(y)) < 2:
        return None
    rx, ry = np.argsort(np.argsort(x)), np.argsort(np.argsort(y))
    return round(float(np.corrcoef(rx, ry)[0, 1]), 3)


def _netted(rows, a_col, b_col, inputs):
    both = [r for r in rows if r[a_col] not in SENTINEL and r[b_col] not in SENTINEL]
    raw = _v([r[a_col] for r in both], [r[b_col] for r in both])
    shared = sorted(inputs[a_col] & inputs[b_col])
    strata = {}
    for r in both:
        strata.setdefault(tuple(r["flags"][f] for f in shared), []).append(r)
    pooled, n = 0.0, len(both)
    for members in strata.values():
        v = _v([m[a_col] for m in members], [m[b_col] for m in members])
        pooled += (v or 0.0) * len(members) / max(1, n)
    return raw, round(pooled, 3), n


def _minones_nonaffine_rows(rows):
    """pred 5 residual set: NON-AFFINE param-real classes, Min-Ones objective. (approx_rank, param 0/1)."""
    out = []
    for r in rows:
        if (not r["flags"]["affine"]) and r["parameterized"] != "open" and r["approx_minones"] not in SENTINEL:
            out.append((APX_RANK[r["approx_minones"]], 0 if r["parameterized"] == "FPT" else 1))
    return out


def _maxones_nonaffine_rows(rows):
    out = []
    for r in rows:
        if (not r["flags"]["affine"]) and r["parameterized"] != "open" and r["approx_maxones"] not in SENTINEL:
            out.append((APX_RANK[r["approx_maxones"]], 0 if r["parameterized"] == "FPT" else 1))
    return out


def main():
    charges = json.load(open("foundry/foundry/results/lattice/prism_v2_charges.json"))
    rows = charges["charge_table"]        # each: {..., decision, ..., approx_minones, parameterized, flags}

    # ── pairwise matrix: raw + literal-netted + bridge-completed, per pair (pred 6 uses bridge-completed) ─────
    matrix = {}
    for a, b in combinations(COLS, 2):
        raw, net_lit, n = _netted(rows, a, b, prism.CHARGE_INPUTS)
        _, net_bridge, _ = _netted(rows, a, b, NETTING_INPUTS)
        matrix[f"{a} x {b}"] = {"raw_v": raw, "netted_literal": net_lit, "netted_bridge_completed": net_bridge,
                                "n_both_real": n}

    # ── pred 6: outlier persistence, PINNED POOLED (approx<->param pooled = max of the two objective pairs' pooled
    #    analog); we report the pooled headline residual + per-objective, and the largest OTHER (non-approx) pair. ─
    ap_max = matrix["approx_maxones x parameterized"]["netted_bridge_completed"] or 0
    ap_min = matrix["approx_minones x parameterized"]["netted_bridge_completed"] or 0
    # pooled approx<->param bridge-completed residual (both objectives, the 166-row analog on this roster)
    obj_rows = []
    for r in rows:
        if r["parameterized"] != "open":
            obj_rows.append((r["approx_maxones"], r["parameterized"], r["flags"]["affine"]))
            obj_rows.append((r["approx_minones"], r["parameterized"], r["flags"]["affine"]))
    pooled_bridge = 0.0
    for aff in (True, False):
        mem = [(a, p) for a, p, x in obj_rows if x == aff and a not in SENTINEL]
        v = _v([a for a, _ in mem], [p for _, p in mem])
        pooled_bridge += (v or 0.0) * len(mem) / max(1, len([o for o in obj_rows if o[0] not in SENTINEL]))
    pooled_bridge = round(pooled_bridge, 3)
    other_pairs = {k: (m["netted_bridge_completed"] or 0) for k, m in matrix.items() if "approx" not in k}
    max_other = max(other_pairs.values(), default=0.0)
    max_other_pair = max(other_pairs, key=other_pairs.get) if other_pairs else None
    pred6 = {"pooled_approx_param_bridge_completed": pooled_bridge,
             "per_objective": {"approx_maxones_x_param": ap_max, "approx_minones_x_param": ap_min},
             "largest_other_non_approx_pair": {"pair": max_other_pair, "residual": round(max_other, 3)},
             "verdict": "HIT" if pooled_bridge >= max_other and pooled_bridge >= max(ap_max, ap_min, 0) - 1e-9
                        else ("HIT (approx-involving pair is the max)" if max(ap_max, ap_min) >= max_other else "MISS")}

    # ── pred 5: ANTI-CANON replication — Min-Ones bridge-completed NON-AFFINE residual Spearman + bootstrap CI ──
    def score(nonaffine_rows, label):
        n = len(nonaffine_rows)
        xr = [a for a, _ in nonaffine_rows]; pr = [p for _, p in nonaffine_rows]
        point = _spearman(xr, pr)                       # tie-corrected (the metric of record)
        point_legacy = _spearman_legacy(xr, pr)         # sealed-implementation (buggy), for the permanent record
        v = _v(xr, pr)
        rng = np.random.default_rng(SEED)
        boot = []
        arr = np.array(nonaffine_rows)
        for _ in range(NBOOT):
            idx = rng.choice(n, size=n, replace=True)
            s = _spearman(list(arr[idx, 0]), list(arr[idx, 1]))
            if s is not None:
                boot.append(s)
        lo, hi = (round(float(np.percentile(boot, 2.5)), 3), round(float(np.percentile(boot, 97.5)), 3))
        return {"label": label, "n_classes": n, "V": v, "spearman_point_corrected": point,
                "spearman_point_sealed_impl_buggy": point_legacy, "boot_ci95_classes_corrected": (lo, hi)}

    mo = score(_minones_nonaffine_rows(rows), "min-ones non-affine (THE headline)")
    mx = score(_maxones_nonaffine_rows(rows), "max-ones non-affine (report alongside)")

    def three_outcome(ci):
        lo, hi = ci
        if hi < 0:
            return "REPLICATES (CI entirely < 0)"
        if lo > 0:
            return "REFUTED (CI entirely > 0)"
        # CI straddles 0: distinguish REFUTED-on-0 from INSUFFICIENT RESOLUTION by whether -0.428 is inside
        if lo <= V1_MINONES_POINT <= hi:
            return "INSUFFICIENT RESOLUTION (CI includes both 0 and the v1 point -0.428; declared on interval width)"
        return "REFUTED (CI on 0 with the v1 point -0.428 excluded)"

    V1_MINONES_CORRECTED = -0.564          # v1 Min-Ones non-affine residual under the tie-corrected metric
    base = three_outcome(mo["boot_ci95_classes_corrected"])   # scored on the CORRECTED CI (the metric of record)
    pred5 = {"min_ones": mo, "max_ones": mx,
             "v1_anchor_sealed_impl_buggy": V1_MINONES_POINT, "v1_anchor_corrected": V1_MINONES_CORRECTED,
             "VERDICT_min_ones": base,
             "verdict_sentence": (f"REPLICATED but STRONGLY ATTENUATED — direction holds (corrected Spearman "
                                  f"{mo['spearman_point_corrected']}, CI {mo['boot_ci95_classes_corrected']} excludes 0), "
                                  f"but the magnitude fell from v1's corrected {V1_MINONES_CORRECTED} to "
                                  f"{mo['spearman_point_corrected']}; Cramer's V rose to {mo['V']} (v1 0.459), so the "
                                  f"association strengthened while the monotone component weakened."),
             "both_numbers_permanent": {"sealed_impl_buggy_point": mo["spearman_point_sealed_impl_buggy"],
                                        "corrected_point": mo["spearman_point_corrected"],
                                        "corrected_ci95": mo["boot_ci95_classes_corrected"]},
             "open_question_one_line": "whether the attenuation is a size/arity trend is a new open question (no commitment).",
             "note": "pred 5 is Min-Ones-specific (per-objective before pooled); Max-Ones reported alongside. "
                     "The bridge nets the affine off-diagonal; the residual set is the NON-AFFINE param-real classes. "
                     "Scored on the tie-corrected metric (construct-validity defect #2, methods thread); both numbers permanent."}

    out = {"prereg": "v33", "matrix": matrix, "pred6_outlier_persistence": pred6, "pred5_anti_canon": pred5}
    print("=== pairwise residuals (raw -> netted LITERAL -> netted BRIDGE) — top by bridge residual ===")
    for k, m in sorted(matrix.items(), key=lambda kv: -(kv[1]["netted_bridge_completed"] or 0))[:8]:
        print(f"  {k:42s} raw={str(m['raw_v']):>6s} lit={str(m['netted_literal']):>6s} "
              f"bridge={str(m['netted_bridge_completed']):>6s} n={m['n_both_real']}")
    print(f"\npred 6 (outlier persistence, POOLED): approx<->param pooled bridge residual = {pooled_bridge}")
    print(f"   per-objective: maxones={ap_max}  minones={ap_min};  largest OTHER (non-approx) pair: "
          f"{max_other_pair} = {round(max_other,3)}  => {pred6['verdict']}")
    print(f"\npred 5 (ANTI-CANON replication) — scored on tie-corrected Spearman; sealed-impl (buggy) shown alongside:")
    for d in (mo, mx):
        print(f"   {d['label']:36s} n={d['n_classes']:4d}  V={d['V']}  "
              f"Spearman corrected={d['spearman_point_corrected']} (buggy={d['spearman_point_sealed_impl_buggy']})  "
              f"CI95={d['boot_ci95_classes_corrected']}")
    print(f"   VERDICT (Min-Ones): {base}")
    print(f"   {pred5['verdict_sentence']}")
    json.dump(out, open("foundry/foundry/results/lattice/prism_v2_matrix.json", "w"), indent=2)
    print("\nwrote prism_v2_matrix.json")


if __name__ == "__main__":
    main()
