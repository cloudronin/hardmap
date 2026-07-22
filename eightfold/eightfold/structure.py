"""Structure-detection harness (C-phase) — association, effective dimensionality, clustering, occupancy.

Retargets the analysis to the charge atlas. numpy + scipy only; MCA is implemented in-house (SVD of the
indicator matrix) to avoid a `prince` dependency. Spec §3.5; Build addenda R3/R4/R9; prereg
`results/prereg/prereg_v2.json`.

**This module runs a PREVIEW on the pilot as a harness sanity-check — NOT the H1–H3 verdict.** The verdict is
A3 on the full ~120-problem atlas; N=22 is far too small for MCA/clustering to be conclusive. Per R7 the
pipeline is debugged on a synthetic toy table (`--selftest`), never tuned on the pilot; the prereg was locked
before this ever ran on real data.

    python -m eightfold.structure --selftest        # R7: exercise the pipeline on synthetic data
    python -m eightfold.structure --pilot           # preview on the atlas -> results/atlas/pilot_structure.json
    python -m eightfold.structure --pilot --drop-measured   # R9 ablation
"""
from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

import numpy as np

from eightfold import charges as C

# Charges used in the R4 complete-case sub-block (the best-populated four; real-valued for the kept problems).
COMPLETE_CASE_CHARGES = ["decision", "counting", "approximation", "parameterized"]
KAISER_Q = len(C.CHARGES)          # MCA mean-eigenvalue threshold = 1/Q over Q variables (prereg H1 rule)
# R11 (pilot-informed, prereg_v3): the locked charge-triples for subspace clustering (mirrors the prereg
# occupancy triples). Plain 8-charge Hamming washes out single-charge decouplings; subspace clustering
# surfaces them in the charge-triple that carries them.
LOCKED_TRIPLES = [
    ["decision", "counting", "parallelization"],
    ["decision", "approximation", "parameterized"],
    ["decision", "average_case", "landscape"],
]


# ── data extraction ───────────────────────────────────────────────────────────────────────────────────────
def _grid(entries, drop_measured=False, drop_derived=False):
    """Return (ids, families, rows) where rows[i] maps charge -> value string (sentinels included).

    drop_measured (R9): recode any `measured`/`measured-scaling` cell to a dropped sentinel so the ablation
    removes self-generated values from the analysis.
    drop_derived (Crucible S4): revert any `derived` (dichotomy-backfilled) cell to `open` — its faithful
    pre-backfill state — so the ablation shows H1's complete-case anchor WITHOUT the S4 fills (back to n=19).
    """
    ids, families, rows = [], [], []
    for e in entries:
        ids.append(e.problem_id)
        families.append(e.problem_family)
        row = {}
        for cell in e.charges:
            v = cell.value
            if drop_measured and cell.status in (C.STATUS_MEASURED, C.STATUS_MEASURED_SCALING):
                v = "n.a."   # ablate: treat the measured value as absent
            if drop_derived and cell.status == C.STATUS_DERIVED:
                v = "open"   # ablate: revert the dichotomy fill to its pre-backfill sentinel
            row[cell.charge] = v
        rows.append(row)
    return ids, families, rows


# ── Cramér's V (bias-corrected) ──────────────────────────────────────────────────────────────────────────
def cramers_v(labels_a, labels_b):
    from scipy.stats import chi2_contingency
    cats_a = sorted(set(labels_a))
    cats_b = sorted(set(labels_b))
    if len(cats_a) < 2 or len(cats_b) < 2:
        return float("nan")
    ia = {c: i for i, c in enumerate(cats_a)}
    ib = {c: i for i, c in enumerate(cats_b)}
    table = np.zeros((len(cats_a), len(cats_b)))
    for a, b in zip(labels_a, labels_b):
        table[ia[a], ib[b]] += 1
    chi2 = chi2_contingency(table, correction=False)[0]
    n = table.sum()
    if n == 0:
        return float("nan")
    phi2 = chi2 / n
    r, k = table.shape
    phi2corr = max(0.0, phi2 - (k - 1) * (r - 1) / (n - 1))
    rcorr = r - (r - 1) ** 2 / (n - 1)
    kcorr = k - (k - 1) ** 2 / (n - 1)
    denom = min(kcorr - 1, rcorr - 1)
    return float(np.sqrt(phi2corr / denom)) if denom > 0 else float("nan")


def cramers_v_matrix(rows, charges):
    cols = {ch: [r[ch] for r in rows] for ch in charges}
    mat = {}
    for a in charges:
        for b in charges:
            if a < b:
                mat[f"{a}|{b}"] = cramers_v(cols[a], cols[b])
    # entailment-linked pairs (E1: decision~counting; E2: decision~parallelization) flagged for the
    # surprising-vs-entailed split (prereg claim_standard). Keys match the matrix convention: sorted pair.
    def _key(a, b):
        return "|".join(sorted([a, b]))
    return mat, [_key("decision", "counting"), _key("decision", "parallelization")]


# ── in-house MCA (SVD of the centered, standardized indicator matrix) ────────────────────────────────────
def _indicator(rows, charges):
    """One-hot indicator matrix Z (n_problems x total_categories) and the column labels."""
    cats = []
    for ch in charges:
        for v in sorted({r[ch] for r in rows}):
            cats.append((ch, v))
    idx = {cv: j for j, cv in enumerate(cats)}
    Z = np.zeros((len(rows), len(cats)))
    for i, r in enumerate(rows):
        for ch in charges:
            Z[i, idx[(ch, r[ch])]] = 1.0
    return Z, cats


def mca(rows, charges):
    """Multiple correspondence analysis via SVD of the standardized residual matrix.

    Returns principal inertias (eigenvalues), how many exceed the 1/Q mean-eigenvalue threshold (prereg H1
    Kaiser-style rule), and total inertia. Trivial dimension removed by centering (P - r c^T).
    """
    Z, cats = _indicator(rows, charges)
    n = Z.shape[0]
    total = Z.sum()
    if total == 0 or n < 3:
        return {"eigenvalues": [], "dims_above_threshold": 0, "threshold": 1.0 / KAISER_Q,
                "total_inertia": 0.0, "n_problems": n, "n_categories": len(cats)}
    P = Z / total
    r = P.sum(axis=1)
    c = P.sum(axis=0)
    # standardized residuals S = Dr^{-1/2} (P - r c^T) Dc^{-1/2}
    Dr_inv = np.diag(1.0 / np.sqrt(np.where(r > 0, r, 1.0)))
    Dc_inv = np.diag(1.0 / np.sqrt(np.where(c > 0, c, 1.0)))
    S = Dr_inv @ (P - np.outer(r, c)) @ Dc_inv
    sv = np.linalg.svd(S, compute_uv=False)
    eig = (sv ** 2)
    eig = eig[eig > 1e-12]
    thr = 1.0 / KAISER_Q
    return {
        "eigenvalues": [float(x) for x in eig[:10]],
        "dims_above_threshold": int((eig > thr).sum()),
        "threshold": thr,
        "total_inertia": float(eig.sum()),
        "n_problems": n,
        "n_categories": len(cats),
    }


def complete_case(rows, charges=COMPLETE_CASE_CHARGES):
    """R4 complete-case sub-block: keep problems real-valued (non-sentinel) on all `charges`."""
    kept = [r for r in rows if all(r[ch] not in C.SENTINELS for ch in charges)]
    return kept, list(charges)


# ── clustering over charge vectors (Hamming distance) + family cohesion ──────────────────────────────────
def _hamming(rows, charges):
    n = len(rows)
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            d = sum(1 for ch in charges if rows[i][ch] != rows[j][ch]) / len(charges)
            D[i, j] = D[j, i] = d
    return D


def cluster(ids, families, rows, charges, k=6):
    from scipy.cluster.hierarchy import fcluster, linkage
    from scipy.spatial.distance import squareform
    D = _hamming(rows, charges)
    Z = linkage(squareform(D, checks=False), method="average")
    labels = fcluster(Z, t=k, criterion="maxclust")
    assign = {ids[i]: int(labels[i]) for i in range(len(ids))}
    # family cohesion (province_separation analog): mean intra-family similarity vs inter-family.
    sim = 1.0 - D
    intra, inter = [], []
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            (intra if families[i] == families[j] else inter).append(sim[i, j])
    cohesion = {
        "intra_family_mean_similarity": float(np.mean(intra)) if intra else float("nan"),
        "inter_family_mean_similarity": float(np.mean(inter)) if inter else float("nan"),
        "separation": (float(np.mean(intra)) - float(np.mean(inter))) if intra and inter else float("nan"),
    }
    # H2 witness checks (does the structure recover the predicted multiplets?)
    def same(a, b):
        return assign.get(a) == assign.get(b) if a in assign and b in assign else None
    witnesses = {
        "clique==independent-set (expect same cluster)": same("clique", "independent-set"),
        "vertex-cover vs clique (both NPC; decouple on approx/param)": same("vertex-cover", "clique"),
        "permanent vs determinant (counting FP vs #P-c)": same("permanent", "determinant"),
        "2-sat vs xor-sat (counting #P-c vs FP)": same("sat-2", "xor-sat"),
    }
    return {"k": k, "assignments": assign, "family_cohesion": cohesion, "witness_checks": witnesses}


def _pair_dist(ids, rows, a, b, charges):
    if a not in ids or b not in ids:
        return None
    ia, ib = ids.index(a), ids.index(b)
    return sum(1 for ch in charges if rows[ia][ch] != rows[ib][ch]) / len(charges)


def cluster_subspaces(ids, families, rows):
    """R11 (pilot-informed): single-charge decouplings live in specific charge-subspaces. For each witness
    pair, report its Hamming distance within the locked triple that should carry its decoupling vs its
    distance over all 8 charges — the subspace should AMPLIFY the decoupling that full-vector clustering
    washes out (permanent/determinant differ on 2 of 8 charges = 0.25, but 2 of 3 = 0.67 in the
    decision+counting+parallelization triple)."""
    pairs = {
        "permanent|determinant": ("permanent", "determinant", ["decision", "counting", "parallelization"]),
        "vertex-cover|clique": ("vertex-cover", "clique", ["decision", "approximation", "parameterized"]),
        "sat-2|xor-sat": ("sat-2", "xor-sat", ["decision", "counting", "parallelization"]),
    }
    out = {}
    for name, (a, b, triple) in pairs.items():
        full = _pair_dist(ids, rows, a, b, C.CHARGES)
        sub = _pair_dist(ids, rows, a, b, triple)
        if full is None or sub is None:
            continue
        out[name] = {"subspace": "+".join(triple), "dist_full8": round(full, 3),
                     "dist_subspace": round(sub, 3), "amplified": sub > full}
    return out


# ── occupancy over marginals + entailment triage + gap list (R3/R5) ──────────────────────────────────────
def occupancy(rows):
    charges = C.CHARGES
    # 1) verify the theorem-forbidden cells (E1/E2) are actually empty in the data.
    forbidden_checks = []
    for a, b in itertools.combinations(charges, 2):
        seen = {(r[a], r[b]) for r in rows}
        for va, vb in seen:
            hits = C.theorem_forbidden_by({a: va, b: vb})
            if hits:
                forbidden_checks.append({"pair": f"{a}={va} & {b}={vb}", "rules": hits,
                                         "status": "OCCUPIED — data violates a theorem (bug!)"})
    # A dedicated scan for the forbidden combos over the value vocab (should be empty in the data):
    forbidden_empty_ok = True
    e1_e2_report = []
    checks = [
        ("counting=FP & decision=NPC", {"counting": "FP", "decision": "NPC"}),
        ("counting=FP & decision=harder", {"counting": "FP", "decision": "harder"}),
        ("decision=NPC & parallelization=NC", {"decision": "NPC", "parallelization": "NC"}),
        ("decision=NPC & parallelization=P-complete", {"decision": "NPC", "parallelization": "P-complete"}),
    ]
    for label, assign in checks:
        rules = C.theorem_forbidden_by(assign)
        occupied = any(all(r[ch] == v for ch, v in assign.items()) for r in rows)
        e1_e2_report.append({"cell": label, "forbidding_rules": rules, "occupied_in_data": occupied})
        if rules and occupied:
            forbidden_empty_ok = False
    # 2) gap candidates: pairs present in the (decision,counting,parallelization) triple that are NOT
    # forbidden and NOT occupied — illustrative only (N=22).
    triple = ["decision", "counting", "parallelization"]
    occupied_triples = {tuple(r[ch] for ch in triple) for r in rows}
    return {
        "data_violates_theorem": forbidden_checks,          # must be empty
        "forbidden_cells_check": e1_e2_report,               # E1/E2 cells: forbidding rule fires & data empty
        "forbidden_cells_all_empty": forbidden_empty_ok,
        "occupied_decision_counting_parallel_triples": sorted(str(t) for t in occupied_triples),
        "note": "Full-grid occupancy/gap enumeration is an A3 deliverable over the ~120-problem atlas; at N=22 this is a harness check that the data respects E1/E2 and that occupancy runs over marginals (R3).",
    }


# ── assemble the preview ─────────────────────────────────────────────────────────────────────────────────
def run(entries, drop_measured=False, drop_derived=False):
    ids, families, rows = _grid(entries, drop_measured=drop_measured, drop_derived=drop_derived)
    cv_full, entailed_pairs = cramers_v_matrix(rows, C.CHARGES)
    cc_rows, cc_charges = complete_case(rows)
    return {
        "preview": True,
        "harness_sanity_check_only": True,
        "not_the_H1_H3_verdict": "A3 on the full ~120-problem atlas is the verdict; N here is a preview.",
        "n_problems": len(ids),
        "drop_measured": drop_measured,
        "drop_derived": drop_derived,
        "cramers_v": cv_full,
        "entailment_linked_pairs": entailed_pairs,
        "mca_full_table": mca(rows, C.CHARGES),
        "mca_complete_case": {**mca(cc_rows, cc_charges), "charges": cc_charges, "n_kept": len(cc_rows)},
        "clustering": cluster(ids, families, rows, C.CHARGES),
        "subspace_clustering_R11": cluster_subspaces(ids, families, rows),
        "approx_param_bridge_R12": {
            "raw_cramers_v": cv_full.get("approximation|parameterized"),
            "note": ("Part of this association is theorem-forced: EPTAS<->FPT (Cesati-Trevisan) and "
                     "W[1]-hardness rules out EPTAS (Marx). Report the RESIDUAL after these known bridges "
                     "before calling it surprising (residual computation is an A3 deliverable)."),
        },
        "occupancy": occupancy(rows),
    }


# ── A3: the verdict run (full battery + H1–H3 under prereg_v5) ────────────────────────────────────────────
def leave_one_charge_out(entries):
    """H1 robustness (LOCO ablation): drop each charge in turn, recompute full-table MCA dims>threshold.
    H1 must not hinge on any single charge — especially counting (frontier, sparse) or the measured cell."""
    _, _, rows = _grid(entries)
    out = {}
    for drop in C.CHARGES:
        keep = [c for c in C.CHARGES if c != drop]
        out[drop] = mca([{c: r[c] for c in keep} for r in rows], keep)["dims_above_threshold"]
    return out


def gap_list(entries, spec=C.EIGHTFOLD_SPEC, triples=None):
    """H3 deliverable: over the locked triples' 2-D projections (real values only), classify each EMPTY cell as
    theorem-forbidden (an entailment rule fires) or a GAP — a falsifiable 'a natural problem with (…) should
    exist; none is known' claim. `spec`/`triples` default to Eightfold's; Foundry passes its own."""
    triples = LOCKED_TRIPLES if triples is None else triples
    _, _, rows = _grid(entries)
    gaps, forbidden, seen = [], [], set()
    for triple in triples:
        for a, b in itertools.combinations(triple, 2):
            if (a, b) in seen:
                continue
            seen.add((a, b))
            va = sorted({r[a] for r in rows if r[a] not in C.SENTINELS})
            vb = sorted({r[b] for r in rows if r[b] not in C.SENTINELS})
            occ = {(r[a], r[b]) for r in rows if r[a] not in C.SENTINELS and r[b] not in C.SENTINELS}
            for x in va:
                for y in vb:
                    if (x, y) in occ:
                        continue
                    hits = spec.theorem_forbidden_by({a: x, b: y})
                    if hits:
                        forbidden.append({"cell": f"{a}={x} & {b}={y}", "rules": hits})
                    else:
                        gaps.append({"pair": f"{a}|{b}",
                                     "claim": f"a natural problem with {a}={x} and {b}={y} should exist; none is in the atlas"})
    return {"gaps": gaps, "forbidden": forbidden, "n_gaps": len(gaps), "n_forbidden": len(forbidden)}


# R25 — Cai-Chen approximability->FPT bridge audit. The 22-member APX-complete x FPT cluster is the H2 headline;
# net out the members whose (in-APX & FPT) co-occurrence is theorem-forced (syntactic MAX SNP / MIN F+Pi_1
# membership, standard parameterization — Cai & Chen JCSS 1997) and confirm the approx|parameterized association
# survives. Membership classification (not per-problem cited — from the class definitions; connectivity/
# modification problems are excluded because acyclicity/connectivity are not first-order-definable):
_CC_FORCED_STD_PARAM = frozenset({          # syntactic member AND recorded standard (objective/solution-size) parameter
    "vertex-cover", "d-hitting-set", "three-dimensional-matching", "k-set-packing"})
_CC_MAXSNP_STRUCTURAL_PARAM = frozenset({   # MAX SNP maximization members, but the atlas recorded a structural parameter
    "sat-3", "nae-sat", "one-in-three-sat", "max-2lin", "max-cut", "max-directed-cut"})


def cai_chen_residual_audit(entries, ca="approximation", cb="parameterized"):
    """R25: recompute the approx|parameterized Cramér's V after netting out the Cai-Chen-forced members, at
    increasing aggressiveness. If the association survives even deleting the whole APX-complete x FPT cell, the
    multiplet is genuine, not theorem-forced. Returns a dict of {level: {v, n, netted_out}}."""
    ids, _, rows = _grid(entries)
    byid = {pid: r for pid, r in zip(ids, rows)}
    all_cell = {pid for pid, r in byid.items()  # the full APX-complete x FPT cluster (extreme floor)
                if r[ca] == "APX-complete" and r[cb] == "FPT"}

    def v_after(drop):
        xs = [(r[ca], r[cb]) for pid, r in byid.items()
              if pid not in drop and r[ca] in C.CHARGE_REAL_VALUES[ca] and r[cb] in C.CHARGE_REAL_VALUES[cb]]
        return (round(cramers_v([x for x, _ in xs], [y for _, y in xs]), 3), len(xs))

    levels = {
        "raw": frozenset(),
        "conservative": _CC_FORCED_STD_PARAM,
        "aggressive": _CC_FORCED_STD_PARAM | _CC_MAXSNP_STRUCTURAL_PARAM,
        "extreme_floor_delete_whole_cell": frozenset(all_cell),
    }
    out = {}
    for name, drop in levels.items():
        v, n = v_after(drop)
        out[name] = {"v": v, "n": n, "netted_out": len(drop)}
    out["survives"] = out["extreme_floor_delete_whole_cell"]["v"] >= 0.5  # genuine iff it holds even at the floor
    return out


def a3(entries):
    """Full A3 battery + H1–H3 verdicts under prereg_v5. This is the VERDICT run, not a preview."""
    base = run(entries, drop_measured=False)
    dropm = run(entries, drop_measured=True)
    dropd = run(entries, drop_derived=True)  # Crucible S4: the anchor WITHOUT the dichotomy fills
    loco = leave_one_charge_out(entries)
    gl = gap_list(entries)
    cc_audit = cai_chen_residual_audit(entries)  # R25

    mca_full = base["mca_full_table"]["dims_above_threshold"]
    mca_cc = base["mca_complete_case"]["dims_above_threshold"]
    loco_min = min(loco.values()) if loco else 0
    h1_both = mca_full >= 3 and mca_cc >= 3
    h1 = "SUPPORTED" if (h1_both and loco_min >= 3) else ("PARTIAL" if h1_both else "NOT SUPPORTED")

    amp = base["subspace_clustering_R11"]
    wit = {k: v.get("amplified") for k, v in amp.items()}
    h2 = "SUPPORTED" if (wit.get("permanent|determinant") and wit.get("vertex-cover|clique")) else "PARTIAL"

    forbidden_ok = base["occupancy"]["forbidden_cells_all_empty"]
    h3 = "SUPPORTED" if forbidden_ok else "VIOLATED (data breaks a theorem — investigate!)"

    return {
        "a3": True, "prereg": "prereg_v5", "n_problems": base["n_problems"],
        "H1_dimensionality": {
            "verdict": h1, "rule": "SUPPORTED iff >=3 dims in BOTH full-table and complete-case MCA (R4) AND >=3 under every leave-one-charge-out.",
            "mca_full_dims": mca_full, "mca_complete_case_dims": mca_cc,
            "complete_case_n_kept": base["mca_complete_case"]["n_kept"],
            "loco_min_dims": loco_min, "loco_per_charge": loco,
            "drop_measured_full_dims": dropm["mca_full_table"]["dims_above_threshold"],
            "drop_derived_full_dims": dropd["mca_full_table"]["dims_above_threshold"],
            "drop_derived_complete_case_dims": dropd["mca_complete_case"]["dims_above_threshold"],
            "drop_derived_complete_case_n_kept": dropd["mca_complete_case"]["n_kept"],
        },
        "H2_multiplets": {
            "verdict": h2, "witness_amplified": wit,
            "approx_param_raw_cramers_v": base["cramers_v"].get("approximation|parameterized"),
            "residual_note_R12": base["approx_param_bridge_R12"]["note"],
            "cai_chen_bridge_audit_R25": cc_audit,
            "family_separation": base["clustering"]["family_cohesion"]["separation"],
        },
        "H3_forbidden_and_gaps": {
            "verdict": h3, "forbidden_cells_all_empty_in_data": forbidden_ok,
            "n_theorem_forbidden_cells": gl["n_forbidden"], "n_gaps": gl["n_gaps"],
            "gap_list": gl["gaps"], "theorem_forbidden": gl["forbidden"],
        },
        "cramers_v": base["cramers_v"], "mca_full_table": base["mca_full_table"],
        "mca_complete_case": base["mca_complete_case"], "subspace_clustering": amp,
    }


# ── R7 synthetic self-test (debug the pipeline WITHOUT touching the pilot) ────────────────────────────────
def _toy_entries():
    """A synthetic table with a deliberate 2-block structure, to exercise the pipeline (R7)."""
    from eightfold.atlas import ChargeCell, ProblemEntry

    def mk(pid, block):
        # block A: all "P/FP/..."; block B: all "NPC/#P-complete/..." — a clean, separable structure.
        vals = ({"decision": "P", "counting": "FP", "approximation": "n.a.", "parameterized": "n.a.",
                 "parallelization": "NC", "proof_size": "n.a.", "average_case": "easy-on-average",
                 "landscape": "n.a."} if block == "A" else
                {"decision": "NPC", "counting": "#P-complete", "approximation": "APX-complete",
                 "parameterized": "FPT", "parallelization": "n.a.", "proof_size": "n.a.",
                 "average_case": "transition-known", "landscape": "clustering-OGP-known"})
        cells = []
        for ch, v in vals.items():
            if v in C.SENTINELS:
                cells.append(ChargeCell(ch, v, "toy", "structural"))
            else:
                persp = "toy-param" if ch in C.PERSPECTIVE_REQUIRED else None
                cells.append(ChargeCell(ch, v, "toy", "claimed", provenance={"citation": "toy"}, perspective=persp))
        return ProblemEntry(pid, pid, "graph", "toy", cells, "2026-07-21", "toy")

    return [mk(f"a{i}", "A") for i in range(5)] + [mk(f"b{i}", "B") for i in range(5)]


def selftest():
    entries = _toy_entries()
    out = run(entries)
    ok = (out["mca_full_table"]["dims_above_threshold"] >= 1
          and out["clustering"]["family_cohesion"] is not None
          and out["occupancy"]["forbidden_cells_all_empty"])
    print("R7 self-test on synthetic toy table:")
    print(f"  MCA dims>threshold: {out['mca_full_table']['dims_above_threshold']} "
          f"(eig {[round(x,3) for x in out['mca_full_table']['eigenvalues'][:4]]})")
    print(f"  clustering ran; assignments: {out['clustering']['assignments']}")
    print(f"  occupancy forbidden-cells-all-empty: {out['occupancy']['forbidden_cells_all_empty']}")
    print(f"  self-test {'PASSED' if ok else 'FAILED'}")
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(prog="eightfold.structure")
    ap.add_argument("--pilot", action="store_true", help="run the preview on the atlas")
    ap.add_argument("--selftest", action="store_true", help="R7: exercise the pipeline on a synthetic toy table")
    ap.add_argument("--a3", action="store_true", help="the A3 VERDICT run (full battery + H1-H3 + gap list)")
    ap.add_argument("--drop-measured", action="store_true", help="R9 ablation: exclude measured cells")
    ap.add_argument("--drop-derived", action="store_true", help="Crucible S4 ablation: revert derived (dichotomy) cells to open")
    ap.add_argument("--path", type=Path, default=None, help="atlas path (default: the bundled atlas)")
    ap.add_argument("--out", type=Path, default=None, help="write JSON here (default: results/atlas/pilot_structure.json)")
    args = ap.parse_args(argv if argv is not None else sys.argv[1:])

    if args.selftest:
        return selftest()

    if args.a3:
        from eightfold.atlas import DEFAULT_PATH, load_atlas
        out = a3(load_atlas(args.path))
        out_path = args.out or (DEFAULT_PATH.parent / "a3_structure.json")
        out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
        h1, h2, h3 = out["H1_dimensionality"], out["H2_multiplets"], out["H3_forbidden_and_gaps"]
        print(f"A3 verdict run (prereg_v5, n={out['n_problems']}) written to {out_path}")
        print(f"  H1 dimensionality: {h1['verdict']}  (full {h1['mca_full_dims']} dims, complete-case "
              f"{h1['mca_complete_case_dims']} dims on n={h1['complete_case_n_kept']}, LOCO min {h1['loco_min_dims']}, "
              f"drop-measured {h1['drop_measured_full_dims']}, drop-derived cc {h1['drop_derived_complete_case_dims']} "
              f"on n={h1['drop_derived_complete_case_n_kept']})")
        print(f"  H2 multiplets:     {h2['verdict']}  (witness amplification {h2['witness_amplified']}; "
              f"approx|param raw V={round(h2['approx_param_raw_cramers_v'], 2)})")
        print(f"  H3 forbidden/gaps: {h3['verdict']}  ({h3['n_theorem_forbidden_cells']} theorem-forbidden cells "
              f"empty in data, {h3['n_gaps']} falsifiable gaps)")
        return 0

    if not args.pilot:
        ap.print_help()
        return 0

    from eightfold.atlas import DEFAULT_PATH, load_atlas
    entries = load_atlas(args.path)
    out = run(entries, drop_measured=args.drop_measured, drop_derived=args.drop_derived)
    out_path = args.out or (DEFAULT_PATH.parent / "pilot_structure.json")
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    m = out["mca_full_table"]
    cc = out["mca_complete_case"]
    print(f"structure preview written to {out_path}  (drop_measured={args.drop_measured}, drop_derived={args.drop_derived})")
    print(f"  MCA full-table:     dims>1/Q = {m['dims_above_threshold']}  "
          f"(eig {[round(x,3) for x in m['eigenvalues'][:4]]}, n={m['n_problems']})")
    print(f"  MCA complete-case:  dims>1/Q = {cc['dims_above_threshold']}  "
          f"(n_kept={cc['n_kept']} on {cc['charges']})")
    print(f"  clustering family separation: "
          f"{out['clustering']['family_cohesion']['separation']:.3f}")
    print(f"  occupancy: forbidden cells all empty in data = {out['occupancy']['forbidden_cells_all_empty']}")
    print(f"  [PREVIEW — harness sanity-check only; the H1–H3 verdict is A3 on the full atlas]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
