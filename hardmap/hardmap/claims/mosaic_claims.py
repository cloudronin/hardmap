"""Repro claims for the Quarry v2 absorption close-out (prereg_v13).

Every function RECOMPUTES its headline number from the frozen atlas_v3 + the mosaic-locality sidecar + the
dual-pass-verified quarry-v2-fills sidecar (no reading-back of a committed result JSON). Deterministic point
estimates only — bootstrap CIs live in the results artifact, not here. `hardmap repro` re-derives:

  * the two-property SPLIT (V(loc,approx) high, V(loc,param) low) on the pooled-111 population,
  * the 2-class absorption MISS (uncond -> 2-class conditional, negative shrinkage),
  * the 3-class power shortfall (7/9, the terminal INSUFFICIENT),
  * Channel B's verified supply (22).

Estimators are the same gated ones the bet battery uses: structure.cramers_v / stratified_cramers_v
(defect #15) and crucible._both_real_v (R25 both-real convention).
"""
from __future__ import annotations

import json
from pathlib import Path

import eightfold
from eightfold import atlas as A, crucible, structure as S


def _atlas_dir() -> Path:
    return Path(eightfold.__file__).resolve().parent / "results" / "atlas"


def _spec():
    import sys
    dev = Path(eightfold.__file__).resolve().parent.parent / "dev"
    if str(dev) not in sys.path:
        sys.path.insert(0, str(dev))
    import quarry_v3_spec
    return quarry_v3_spec.V3_SPEC


_SENT = {"open", "n.a.", "unmeasured"}
_SCHEME = {"PTAS", "FPTAS", "EPTAS", "QPTAS"}
_POLYW = {"poly-APX", "inapprox", "no-APX", "superpoly-APX"}


def _approx3(v: str) -> str:
    if v in _SCHEME:
        return "scheme"
    if v in _POLYW:
        return "poly-or-worse"
    return "const-or-log"


def _loc():
    d = _atlas_dir()
    return {json.loads(l)["problem_id"]: json.loads(l)["locality_3class"]
            for l in (d / "mosaic-locality.jsonl").read_text().splitlines() if l.strip()}


def _fills():
    d = _atlas_dir()
    return {json.loads(l)["problem_id"]: json.loads(l)["parameterized"]
            for l in (d / "quarry-v2-fills.jsonl").read_text().splitlines() if l.strip()}


def _pooled_triples():
    """(locality3, approx, param) over pooled-111 = prior-89 both-real + verified Channel-B fills."""
    spec = _spec()
    real = spec.charge_real_values
    v3 = {e.problem_id: {c.charge: c.value for c in e.charges}
          for e in A.load_atlas(str(_atlas_dir() / "atlas_v3.jsonl"))}
    loc, fills = _loc(), _fills()
    out = []
    for pid, c in v3.items():
        a, p = c["approximation"], c["parameterized"]
        if pid in fills and p in _SENT:
            p = fills[pid]
        if a not in real["approximation"] or p not in real["parameterized"]:
            continue
        l = loc.get(pid)
        if l in ("uncodable", "?", None):
            continue
        out.append((l, a, p))
    return out


def split_pooled() -> dict:
    """The two-property split on pooled-111: locality predicts approximation, not parameterized."""
    tr = _pooled_triples()
    va = S.cramers_v([l for l, a, p in tr], [a for l, a, p in tr])
    vp = S.cramers_v([l for l, a, p in tr], [p for l, a, p in tr])
    return {"n": len(tr), "V_loc_approx": round(float(va), 3), "V_loc_param": round(float(vp), 3)}


def absorption_2class() -> dict:
    """The scored absorption verdict: 2-class locality does NOT absorb the coupling (negative shrinkage)."""
    tr = _pooled_triples()
    def loc2(l): return "delocalized" if l == "delocalized" else "local"
    uncond = crucible._both_real_v(
        [{"approximation": a, "parameterized": p} for l, a, p in tr], "approximation", "parameterized", _spec())
    cond = S.stratified_cramers_v([(a, p, loc2(l)) for l, a, p in tr])
    shr = (uncond - cond) / uncond if uncond else float("nan")
    return {"uncond_V": round(float(uncond), 3), "cond_2class_V": round(float(cond), 3),
            "shrinkage": round(float(shr), 3), "absorbs": bool(shr == shr and shr >= 0.5)}


def power_3class() -> dict:
    """The terminal 3-class power shortfall: fraction of the 9 locality[3] x approx[3] cells with exp>=5."""
    import numpy as np
    tr = _pooled_triples()
    locs = ["decomposable", "local-covering", "delocalized"]
    aps = ["scheme", "const-or-log", "poly-or-worse"]
    T = np.zeros((3, 3))
    for l, a, p in tr:
        if l in locs:
            T[locs.index(l), aps.index(_approx3(a))] += 1
    N = T.sum()
    exp = np.outer(T.sum(1), T.sum(0)) / N
    ge5 = int((exp >= 5).sum())
    return {"n": int(N), "cells_ge5": ge5, "frac_ge5": round(ge5 / 9, 3),
            "clears_floor": bool(ge5 >= 8 and (exp >= 1).all())}


def supply_channelB() -> dict:
    """Channel B verified net-new both-real supply (dual-pass R20)."""
    return {"n_verified_fills": len(_fills())}
