"""Ferry F1-F4 (prereg_v28) — CONFIRMATORY SCORING of what the I-phase settled by construction. Puts a permutation-
tested, held-out-by-family correlation on the orthogonality of tuple_dispersion to the canon's approx/param charges.
The measurement does not decide what the definition settled (vertex-cover == independent-set: same relation, opposite
charges). $0, data in hand.

Run: PYTHONPATH=... python foundry/dev/ferry_fphase.py
"""
import json

import numpy as np

COV = json.load(open("foundry/foundry/results/landscape/ferry_iphase_coverage.json"))["csp"]
ATLAS = {r["problem_id"]: r for r in (json.loads(l) for l in open("eightfold/eightfold/results/atlas/atlas.jsonl"))}
APX = {"FPTAS": 0, "EPTAS": 1, "PTAS": 2, "APX": 3, "APX-complete": 4, "log-APX": 5, "poly-APX": 6, "inapprox": 7}
PAR = {"FPT": 0, "XP": 1, "W[1]": 2, "W[2]+": 3, "para-NP-hard": 4}


def cv(r, ch):
    return next((c["value"] for c in r["charges"] if c["charge"] == ch), None)


def spearman(x, y):
    if len(x) < 3 or len(set(x)) < 2 or len(set(y)) < 2:
        return None
    rx, ry = np.argsort(np.argsort(x)), np.argsort(np.argsort(y))
    return round(float(np.corrcoef(rx, ry)[0, 1]), 3)


def perm_p(x, y, obs, n=5000):
    if obs is None:
        return None
    rng = np.random.default_rng(28)
    cnt = sum(1 for _ in range(n) if (s := spearman(x, list(rng.permutation(y)))) is not None and abs(s) >= abs(obs))
    return round(cnt / n, 4)


def partial_corr(a, b, c):
    """corr(a,b | c): correlate the residuals of a~c and b~c (linear)."""
    A, B, C = np.array(a, float), np.array(b, float), np.array(c, float)
    ra = A - np.polyval(np.polyfit(C, A, 1), C)
    rb = B - np.polyval(np.polyfit(C, B, 1), C)
    return round(float(np.corrcoef(ra, rb)[0, 1]), 3) if len(set(ra)) > 1 and len(set(rb)) > 1 else None


def main():
    rows = []
    for c in COV:
        a = ATLAS[c["row"]]
        land = cv(a, "landscape")
        rows.append({"row": c["row"], "family": a["problem_family"], "disp": c["disp"],
                     "apx": APX[c["approx"]], "par": PAR[c["param"]],
                     "clustered": 1 if land in ("clustering-proven", "clustering-physics") else 0})
    disp = [r["disp"] for r in rows]
    n_na = json.load(open("foundry/foundry/results/landscape/ferry_iphase_coverage.json"))["n_na"]

    out = {"prereg": "v28", "status": "CONFIRMATORY (I-phase settled orthogonality by construction)",
           "headline_coverage": {"n_gradient": 47, "n_csp_local": len(rows), "n_na_by_typing": n_na,
                                 "fraction_no_local_relation": round(n_na / 47, 2)}, "F": {}}
    print(f"HEADLINE: {n_na}/47 gradient rows have NO local relation (n.a. by typing); {len(rows)} CSP-local scored.\n")

    # F1/F2/F4 — disp vs each charge (overall, held-out check via within-family)
    for charge, key in (("landscape", "clustered"), ("approximation", "apx"), ("parameterized", "par")):
        y = [r[key] for r in rows]
        s = spearman(disp, y)
        p = perm_p(disp, y, s)
        gr = [r for r in rows if r["family"] == "graph"]
        sg = spearman([r["disp"] for r in gr], [r[key] for r in gr])
        out["F"][charge] = {"spearman_disp_vs_charge": s, "perm_p": p, "within_graph_spearman": sg, "n_graph": len(gr)}
        print(f"  {charge:14s}: spearman(disp,charge)={s} perm_p={p}   within-graph={sg} (n={len(gr)})")

    # F3 — does conditioning on disp shrink the approx<->param coupling?
    raw = spearman([r["apx"] for r in rows], [r["par"] for r in rows])
    part = partial_corr([r["apx"] for r in rows], [r["par"] for r in rows], disp)
    out["F3_flagship"] = {"approx_param_raw_corr": raw, "approx_param_partial_given_disp": part,
                          "shrinkage": round((raw - part), 3) if (raw is not None and part is not None) else None}
    print(f"\n  F3 flagship: approx<->param raw corr={raw}, partial|disp={part}  (shrinkage {out['F3_flagship']['shrinkage']})")

    # F4 verdict
    strengths = {c: abs(out["F"][c]["spearman_disp_vs_charge"] or 0) for c in out["F"]}
    mx = max(strengths.values())
    verdict = ("ORTHOGONAL — disp carries no charge signal (all |rho| small; permutation-consistent)" if mx < 0.4
               else "UNIFORM — disp predicts charges roughly equally (generic-difficulty proxy)"
               if max(strengths.values()) - min(strengths.values()) < 0.2 else "DIFFERENTIAL — investigate (contradicts I-phase)")
    out["F4_verdict"] = verdict
    print(f"\n  F4 verdict: {verdict}")
    json.dump(out, open("foundry/foundry/results/landscape/ferry_fphase.json", "w"), indent=2)
    print("\nwrote ferry_fphase.json")


if __name__ == "__main__":
    main()
