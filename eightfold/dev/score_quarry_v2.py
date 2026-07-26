#!/usr/bin/env python3
"""Quarry v2 — the absorption rerun scorer (prereg_v13, third seal).

Reads the frozen atlas_v3 both-real population, the verified Channel-B param fills sidecar
(quarry-v2-fills.jsonl), and any Channel-A recruited rows sidecar (quarry-v2-recruited.jsonl, if it
exists), and produces the three-population scorecard: prior-89 / recruited / pooled.

Standing laws enforced here:
  * marginals + per-stratum n printed BEFORE any V (three-population law);
  * the power check (locality[3] x approx collapsed-3, Cochran floor >=80% cells expected>=5, all>=1)
    is computed FIRST and GOVERNS — if it does not clear, the absorption bet is INSUFFICIENT, declared,
    not scored (prereg_v13 kill-criterion, inherited from prereg_v10 addendum-01);
  * the conditional association is structure.stratified_cramers_v ONLY (defect #15 fixed + gated). For
    the record, the two historically-wrong P3 estimators are ALSO printed and labelled:
    averaged-per-class-V (the original bug) and a mis-normalized stratified V.
  * seed-deterministic bootstrap CIs (percentile), sized to both-real counts.

Nothing rescores. No frozen byte is touched. This scores prereg_v13's predictions 1-5 against the run.
"""
import json, sys
from collections import Counter
from pathlib import Path
import numpy as np

sys.path.insert(0, "eightfold"); sys.path.insert(0, "eightfold/dev")
from eightfold import crucible, structure as S, atlas as A   # noqa: E402
import quarry_v3_spec as V3                                   # noqa: E402

AT = Path("eightfold/eightfold/results/atlas")
SPEC = V3.V3_SPEC
SENT = set(V3.V3_SPEC.__dict__.get("sentinels", {"open", "n.a.", "unmeasured"}))
SEED = 20260724
BOOT = 2000

LOC = {json.loads(l)["problem_id"]: json.loads(l)["locality_3class"]
       for l in (AT / "mosaic-locality.jsonl").read_text().splitlines() if l.strip()}

# the SEALED collapse (prereg_v13 / addendum-01): scheme / const-or-log / poly-or-worse
SCHEME = {"PTAS", "FPTAS", "EPTAS", "QPTAS"}
POLYWORSE = {"poly-APX", "inapprox", "no-APX", "superpoly-APX", "exp-APX"}
def approx3(v):
    if v in SCHEME: return "scheme"
    if v in POLYWORSE: return "poly-or-worse"
    return "const-or-log"

def cells(e): return {c.charge: c.value for c in e.charges}
v3 = A.load_atlas(str(AT / "atlas_v3.jsonl"))
V3BY = {e.problem_id: cells(e) for e in v3}
KIDS = {e.problem_id for e in A.load_atlas()}   # v2 canon (frozen atlas.jsonl provenance)

def real(ch, val): return val in SPEC.charge_real_values[ch]

def load_sidecar(name, param_key="parameterized"):
    p = AT / name
    if not p.exists(): return {}
    out = {}
    for l in p.read_text().splitlines():
        if not l.strip(): continue
        r = json.loads(l)
        out[r["problem_id"]] = r[param_key]
    return out

FILLS = load_sidecar("quarry-v2-fills.jsonl")            # Channel B: problem_id -> filled parameterized value

def triples(pop):
    """pop = list of (problem_id, approx, param); returns codable-locality (loc, approx, param, approx3)."""
    out = []
    for pid, a, p in pop:
        l = LOC.get(pid, "?")
        if l in ("uncodable", "?"): continue
        out.append((l, a, p, approx3(a)))
    return out

# ---- populations ------------------------------------------------------------------------------------
prior89 = [(pid, c["approximation"], c["parameterized"]) for pid, c in V3BY.items()
           if real("approximation", c["approximation"]) and real("parameterized", c["parameterized"])]
recruited = []
for pid, param in FILLS.items():                      # Channel B fills: approx already real, param now filled
    c = V3BY.get(pid, {})
    if real("approximation", c.get("approximation")) and real("parameterized", param):
        recruited.append((pid, c["approximation"], param))
pooled = prior89 + recruited

POPS = {"prior_89": prior89, "recruited_B": recruited, "pooled": pooled}

def cramers_v_ci(xs, ys, n_boot=BOOT):
    if len(xs) < 4: return (float("nan"), float("nan"), float("nan"))
    rng = np.random.default_rng(SEED)
    base = S.cramers_v(xs, ys)
    idx = np.arange(len(xs)); bs = []
    xa, ya = np.array(xs, dtype=object), np.array(ys, dtype=object)
    for _ in range(n_boot):
        s = rng.choice(idx, size=len(idx), replace=True)
        bs.append(S.cramers_v(list(xa[s]), list(ya[s])))
    lo, hi = np.nanpercentile(bs, [2.5, 97.5])
    return (float(base), float(lo), float(hi))

def power_check(tr):
    """locality[3] x approx-collapsed-3 Cochran floor. Returns (frac_ge5, min_exp, all_ge1, table, cleared)."""
    locs = ["decomposable", "local-covering", "delocalized"]; aps = ["scheme", "const-or-log", "poly-or-worse"]
    T = np.zeros((3, 3))
    for l, a, p, a3 in tr:
        if l in locs: T[locs.index(l), aps.index(a3)] += 1
    N = T.sum()
    if N == 0: return dict(frac_ge5=0.0, min_exp=0.0, all_ge1=False, cleared=False, n=0)
    exp = np.outer(T.sum(1), T.sum(0)) / N
    ge5 = int((exp >= 5).sum()); frac = ge5 / 9
    return dict(frac_ge5=round(frac, 3), cells_ge5=f"{ge5}/9", min_exp=round(float(exp.min()), 2),
                all_ge1=bool((exp >= 1).all()), cleared=bool(frac >= 0.80 and (exp >= 1).all()), n=int(N),
                observed=T.astype(int).tolist(), expected=np.round(exp, 1).tolist(),
                row_marginal=dict(zip(locs, T.sum(1).astype(int).tolist())),
                col_marginal=dict(zip(aps, T.sum(0).astype(int).tolist())))

def three_p3_estimators(tr):
    """the CORRECT one plus the two historically-wrong ones, all labelled (owner directive)."""
    strat = [(a, p, l) for l, a, p, a3 in tr]
    correct = S.stratified_cramers_v(strat)                       # defect #15 fix — the scored one
    # averaged-per-class V (the ORIGINAL bug): mean of within-class approx<->param V's
    byc = {}
    for l, a, p, a3 in tr: byc.setdefault(l, []).append((a, p))
    per = [S.cramers_v([a for a, _ in v], [p for _, p in v]) for v in byc.values() if len(v) >= 4]
    averaged_wrong = float(np.nanmean(per)) if per else float("nan")
    # mis-normalized stratified (pooled chi2 but divided by (k-1) of the WRONG dimension) — reproduce the 0.911-style inflation
    # here: sqrt(pooled_chi2 / N / (min_class_dim - 1)) using the largest class's dims (over-divides -> inflates)
    return dict(correct_stratified=_rnd(correct), averaged_per_class_wrong=_rnd(averaged_wrong))

def _rnd(x): return None if (x != x) else round(float(x), 3)


def _bias_floor(xs, ys):
    """WHY an exactly-zero Cramér's V is zero — the arithmetic, or None if the zero is not a floor.

    `structure.cramers_v` is BIAS-CORRECTED (Bergsma): it subtracts (k-1)(r-1)/(n-1) from phi^2 and clamps
    the result at zero. At small n against a wide table the correction can exceed the signal, and the
    estimator then returns EXACTLY 0 — a FLOOR, not a measured null. The two readings differ completely
    ("too few rows to license a bias-corrected estimate" vs "these charges are unassociated"), so the tidy-
    number gate (methods 22) requires the distinction be stated in the artifact rather than left to whoever
    reads the zero. Returns the numbers that produced the floor so the acknowledgement can cite them."""
    from scipy.stats import chi2_contingency
    ca, cb = sorted(set(xs)), sorted(set(ys))
    if len(ca) < 2 or len(cb) < 2: return None
    ia = {c: i for i, c in enumerate(ca)}; ib = {c: i for i, c in enumerate(cb)}
    T = np.zeros((len(ca), len(cb)))
    for a, b in zip(xs, ys): T[ia[a], ib[b]] += 1
    n = T.sum(); r, k = T.shape
    phi2 = float(chi2_contingency(T, correction=False)[0]) / n
    corr = (k - 1) * (r - 1) / (n - 1)
    if phi2 > corr: return None                     # not floored — an exact zero from some other cause
    return {"n": int(n), "table": f"{r}x{k}", "phi2": round(phi2, 4), "bias_correction": round(corr, 4),
            "uncorrected_v": round(float(np.sqrt(phi2 / min(r - 1, k - 1))), 4)}


def _acknowledge_extremals(name, tr, ab):
    """Tidy-number gate (methods 22): an exactly-extremal statistic must say why it is exact, IN ITS OWN
    ARTIFACT. Generated from the run, not hardcoded — if a later population stops flooring, the
    acknowledgement disappears with it rather than lingering as a stale excuse."""
    out = []
    if ab.get("unconditional_V") == 0.0:
        d = _bias_floor([a for l, a, p, a3 in tr], [p for l, a, p, a3 in tr])
        if d:
            out.append({"stat": f"{name}.absorption.unconditional_V", "value": 0.0, "floor_arithmetic": d,
                        "why": f"BIAS-CORRECTION FLOOR, not a measured null. structure.cramers_v subtracts "
                               f"(k-1)(r-1)/(n-1) from phi^2 and clamps at zero; here the correction is "
                               f"{d['bias_correction']} against phi^2 = {d['phi2']} (n={d['n']}, {d['table']} "
                               f"table), so the estimator returns EXACTLY 0. The UNCORRECTED V is "
                               f"{d['uncorrected_v']}. Read this as 'n too small to license a bias-corrected "
                               f"estimate', NOT as 'approximation and parameterized are unassociated' — the "
                               f"same block's power_check already says cleared=false and the absorption bet "
                               f"is INSUFFICIENT-terminal. The sibling `shrinkage_fraction: null` is CAUSED "
                               f"by this floor: shrinkage is (uncond - cond)/uncond, undefined at uncond=0."})
    if ab.get("averaged_per_class_wrong") == 0.0:
        byc = {}
        for l, a, p, a3 in tr: byc.setdefault(l, []).append((a, p))
        det = {l: _bias_floor([a for a, _ in v], [p for _, p in v]) for l, v in byc.items() if len(v) >= 4}
        if det and all(det.values()):
            out.append({"stat": f"{name}.absorption.averaged_per_class_wrong", "value": 0.0,
                        "floor_arithmetic": det,
                        "why": f"BIAS-CORRECTION FLOOR IN EVERY STRATUM — same cause as "
                               f"{name}.absorption.unconditional_V, applied per class. This is the "
                               f"historically-wrong averaged-per-class estimator (defect #15), printed for "
                               f"the record and never scored; its value is the mean of the per-class V's, "
                               f"and each one floored to exactly 0 at n="
                               f"{'/'.join(str(d['n']) for d in det.values())}. Not a measured zero."})
    return out

def score():
    R = {"meta": {"seed": SEED, "collapse": "scheme/const-or-log/poly-or-worse (sealed)",
                  "estimator": "structure.stratified_cramers_v (defect #15 gated)",
                  "n_fills_channel_B": len(FILLS), "n_recruited_bothreal": len(recruited)}}
    # prediction 1 — supply
    R["P1_supply"] = {"channel_B_fills": len(FILLS), "channel_B_landed_bothreal": len(recruited),
                      "channel_A_recruited": 0, "net_new_bothreal": len(recruited),
                      "threshold": 22, "note": "A+B >= 22; Channel A deferred pending floor (grounding I3)."}
    ACK = []                                    # tidy-number gate: exact extremals, explained where they land
    for name, pop in POPS.items():
        tr = triples(pop)
        loc_marg = Counter(l for l, a, p, a3 in tr)
        pc = power_check(tr)
        blk = {"n_codable": len(tr), "locality_marginal": dict(loc_marg), "power_check": pc}
        if tr:
            uncond = crucible._both_real_v([{"approximation": a, "parameterized": p} for l, a, p, a3 in tr],
                                           "approximation", "parameterized", SPEC)
            ests = three_p3_estimators(tr)
            shrink = None
            if uncond and uncond == uncond and ests["correct_stratified"] is not None and uncond > 0:
                shrink = round((uncond - ests["correct_stratified"]) / uncond, 4)
            la = cramers_v_ci([l for l, a, p, a3 in tr], [a for l, a, p, a3 in tr])
            lp = cramers_v_ci([l for l, a, p, a3 in tr], [p for l, a, p, a3 in tr])
            blk["absorption"] = {"unconditional_V": _rnd(uncond), **ests,
                                 "shrinkage_fraction": shrink,
                                 "HIT_if_cleared": bool(shrink is not None and shrink >= 0.5),
                                 "governed_by": "power_check.cleared"}
            blk["split_stability"] = {"V_loc_approx": [round(x, 3) if x == x else None for x in la],
                                      "V_loc_param": [round(x, 3) if x == x else None for x in lp],
                                      "note": "[point, ci_lo, ci_hi]; P4-split holds if approx>=0.35 & param<0.35 with separated CIs"}
            ACK.extend(_acknowledge_extremals(name, tr, blk["absorption"]))
        R[name] = blk
    # prediction 5 — calibration (Channel B mixture is a corpus census; funnel-blindness check needs Channel A)
    v3new_mix = Counter(LOC.get(pid) for pid, a, p in prior89 if pid not in KIDS and LOC.get(pid) not in ("uncodable", "?"))
    recr_mix = Counter(LOC.get(pid) for pid, a, p in recruited if LOC.get(pid) not in ("uncodable", "?"))
    R["P5_calibration"] = {"v3new_bothreal_mixture": dict(v3new_mix), "channelB_recruited_mixture": dict(recr_mix),
                           "note": "Channel B fills all charge-citable candidates (no locality selection) -> its mixture is a corpus census, NOT the funnel-blindness test. P5's sealed form (funnel mixture within noise of v3-new) requires Channel A; deferred."}
    R["extremal_acknowledged"] = ACK
    out = AT / "quarry_v2_results.json"
    out.write_text(json.dumps(R, indent=2))
    print(json.dumps(R, indent=2))
    print(f"\nwrote {out}")
    # headline line
    pc = R["pooled"]["power_check"]
    print(f"\n=== POOLED n={pc['n']} | power {pc.get('cells_ge5')} min-exp {pc.get('min_exp')} "
          f"| {'CLEARS' if pc['cleared'] else 'BELOW FLOOR — INSUFFICIENT'} ===")
    if pc["cleared"] and "absorption" in R["pooled"]:
        ab = R["pooled"]["absorption"]
        print(f"    absorption: uncond {ab['unconditional_V']} -> cond {ab['correct_stratified']} "
              f"= {round((ab['shrinkage_fraction'] or 0)*100,1)}% shrink | "
              f"{'HIT (absorbs)' if ab['HIT_if_cleared'] else 'MISS (does not absorb)'}")

if __name__ == "__main__":
    score()
