"""Prism v2 R1 (prereg_v33) — build the arity-<=4 Boolean single-relation roster (permutation-only dedup),
run the gates (pred 1: NPI + reproduction of v1's V=0.256 on the arity-<=3 SUBSET), report marginals +
the pred-2 descriptive bounded-width marginal (purely-affine unbounded classes enumerated), persist.

Run: PYTHONPATH=... python foundry/dev/prism_v2_build.py
"""
import json
import time
from collections import Counter

from eightfold import structure as S
from foundry import prism

PER_RELATION = ("decision", "counting", "localization", "parallelization", "approx_counting", "parameterized")
OBJ_APPROX = ("approx_maxones", "approx_minones")


def _approx_param_v(classes):
    """v1 headline: approx<->param on the both-real (relation,objective) rows (pool Max/Min)."""
    rows = []
    for _, _, _, c in classes:
        if c["parameterized"] != "open":
            rows.append((c["approx_maxones"], c["parameterized"]))
            rows.append((c["approx_minones"], c["parameterized"]))
    xs = [a for a, _ in rows]; ys = [p for _, p in rows]
    return S.cramers_v(xs, ys), len(rows)


def main():
    t0 = time.time()
    roster = prism.build_roster(4)           # [(arity, rel, class_size, charges)] for arity 1..4
    build_s = time.time() - t0
    n_classes = len(roster)
    by_arity = Counter(a for a, _, _, _ in roster)

    # ── pred 1a: NPI calibration — decision in {P, NPC}, no intermediate ─────────────────────────────────────
    decisions = {c["decision"] for _, _, _, c in roster}
    npi_ok = decisions <= {"P", "NPC"}
    if not npi_ok:
        raise SystemExit(f"NPI CALIBRATION FAILED (pred 1): decision values = {decisions} — HALT")

    # ── pred 1b: reproduction gate — arity-<=3 SUBSET reproduces v1's approx<->param V = 0.256 ───────────────
    sub3 = [r for r in roster if r[0] <= 3]
    n_sub3 = len(sub3)
    v3_repro, n_both3 = _approx_param_v(sub3)
    repro_ok = abs(v3_repro - 0.256) < 0.01
    if not repro_ok:
        raise SystemExit(f"REPRODUCTION GATE FAILED (pred 1): arity<=3 subset approx<->param V={v3_repro:.4f} "
                         f"(target 0.256) — HALT. arity<=3 classes={n_sub3}")

    # full-roster approx<->param V (descriptive, the arity-<=4 headline denominator)
    v_full, n_both_full = _approx_param_v(roster)

    # ── marginals per column (marginals-first) ──────────────────────────────────────────────────────────────
    marginals = {col: dict(Counter(c[col] for _, _, _, c in roster)) for col in PER_RELATION + OBJ_APPROX}

    # ── pred 2 (descriptive): bounded-width marginal + the PURELY-AFFINE unbounded classes (the arity-4 novelty)
    # purely-affine = affine AND unbounded-width (constant-free, majority-free, semilattice-free). At arity<=3
    # this set is EMPTY (v1 §2); at arity 4 it is the odd-parity-like classes. These are param-FPT (affine=>FPT).
    purely_affine_unbounded = [(a, c) for a, _, _, c in roster
                               if c["flags"]["affine"] and c["localization"] == "unbounded-width"]
    pa_by_arity = Counter(a for a, _ in purely_affine_unbounded)
    pa_paramreal = [c for _, c in purely_affine_unbounded if c["parameterized"] != "open"]
    # cross-check the confound: among PARAM-REAL rows, is every unbounded-width class affine?
    unbounded_paramreal = [c for _, _, _, c in roster
                           if c["localization"] == "unbounded-width" and c["parameterized"] != "open"]
    unbounded_paramreal_all_affine = all(c["flags"]["affine"] for c in unbounded_paramreal)

    out = {"prereg": "v33", "codename": "Prism v2 — arity-<=4 anti-canon replication",
           "n_symmetry_classes": n_classes, "classes_by_arity": dict(sorted(by_arity.items())),
           "build_seconds": round(build_s, 1),
           "pred1a_NPI": {"decision_values": sorted(decisions), "passed": npi_ok},
           "pred1b_reproduction_gate": {"arity_le3_classes": n_sub3, "approx_param_V": round(float(v3_repro), 4),
                                        "n_both_real_rows": n_both3, "target": 0.256, "passed": bool(repro_ok)},
           "full_roster_approx_param_V_descriptive": {"V": round(float(v_full), 4), "n_both_real_rows": n_both_full},
           "marginals": marginals,
           "pred2_bounded_width_marginal_descriptive": {
               "localization_marginal": marginals["localization"],
               "purely_affine_unbounded_classes_total": len(purely_affine_unbounded),
               "purely_affine_unbounded_by_arity": dict(sorted(pa_by_arity.items())),
               "purely_affine_unbounded_param_real": len(pa_paramreal),
               "CONFOUND_CHECK_every_unbounded_paramreal_class_is_affine": bool(unbounded_paramreal_all_affine),
               "n_unbounded_paramreal_classes": len(unbounded_paramreal),
               "note": "purely-affine-unbounded is EMPTY at arity<=3 (v1) and non-empty only at arity 4 (odd-parity-like). "
                       "The confound check confirms unbounded-width AND param-real => affine => netted by the bridge => "
                       "the localization arm is untestable on the bridge-completed residual (prereg_v33, preds 3&4 dropped)."},
           "class_sizes": {"total_raw_relations": sum(sz for _, _, sz, _ in roster),
                           "size_distribution": dict(sorted(Counter(sz for _, _, sz, _ in roster).items()))}}

    # persist the charge table (relation as sorted tuple-list; class size; all charges + flags)
    table = [{"arity": a, "relation": [list(t) for t in sorted(rel)], "class_size": sz,
              **{k: c[k] for k in PER_RELATION + OBJ_APPROX}, "flags": c["flags"]}
             for a, rel, sz, c in roster]
    out["charge_table"] = table

    print(f"build_roster(4): {n_classes} classes in {build_s:.1f}s  (by arity {dict(sorted(by_arity.items()))})")
    print(f"pred 1a NPI: decision={sorted(decisions)} passed={npi_ok}")
    print(f"pred 1b reproduction gate: arity<=3 subset ({n_sub3} classes) approx<->param V={v3_repro:.4f} "
          f"(target 0.256) passed={repro_ok}")
    print(f"full arity<=4 approx<->param V={v_full:.4f} on {n_both_full} both-real rows (descriptive)")
    print("marginals:")
    for col in PER_RELATION + OBJ_APPROX:
        print(f"  {col:16s} {marginals[col]}")
    print(f"pred 2 (descriptive): localization {marginals['localization']}; "
          f"purely-affine-unbounded={len(purely_affine_unbounded)} (by arity {dict(sorted(pa_by_arity.items()))}), "
          f"param-real={len(pa_paramreal)}")
    print(f"CONFOUND CHECK: every unbounded-width param-real class is affine = "
          f"{unbounded_paramreal_all_affine} (over {len(unbounded_paramreal)} such classes)")
    json.dump(out, open("foundry/foundry/results/lattice/prism_v2_charges.json", "w"), indent=2)
    print("\nwrote prism_v2_charges.json")


if __name__ == "__main__":
    main()
