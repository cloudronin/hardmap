"""Pebble parity diagnostic (prereg_v20). Does the QUALIFIED `corr` observable read near-zero on >=3-ary PARITY —
whose point-to-set propagation is maximal (affine, globally rigid) but whose PAIRWISE correlation is ~0? If yes,
ξ-as-built is disqualified for measuring reach-proper (it computes the pairwise shadow, not the point-to-set length).

Exact coset enumeration at n=16 (no sampler noise). Parity is UNSAT at the calibration alpha=1.4, so measured at
alpha=0.6 (SAT regime); a same-density 2-affine reference controls for density. Poles (alpha=1.4): short 0 / medium
2-SAT 0.074 / long 2-affine 0.5.

Run: PYTHONPATH=... python foundry/dev/reach_parity_diagnostic.py
"""
import json
import statistics as st
from itertools import product

from foundry import reach as X
from foundry import ensemble as E

R3_XOR = frozenset({(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)})              # x⊕y⊕z = 0
R4_XOR = frozenset(t for t in product((0, 1), repeat=4) if sum(t) % 2 == 0)   # even parity, 8 tuples
R_EQ = X.R_EQ                                                                 # 2-affine reference (pairwise-visible)

N, ALPHA, NINST = 16, 0.6, 8
MEDIUM_POLE = 0.074


def measure(name, rels):
    scores, ncoset = [], []
    for i in range(NINST):
        inst = E.gen_instance(rels, (0, 1), N, ALPHA, 950000 + i, family_id=name)
        sols = X.enumerate_solutions(inst)
        if len(sols) < 2:
            continue
        scores.append(X.reach_corr_from_sols(inst, sols)["reach_score"])
        ncoset.append(len(sols))
    return {"name": name, "reach_score": round(st.mean(scores), 4) if scores else None,
            "per_instance": [round(s, 4) for s in scores], "median_coset": int(st.median(ncoset)) if ncoset else 0,
            "n_instances": len(scores)}


def main():
    res = {r["name"]: r for r in (measure("3-XOR (parity)", (R3_XOR,)),
                                  measure("4-XOR (parity)", (R4_XOR,)),
                                  measure("2-affine reference", (R_EQ,)))}
    for r in res.values():
        print(f"  {r['name']:22s} reach_score={r['reach_score']} (coset~{r['median_coset']}, n={r['n_instances']}) "
              f"per_inst={r['per_instance']}")

    p3 = res["3-XOR (parity)"]["reach_score"]
    p4 = res["4-XOR (parity)"]["reach_score"]
    ref = res["2-affine reference"]["reach_score"]
    parity_max = max(x for x in (p3, p4) if x is not None)
    verdict = ("DISQUALIFIED" if parity_max < MEDIUM_POLE else "PROCEEDS_WITH_CAVEAT")

    out = {"prereg": "v20", "n": N, "alpha": ALPHA, "medium_pole": MEDIUM_POLE,
           "results": res, "parity_max_reach": parity_max, "reference_reach": ref,
           "poles_at_alpha_1.4": {"short": 0.0, "medium": MEDIUM_POLE, "long": 0.5}, "VERDICT": verdict}
    json.dump(out, open("foundry/foundry/results/landscape/reach_parity_diagnostic.json", "w"), indent=2)
    print(f"\nparity max reach={parity_max}  vs  medium pole={MEDIUM_POLE}  vs  2-affine reference={ref}")
    print(f"VERDICT: {verdict}")


if __name__ == "__main__":
    main()
