"""Sprint 4 domain-confound check (Task 3 hold) — reproducible: |D|=3 poles, same-relation isolator, class
contrasts (normalized + raw), and the H_I6a Mann-Whitney. Writes results/landscape/confound_check.json.

Run: PYTHONPATH=... python foundry/dev/confound_check.py
"""
import json
import statistics as st

from foundry import domain3 as D3
from foundry import ensemble as E
from foundry import landscape_run as LR
from foundry import postlattice as PL
from foundry import solscape as S

R_IMPL = frozenset({(0, 0), (0, 1), (1, 1)})                                  # x<=y over |D|=2 (implication)
R_ZERO = frozenset((a, b) for a in (0, 1, 2) for b in (0, 1, 2) if a == 0 or b == 0)   # |D|=3 0-attractor
R_EQ = frozenset({(0, 0), (1, 1), (2, 2)})                                    # |D|=3 equality (bad pole)


def _raw(rels, dom, n, a, seeds):
    vals = []
    for s in seeds:
        sols = S.sample_dpll(E.gen_instance(rels, dom, n, a, s, "r"), s, K=40)
        if len(sols) >= 3:
            vals.append((1 - st.mean(S.pairwise_overlaps(sols))) / 2)
    return round(st.mean(vals), 3) if vals else None


def reading(name, rels, dom, n):
    a_struct, _ = LR.locate_alpha_struct(rels, dom, n, 77000, K=40)
    out = {"alpha_struct": a_struct, "domain_size": len(dom)}
    for frac in (0.7, 0.9):
        a = round(frac * a_struct, 3)
        norm = S.landscape_reading(rels, dom, n, a, base_seed=79000, K=40, n_instances=6)["pooled_score"]
        out[str(frac)] = {"alpha": a, "normalized": norm, "raw": _raw(rels, dom, n, a, range(79500, 79506))}
    return out


def mann_whitney(a, b, n_perm=20000, seed=1):
    import numpy as np
    def U(av, bv):
        return sum(1 for x in av for y in bv if x > y) + 0.5 * sum(1 for x in av for y in bv if x == y)
    obs = U(a, b)
    rng = np.random.default_rng(seed)
    vals, na = a + b, len(a)
    ge = 0
    for _ in range(n_perm):
        p = rng.permutation(len(vals))
        aa = [vals[p[i]] for i in range(na)]
        bb = [vals[p[i]] for i in range(na, len(vals))]
        if U(aa, bb) >= obs - 1e-9:
            ge += 1
    return {"U": obs, "max": na * len(b), "rank_biserial": round(2 * obs / (na * len(b)) - 1, 3),
            "perm_p": round((ge + 1) / (n_perm + 1), 4), "n_affine": na, "n_bounded": len(b)}


def main():
    res = {"poles_and_contrasts": {
        "implication_leq_D2": reading("implication", (R_IMPL,), (0, 1), 20),
        "NAND_horn_D2": reading("nand-horn", (PL.R_NOR3, PL.R_TRUE), (0, 1), 20),
        "order3_leq_D3": reading("order-3", (D3.R_LEQ3,), (0, 1, 2), 15),
        "zero_attractor_D3_SMOOTH_POLE": reading("0-attractor", (R_ZERO,), (0, 1, 2), 15),
        "equality_D3_bad_pole": reading("equality", (R_EQ,), (0, 1, 2), 15),
        "lineq_z3_D3_RUGGED_POLE": reading("lin-eq-z3", (D3.R_LINEQ3,), (0, 1, 2), 15),
        "2sat_D2": reading("2-sat", (PL.R_POS2, PL.R_NEG2), (0, 1), 20),
    }}
    conf = json.load(open("foundry/foundry/results/landscape/confirm_v7.json"))["measured"]
    res["H_I6a_mann_whitney"] = {}
    for tag in ("0.7", "0.9"):
        aff = [f["readings"][tag]["score"] for f in conf.values() if f["localization"] == "unbounded"]
        bnd = [f["readings"][tag]["score"] for f in conf.values() if f["localization"] == "bounded"]
        res["H_I6a_mann_whitney"][tag] = mann_whitney(aff, bnd)
    res["_manifest"] = {"prereg": "v8", "provenance": "sampled-population", "instrument": "foundry.solscape",
                        "conclusion": "metric NOT domain-biased; ruggedness is relation-specific; anomaly WITHDRAWN"}
    json.dump(res, open("foundry/foundry/results/landscape/confound_check.json", "w"), indent=2)
    print("wrote confound_check.json")
    print("0-attractor(smooth pole) norm:", res["poles_and_contrasts"]["zero_attractor_D3_SMOOTH_POLE"]["0.9"]["normalized"])
    print("implication(<=,D2) norm:", res["poles_and_contrasts"]["implication_leq_D2"]["0.9"]["normalized"])
    print("H_I6a MWU @0.9:", res["H_I6a_mann_whitney"]["0.9"])


if __name__ == "__main__":
    main()
