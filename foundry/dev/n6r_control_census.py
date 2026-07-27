#!/usr/bin/env python3
"""N6-R Phase 0 — the control-ladder census. THE KILL INPUT, AND NOTHING ELSE.

CENSUS MINIMALISM (methods, minted from N6's contamination): a census computes its kill's inputs and
nothing else. Joining predictor to outcome before the seal is contamination however natural the join.
This file therefore reads the ROSTER and computes CONTROL VIABILITY. It does not read, import, compute,
or touch excess, inflation, hulls, or any outcome — enforced by a test, not by intention.

WHAT IT DECIDES. The standing fair-null ladder was built for natural rows at ambient 2^10..2^14 with 10-14
coordinates. The roster lives at ambient <= 16 with **arity <= 4 coordinates**. Two routes, two ways to die:

  TIER 1.5 (swap randomisation) needs rows x columns to move. At 4 columns there are only C(4,2)=6 column
  pairs, and Terrain already found the chain freezes on dense regions. The roster is dense by construction.

  CP (conditional-Poisson) draws each member at its own cardinality with fitted marginals. At arity n the
  number of vectors of cardinality k is C(n,k) — at most 6. **If a class contains ALL vectors of some
  cardinality, CP has no freedom at that cardinality.** Its total freedom is

      FREEDOM = prod_k  C( C(n,k), count_k )

  and a class with FREEDOM == 1 has exactly one admissible control: the region itself. Excess would be
  identically zero by construction. That is computable in closed form, before drawing anything, and it is
  the sharpest thing this census can report.

KILL: if neither route yields a varying control for a majority of classes, Tier A stops and this census is
the finding.
"""
import hashlib
import json
import random
import sys
from math import comb
from pathlib import Path
from statistics import pstdev

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "dev"))
LAT = ROOT / "foundry" / "results" / "lattice"
ROSTER = LAT / "prism_v2_charges.json"
OUT = LAT / "n6r_control_census.json"
import terrain_score as T                                              # noqa: E402
import n2_dense_control as N2                                          # noqa: E402
from sounding_v1 import BOOL_OPS                                       # noqa: E402

SAMPLE_PER_CELL = 6          # classes sampled per (arity, |R|) cell — for COVERAGE, not for the estimate
K_DRAWS = 30                 # raised: at ambient <= 16 the violation rate is quantised to k/C(r,m), so a
                             # thin draw can show zero spread from resolution rather than from degeneracy
BLEND_FLOOR = 2              # |R| < m cannot blend at all — a FLOOR exclusion, not a control failure
SEED = 20260726


def cp_freedom(rel, n):
    """Closed-form count of distinct CP-admissible controls: prod_k C(C(n,k), count_k).

    Computed rather than sampled, because a sampled estimate of "can this vary?" would itself need a
    variance census. FREEDOM == 1 means the only admissible control IS the region.
    """
    cnt = {}
    for t in rel:
        cnt[sum(t)] = cnt.get(sum(t), 0) + 1
    f = 1
    for k, c in cnt.items():
        avail = comb(n, k)
        if c > avail:
            return 0                      # impossible; would mean a malformed relation
        f *= comb(avail, c)
    return f


def main() -> int:
    roster = json.loads(ROSTER.read_text())["charge_table"]
    rng = random.Random(SEED)

    # stratified sample by (arity, |R|), declared before looking at anything else
    cells = {}
    for i, c in enumerate(roster):
        rel = [tuple(t) for t in c["relation"]]
        cells.setdefault((c["arity"], len(rel)), []).append((i, rel))
    picked = []
    for key in sorted(cells):
        pool = cells[key]
        rng.shuffle(pool)
        picked.extend((key, i, rel) for i, rel in pool[:SAMPLE_PER_CELL])

    rows = []
    for (arity, r), idx, rel in picked:
        n = arity
        freedom = cp_freedom(rel, n)
        # TIER 1.5 — does the chain clear its declared mixing floor?
        floor = max(50, r // 4)
        swaps = []
        t15_rates = []
        for _ in range(4):
            ctrl, sw = T.tier15(rel, rng)
            swaps.append(sw)
            if sw >= floor:
                v = T.rate_of(ctrl, "min", rng)
                if v is not None:
                    t15_rates.append(v)
        t15_ok = bool(t15_rates) and pstdev(t15_rates) > 0 if len(t15_rates) > 1 else False
        # CP — does it produce distinct, varying controls?
        cp_rates, cp_err, cp_uniq = [], [], []
        if freedom > 1:
            for _ in range(K_DRAWS):
                cc, err, uniq = N2.cp_control(rel, rng)
                cp_err.append(err); cp_uniq.append(uniq)
                v = N2.rate_of(cc, "min", rng)
                if v is not None:
                    cp_rates.append(v)
        cp_ok = len(cp_rates) > 1 and pstdev(cp_rates) > 0
        rows.append({"class_index": idx, "arity": arity, "r": r,
                     "ambient": 2 ** arity,
                     "cp_freedom": freedom,
                     "cp_forced": freedom <= 1,
                     "tier15_mixing_floor": floor,
                     "tier15_accepted_swaps": swaps,
                     "tier15_clears_floor": max(swaps) >= floor if swaps else False,
                     "tier15_varies": t15_ok,
                     "cp_varies": cp_ok,
                     "cp_marginal_fit_error": round(sum(cp_err) / len(cp_err), 4) if cp_err else None,
                     "cp_distinct_fraction": round(sum(cp_uniq) / len(cp_uniq), 4) if cp_uniq else None,
                     "route": ("tier1.5" if t15_ok else ("CP" if cp_ok else "NONE"))})

    n = len(rows)
    # THE ESTIMATE MUST BE ROSTER-WEIGHTED. Sampling 6 per cell gives a 2-class cell the same voice as a
    # 730-class cell, and the roster's mass is overwhelmingly arity-4. An unweighted fraction here is a
    # fact about the sampling design, not about the roster — and it fired a false kill on the first run.
    by_route = {}
    for x in rows:
        by_route[x["route"]] = by_route.get(x["route"], 0) + 1
    w_usable = w_none = w_floor = 0.0
    per_cell = {}
    for x in rows:
        key = (x["arity"], x["r"])
        pop = len(cells[key]); taken = min(SAMPLE_PER_CELL, pop); wt = pop / taken
        d = per_cell.setdefault(f"arity{key[0]}_r{key[1]}",
                                {"roster_classes": pop, "sampled": 0, "usable": 0, "below_floor": 0})
        d["sampled"] += 1
        if x["r"] < BLEND_FLOOR:
            w_floor += wt; d["below_floor"] += 1
        elif x["route"] == "NONE":
            w_none += wt
        else:
            w_usable += wt; d["usable"] += 1
    tot_w = w_usable + w_none + w_floor
    usable = sum(v for k, v in by_route.items() if k != "NONE")
    # the closed-form freedom census over the WHOLE roster, not just the sample — it is free
    allfree = []
    for c in roster:
        rel = [tuple(t) for t in c["relation"]]
        allfree.append(cp_freedom(rel, c["arity"]))
    forced_all = sum(1 for f in allfree if f <= 1)

    # the kill reads the ROSTER-WEIGHTED fraction, excluding classes below the blending floor — those
    # cannot be measured at all and are a separate, pre-declared exclusion.
    measurable_w = w_usable + w_none
    kill = ("KILL FIRES — neither route yields a varying control for a majority of the roster"
            if measurable_w <= 0 or w_usable <= measurable_w / 2
            else "census passes — a varying control exists for the majority of the roster")

    doc = {"schema": "n6r-control-census/v1",
           "STATUS": "PHASE 0 — kill input only. No excess, no hull, no outcome touched.",
           "census_minimalism": ("this file reads the roster and computes control viability. It does not "
                                 "read, import or compute any excess, inflation or outcome. Enforced by "
                                 "test, not by intention."),
           "why_the_ladder_needs_regrounding": (
               "the fair-null ladder was built for natural rows at ambient 2^10..2^14 with 10-14 "
               "coordinates. The roster lives at ambient <= 16 with arity <= 4 coordinates. Tier 1.5's "
               "swap chain has only C(4,2)=6 column pairs to work with, and CP's freedom is bounded by "
               "how many vectors share each cardinality."),
           "cp_freedom_definition": ("prod_k C(C(n,k), count_k) — the exact number of distinct "
                                     "CP-admissible controls, in closed form. FREEDOM == 1 means the only "
                                     "admissible control is the region itself and excess is identically "
                                     "zero by construction."),
           "sample": {"per_cell": SAMPLE_PER_CELL, "n_sampled": n, "cells": len(cells)},
           "route_counts_UNWEIGHTED_do_not_read_as_an_estimate": by_route,
           "why_weighting_is_load_bearing": (
               "6 samples per cell gives a 2-class cell the same voice as a 730-class cell, and the "
               "roster is 3982/4072 arity-4. The first run reported 33.3% usable and FIRED A FALSE KILL "
               "on that basis. The roster-weighted figure is the estimate; the unweighted counts are "
               "coverage bookkeeping."),
           "roster_weighted": {
               "usable": round(w_usable, 1), "no_control": round(w_none, 1),
               "below_blending_floor": round(w_floor, 1),
               "usable_fraction_of_measurable": round(w_usable / (w_usable + w_none), 4)
               if (w_usable + w_none) else None},
           "per_cell": per_cell,
           "whole_roster_cp_freedom": {
               "n_classes": len(allfree),
               "forced_freedom_1": forced_all,
               "forced_share": round(forced_all / len(allfree), 4),
               "median": sorted(allfree)[len(allfree) // 2],
               "max": max(allfree),
               "note": ("computed over EVERY class, not just the sample — it is closed-form and free. "
                        "These are the classes where CP cannot vary and which must leave the discovery "
                        "population if CP is the route that carries the roster.")},
           "CENSUS_KILL": kill,
           "rows": rows}
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    print("N6-R PHASE 0 — CONTROL-LADDER CENSUS (kill input only)\n")
    print(f"  sampled {n} classes across {len(cells)} (arity, |R|) cells\n")
    print(f"  {'arity':>6}{'|R|':>5}{'freedom':>10}{'t1.5 swaps':>12}{'t1.5':>7}{'CP':>5}   route")
    for x in rows[:26]:
        print(f"  {x['arity']:>6}{x['r']:>5}{x['cp_freedom']:>10}{max(x['tier15_accepted_swaps']):>12}"
              f"{str(x['tier15_varies']):>7}{str(x['cp_varies']):>5}   {x['route']}")
    if len(rows) > 26:
        print(f"  ... {len(rows)-26} more")
    print(f"\n  routes (UNWEIGHTED, coverage only): {by_route}")
    print(f"\n  ROSTER-WEIGHTED — the estimate the kill reads:")
    print(f"    usable            {w_usable:8.0f}  = {w_usable/(w_usable+w_none):.1%} of measurable")
    print(f"    no control        {w_none:8.0f}")
    print(f"    below blend floor {w_floor:8.0f}  (|R| < {BLEND_FLOOR}: cannot blend; a floor exclusion)")
    print(f"\n  WHOLE-ROSTER CP freedom (closed form, all {len(allfree)} classes):")
    print(f"    forced (freedom == 1): {forced_all} = {forced_all/len(allfree):.1%}")
    print(f"    median {sorted(allfree)[len(allfree)//2]}   max {max(allfree)}")
    print(f"\n  {kill}")
    print(f"\nwrote {OUT.name}  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
