"""Pebble P3 (re-opened) — the FULL point-to-set sweep (prereg_v24). Qualified observable: measure_pointset,
reach_score = signal at r=2. Tests WHY the dichotomy holds: within-co-clone replication (reach constant within a
co-clone = algebra-echo (a); varying = below-the-algebra (b)) and a size ladder (gap changes with n = finite-size
(c)). Provenance + bucket-population reported per cell BEFORE any reading is scored (thin cells unmeasurable).

Run: PYTHONPATH=... python foundry/dev/pointset_sweep.py
"""
import json
import statistics as st
from itertools import product

from foundry import pointset as PS
from foundry import ensemble as E
from foundry.landscape_run import locate_alpha_struct

SIZES = [12, 15, 18]           # all <= ENUM_N_MAX=18 (exact); constant density across the ladder isolates finite-size
NINST, RADIUS = 4, 2
DENSITY_FRAC = 0.6
COARSE = [round(0.3 + 0.3 * i, 2) for i in range(14)]
BW = {"horn", "dhorn", "bij"}  # bounded-width flags


def classify(profile):
    flags = set(profile.split("+"))
    if flags & BW:
        return "SHORT"                       # bounded-width
    if "aff" in flags:
        return "LONG"                        # unbounded-width / affine
    return "OTHER"


def long_anchors():
    """Pure-affine (unbounded-width) LONG-class anchors: 3-XOR and 4-XOR, both parities. Few affine relations exist
    (parity is essentially unique per arity/parity), so the affine class is anchored, not richly replicated."""
    a3 = [frozenset(t for t in product((0, 1), repeat=3) if sum(t) % 2 == c) for c in (0, 1)]
    a4 = [frozenset(t for t in product((0, 1), repeat=4) if sum(t) % 2 == c) for c in (0, 1)]
    out = []
    for k, R in enumerate(a3 + a4):
        prof = "0v+aff" if tuple([0] * len(next(iter(R)))) in R else "1v+aff"
        out.append({"profile": prof, "class": "LONG", "id": f"xor{len(next(iter(R)))}-{k}",
                    "relation": sorted(tuple(t) for t in R), "alpha_struct": None})
    return out


def short_reps():
    """Bounded-width reps from the Sprint 4.6 roster, grouped by co-clone profile; profiles with >=3 reps, <=4 each
    — the rich within-co-clone replication where (a) vs (b) is discriminated."""
    rows = json.load(open("foundry/foundry/results/landscape/sprint46_roster.json"))["rows"]
    byprof = {}
    for r in rows:
        if classify(r["profile"]) == "SHORT":
            byprof.setdefault(r["profile"], []).append(r)
    sel = []
    for prof, rs in byprof.items():
        if len(rs) < 3:
            continue
        for k, r in enumerate(rs[:4]):
            sel.append({"profile": prof, "class": "SHORT", "id": f"{prof}#{k}",
                        "relation": r["relation"], "alpha_struct": r["alpha_struct"]})
    return sel


def density_for(rec, n):
    a_struct = rec["alpha_struct"]
    if a_struct is None:                     # affine anchors: locate once (middle size), reuse across ladder
        a_struct, _ = locate_alpha_struct((frozenset(map(tuple, rec["relation"])),), (0, 1), 15, 500000, K=35, grid=COARSE)
        rec["alpha_struct"] = a_struct
    return round(DENSITY_FRAC * a_struct, 3)


def main():
    roster = long_anchors() + short_reps()
    print(f"roster: {len(roster)} relations "
          f"(LONG {sum(r['class']=='LONG' for r in roster)}, SHORT {sum(r['class']=='SHORT' for r in roster)}); "
          f"profiles {sorted(set(r['profile'] for r in roster))}", flush=True)

    cells = []
    for rec in roster:
        R = frozenset(tuple(t) for t in rec["relation"])
        for n in SIZES:
            alpha = density_for(rec, n)
            m = PS.measure_pointset((R,), (0, 1), n, alpha, n_instances=NINST, base_seed=970000, reach_radius=RADIUS)
            r2 = m["radii"].get(RADIUS, {})
            cells.append({"profile": rec["profile"], "class": rec["class"], "id": rec["id"], "n": n, "alpha": alpha,
                          "reach": m["reach_score"], "exact_fraction": m["exact_fraction"], "median_coset": m["median_coset"],
                          "r2_n_buckets": r2.get("mean_buckets"), "r2_measurable": bool(r2.get("measurable")),
                          "n_units": len(m["per_unit_reach"])})
        print(f"  {rec['id']:26s} [{rec['class']}] reach by n: "
              f"{ {c['n']: c['reach'] for c in cells if c['id']==rec['id']} }", flush=True)

    # ---- provenance + population report FIRST; a cell is scored only if measurable + reach not None ----
    measurable = [c for c in cells if c["r2_measurable"] and c["reach"] is not None]
    unmeasurable = [c for c in cells if not (c["r2_measurable"] and c["reach"] is not None)]

    # within-co-clone SD (per profile, per n) over measurable cells
    within = {}
    for c in measurable:
        within.setdefault((c["profile"], c["n"]), []).append(c["reach"])
    within_sd = {f"{p}@n{n}": round(st.pstdev(v), 4) for (p, n), v in within.items() if len(v) >= 2}

    # between-class gap per n; size trend
    gap_by_n, class_means = {}, {}
    for n in SIZES:
        lo = [c["reach"] for c in measurable if c["class"] == "LONG" and c["n"] == n]
        sh = [c["reach"] for c in measurable if c["class"] == "SHORT" and c["n"] == n]
        class_means[n] = {"LONG": round(st.mean(lo), 4) if lo else None, "SHORT": round(st.mean(sh), 4) if sh else None}
        gap_by_n[n] = round(st.mean(lo) - st.mean(sh), 4) if (lo and sh) else None

    gaps = [gap_by_n[n] for n in SIZES if gap_by_n[n] is not None]
    gap_rel_change = round((gaps[-1] - gaps[0]) / gaps[0], 3) if len(gaps) >= 2 and gaps[0] else None
    max_within_sd = max(within_sd.values()) if within_sd else None
    med_gap = st.median(gaps) if gaps else None
    # readings
    a_echo = bool(within_sd and med_gap and max_within_sd < 0.25 * med_gap and all(g > 0 for g in gaps))
    b_below = bool(within_sd and med_gap and max_within_sd >= 0.25 * med_gap)
    c_finite = bool(gap_rel_change is not None and abs(gap_rel_change) >= 0.30)

    out = {"prereg": "v24", "sizes": SIZES, "n_instances": NINST, "reach_radius": RADIUS,
           "provenance_population_report": {
               "n_cells": len(cells), "n_measurable": len(measurable), "n_unmeasurable": len(unmeasurable),
               "unmeasurable_cells": [{"id": c["id"], "n": c["n"], "reach": c["reach"],
                                       "r2_buckets": c["r2_n_buckets"], "coset": c["median_coset"]} for c in unmeasurable],
               "exact_fraction_overall": round(st.mean([c["exact_fraction"] for c in cells if c["exact_fraction"] is not None]), 3)},
           "cells": cells,
           "within_co_clone_sd": within_sd, "max_within_sd": max_within_sd,
           "between_class_means_by_n": class_means, "gap_by_n": gap_by_n, "median_gap": med_gap,
           "gap_relative_change_small_to_large_n": gap_rel_change,
           "readings": {"a_algebra_echo": a_echo, "b_below_the_algebra": b_below, "c_finite_size": c_finite,
                        "dominant": ("b_below_the_algebra" if b_below else "c_finite_size" if c_finite
                                     else "a_algebra_echo" if a_echo else "inconclusive")}}
    json.dump(out, open("foundry/foundry/results/landscape/pointset_sweep.json", "w"), indent=2)

    print("\n=== provenance/population gate (before interpretation) ===")
    print(f"  {len(measurable)}/{len(cells)} cells measurable; {len(unmeasurable)} unmeasurable (declared, not averaged)")
    print("=== readings ===")
    print(f"  between-class gap by n: {gap_by_n}  (rel change small->large n = {gap_rel_change})")
    print(f"  max within-co-clone SD: {max_within_sd}  vs 0.25*median_gap = {round(0.25*med_gap,4) if med_gap else None}")
    print(f"  (a) algebra-echo={a_echo}  (b) below-algebra={b_below}  (c) finite-size={c_finite}")
    print(f"  DOMINANT READING: {out['readings']['dominant']}")


if __name__ == "__main__":
    main()
