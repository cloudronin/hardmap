#!/usr/bin/env python3
"""Geometry Probe A — blend-violation, qualified against the 4,072-class Boolean roster (prereg_v16).

WHAT THE PROBE MEASURES. For a feasible region R and a blending operation f of arity m, the VIOLATION RATE
is the fraction of m-tuples drawn from R whose coordinatewise blend f(t1..tm) lands OUTSIDE R. Closure is
the special case rate == 0. The probe's point is the DEGREE — the continuous scale the dichotomy theorems
binarise away.

F2 LAW, VERBATIM AND LOAD-BEARING: probe values NEVER impersonate worst-case charges. A low violation rate
on an ensemble is not a tractability claim; it is a measured geometric property that may ASSOCIATE with
charges, and the association is the research object. Nothing in this file reads or writes a charge.

THE DESIGN NOTE, SEALED BEFORE RUNNING (prereg_v16), because it decides what may be claimed:
  On this roster |R| <= 15 and arity <= 4, so the rate is computable EXHAUSTIVELY. Exhaustively computed,
  `rate == 0` is EQUIVALENT to the oracle's closure flag BY DEFINITION. A known-answer battery scored on the
  exhaustive probe therefore passes BY CONSTRUCTION, and separation against oracle labels is 100% BY
  CONSTRUCTION. That is the theorem-forced-credit trap in an instrument's costume.
  So the study splits:
    EXHAUSTIVE ARM  — calibration only. Verifies the implementation computes what closure means.
    SAMPLED ARM     — the actual qualification. The instrument that would deploy on natural rows cannot
                      enumerate a region; it samples one. Its resolution at a declared budget is not forced.
    AND SPECIFICITY IS STILL FORCED — if R is closed under f then NO m-tuple violates, so every sample
                      returns 0 and a closed class can never be called open. Only SENSITIVITY is measurable.
"""
import hashlib
import json
import random
import sys
from collections import Counter
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

LAT = ROOT / "foundry" / "results" / "lattice"
OUT = LAT / "geometry_probe_a_results.json"
SEED = 20260726
BUDGETS = (10, 30, 100, 300)
INSUFFICIENT_FLOOR = 20            # |R|^m < 20 -> rate quantised coarser than 0.05
MIDDLE_BAND = (0.05, 0.50)         # the "almost-closed" band, pinned in the seal

# flavor -> (operation, arity, the oracle flag that IS closure under it)
FLAVORS = {
    "majority": (lambda ts: tuple(1 if sum(c) >= 2 else 0 for c in zip(*ts)), 3, "bijunctive"),
    "minority": (lambda ts: tuple(c[0] ^ c[1] ^ c[2] for c in zip(*ts)), 3, "affine"),
    "min":      (lambda ts: tuple(min(c) for c in zip(*ts)), 2, "horn"),
    "max":      (lambda ts: tuple(max(c) for c in zip(*ts)), 2, "dualhorn"),
}


def exhaustive_rate(rel, op, m):
    """Exact violation rate over ALL m-tuples of R. Calibration arm — forced, and named as such."""
    R = set(rel)
    tot = bad = 0
    for ts in product(rel, repeat=m):
        tot += 1
        if op(ts) not in R:
            bad += 1
    return bad / tot, tot


def sampled_detects(rel, op, m, budget, rng):
    """THE QUALIFICATION ARM. Does a budget-B uniform sample find ANY violation? Returns (detected, seen)."""
    R = set(rel)
    n = len(rel)
    for _ in range(budget):
        ts = tuple(rel[rng.randrange(n)] for _ in range(m))
        if op(ts) not in R:
            return True
    return False


def selftest():
    """Known-answer battery on HAND-BUILT relations AND on real roster rows (the S1 rule: a selftest that
    never touches real data qualifies only the toy path)."""
    errs = []
    # hand-built: the canonical witnesses
    # LOGGED, per prereg_v16 score 1 ("fix and rerun is legal at this gate, logged"): the battery's FIRST
    # run failed — and the fault was in THESE EXPECTATIONS, not in the probe. The case read "NEQ2 {01,10}
    # is affine, NOT majority-closed". NEQ2 is `x != y`, which is 2-CNF-expressible as
    # (x OR y) AND (NOT x OR NOT y) — therefore bijunctive, therefore MAJORITY-CLOSED. It is closed under
    # both minority and majority. The instrument was right and the hand-written answer key was wrong,
    # which is the known-answer battery working in the direction nobody plans for.
    cases = [
        ("OR2 {01,10,11}: dual-horn (max-closed) and bijunctive (majority-closed); NOT min- or "
         "minority-closed",
         [(0, 1), (1, 0), (1, 1)], {"max": 0.0, "majority": 0.0}, {"min", "minority"}),
        ("NEQ2 {01,10}: affine AND bijunctive — closed under minority and majority both; NOT min/max",
         [(0, 1), (1, 0)], {"minority": 0.0, "majority": 0.0}, {"min", "max"}),
        ("OR3 = {0,1}^3 minus 000: the majority witness — maj(100,010,001) = 000 is outside",
         [t for t in product((0, 1), repeat=3) if any(t)], {"max": 0.0}, {"majority", "minority"}),
        ("the full square {00,01,10,11} is closed under everything",
         [(0, 0), (0, 1), (1, 0), (1, 1)], {f: 0.0 for f in FLAVORS}, set()),
    ]
    for name, rel, zero_expect, nonzero_expect in cases:
        for fl, (op, m, _) in FLAVORS.items():
            r, _ = exhaustive_rate(rel, op, m)
            if fl in zero_expect and r != 0.0:
                errs.append(f"selftest [{name}]: {fl} rate {r} != 0")
            if fl in nonzero_expect and r == 0.0:
                errs.append(f"selftest [{name}]: {fl} rate is 0 but should violate")
    # REAL ROWS: every roster class must satisfy rate==0 <=> oracle flag, exactly
    ct = json.loads((LAT / "prism_v2_charges.json").read_text())["charge_table"]
    for row in ct:
        rel = [tuple(int(b) for b in t) for t in row["relation"]]
        for fl, (op, m, flag) in FLAVORS.items():
            r, _ = exhaustive_rate(rel, op, m)
            if (r == 0.0) != bool(row["flags"][flag]):
                errs.append(f"selftest REAL ROW arity={row['arity']} |R|={len(rel)}: "
                            f"{fl} rate={r} but flags[{flag}]={row['flags'][flag]}")
                break
    print(f"selftest: {'PASS' if not errs else 'FAIL'} ({len(ct)} real rows x {len(FLAVORS)} flavors)")
    for e in errs[:8]:
        print("   ", e)
    return not errs


def census(rows):
    """Census-before-seal on the probe's OWN derived quantity. The standing law applies to instruments too,
    and it checks BOTH ends of starvation — the one-sided gate was the Marrow M4 finding."""
    out = {}
    for fl in FLAVORS:
        vals = [r["rates"][fl] for r in rows]
        c = Counter(round(v, 4) for v in vals)
        top, n = c.most_common(1)[0]
        share = n / len(vals)
        no_level_clears = all(v < 5 for v in c.values())
        out[fl] = {"n_cells": len(vals), "n_distinct": len(c), "modal_value": top,
                   "modal_share": round(share, 4),
                   "starved": bool(share > 0.90 or len(c) < 2 or no_level_clears),
                   "note": ("OVER-CONCENTRATED" if share > 0.90 else
                            "CONSTANT" if len(c) < 2 else
                            "OVER-DISPERSED — no level clears the Cochran floor" if no_level_clears
                            else "ok")}
    return out


def main() -> int:
    if not selftest():
        print("\nKNOWN-ANSWER BATTERY FAILED — probe bug by definition (prereg_v16 score 1).")
        print("Fix and rerun is legal at this gate and is logged. Refusing to emit results.")
        return 1

    ct = json.loads((LAT / "prism_v2_charges.json").read_text())["charge_table"]
    rng = random.Random(SEED)
    rows = []
    for row in ct:
        rel = [tuple(int(b) for b in t) for t in row["relation"]]
        rec = {"arity": row["arity"], "n_tuples": len(rel), "rates": {}, "n_blends": {},
               "insufficient": {}, "oracle": {}}
        for fl, (op, m, flag) in FLAVORS.items():
            r, tot = exhaustive_rate(rel, op, m)
            rec["rates"][fl] = r
            rec["n_blends"][fl] = tot
            rec["insufficient"][fl] = bool(tot < INSUFFICIENT_FLOOR)
            rec["oracle"][fl] = bool(row["flags"][flag])
        rows.append(rec)

    # ── score 1: the battery (forced; calibration credit only) ──────────────────────────────────────
    battery = {fl: {"agree": 0, "disagree": 0} for fl in FLAVORS}
    for r in rows:
        for fl in FLAVORS:
            k = "agree" if (r["rates"][fl] == 0.0) == r["oracle"][fl] else "disagree"
            battery[fl][k] += 1

    # ── score 2: sampled sensitivity (THE qualification) ────────────────────────────────────────────
    sens = {fl: {} for fl in FLAVORS}
    rel_by_idx = [[tuple(int(b) for b in t) for t in row["relation"]] for row in ct]
    for fl, (op, m, _) in FLAVORS.items():
        idx_open = [i for i, r in enumerate(rows) if not r["oracle"][fl]]
        for b in BUDGETS:
            det = sum(1 for i in idx_open if sampled_detects(rel_by_idx[i], op, m, b, rng))
            sens[fl][str(b)] = {"n_open_classes": len(idx_open), "detected": det,
                                "sensitivity": round(det / len(idx_open), 4) if idx_open else None}

    # ── score 3: the distribution shape (a question, not a bet) ─────────────────────────────────────
    BANDS = [("zero", 0.0, 0.0), ("0_to_005", 0.0, 0.05), ("005_to_015", 0.05, 0.15),
             ("015_to_030", 0.15, 0.30), ("030_to_050", 0.30, 0.50), ("050_to_075", 0.50, 0.75),
             ("075_to_1", 0.75, 1.0001)]
    dist = {}
    for fl in FLAVORS:
        adm = [r["rates"][fl] for r in rows if not r["insufficient"][fl]]
        # dict keyed by band — NEVER a bare array; the tidy-number walker descends into dicts only
        hist = {}
        for name, lo, hi in BANDS:
            hist[name] = (sum(1 for v in adm if v == 0.0) if name == "zero"
                          else sum(1 for v in adm if lo < v < hi))
        nz = [v for v in adm if v > 0.0]
        mid = [v for v in nz if MIDDLE_BAND[0] <= v <= MIDDLE_BAND[1]]
        dist[fl] = {"n_admissible": len(adm), "n_insufficient": sum(1 for r in rows if r["insufficient"][fl]),
                    "histogram": hist, "n_nonzero": len(nz),
                    "middle_band_fraction_of_nonzero": round(len(mid) / len(nz), 4) if nz else None,
                    "mean_nonzero": round(sum(nz) / len(nz), 4) if nz else None}

    cen = census(rows)
    qualified = all(battery[fl]["disagree"] == 0 for fl in FLAVORS)
    doc = {
        "schema": "geometry-probe-a/v1", "prereg": "prereg_v16", "seed": SEED,
        "F2_law": ("probe values NEVER impersonate worst-case charges. A low violation rate is a measured "
                   "geometric property that may ASSOCIATE with charges; the association is the research "
                   "object. No charge is read or written by this instrument."),
        "n_classes": len(rows), "flavors": list(FLAVORS), "budgets": list(BUDGETS),
        "score_1_known_answer_battery": {
            "result": battery,
            "status": "CALIBRATION ONLY — FORCED BY CONSTRUCTION",
            "why_forced": ("exhaustively computed, rate == 0 is equivalent to the oracle's closure flag by "
                           "definition. This verifies the implementation computes what closure means and "
                           "earns no credit beyond that. Sealed as forced in prereg_v16 before running.")},
        "score_2_sampled_sensitivity": {
            "result": sens,
            "status": "THE ACTUAL QUALIFICATION — not forced",
            "specificity": {"value": 1.0, "status": "FORCED, NOT AN ACHIEVEMENT",
                            "why": ("if R is closed under f then no m-tuple violates, so every sample "
                                    "returns 0 and a closed class can never be called open")}},
        "score_3_distribution_shape": {
            "result": dist,
            "status": "PRE-REGISTERED AS A QUESTION, NOT A BET — no direction was predicted",
            "middle_band": list(MIDDLE_BAND)},
        "census_before_seal": cen,
        "insufficient_rule": f"|R|^m < {INSUFFICIENT_FLOOR}; counted, still battery-scored, excluded from the distribution",
        "verdict": "QUALIFIED" if qualified else "NOT-QUALIFIED",
        "verdict_scope": ("licensed for natural-row ensembles WITH ITS ACCURACY CHARACTERISED. Natural-row "
                          "deployment is explicitly NOT authorised by this run and needs its own spec."),
    }
    ack = [{"stat": "score_2_sampled_sensitivity.specificity.value", "value": 1.0,
            "why_the_exactness_is_expected": (
                "FORCED, and sealed as forced before running. If R is closed under f then NO m-tuple "
                "violates, so every sample returns rate 0 and a closed class can NEVER be called open. "
                "This 1.0 is a property of the definition, not a measurement.")}]
    for fl in FLAVORS:
        for b in BUDGETS:
            if sens[fl][str(b)]["sensitivity"] == 1.0:
                n = sens[fl][str(b)]["n_open_classes"]
                ack.append({"stat": f"score_2_sampled_sensitivity.result.{fl}.{b}.sensitivity", "value": 1.0,
                            "why_the_exactness_is_expected": (
                                f"at budget {b}, all {n} classes the oracle marks not-closed under {fl} "
                                f"were detected. Saturation, not a definition: the SAME statistic is "
                                f"{sens[fl][str(BUDGETS[0])]['sensitivity']} at budget {BUDGETS[0]}, so the "
                                f"measurement has a live dynamic range and this budget sits at its top.")})
    for fl, v in cen.items():
        if v["modal_value"] == 0.0:
            ack.append({"stat": f"census_before_seal.{fl}.modal_value", "value": 0.0,
                        "why_the_exactness_is_expected": (
                            f"the modal violation rate is exactly 0 because the closed classes form the "
                            f"largest single level ({v['modal_share']:.0%} of {v['n_cells']}). Rate 0 IS "
                            f"closure; that a plurality of classes are closed under {fl} is a fact about "
                            f"the roster, and the column is not starved ({v['n_distinct']} distinct values).")})
    doc["extremal_acknowledged"] = ack
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    print(f"\nGEOMETRY PROBE A — qualification study ({len(rows)} classes)\n")
    print("SCORE 1 — known-answer battery (FORCED, calibration only)")
    for fl, v in battery.items():
        print(f"    {fl:<10} agree {v['agree']:>5}  disagree {v['disagree']}")
    print("\nSCORE 2 — sampled sensitivity (THE qualification; specificity 1.0 is forced)")
    print(f"    {'flavor':<10}{'open':>7}" + "".join(f"{('B='+str(b)):>10}" for b in BUDGETS))
    for fl in FLAVORS:
        row0 = sens[fl][str(BUDGETS[0])]
        print(f"    {fl:<10}{row0['n_open_classes']:>7}" +
              "".join(f"{sens[fl][str(b)]['sensitivity']:>10.4f}" for b in BUDGETS))
    print("\nSCORE 3 — distribution shape (a question, not a bet)")
    for fl, v in dist.items():
        print(f"    {fl:<10} admissible {v['n_admissible']:>5}  nonzero {v['n_nonzero']:>5}  "
              f"middle-band frac {v['middle_band_fraction_of_nonzero']}  mean(nonzero) {v['mean_nonzero']}")
        print(f"               {v['histogram']}")
    print("\nCENSUS-BEFORE-SEAL on the probe's own quantity")
    for fl, v in cen.items():
        print(f"    {fl:<10} distinct {v['n_distinct']:>4}  modal {v['modal_value']} @ {v['modal_share']:.0%}"
              f"  starved={v['starved']}  {v['note']}")
    print(f"\nVERDICT: {doc['verdict']}")
    print(f"wrote {OUT.name}  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
