"""Prism R1 (prereg_v32) — build the multi-charge table on the 90 symmetry classes, run the gates
(NPI calibration + v3 reproduction), report marginals + distinct-profile counts per column, persist.

Run: PYTHONPATH=... python foundry/dev/prism_build.py
"""
import json
from collections import Counter

from eightfold import structure as S
from foundry import prism

PER_RELATION = ("decision", "counting", "localization", "parallelization", "approx_counting", "parameterized")
OBJ_APPROX = ("approx_maxones", "approx_minones")


def main():
    roster = prism.build_roster(3)   # [(arity, rel, class_size, charges)]
    n_classes = len(roster)

    # ── NPI calibration (prediction 1): decision has no intermediate value ──────────────────────────────────
    decisions = {c["decision"] for _, _, _, c in roster}
    npi_ok = decisions <= {"P", "NPC"}
    if not npi_ok:
        raise SystemExit(f"NPI CALIBRATION FAILED (pred 1): decision values = {decisions} — HALT")

    # ── marginals + distinct-profile counts per column (marginals-first) ────────────────────────────────────
    marginals = {}
    for col in PER_RELATION + OBJ_APPROX:
        marginals[col] = dict(Counter(c[col] for _, _, _, c in roster))

    # ── v3 reproduction (sanity gate): approx<->param on the 166 both-real (relation,objective) rows -> 0.256 ─
    rows = []
    for _, _, _, c in roster:
        if c["parameterized"] != "open":
            rows.append((c["approx_maxones"], c["parameterized"]))
            rows.append((c["approx_minones"], c["parameterized"]))
    xs = [a for a, _ in rows]; ys = [p for _, p in rows]
    v3_repro = S.cramers_v(xs, ys)
    v3_ok = abs(v3_repro - 0.256) < 0.01

    out = {"prereg": "v32", "n_symmetry_classes": n_classes,
           "npi_calibration_pred1": {"decision_values": sorted(decisions), "passed": npi_ok},
           "v3_reproduction_gate": {"approx_param_V_on_both_real_rows": round(float(v3_repro), 4),
                                    "n_both_real_rows": len(rows), "target": 0.256, "passed": bool(v3_ok)},
           "marginals": marginals,
           "distinct_profile_counts": {
               "full_per_relation_profile": len({tuple(c[k] for k in PER_RELATION) for _, _, _, c in roster}),
               "per_column": {col: len(marginals[col]) for col in PER_RELATION + OBJ_APPROX}},
           "class_sizes": {"total_raw_relations": sum(sz for _, _, sz, _ in roster),
                           "n_classes": n_classes,
                           "size_distribution": dict(Counter(sz for _, _, sz, _ in roster))}}

    # persist the full charge table (relation as sorted tuple-list; class size; all charges + flags)
    table = []
    for a, rel, sz, c in roster:
        table.append({"arity": a, "relation": [list(t) for t in sorted(rel)], "class_size": sz,
                      **{k: c[k] for k in PER_RELATION + OBJ_APPROX}, "flags": c["flags"]})
    out["charge_table"] = table

    print(f"classes={n_classes}  NPI pred1 passed={npi_ok} (decision={sorted(decisions)})")
    print(f"v3 reproduction: approx<->param V = {round(float(v3_repro),4)} on {len(rows)} both-real rows  "
          f"(target 0.256, passed={v3_ok})")
    print("marginals:")
    for col in PER_RELATION + OBJ_APPROX:
        print(f"  {col:16s} {marginals[col]}")
    print(f"distinct full per-relation profiles = {out['distinct_profile_counts']['full_per_relation_profile']}")
    json.dump(out, open("foundry/foundry/results/lattice/prism_charges.json", "w"), indent=2)
    print("\nwrote prism_charges.json")


if __name__ == "__main__":
    main()
