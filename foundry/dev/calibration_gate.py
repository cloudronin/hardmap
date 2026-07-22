"""Sprint 4 calibration gate (Task 1c) — reproducible run: two-pole Vega, affine-exact bias, 14-family table.

Run: PYTHONPATH=... python foundry/dev/calibration_gate.py
This is the owner-review artifact behind docs/findings/Sprint4-calibration-gate.md. Sampled-population (R-d);
numbers are stable to the samplers' string-seeded RNG.
"""
import statistics as st

from foundry import domain3 as D3
from foundry import finer as FN
from foundry import postlattice as PL
from foundry import solscape as S

R1 = FN.R_XOR3_1
FAMILIES = [
    ("xor-sat", "affine", (PL.R_XOR3, PL.R_XOR2), (0, 1), 16, 0.5),
    ("zerovalid-affine", "affine", (PL.R_XOR3,), (0, 1), 16, 0.5),
    ("onevalid-affine", "affine", (R1,), (0, 1), 16, 0.5),
    ("lin-eq-z3", "affine", (D3.R_LINEQ3,), (0, 1, 2), 12, 0.5),
    ("lin-eq-z3-b", "affine", (D3.R_LINEQ3B,), (0, 1, 2), 12, 0.5),
    ("horn-sat", "bounded", (PL.R_NOR3, PL.R_TRUE), (0, 1), 16, 0.4),
    ("dual-horn", "bounded", (PL.R_OR3, PL.R_FALSE), (0, 1), 16, 0.4),
    ("2-sat", "bounded", (PL.R_POS2, PL.R_NEG2), (0, 1), 16, 0.6),
    ("zerovalid-horn", "bounded", (PL.R_NOR3, PL.R_FALSE), (0, 1), 16, 0.4),
    ("zerovalid-bijunctive", "bounded", (PL.R_NEG2,), (0, 1), 16, 0.6),
    ("onevalid-dualhorn", "bounded", (PL.R_OR3, PL.R_TRUE), (0, 1), 16, 0.4),
    ("onevalid-bijunctive", "bounded", (PL.R_POS2,), (0, 1), 16, 0.6),
    ("order-3", "bounded", (D3.R_LEQ3,), (0, 1, 2), 12, 0.7),
    ("median-3", "bounded", (D3.R_LEQ3, D3.R_MIN_SL), (0, 1, 2), 12, 0.7),
]


def main():
    xor = dict(rels=(PL.R_XOR3,), domain=(0, 1), n=16, alpha=0.5)
    horn = dict(rels=(PL.R_NOR3, PL.R_TRUE), domain=(0, 1), n=16, alpha=0.4)
    twosat = dict(rels=(PL.R_POS2, PL.R_NEG2), domain=(0, 1), n=16, alpha=0.6)
    print("VEGA XOR(rugged) vs HORN(smooth):", S.vega_calibration(xor, horn))
    print("VEGA XOR(rugged) vs 2SAT(invalid smooth):", S.vega_calibration(xor, twosat))
    print("AFFINE-EXACT sampler bias (XOR):", S.affine_bias((PL.R_XOR3,), (0, 1), 16, 0.5))
    print("\n14-family landscape table (pooled dpll+walksat, 4 instances):")
    rows = []
    for fid, arm, rels, dom, n, a in FAMILIES:
        r = S.landscape_reading(rels, dom, n, a)
        rows.append((fid, arm, r["pooled_score"], r["concordance_gap"]))
        print(f"  {fid:22s} {arm:8s} score={r['pooled_score']} concord={r['concordance_gap']}")
    aff = [r[2] for r in rows if r[1] == "affine"]
    bnd = [r[2] for r in rows if r[1] == "bounded"]
    print(f"\naffine mean={st.mean(aff):.3f}  bounded mean={st.mean(bnd):.3f}  "
          f"separation={st.mean(aff) - st.mean(bnd):+.3f}  bounded range=[{min(bnd):.2f},{max(bnd):.2f}]")
    print(f"max concordance gap across families = {max(r[3] for r in rows)}")


if __name__ == "__main__":
    main()
