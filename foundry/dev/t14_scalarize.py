"""Pebble T1.4 (scalarization, prereg_v14) + T1.3 (structural race, prereg_v13), run together (prereg_v26).
Does [v13 graph geometry + tuple_dispersion] reproduce measured point-to-set reach at its self-reliability ceiling
(rho >= 0.90, sealed)? AND — the added reported number — does graph geometry improve on the scalar's standalone ~0.78
at all (increment)? Density-resolved (T1.3). Held out by co-clone; permutation null; R* = ensemble split-half.

Run: PYTHONPATH=... python foundry/dev/t14_scalarize.py
"""
import json
import statistics as st
import os
import sys

import numpy as np

from foundry import pointset as PS
from foundry import structural as ST
from foundry import ensemble as E
from foundry import relfeatures as RF
sys.path.insert(0, os.path.join(os.getcwd(), "foundry", "dev"))
import pointset_sweep as SW

N, NINST, RADIUS = 15, 4, 2
DENSITIES = [0.5, 0.7]
SEED_A, SEED_B = 990000, 993000
FEATS_STRUCT = ["spectral_gap", "expansion_proxy", "degree_mean", "degree_var", "treewidth_ub"]
SCALAR = ["tuple_dispersion"]
FULL = SCALAR + FEATS_STRUCT
CEILING = 0.90


def mean_structural(R, n, alpha, base_seed, ninst):
    acc = {f: [] for f in FEATS_STRUCT}
    for i in range(ninst):
        f = ST.structural_features(E.gen_instance((R,), (0, 1), n, alpha, base_seed + i, family_id="ps"))
        for k in FEATS_STRUCT:
            acc[k].append(f[k])
    return {k: float(st.mean(v)) for k, v in acc.items()}


def reach_of(R, n, alpha, base_seed):
    return PS.measure_pointset((R,), (0, 1), n, alpha, n_instances=NINST, base_seed=base_seed, reach_radius=RADIUS)["reach_score"]


def heldout_R(rows, feats):
    ccs = sorted({r["coclone"] for r in rows})
    preds, acts = [], []
    for cc in ccs:
        tr = [r for r in rows if r["coclone"] != cc]
        te = [r for r in rows if r["coclone"] == cc]
        if len(tr) < 5 or not te:
            continue
        X = np.array([[r[f] for f in feats] for r in tr], float)
        y = np.array([r["reach"] for r in tr], float)
        _, beta = RF.fit_r2(X, y)
        for r in te:
            preds.append(beta[0] + sum(beta[i + 1] * r[f] for i, f in enumerate(feats)))
            acts.append(r["reach"])
    if len(set(preds)) < 2 or len(set(acts)) < 2:
        return None
    return float(np.corrcoef(preds, acts)[0, 1])


def main():
    recs = SW.long_anchors() + SW.short_reps()
    print(f"T1.4/T1.3: {len(recs)} relations; n={N}; densities {DENSITIES}", flush=True)
    per_density = {}
    for dfrac in DENSITIES:
        rows = []
        for i, rec in enumerate(recs):
            R = frozenset(tuple(t) for t in rec["relation"])
            a_struct = rec["alpha_struct"] if rec["alpha_struct"] is not None else SW.density_for(rec, N) / SW.DENSITY_FRAC
            alpha = round(dfrac * a_struct, 3)
            rA = reach_of(R, N, alpha, SEED_A + 100 * i)
            rB = reach_of(R, N, alpha, SEED_B + 100 * i)
            if rA is None or rB is None:
                continue
            row = {"coclone": rec["profile"], "reach": (rA + rB) / 2, "reach_A": rA, "reach_B": rB,
                   "tuple_dispersion": RF.tuple_dispersion(R)}
            row.update(mean_structural(R, N, alpha, SEED_A + 100 * i, NINST))
            rows.append(row)
        if len(rows) < 10:
            continue
        R_star = float(np.corrcoef([r["reach_A"] for r in rows], [r["reach_B"] for r in rows])[0, 1])
        ho_scalar = heldout_R(rows, SCALAR)
        ho_full = heldout_R(rows, FULL)
        ho_struct = heldout_R(rows, FEATS_STRUCT)
        rho = round(ho_full / R_star, 3) if (ho_full is not None and R_star) else None
        increment = round(ho_full - ho_scalar, 4) if (ho_full is not None and ho_scalar is not None) else None
        # permutation null on the full-model held-out-R (shuffle reach)
        rng = np.random.default_rng(26)
        perm = []
        reaches = [r["reach"] for r in rows]
        for _ in range(500):
            sh = rng.permutation(reaches)
            pr = [dict(r, reach=float(sh[j])) for j, r in enumerate(rows)]
            f = heldout_R(pr, FULL)
            if f is not None:
                perm.append(f)
        p_val = round(float(np.mean([pf >= ho_full for pf in perm])), 4) if (perm and ho_full is not None) else None
        per_density[dfrac] = {"n_rows": len(rows), "R_star_split_half": round(R_star, 3),
                              "ho_scalar_only": round(ho_scalar, 4) if ho_scalar is not None else None,
                              "ho_full_scalar_plus_structural": round(ho_full, 4) if ho_full is not None else None,
                              "ho_structural_only_T1_3": round(ho_struct, 4) if ho_struct is not None else None,
                              "rho_vs_ceiling": rho, "increment_geometry_over_scalar": increment,
                              "perm_p": p_val,
                              "sealed_verdict": ("SCALARIZABLE" if (rho is not None and rho >= CEILING)
                                                 else "PARTIAL" if (rho is not None and rho >= 0.50)
                                                 else "NOT_SCALARIZABLE" if rho is not None else "n/a")}
        pd = per_density[dfrac]
        print(f"\n[density {dfrac}*alpha_struct] R*={pd['R_star_split_half']}  scalar_only={pd['ho_scalar_only']}  "
              f"full={pd['ho_full_scalar_plus_structural']}  struct_only={pd['ho_structural_only_T1_3']}", flush=True)
        print(f"   rho={rho} (ceiling {CEILING}) -> {pd['sealed_verdict']};  INCREMENT(geometry over scalar)="
              f"{increment}  perm_p={p_val}", flush=True)

    out = {"prereg": "v14/v13/v26", "n": N, "densities": DENSITIES, "ceiling": CEILING,
           "scalar_declared": "tuple_dispersion", "structural_features": FEATS_STRUCT, "per_density": per_density,
           "owner_odds_scalarizable": 0.35}
    json.dump(out, open("foundry/foundry/results/landscape/t14_scalarization.json", "w"), indent=2)
    print(f"\nwrote t14_scalarization.json")


if __name__ == "__main__":
    main()
