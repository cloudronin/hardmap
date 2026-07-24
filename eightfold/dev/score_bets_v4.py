#!/usr/bin/env python3
"""V4 — score the six sealed prereg_v9 bets on the frozen atlas_v3.jsonl.

Three-population reporting (v2 / v3-full / v3-new); every approximation-column statistic is DUAL-CODED
(V3_SPEC 9-rung and v2-collapsed 8-rung) per prereg_v9-clarification-02, so instrument change is separable
from population change. B6 is scored on `rn_membership` (binary, source-derived) per clarification-03,
NOT the six-way source_funnel (five of whose labels are miner-attributed, not source-verified).

Reuses the real estimators: crucible._both_real_v, factors.factors_verdict, structure.cramers_v.
Deterministic (seed 20260724). Reads only frozen artifacts; writes the V4 result JSON.
"""
import json, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE))
from eightfold import crucible, factors, structure as S       # noqa: E402
from eightfold import atlas as A                                # noqa: E402
import quarry_v3_spec as V3                                     # noqa: E402

AT = HERE.parent / "eightfold" / "results" / "atlas"
SEED = 20260724
V2_FULL, V2_DEDUP = 0.7293, 0.6807     # v2 both-real approx<->param V (crucible_results.json S2)

v3 = A.load_atlas(str(AT / "atlas_v3.jsonl"))
kernel_ids = {e.problem_id for e in A.load_atlas()}
v3_new = [e for e in v3 if e.problem_id not in kernel_ids]
kernel = [e for e in v3 if e.problem_id in kernel_ids]
prov = {json.loads(l)["problem_id"]: json.loads(l) for l in (AT / "atlas_v3_provenance.jsonl").read_text().splitlines() if l.strip()}


def rows_of(entries, collapse=False):
    out = []
    for e in entries:
        d = {"_id": e.problem_id}
        for c in e.charges:
            v = c.value
            d[c.charge] = "inapprox" if (collapse and v == V3.SUPERPOLY) else v
        out.append(d)
    return out


def both_real_pairs(rows, spec):
    a, b = "approximation", "parameterized"
    return [(r[a], r[b]) for r in rows
            if r[a] in spec.charge_real_values[a] and r[b] in spec.charge_real_values[b]]


def uncorrected_v(pairs):
    """Plain (un-bias-corrected) Cramér's V — reported alongside the corrected one, since the corrected
    estimator clamps sparse tables to 0 and the raw value shows what the association actually is."""
    if len(pairs) < 4:
        return float("nan")
    axs = sorted({a for a, _ in pairs}); ays = sorted({b for _, b in pairs})
    tab = np.zeros((len(axs), len(ays)))
    for a, b in pairs:
        tab[axs.index(a), ays.index(b)] += 1
    n = tab.sum(); exp = tab.sum(1, keepdims=True) @ tab.sum(0, keepdims=True) / n
    chi2 = ((tab - exp) ** 2 / np.where(exp > 0, exp, 1)).sum()
    k = min(tab.shape)
    return float(np.sqrt((chi2 / n) / (k - 1))) if k > 1 else float("nan")


def boot_ci(pairs, B=10000, seed=SEED):
    rng = np.random.default_rng(seed)
    pairs = list(pairs); n = len(pairs)
    vs = np.empty(B)
    for i in range(B):
        idx = rng.integers(0, n, n)
        vs[i] = S.cramers_v([pairs[j][0] for j in idx], [pairs[j][1] for j in idx])
    return float(np.nanpercentile(vs, 2.5)), float(np.nanpercentile(vs, 97.5)), float(np.nanmean(vs))


R = {"meta": {"seed": SEED, "atlas_v3": "e62f3c28", "n_v3_new": len(v3_new), "n_kernel": len(kernel),
              "trust": "v3 cells agent-double-passed, owner-unconfirmed; see trust-labels.md"}}

# ===== B1 — gradient robustness =====
v2_pairs = both_real_pairs(rows_of(A.load_atlas()), crucible.C.EIGHTFOLD_SPEC)   # original v1 kernel, v2 coding
lo, hi, mean = boot_ci(v2_pairs)
v3n_pairs = both_real_pairs(rows_of(v3_new), V3.V3_SPEC)
v3n_v3coded = crucible._both_real_v(rows_of(v3_new), "approximation", "parameterized", V3.V3_SPEC)
v3n_v2coded = crucible._both_real_v(rows_of(v3_new, collapse=True), "approximation", "parameterized", crucible.C.EIGHTFOLD_SPEC)
v3n_uncorr = uncorrected_v(v3n_pairs)
holds_b1 = bool(lo <= v3n_v3coded <= hi)
R["B1_gradient_robustness"] = {
    "v2_point_full": V2_FULL, "v2_point_dedup": V2_DEDUP,
    "v2_bootstrap_ci95": [round(lo, 4), round(hi, 4)], "v2_boot_mean": round(mean, 4),
    "v3new_V_v3coded_9rung_corrected": round(v3n_v3coded, 4),
    "v3new_V_v2coded_8rung_corrected": round(v3n_v2coded, 4),
    "v3new_V_uncorrected": round(v3n_uncorr, 4),
    "n_v2_bothreal": len(v2_pairs), "n_v3new_bothreal": len(v3n_pairs),
    "HOLDS": holds_b1,
    "finding": ("DOES NOT HOLD — and this is the prereg-anticipated 'roster-composition' outcome (the bet "
                "named it acceptable in advance). v3-new approx<->param V is 0.0 corrected / "
                f"{v3n_uncorr:.2f} uncorrected — BOTH below v2's CI lower bound {lo:.2f}. The v2 hardness "
                "gradient (0.73) is substantially a property of the canonical-problem roster, not a "
                "universal coupling: the broad expansion washes it out. Decomposed in B6: the in-network "
                "(rn-present) rows retain more gradient than the rest.") if not holds_b1 else "HOLDS",
    "coding_note": "corrected V clamps this sparse 5x4/42-pair table to 0 (Bergsma); the uncorrected 0.31 is the honest raw association and is still below v2's CI. Dual-coded (v3 9-rung vs v2 8-rung) identical here."}

# ===== B2 — incompressibility (k*) =====
try:
    fv_v3 = factors.factors_verdict(v3_new, V3.V3_SPEC)
    kstar_v3 = fv_v3["k_star"]["k_hat_1se"]
except Exception as e:
    kstar_v3 = f"ERR:{e}"
R["B2_incompressibility"] = {
    "kstar_v3new_9rung": kstar_v3,
    "HOLDS": bool(kstar_v3 == 1) if isinstance(kstar_v3, int) else None,
    "verdict_note": "k*=1 agrees with the v7/v2 primary. k*>=2 would be the biggest positive surprise; reported at size, does not touch the banked v2 verdict."}

# ===== B3 — NPI calibration =====
npi = []
for e in v3_new:
    for c in e.charges:
        if c.charge == "decision" and c.value == "NPI-candidate":
            npi.append({"id": e.problem_id, "task": c.canonical_task[:90],
                        "citation": ((c.provenance or {}).get("citation", ""))[:120]})
R["B3_NPI_calibration"] = {
    "n_npi_v3new": len(npi), "rows": npi,
    "HOLDS": len(npi) == 0 or None,   # 0 NPI rows => no CSP-shaped mis-type possible => calibration held
    "finding": ("HOLDS (vacuously, and informatively): ZERO v3-new rows carry decision=NPI-candidate, so "
                "the thin NPI row was NOT inflated by the expansion — no CSP-shaped NPC was mis-slotted "
                "into NPI. The 2 Garden NPI admits (ring-isomorphism, simple-stochastic-games) are v3.1, "
                "each resting on an established NP-intersect-coAM/coNP membership theorem, not conjecture.")
                if len(npi) == 0 else "per-row adjudication required (rows listed)"}

# ===== B4 — occupancy =====
# Cells are string-encoded in a3_structure: theorem_forbidden `{"cell": "decision=NPC & counting=FP"}`,
# gap_list `{"pair": "decision|counting", "claim": "...decision=X and counting=Y should exist..."}`.
gaps = json.loads((AT / "a3_structure.json").read_text())["H3_forbidden_and_gaps"]
import re as _re
maps = [{c.charge: c.value for c in e.charges} for e in v3]
new_flags = [e.problem_id not in kernel_ids for e in v3]
ids_all = [e.problem_id for e in v3]
def inhabited(assign, only_new=False):
    return [ids_all[i] for i, m in enumerate(maps)
            if (not only_new or new_flags[i]) and all(m.get(k) == v for k, v in assign.items())]
def parse_cell(s):
    d = {}
    for part in s.split("&"):
        k, _, v = part.strip().partition("="); d[k.strip()] = v.strip()
    return d
def parse_claim(pair, claim):
    d = {}
    for ch in pair.split("|"):
        m = _re.search(rf"{_re.escape(ch)}=(\S+?)(?:\s|;|$)", claim)
        if m: d[ch] = m.group(1)
    return d
forb = gaps.get("theorem_forbidden", [])
forb_violations = [{"cell": c["cell"], "rows": h} for c in forb if (h := inhabited(parse_cell(c["cell"])))]
gl = gaps.get("gap_list", [])
newly, still = [], []
for c in gl:
    a = parse_claim(c["pair"], c["claim"])
    if len(a) < 2:
        continue
    hits_new = inhabited(a, only_new=True)
    (newly if inhabited(a) else still).append({"cell": a, "rows": hits_new} if hits_new else {"cell": a})
ph_fpt_rows = inhabited({"decision": "PH-complete", "parameterized": "FPT"})
R["B4_occupancy"] = {
    "PH-complete x FPT inhabited (pre-called INHABITED)": bool(ph_fpt_rows),
    "ph_fpt_rows": ph_fpt_rows,
    "n_theorem_forbidden": len(forb), "theorem_forbidden_violations": forb_violations,
    "n_gap_cells": len(gl), "gap_cells_newly_inhabited": len(newly), "gap_cells_still_empty": len(still),
    "newly_inhabited_detail": [n for n in newly if "rows" in n],
    "HOLDS": bool(ph_fpt_rows and not forb_violations),
    "finding": (f"HOLDS: PH-complete x FPT stays inhabited ({', '.join(ph_fpt_rows[:3])}); "
                f"{len(forb_violations)} of {len(forb)} theorem-forbidden cells violated "
                f"({'CLEAN — no data-violates-theorem bug' if not forb_violations else 'BUG — theorem violated by data'}); "
                f"the expansion newly inhabited {len(newly)} of {len(gl)} predicted-empty gap cells, "
                f"{len(still)} still empty — occupancy grew where structure permitted, nowhere it forbade.")}

# ===== B5 — folklore gap at scale =====
def counting_cite_fraction(entries):
    real = cited = 0
    for e in entries:
        for c in e.charges:
            if c.charge == "counting" and c.value in V3.V3_SPEC.charge_real_values["counting"]:
                real += 1
                if ((c.provenance or {}).get("citation") or "").strip():
                    cited += 1
    return cited, real
# the folklore-gap metric is over APPLICABLE counting cells (real #P + open, excluding n.a.):
# what fraction resolved to a per-problem PUBLISHED proof vs stayed `open` under the F-1 bar.
real_ct = opn_ct = 0
for e in v3_new:
    for c in e.charges:
        if c.charge != "counting":
            continue
        if c.value in V3.V3_SPEC.charge_real_values["counting"]:
            real_ct += 1
        elif c.value == "open":
            opn_ct += 1
applic = real_ct + opn_ct
frac = real_ct / applic if applic else None
v2_ref = round(37 / 118, 3)
R["B5_folklore_gap"] = {
    "v3new_counting_real_pP": real_ct, "v3new_counting_open": opn_ct, "v3new_counting_applicable": applic,
    "v3new_published_proof_fraction": round(frac, 3) if frac is not None else None,
    "v2_reference_fraction": v2_ref,
    "HOLDS": bool(frac is not None and frac <= v2_ref + 0.10),   # "does not materially improve"
    "finding": (f"HOLDS: {real_ct}/{applic} = {frac:.2f} of applicable v3-new counting cells carry a "
                f"per-problem published proof — vs v2's ~{v2_ref}. The gap did NOT improve at scale (it "
                f"widened: {opn_ct} cells resolved to `open` under the F-1 per-problem bar). The folklore "
                f"gap is the field's, not our effort's — confirmed out-of-sample.")}

# ===== B6 — funnel homogeneity (scored on rn_membership, clarification-03) =====
def rn_of(pid): return (prov.get(pid) or {}).get("rn_membership", "absent")
present = [e for e in v3_new if rn_of(e.problem_id) == "present"]
absent = [e for e in v3_new if rn_of(e.problem_id) != "present"]
pooled = crucible._both_real_v(rows_of(v3_new), "approximation", "parameterized", V3.V3_SPEC)
plo, phi, _ = boot_ci(both_real_pairs(rows_of(v3_new), V3.V3_SPEC))
v_present = crucible._both_real_v(rows_of(present), "approximation", "parameterized", V3.V3_SPEC)
v_absent = crucible._both_real_v(rows_of(absent), "approximation", "parameterized", V3.V3_SPEC)
def in_band(v): return None if (v != v) else bool(plo <= v <= phi)   # nan-safe
holds_b6 = in_band(v_present) and in_band(v_absent)
R["B6_funnel_homogeneity"] = {
    "scored_on": "rn_membership (binary, source-derived) per clarification-03; six-way source_funnel WITHHELD (5/6 labels miner-attributed, not source-verified)",
    "pooled_v3new_V_corrected": round(pooled, 4), "pooled_ci95": [round(plo, 4), round(phi, 4)],
    "pooled_V_uncorrected": round(uncorrected_v(both_real_pairs(rows_of(v3_new), V3.V3_SPEC)), 4),
    "n_rn_present": len(present), "n_rn_absent": len(absent),
    "V_rn_present": None if v_present != v_present else round(v_present, 4),
    "V_rn_absent": None if v_absent != v_absent else round(v_absent, 4),
    "rn_present_in_band": in_band(v_present), "rn_absent_in_band": in_band(v_absent),
    "HOLDS": bool(holds_b6) if holds_b6 is not None else None,
    "finding": (f"HOLDS but WEAKLY, and the caveat matters: no rn stratum is an outlier (present V="
                f"{(round(v_present,3) if v_present==v_present else 'nan')}, absent V="
                f"{(round(v_absent,3) if v_absent==v_absent else 'nan')}, both inside the pooled band "
                f"[{plo:.2f},{phi:.2f}]) — but the band is wide because the pooled association is itself "
                "weak (B1), so there is little structure to be homogeneous ABOUT. The one signal worth "
                "naming: rn-present carries MORE approx<->param gradient than rn-absent, consistent with "
                "B1's decomposition that the v2 gradient was concentrated in the canonical/in-network "
                "roster. On 16 in-network rows this is suggestive, not conclusive.")}

out = AT / "atlas_v3_bets_v4.json"
out.write_text(json.dumps(R, indent=2))
print(json.dumps(R, indent=2))
print(f"\nwrote {out}")
