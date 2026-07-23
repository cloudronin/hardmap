"""Pebble P4 (prereg_v25) — is the point-to-set reach residue TERRAIN-RELEVANT? For each bounded-width roster
relation, measure point-to-set reach (r=2) AND ruggedness at a COMMON density/size (n=18, 0.6*alpha_struct);
tuple_dispersion is a density-free relation property. Then: does reach add INCREMENTAL held-out (leave-one-co-clone-
out) predictive power for ruggedness OVER a tuple_dispersion baseline? Permutation null on the increment. If not,
reach is a slower route to what the free scalar already carries — a clean negative.

Run: PYTHONPATH=... python foundry/dev/pointset_p4.py
"""
import json
import statistics as st

import numpy as np

from foundry import pointset as PS
from foundry import solscape as S
from foundry import ensemble as E
from foundry import relfeatures as RF

N, NINST, RADIUS, DFRAC = 18, 4, 2, 0.6
BW = {"horn", "dhorn", "bij"}


def heldout_corr(rows, feats):
    """Leave-one-co-clone-out; fit ruggedness ~ feats on train, predict test, pooled corr(pred, actual)."""
    ccs = sorted({r["coclone"] for r in rows})
    preds, acts = [], []
    for cc in ccs:
        tr = [r for r in rows if r["coclone"] != cc]
        te = [r for r in rows if r["coclone"] == cc]
        if len(tr) < 5 or not te:
            continue
        X = np.array([[r[f] for f in feats] for r in tr], float)
        y = np.array([r["ruggedness"] for r in tr], float)
        _, beta = RF.fit_r2(X, y)
        for r in te:
            preds.append(beta[0] + sum(beta[i + 1] * r[f] for i, f in enumerate(feats)))
            acts.append(r["ruggedness"])
    if len(set(preds)) < 2 or len(set(acts)) < 2:
        return None
    return float(np.corrcoef(preds, acts)[0, 1])


def main():
    roster = json.load(open("foundry/foundry/results/landscape/sprint46_roster.json"))["rows"]
    bw = [r for r in roster if set(r["profile"].split("+")) & BW]
    print(f"P4: {len(bw)} bounded-width relations; measuring reach + ruggedness @ n={N}, 0.6*alpha_struct", flush=True)

    rows = []
    for i, rec in enumerate(bw):
        R = frozenset(tuple(t) for t in rec["relation"])
        alpha = round(DFRAC * rec["alpha_struct"], 3)
        reach = PS.measure_pointset((R,), (0, 1), N, alpha, n_instances=NINST, base_seed=980000 + i, reach_radius=RADIUS)["reach_score"]
        rug = S.landscape_reading((R,), (0, 1), N, alpha, base_seed=981000 + i, K=35, n_instances=NINST)["pooled_score"]
        td = RF.tuple_dispersion(R)
        if reach is None or rug is None:
            continue
        rows.append({"coclone": rec["profile"], "tuple_dispersion": td, "reach": reach, "ruggedness": rug})
    print(f"  usable rows: {len(rows)} across {len(set(r['coclone'] for r in rows))} co-clones", flush=True)

    base = heldout_corr(rows, ["tuple_dispersion"])
    full = heldout_corr(rows, ["tuple_dispersion", "reach"])
    reach_only = heldout_corr(rows, ["reach"])
    increment = round(full - base, 4) if (base is not None and full is not None) else None

    # permutation null on the increment: shuffle reach across rows, recompute increment
    rng = np.random.default_rng(25)
    perm_incs = []
    reaches = [r["reach"] for r in rows]
    for _ in range(2000):
        perm = rng.permutation(reaches)
        pr = [dict(r, reach=float(perm[j])) for j, r in enumerate(rows)]
        f = heldout_corr(pr, ["tuple_dispersion", "reach"])
        if f is not None and base is not None:
            perm_incs.append(f - base)
    p_val = round(float(np.mean([pi >= increment for pi in perm_incs])), 4) if (perm_incs and increment is not None) else None

    # concentration: per-co-clone partial corr of reach with ruggedness residual (after removing tuple_dispersion)
    conc = {}
    for cc in sorted({r["coclone"] for r in rows}):
        sub = [r for r in rows if r["coclone"] == cc]
        if len(sub) < 3:
            continue
        X = np.array([[r["tuple_dispersion"]] for r in sub], float)
        y = np.array([r["ruggedness"] for r in sub], float)
        _, beta = RF.fit_r2(X, y)
        resid = [r["ruggedness"] - (beta[0] + beta[1] * r["tuple_dispersion"]) for r in sub]
        rc = [r["reach"] for r in sub]
        if len(set(rc)) > 1 and len(set(resid)) > 1:
            conc[cc] = round(float(np.corrcoef(rc, resid)[0, 1]), 3)

    verdict = ("INCREMENTAL" if (increment is not None and increment > 0 and p_val is not None and p_val < 0.05)
               else "NOT_INCREMENTAL" if (increment is not None and increment <= 0.02)
               else "INCONCLUSIVE")
    out = {"prereg": "v25", "n": N, "n_rows": len(rows), "n_coclones": len(set(r["coclone"] for r in rows)),
           "heldout_corr": {"tuple_dispersion_baseline": round(base, 4) if base is not None else None,
                            "plus_reach": round(full, 4) if full is not None else None,
                            "reach_only_standalone": round(reach_only, 4) if reach_only is not None else None},
           "increment_reach_over_tupledisp": increment, "permutation_p": p_val,
           "concentration_per_coclone_reach_vs_ruggedness_residual": conc, "VERDICT": verdict}
    json.dump(out, open("foundry/foundry/results/landscape/pointset_p4.json", "w"), indent=2)
    print(f"\nheld-out corr: baseline(tuple_disp)={out['heldout_corr']['tuple_dispersion_baseline']}  "
          f"+reach={out['heldout_corr']['plus_reach']}  reach_only={out['heldout_corr']['reach_only_standalone']}")
    print(f"INCREMENT (reach over tuple_disp) = {increment}  perm_p = {p_val}")
    print(f"concentration (per-co-clone reach vs ruggedness residual): {conc}")
    print(f"VERDICT: {verdict}")


if __name__ == "__main__":
    main()
