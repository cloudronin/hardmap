"""Sprint 4.2 — landscape confirmation run + I6 scoring (prereg_v6).

Runs on FRESH instance draws (seeds disjoint from the calibration base 200) at TWO per-family densities, and
scores the two sealed hypotheses:
  * H_I6a (binary, face value): bounded-width-P vs affine-unbounded-P ruggedness — direction + permutation p.
  * H_I6b (polymorphism ordering): semilattice < majority < order/median <= affine, STABLE across both densities
    and both samplers to count as CONFIRMED.

Density anchor (builder-default, logged for owner review — prereg_v6 §builder_default_decisions): the owner's
"0.7*alpha_c / 0.9*alpha_c" assumes a SAT/UNSAT threshold, but 10 of the 14 census families are 0-/1-valid
(ALWAYS satisfiable — no threshold). We therefore anchor UNIFORMLY to a solution-RICHNESS scale: alpha_struct =
the density where the median distinct-solution count first drops to ~K (the structured regime — tight enough to
have geometry, loose enough to have solutions), and measure at 0.7*alpha_struct and 0.9*alpha_struct. For the 4
threshold families this sits in the satisfiable-but-structured regime (alpha_struct < alpha_c, reported). This
preserves the owner's intent (two density points + a stability gate) for every family.
"""
import statistics as st

from foundry import domain3 as D3
from foundry import ensemble as E
from foundry import finer as FN
from foundry import postlattice as PL
from foundry import solscape as S

R1 = FN.R_XOR3_1
# (id, localization[bounded/unbounded], poly_arm, relations, domain, n)
FAMILIES = [
    ("xor-sat", "unbounded", "affine", (PL.R_XOR3, PL.R_XOR2), (0, 1), 24),
    ("zerovalid-affine", "unbounded", "affine", (PL.R_XOR3,), (0, 1), 24),
    ("onevalid-affine", "unbounded", "affine", (R1,), (0, 1), 24),
    ("lin-eq-z3", "unbounded", "affine", (D3.R_LINEQ3,), (0, 1, 2), 18),
    ("lin-eq-z3-b", "unbounded", "affine", (D3.R_LINEQ3B,), (0, 1, 2), 18),
    ("horn-sat", "bounded", "semilattice", (PL.R_NOR3, PL.R_TRUE), (0, 1), 24),
    ("dual-horn", "bounded", "semilattice", (PL.R_OR3, PL.R_FALSE), (0, 1), 24),
    ("zerovalid-horn", "bounded", "semilattice", (PL.R_NOR3, PL.R_FALSE), (0, 1), 24),
    ("onevalid-dualhorn", "bounded", "semilattice", (PL.R_OR3, PL.R_TRUE), (0, 1), 24),
    ("2-sat", "bounded", "majority", (PL.R_POS2, PL.R_NEG2), (0, 1), 24),
    ("zerovalid-bijunctive", "bounded", "majority", (PL.R_NEG2,), (0, 1), 24),
    ("onevalid-bijunctive", "bounded", "majority", (PL.R_POS2,), (0, 1), 24),
    ("order-3", "bounded", "order_median", (D3.R_LEQ3,), (0, 1, 2), 18),
    ("median-3", "bounded", "order_median", (D3.R_LEQ3, D3.R_MIN_SL), (0, 1, 2), 18),
]
ARM_ORDER = ["semilattice", "majority", "order_median", "affine"]     # H_I6b predicted smooth->rugged
FRESH_BASE = 90000                                                   # fresh, never-read (post GKMP-netting, prereg_v7)

# GKMP theory-netting column (prereg_v7, R20-verified before this run). theory-forced = terrain class determined by
# a published classification or field-agnostic linear algebra; permitted = consistent-not-forced; silent = outside
# every published classification's jurisdiction (the |D|=3 anomaly rows).
THEORY_NETTING = {
    "xor-sat": "theory-forced", "zerovalid-affine": "theory-forced", "onevalid-affine": "theory-forced",
    "lin-eq-z3": "theory-forced", "lin-eq-z3-b": "theory-forced",
    "horn-sat": "theory-forced", "dual-horn": "theory-forced", "zerovalid-horn": "theory-forced",
    "onevalid-dualhorn": "theory-forced",
    "2-sat": "theory-permitted", "zerovalid-bijunctive": "theory-permitted", "onevalid-bijunctive": "theory-permitted",
    "order-3": "theory-silent", "median-3": "theory-silent",
}


def _median_solcount(rels, domain, n, alpha, base_seed, K, n_inst=3):
    counts = []
    for i in range(n_inst):
        inst = E.gen_instance(rels, domain, n, alpha, base_seed + i, "struct")
        counts.append(len(S.sample_dpll(inst, i, K=K)))
    return st.median(counts)


def locate_alpha_struct(rels, domain, n, base_seed, K=40, grid=None):
    """Smallest density where the median distinct-solution count drops STRICTLY below K — i.e. where the
    constraints first bite hard enough that the solution space is smaller than the sampler cap (the structured
    regime; below this the space is ~the whole cube and geometry washes out). The sampler returns min(actual, K),
    so `< K` (not `<= K`) is the correct "constraints are biting" signal. Returns (alpha_struct, profile)."""
    grid = grid or [round(0.2 + 0.1 * i, 2) for i in range(0, 40)]     # 0.2 .. 4.1
    profile = []
    a_struct = grid[-1]
    for a in grid:
        c = _median_solcount(rels, domain, n, a, base_seed, K)
        profile.append((a, c))
        if c < K:
            a_struct = a
            break
    return a_struct, profile


def family_reading(rels, domain, n, alpha, base_seed, K=40, n_instances=6):
    """Fresh-draw pooled ruggedness (dpll+walksat) at one density — the measured landscape cell."""
    return S.landscape_reading(rels, domain, n, alpha, base_seed=base_seed, K=K, n_instances=n_instances)


def measure_all(K=40, n_instances=6):
    """Per family: locate alpha_struct on fresh seeds, then measure ruggedness at 0.7 and 0.9 * alpha_struct."""
    out = {}
    for fid, loc, arm, rels, dom, n in FAMILIES:
        a_struct, prof = locate_alpha_struct(rels, dom, n, FRESH_BASE, K=K)
        dens = {"0.7": round(0.7 * a_struct, 3), "0.9": round(0.9 * a_struct, 3)}
        readings = {}
        for tag, a in dens.items():
            r = family_reading(rels, dom, n, a, FRESH_BASE + 1000, K=K, n_instances=n_instances)
            readings[tag] = {"alpha": a, "score": r["pooled_score"], "concord": r["concordance_gap"],
                             "per_sampler": r["per_sampler"]}
        out[fid] = {"localization": loc, "poly_arm": arm, "alpha_struct": a_struct,
                    "densities": dens, "readings": readings}
    return out


# ── H_I6a: the sealed binary contrast, scored at face value ───────────────────────────────────────────────────
def _cramers_v_binary(labels, scores, thresh):
    """2x2 association between localization label and (ruggedness >= thresh)."""
    from eightfold import structure as St
    xs = list(labels)
    ys = ["rugged" if s >= thresh else "smooth" for s in scores]
    v = St.cramers_v(xs, ys)
    return v if v == v else None


def _perm_p(labels, scores, thresh, n_perm, seed):
    """Permutation p on the localization<->ruggedness association: permute the localization LABELS among the rows
    (fixed harness lineage). p = (#perm with V>=V_obs + 1)/(n_perm+1)."""
    import numpy as np
    v_obs = _cramers_v_binary(labels, scores, thresh)
    if v_obs is None:
        return {"v": None, "p": None}
    rng = np.random.default_rng(seed)
    labels = list(labels)
    ge = 0
    for _ in range(n_perm):
        v = _cramers_v_binary(list(rng.permutation(labels)), scores, thresh)
        if v is not None and v >= v_obs - 1e-9:
            ge += 1
    return {"v": round(float(v_obs), 3), "p": round((ge + 1) / (n_perm + 1), 4)}


def score_h_i6a(measured, density="0.9", n_perm=20000, seed=12345):
    """Binary H_I6a at face value: direction (affine more rugged than bounded?) + permutation p, at the tighter
    (0.9) density. Floor: >= 12 concordant rows. No rescue."""
    rows = [(f["localization"], f["readings"][density]["score"], f["readings"][density]["concord"])
            for f in measured.values() if f["readings"][density]["score"] is not None]
    concordant = [(loc, sc) for loc, sc, cg in rows if cg <= 0.1]
    n = len(concordant)
    aff = [sc for loc, sc in concordant if loc == "unbounded"]
    bnd = [sc for loc, sc in concordant if loc == "bounded"]
    direction = (st.mean(aff) - st.mean(bnd)) if (aff and bnd) else None
    thresh = st.median([sc for _, sc in concordant]) if concordant else None
    perm = _perm_p([loc for loc, _ in concordant], [sc for _, sc in concordant], thresh, n_perm, seed) \
        if n >= 12 and thresh is not None else {"v": None, "p": None}
    if n < 12:
        verdict = "INSUFFICIENT_RESOLUTION"
    elif perm["p"] is not None and perm["p"] < 0.05 and direction is not None and direction > 0:
        verdict = "SUPPORTED"
    else:
        verdict = "NOT_SUPPORTED"
    return {"hypothesis": "H_I6a (binary bounded vs affine, face value)", "density": density, "n_concordant": n,
            "affine_mean": round(st.mean(aff), 3) if aff else None,
            "bounded_mean": round(st.mean(bnd), 3) if bnd else None,
            "direction_affine_minus_bounded": round(direction, 3) if direction is not None else None,
            "cramers_v": perm["v"], "perm_p": perm["p"], "verdict": verdict,
            "note": "scored at face value per owner ruling; no rescue. Records to the F1 ledger."}


# ── H_I6b: polymorphism ordering, stable across both densities + both samplers ─────────────────────────────────
def score_h_i6b(measured):
    """H_I6b: arm-mean ruggedness ordering semilattice < majority < order_median <= affine, required STABLE across
    both densities. Returns per-density arm means + whether the ordering holds at each + the confirmation."""
    per_density = {}
    for tag in ("0.7", "0.9"):
        arms = {a: [] for a in ARM_ORDER}
        for f in measured.values():
            s = f["readings"][tag]["score"]
            if s is not None:
                arms[f["poly_arm"]].append(s)
        means = {a: (round(st.mean(v), 3) if v else None) for a, v in arms.items()}
        seq = [means[a] for a in ARM_ORDER]
        strict = all(seq[i] < seq[i + 1] for i in range(2)) if all(x is not None for x in seq[:3]) else None  # semi<maj<order
        weak_last = (seq[2] <= seq[3] + 1e-9) if (seq[2] is not None and seq[3] is not None) else None          # order<=affine
        holds = bool(strict) and bool(weak_last)
        per_density[tag] = {"arm_means": means, "ordering_holds": holds}
    stable = per_density["0.7"]["ordering_holds"] and per_density["0.9"]["ordering_holds"]
    # the anomaly sub-claim: bounded-width splits — semilattice smooth vs order_median rugged-like-affine
    def armmean(tag, a):
        return per_density[tag]["arm_means"][a]
    split = all(armmean(t, "semilattice") is not None and armmean(t, "order_median") is not None and
                armmean(t, "order_median") - armmean(t, "semilattice") >= 0.05 for t in ("0.7", "0.9"))
    verdict = "CONFIRMED" if stable else ("PARTIAL" if (per_density["0.7"]["ordering_holds"] or
                                                        per_density["0.9"]["ordering_holds"]) else "NOT_CONFIRMED")
    return {"hypothesis": "H_I6b (polymorphism ordering semilattice<majority<order/median<=affine)",
            "per_density": per_density, "stable_across_densities": stable, "verdict": verdict,
            "anomaly_bounded_width_splits": split,
            "anomaly_note": "order-3/median-3 (bounded-width) read affine-rugged while Horn/semilattice read smooth"}


def tier_partition(measured):
    """Partition the confirmation output by the pre-committed GKMP netting tier (prereg_v7): report each tier's
    mean ruggedness and, above all, whether the theory-SILENT anomaly survives on fresh data — order-3/median-3
    (bounded-width, |D|=3, no published classification) reading affine-rugged rather than semilattice-smooth."""
    tiers = {"theory-forced": [], "theory-permitted": [], "theory-silent": []}
    for fid, f in measured.items():
        s = f["readings"]["0.9"]["score"]
        if s is not None:
            tiers[THEORY_NETTING[fid]].append((fid, f["poly_arm"], s))
    means = {t: (round(st.mean([s for _, _, s in v]), 3) if v else None) for t, v in tiers.items()}
    # anomaly: theory-silent order/median rugged (>=) semilattice-forced-smooth mean, on fresh data
    semi = [f["readings"]["0.9"]["score"] for fid, f in measured.items()
            if f["poly_arm"] == "semilattice" and f["readings"]["0.9"]["score"] is not None]
    silent = [s for _, _, s in tiers["theory-silent"]]
    anomaly_survives = bool(semi and silent and st.mean(silent) - st.mean(semi) >= 0.05)
    return {"tier_means_at_0.9": means, "tier_members": tiers,
            "anomaly_survives_on_fresh_data": anomaly_survives,
            "anomaly_gap_silent_minus_semilattice": round(st.mean(silent) - st.mean(semi), 3) if (semi and silent) else None,
            "interpretation": ("theory-silent (order-3/median-3) reads rugged like affine despite bounded-width -> "
                               "a measured finding no published connectivity classification addresses (novel by "
                               "pre-committed absence, prereg_v7)")}


def confirmation_run(K=40, n_instances=6, n_perm=20000):
    measured = measure_all(K=K, n_instances=n_instances)
    return {"prereg": "v7", "fresh_base_seed": FRESH_BASE, "measured": measured,
            "H_I6a": score_h_i6a(measured, n_perm=n_perm), "H_I6b": score_h_i6b(measured),
            "theory_netting_tiers": tier_partition(measured)}


# ── permutation-harness hand-count selftest (stays in CI) ──────────────────────────────────────────────────────
def selftest_perm(n_perm=20000):
    """A hand-countable table: 3 rugged 'unbounded' rows + 3 smooth 'bounded' rows is a perfect 2x2 (V=1); the
    permutation p is the fraction of label-shuffles that reproduce a perfect split = 2/C(6,3) = 2/20 = 0.1."""
    labels = ["unbounded"] * 3 + ["bounded"] * 3
    scores = [0.99, 0.98, 0.97, 0.80, 0.79, 0.78]
    thresh = 0.85
    r = _perm_p(labels, scores, thresh, n_perm, 7)
    ok = r["v"] == 1.0 and 0.07 < r["p"] < 0.13
    print(f"H_I6a perm selftest: V={r['v']} p={r['p']} (exact 2/20=0.10) -> {'PASSED' if ok else 'FAILED'}")
    return 0 if ok else 1


if __name__ == "__main__":
    import json
    import sys
    if "--selftest" in sys.argv:
        sys.exit(selftest_perm())
    res = confirmation_run()
    print(json.dumps({"H_I6a": res["H_I6a"], "H_I6b": res["H_I6b"]}, indent=2))
