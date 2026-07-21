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
def _grid(entries, drop_measured=False):
    """Return (ids, families, rows) where rows[i] maps charge -> value string (sentinels included).

    drop_measured (R9): recode any `measured`/`measured-scaling` cell to a dropped sentinel so the ablation
    removes self-generated values from the analysis.
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
def run(entries, drop_measured=False):
    ids, families, rows = _grid(entries, drop_measured=drop_measured)
    cv_full, entailed_pairs = cramers_v_matrix(rows, C.CHARGES)
    cc_rows, cc_charges = complete_case(rows)
    return {
        "preview": True,
        "harness_sanity_check_only": True,
        "not_the_H1_H3_verdict": "A3 on the full ~120-problem atlas is the verdict; N here is a preview.",
        "n_problems": len(ids),
        "drop_measured": drop_measured,
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
    ap.add_argument("--drop-measured", action="store_true", help="R9 ablation: exclude measured cells")
    ap.add_argument("--path", type=Path, default=None, help="atlas path (default: the bundled atlas)")
    ap.add_argument("--out", type=Path, default=None, help="write JSON here (default: results/atlas/pilot_structure.json)")
    args = ap.parse_args(argv if argv is not None else sys.argv[1:])

    if args.selftest:
        return selftest()

    if not args.pilot:
        ap.print_help()
        return 0

    from eightfold.atlas import DEFAULT_PATH, load_atlas
    entries = load_atlas(args.path)
    out = run(entries, drop_measured=args.drop_measured)
    out_path = args.out or (DEFAULT_PATH.parent / "pilot_structure.json")
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    m = out["mca_full_table"]
    cc = out["mca_complete_case"]
    print(f"structure preview written to {out_path}  (drop_measured={args.drop_measured})")
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
