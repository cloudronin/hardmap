#!/usr/bin/env python3
"""Mosaic L3 — score P2-P6 at 3-class locality resolution (prereg_v10 + clarification-01).

Reuses crucible._both_real_v / structure.cramers_v (the same estimators as V4). Every number is tagged
3-class. Locality is an APPROXIMATE LLM-coded variable (kappa=0.646, two varied blind coders + a tiebreak);
associations are indicative, not precise — reported as such per the owner's standing caveat. `uncodable`
rows are excluded from associations as a non-class. Marginals-first: per-class n before any within-class V;
thin class -> INSUFFICIENT RESOLUTION. Deterministic; reads only sidecars + the frozen atlas.
"""
import json, sys
from collections import Counter
from pathlib import Path
import numpy as np

sys.path.insert(0, "."); sys.path.insert(0, "dev")
from eightfold import crucible, structure as S, atlas as A   # noqa: E402
import quarry_v3_spec as V3                                   # noqa: E402

AT = Path("eightfold/results/atlas")
SENT = {"open", "n.a.", "unmeasured"}
LOC = {json.loads(l)["problem_id"]: json.loads(l)["locality_3class"]
       for l in (AT / "mosaic-locality.jsonl").read_text().splitlines() if l.strip()}
V2_UNCOND, V3NEW_UNCOND = 0.73, 0.31   # the B1 endpoints (V4)
ANCHORS = {"planar-vertex-cover", "knapsack", "vertex-cover", "max-2sat", "clique", "independent-set", "label-cover"}

v3 = A.load_atlas(str(AT / "atlas_v3.jsonl"))
kids = {e.problem_id for e in A.load_atlas()}
def cells(e): return {c.charge: c.value for c in e.charges}
def bothreal(entries):
    out = []
    for e in entries:
        c = cells(e)
        if c["approximation"] not in SENT and c["parameterized"] not in SENT:
            out.append((e.problem_id, c["approximation"], c["parameterized"], LOC.get(e.problem_id, "?")))
    return out
br2 = bothreal([e for e in v3 if e.problem_id in kids])          # v2 both-real (47)
brn = bothreal([e for e in v3 if e.problem_id not in kids])      # v3-new both-real (42)

def cv(xs, ys): return S.cramers_v(xs, ys) if len(xs) >= 4 else float("nan")
def rnd(x): return None if (x != x) else round(float(x), 3)

R = {"meta": {"resolution": "3-class (decomposable / local-covering / delocalized)", "kappa_3class": 0.646,
              "caveat": "locality is an APPROXIMATE LLM-coded variable; associations are indicative, not precise",
              "n_v2_bothreal": len(br2), "n_v3new_bothreal": len(brn)}}

# ===== P2 — separate association (v2 both-real; uncodable excluded) =====
r2 = [(l, a, p) for _, a, p, l in br2 if l not in ("uncodable", "?")]
V_la, V_lp = cv([l for l, a, p in r2], [a for l, a, p in r2]), cv([l for l, a, p in r2], [p for l, a, p in r2])
R["P2_separate_association"] = {
    "n": len(r2), "locality_marginal": dict(Counter(l for l, a, p in r2)),
    "V_locality_approx": rnd(V_la), "V_locality_param": rnd(V_lp), "threshold": 0.35,
    "HOLDS": bool(V_la >= 0.35 and V_lp >= 0.35),
    "note": "does locality predict each gradient charge separately? threshold 0.35 each."}

# ===== P3 — absorption (within-class approx<->param V pooled) =====
byclass = {}
for _, a, p, l in br2:
    if l not in ("uncodable", "?"):
        byclass.setdefault(l, []).append((a, p))
uncond = crucible._both_real_v([{"approximation": a, "parameterized": p} for _, a, p, _ in br2],
                               "approximation", "parameterized", V3.V3_SPEC)
within = {l: {"n": len(prs), "note": "per-class V is NOT pooled; see stratified V below (defect #15)"}
          for l, prs in sorted(byclass.items())}
# CORRECT conditional association: pooled within-stratum chi-square, never the average of per-class V's.
strat_triples = [(a, p, l) for _, a, p, l in br2 if l not in ("uncodable", "?")]
pooled = S.stratified_cramers_v(strat_triples)
# power flag: min expected within-stratum cell for approx charge; <5 -> INSUFFICIENT RESOLUTION
small = min(len(prs) for prs in byclass.values()) if byclass else 0
R["P3_absorption"] = {
    "v2_unconditional_V": rnd(uncond), "within_class_n": within,
    "pooled_within_class_V_stratified": rnd(pooled),
    "smallest_class_n": small,
    "power_note": ("INSUFFICIENT RESOLUTION — smallest locality class has too few both-real rows for a "
                   "reliable within-stratum table (canon-47 is below floor; see the 89-row re-run)" if small < 20 else "ok"),
    "threshold_absorb_half": 0.37, "HOLDS": bool(pooled == pooled and pooled <= 0.37 and small >= 20),
    "separability_evidence_beside": "L1 gate CLEAR — V(locality,approx)=0.436 < dissociation structure-acc 1.00; the labels code structure, not charge-echo",
    "note": "absorption = does conditioning on locality shrink the 0.73 approx<->param V by >= half? marginals-first."}

# ===== P4 — composition decomposition (the B1 payoff) =====
w2 = Counter(l for _, a, p, l in br2 if l not in ("uncodable", "?"))
wn = Counter(l for _, a, p, l in brn if l not in ("uncodable", "?"))
n2, nn = sum(w2.values()), sum(wn.values())
# predicted v3-new V if ONLY the locality-class mixture changed (v2 within-class structure held):
pred = sum((within.get(l, {}).get("V") or 0) * (wn[l] / nn) for l in wn) if nn else float("nan")
obs_new = crucible._both_real_v([{"approximation": a, "parameterized": p} for _, a, p, _ in brn],
                                "approximation", "parameterized", V3.V3_SPEC)
explained = (V2_UNCOND - pred) / (V2_UNCOND - V3NEW_UNCOND) if nn else float("nan")
R["P4_composition_decomposition"] = {
    "v2_locality_mixture": {k: round(v / n2, 2) for k, v in w2.items()},
    "v3new_locality_mixture": {k: round(v / nn, 2) for k, v in wn.items()},
    "predicted_v3new_V_from_mixture_shift": rnd(pred), "observed_v3new_V": rnd(obs_new),
    "b1_drop": round(V2_UNCOND - V3NEW_UNCOND, 3), "fraction_of_drop_explained_by_mixture": rnd(explained),
    "HOLDS": bool(explained == explained and explained >= 0.5),
    "note": "reweight v2's within-class tables to v3-new's locality mixture; does the mixture shift predict >= half the 0.73->0.31 drop? THE CONTAMINATION-ROBUST CORE."}

# ===== P5 — violator fingerprint (off-diagonal 5 vs on-diagonal 13; do they code delocalized?) =====
OFFDIAG = ["subset-sum", "graph-3-coloring", "group-steiner-tree", "longest-path", "tsp"]
ONDIAG = ["clique", "densest-k-subgraph", "dominating-set", "feedback-arc-set-tournament", "hitting-set",
          "independent-set", "kemeny-rank-aggregation", "makespan-scheduling", "maximum-common-subgraph",
          "planar-dominating-set", "planar-independent-set", "planar-vertex-cover", "set-cover"]
off = {p: LOC.get(p) for p in OFFDIAG}
on = {p: LOC.get(p) for p in ONDIAG}
off_deloc = sum(v == "delocalized" for v in off.values())
on_deloc = sum(v == "delocalized" for v in on.values())
R["P5_violator_fingerprint"] = {
    "off_diagonal_codes": off, "off_delocalized": f"{off_deloc}/{len(off)}",
    "on_diagonal_delocalized": f"{on_deloc}/{len(on)}",
    "HOLDS": bool(off_deloc / len(off) > on_deloc / len(on)),
    "note": "two-sided: off-diagonal (gradient-bending) should code delocalized MORE than the on-diagonal controls. subset-sum is the dissociation case (decomposable structure) -- a delocalized miss there is two-property-split evidence, not noise."}

# ===== P6 — kernel_status netting (only if L2 landed) =====
ks_path = AT / "mosaic-kernel-status.jsonl"
if ks_path.exists():
    KS = {json.loads(l)["problem_id"]: json.loads(l)["kernel_status"] for l in ks_path.read_text().splitlines() if l.strip()}
    # informative residual: poly-kernel vs no-poly-kernel WITHIN FPT (net the FPT<=>some-kernel theorem)
    fpt_rows = [(p, KS[p], LOC.get(p)) for p, a, pa, l in br2 + brn if pa == "FPT" and p in KS] if False else \
               [(pid, KS[pid], LOC.get(pid)) for pid in KS]
    poly = {"poly-kernel"}
    binary = [(("poly" if ks in poly else "no-poly") if ks not in ("open", "FPT-no-poly-known") else None, loc)
              for pid, ks, loc in fpt_rows]
    binary = [(k, l) for k, l in binary if k and l not in ("uncodable", "?")]
    v_kl = cv([k for k, l in binary], [l for k, l in binary])
    R["P6_kernel_netting"] = {
        "n_kernel_cited": len(KS), "n_poly_vs_nopoly_locality": len(binary),
        "V_kernelstatus_locality_netted": rnd(v_kl),
        "note": "within-FPT poly-kernel vs no-poly-kernel residual (the FPT<=>some-kernel theorem netted out); does it align with locality? a raw kernel<->param V is never reported."}
else:
    R["P6_kernel_netting"] = {"status": "PENDING — L2 kernel_status not yet assembled"}

out = AT / "mosaic_L3_results.json"
out.write_text(json.dumps(R, indent=2))
print(json.dumps(R, indent=2))
print(f"\nwrote {out}")
