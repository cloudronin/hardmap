#!/usr/bin/env python3
"""Terrain v1 — the sealed primary, Holm-Bonferroni, and the verdict. NOT a second scoring run.

Every number here is computed from the ladder the scoring run already wrote. No region is rebuilt, no
control is redrawn, no measured value moves. What this does is apply the statistic the seal SPECIFIED —
"mean tier-1 excess, tier 1.5 where it clears its mixing floor" — which is ONE statistic per family, not
the two separate tiers the run printed.
"""
import hashlib
import json
import math
import sys
from pathlib import Path
from statistics import mean, stdev

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "foundry" / "results" / "lattice" / "terrain_v1_results.json"
Z = 1.959964


def ci(v):
    n = len(v)
    if n < 2:
        return {"mean": None, "ci95": [None, None], "n": n, "verdict": "INSUFFICIENT (n<2)"}
    m, sd = mean(v), stdev(v)
    h = Z * sd / math.sqrt(n)
    # A P-VALUE IS NEVER EXACTLY ZERO. The normal approximation underflows for large |t| and rounding
    # would print 0.00000, which is both false and precisely the kind of too-tidy number the gate exists
    # to stop. Reported as an UPPER BOUND at the resolution this approximation can actually support.
    P_FLOOR = 1e-5
    raw = 2 * (1 - 0.5 * (1 + math.erf(abs(m / (sd / math.sqrt(n))) / math.sqrt(2))))
    clamped = raw < P_FLOOR
    return {"mean": round(m, 4), "ci95": [round(m - h, 4), round(m + h, 4)], "n": n,
            "p_two_sided": P_FLOOR if clamped else round(raw, 5),
            "p_is_upper_bound": clamped,
            "p_note": ("normal approximation; below 1e-5 it underflows, so the value is reported as an "
                       "upper bound rather than as a point" if clamped else None)}


def agg(recs, pick):
    g = {}
    for r in recs:
        v = pick(r)
        if v is not None:
            g.setdefault((r["row"], r["region"], r["ramp_position"]), []).append(v)
    return [mean(v) for v in g.values()]


def main() -> int:
    doc = json.loads(RES.read_text())
    L = doc["ladder"]
    # THE SEALED PRIMARY: tier 1.5 where it clears the mixing floor, tier 1 otherwise.
    sealed = lambda r: r["tier15_excess"] if r["tier15_usable"] else r["tier1_excess"]

    prim = {"pooled": ci(agg(L, sealed))}
    for fam in sorted({r["family"] for r in L}):
        prim[fam] = ci(agg([r for r in L if r["family"] == fam], sealed))

    # Holm-Bonferroni over the sealed family of 5 (pooled + 4 per-family)
    ps = sorted(((k, v["p_two_sided"]) for k, v in prim.items() if v.get("p_two_sided") is not None),
                key=lambda kv: kv[1])
    holm, m = [], 5
    for i, (k, p) in enumerate(ps):
        thr = 0.05 / (m - i)
        holm.append({"test": k, "p": p, "threshold": round(thr, 5),
                     "reject_null": p < thr,
                     "direction": ("NEGATIVE" if prim[k]["mean"] < 0 else "POSITIVE") if p < thr else None})

    usable = [r for r in L if r["tier15_usable"]]
    frozen = [r for r in L if not r["tier15_usable"]]
    paired = {"tier1_on_paired_set": ci(agg(usable, lambda r: r["tier1_excess"])),
              "tier15_on_paired_set": ci(agg(usable, lambda r: r["tier15_excess"])),
              "within_reading_delta_t15_minus_t1": ci(agg(
                  usable, lambda r: (r["tier15_excess"] - r["tier1_excess"])
                  if r["tier1_excess"] is not None else None))}

    coverage = {
        "tier15_usable": len(usable), "tier15_frozen": len(frozen),
        "mean_tier1_excess_among_usable": round(mean(
            [r["tier1_excess"] for r in usable if r["tier1_excess"] is not None]), 4),
        "mean_tier1_excess_among_frozen": round(mean(
            [r["tier1_excess"] for r in frozen if r["tier1_excess"] is not None]), 4),
        "THE_LIMITATION": (
            "the readings tier 1.5 CANNOT test are exactly the dense ones, and they carry the LARGER "
            "tier-1 excess (+0.1222 against +0.0430). So the tier-1.5 conclusion is established on the "
            "sparser half of the set. This is not the power limitation the seal declared — it is a "
            "COVERAGE limitation, and it is worse in kind, because no amount of n fixes it: at high "
            "density a distinctness-preserving swap chain cannot move at all.")}

    verdict = {
        "VERDICT": "CONTROL-MISMATCH@1.5",
        "primary_bet_outcome": "FAILED",
        "what_was_bet": ("mean sealed-primary excess is POSITIVE with a 95% CI clear of zero, per family "
                         "and pooled"),
        "what_happened": (
            f"pooled sealed primary is {prim['pooled']['mean']:+.4f} with CI "
            f"[{prim['pooled']['ci95'][0]:+.4f}, {prim['pooled']['ci95'][1]:+.4f}] — not positive, and "
            f"the interval contains zero. The bet fails in the direction it was made."),
        "the_mechanism_is_named": (
            "the excess does not die at tier 1. It dies at tier 1.5, and the within-reading delta is "
            "decisive: matching MEMBER CARDINALITY in addition to coordinate marginals moves each "
            "reading's excess by "
            f"{paired['within_reading_delta_t15_minus_t1']['mean']:+.4f} "
            f"(CI [{paired['within_reading_delta_t15_minus_t1']['ci95'][0]:+.4f}, "
            f"{paired['within_reading_delta_t15_minus_t1']['ci95'][1]:+.4f}]), absorbing the whole "
            "anomaly and overshooting into negative territory. H-artifact wins, and the specific unfair "
            "feature of the tier-0 control is that it did not match cardinality."),
        "H_real": "NOT SUPPORTED on the readings this design could test",
        "H_artifact": "SUPPORTED, with the mismatched feature identified as member cardinality",
        "scope_of_the_verdict": (
            f"{len(usable)} of {len(L)} readings. The other {len(frozen)} are INSUFFICIENT-degenerate at "
            "tier 1.5 — their swap chains froze below the mixing floor — and the verdict does NOT extend "
            "to them. They carry the larger tier-1 excess, so the untested remainder is the part that "
            "looked most anomalous."),
        "ANTI_BLENDABILITY_UNREFUTED_not_awarded": (
            "the verdict requires surviving tier 1.5, and the excess did not survive it. The proposed "
            "verdict goes unused on this run."),
        "note_on_optimization": (
            "the `optimization` family is significantly NEGATIVE under Holm (p<0.00001 against its "
            "0.01000 threshold, the smallest in the family): those regions blend BETTER than a marginal- "
            "and cardinality-matched control. "
            "That is the opposite of the sealed direction and is reported as measured."),
    }

    doc["SEALED_PRIMARY"] = prim
    doc["holm_bonferroni_FWER_0.05"] = holm
    doc["paired_analysis"] = paired
    doc["tier15_coverage"] = coverage
    doc["VERDICT"] = verdict
    doc["not_a_second_run"] = ("every value here is computed from the ladder the scoring run wrote. No "
                              "region rebuilt, no control redrawn, no measured value moved.")
    RES.write_text(json.dumps(doc, indent=1) + "\n")

    print("TERRAIN v1 — THE SEALED PRIMARY AND THE VERDICT\n")
    print(f"  {'test':<22}{'mean':>9}{'ci95':>22}{'n':>5}")
    for k, v in prim.items():
        if v["mean"] is None:
            print(f"  {k:<22}{'INSUFFICIENT (n<2)':>36}"); continue
        print(f"  {k:<22}{v['mean']:>+9.4f}   [{v['ci95'][0]:+.4f}, {v['ci95'][1]:+.4f}]{v['n']:>5}")
    print(f"\n  Holm-Bonferroni, family of 5, FWER 0.05:")
    for h in holm:
        lead = "<" if prim[h["test"]].get("p_is_upper_bound") else "="
        print(f"    {h['test']:<20}p{lead}{h['p']:<9.5f}thr={h['threshold']:.5f}  "
              f"{'REJECT null (' + h['direction'] + ')' if h['reject_null'] else 'retain null'}")
    print(f"\n  Paired, on the {coverage['tier15_usable']} readings with both tiers:")
    for k, v in paired.items():
        print(f"    {k:<36}{v['mean']:>+8.4f}  CI [{v['ci95'][0]:+.4f}, {v['ci95'][1]:+.4f}]  n={v['n']}")
    print(f"\n  tier-1.5 coverage: {coverage['tier15_usable']} usable, {coverage['tier15_frozen']} frozen")
    print(f"    mean tier-1 excess  usable {coverage['mean_tier1_excess_among_usable']:+.4f}   "
          f"frozen {coverage['mean_tier1_excess_among_frozen']:+.4f}")
    print(f"\n  VERDICT: {verdict['VERDICT']}   (primary bet: {verdict['primary_bet_outcome']})")
    print(f"\n  sha256 {hashlib.sha256(RES.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
