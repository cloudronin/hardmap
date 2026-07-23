"""Prism direction check (post-hoc descriptive; NOT sealed) — pin the direction of the bridge-completed
(non-affine) approx<->param residual. The bridge nets the affine off-diagonal (affine=>WS=>FPT), so the
residual set is the NON-AFFINE both-real objective rows. Report V + Spearman for the pooled set and Min-Ones
only, with the class-level effective-n. Mirrors prism_matrix.py conventions exactly (APX_RANK, FPT=0/W1=1).

Run: PYTHONPATH=... python foundry/dev/prism_direction_check.py
"""
import numpy as np

from eightfold import structure as S
from foundry import prism

APX_RANK = {v: i for i, v in enumerate(prism.OO.APPROX_ORDER)}


def _spearman(x, y):
    if len(x) < 3 or len(set(x)) < 2 or len(set(y)) < 2:
        return None
    rx, ry = np.argsort(np.argsort(x)), np.argsort(np.argsort(y))
    return round(float(np.corrcoef(rx, ry)[0, 1]), 3)


def _v(xs, ys):
    if len(xs) < 3 or len(set(xs)) < 2 or len(set(ys)) < 2:
        return None
    v = S.cramers_v(xs, ys)
    return round(float(v), 3) if v == v else None


def main():
    roster = prism.build_roster(3)
    rows = [c for _, _, _, c in roster]

    # both-real objective rows, carrying the affine flag and which objective
    pooled, minones, maxones = [], [], []
    for r in rows:
        if r["parameterized"] == "open":
            continue
        aff = r["flags"]["affine"]
        for obj, key in (("max", "approx_maxones"), ("min", "approx_minones")):
            row = (r[key], r["parameterized"], aff)
            pooled.append(row)
            (maxones if obj == "max" else minones).append(row)

    n_param_classes = sum(1 for r in rows if r["parameterized"] != "open")
    n_nonaffine_classes = sum(1 for r in rows if r["parameterized"] != "open" and not r["flags"]["affine"])

    def report(label, data):
        nonaff = [(a, p) for a, p, x in data if not x]
        ax = [APX_RANK[a] for a, _ in nonaff]
        px = [0 if p == "FPT" else 1 for _, p in nonaff]
        av = [a for a, _ in nonaff]; pv = [p for _, p in nonaff]
        print(f"  {label:12s} n_rows={len(nonaff):3d}  V={_v(av, pv)}  Spearman={_spearman(ax, px)}")

    print(f"param-real classes = {n_param_classes}; non-affine param-real classes = {n_nonaffine_classes}")
    print("bridge-completed (NON-AFFINE) residual — post-hoc descriptive, effective-n = classes above:")
    report("pooled", pooled)
    report("max-ones", maxones)
    report("min-ones", minones)


if __name__ == "__main__":
    main()
