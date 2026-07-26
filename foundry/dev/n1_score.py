#!/usr/bin/env python3
"""N1 — the protective-structure seal. prereg_v20, sealed 2026-07-26. Scores ONCE.

PRIMARY (sealed): on the scored population, mean FAIR-NULL excess remains NEGATIVE with a 95% CI clear of
zero, per family and pooled, at the (row, region, ramp-step) unit.
  Fair null per coverage: tier 1.5 where its mixing floor max(50, r/4) is cleared, CP (N2's qualified
  conditional-Poisson control) otherwise.
  LOSABLE: the primary FAILS if absorption reaches +0.1604. Measured absorptions are +0.1297 (Terrain,
  sparse) and +0.1586 (N2, dense) -- the latter within 0.0018 of flipping it.

SECONDARY (same family): the easy-hard contrast within each DECLARED region kind. Region kinds declared
before looking: feasible, solutions, optimal.

VERDICTS: PROTECTIVE-STRUCTURE-REAL / ABSORBED / MIXED-BY-REGION-KIND / INSUFFICIENT.
Holm-Bonferroni over a family of 8 at FWER 0.05.

NO NEW READINGS. Regions regenerated from stored seeds; a replay whose recomputed rate does not match the
frozen reading to 5e-4 drops that reading to INSUFFICIENT-replay rather than substituting a region.
horn-sat is EXCLUDED-drift and never enters.
"""
import hashlib
import json
import math
import random
import sys
from pathlib import Path
from statistics import mean, pstdev, stdev

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "dev"))
LAT = ROOT / "foundry" / "results" / "lattice"
OUT = LAT / "n1_results.json"
import terrain_score as T                                              # noqa: E402
import n2_dense_control as N2                                          # noqa: E402
from sounding_v1 import BOOL_OPS                                       # noqa: E402

K_DRAWS, Z = 6, 1.959964
REGION_KINDS = ("feasible", "solutions", "optimal")     # DECLARED before looking


def ci(v):
    n = len(v)
    if n < 2:
        return {"mean": None, "ci95": [None, None], "n": n, "verdict": "INSUFFICIENT (n<2)"}
    m, sd = mean(v), stdev(v)
    h = Z * sd / math.sqrt(n)
    P = 1e-5
    raw = 2 * (1 - 0.5 * (1 + math.erf(abs(m / (sd / math.sqrt(n))) / math.sqrt(2))))
    cl = raw < P
    return {"mean": round(m, 4), "ci95": [round(m - h, 4), round(m + h, 4)], "n": n,
            "p_two_sided": P if cl else round(raw, 5), "p_is_upper_bound": cl}


def agg(recs, pick):
    g = {}
    for r in recs:
        v = pick(r)
        if v is not None:
            g.setdefault((r["row"], r["region"], r["ramp_position"]), []).append(v)
    return [mean(v) for v in g.values()]


def main() -> int:
    rows = []
    for f in ("sounding_survey_readings.json", "sounding_v3_survey.json"):
        for x in json.loads((LAT / f).read_text())["readings"]:
            if (x.get("region") and x.get("flavor") and x.get("excess") is not None
                    and x.get("theorem_forced") is not True and not x.get("forced_saturated")
                    and not x.get("insufficient") and x["domain"] == 2
                    and x.get("excluded_from_studies") != "EXCLUDED-drift"
                    and x.get("seed") is not None):
                rows.append(x)
    rng = random.Random(20260729)
    ladder, dropped = [], []
    steps = {}
    for x in rows:
        key = (x["row"], x["ramp_position"])
        if key not in steps:
            steps[key] = T.replay(x["row"], x["ramp_position"], x["seed"])
        regions, rates = steps[key]
        got = rates.get((x["region"], x["flavor"]))
        if got is None or abs(got - x["measured_rate"]) > 5e-4:
            dropped.append({"row": x["row"], "region": x["region"], "flavor": x["flavor"],
                            "why": "INSUFFICIENT-replay"})
            continue
        regs = regions.get(x["region"], [])
        if not regs:
            dropped.append({"row": x["row"], "region": x["region"], "flavor": x["flavor"],
                            "why": "INSUFFICIENT-replay (no region)"})
            continue
        t15, cp, mix = [], [], []
        for region in regs:
            for _ in range(max(1, K_DRAWS // len(regs))):
                c15, sw = T.tier15(region, rng)
                mix.append(sw)
                if sw >= max(50, len(region) // 4):
                    v = T.rate_of(c15, x["flavor"], rng)
                    if v is not None:
                        t15.append(v)
                else:
                    cc, _e, _u = N2.cp_control(region, rng)
                    v = N2.rate_of(cc, x["flavor"], rng)
                    if v is not None:
                        cp.append(v)
        route = "tier1.5" if t15 else ("CP" if cp else None)
        vals = t15 or cp
        if not vals:
            dropped.append({"row": x["row"], "region": x["region"], "flavor": x["flavor"],
                            "why": "INSUFFICIENT-degenerate (neither route produced a control)"})
            continue
        ladder.append({"row": x["row"], "family": x["family"], "region": x["region"],
                       "flavor": x["flavor"], "ramp_position": x["ramp_position"], "r": x["r"],
                       "decision": x.get("decision"), "measured_rate": x["measured_rate"],
                       "tier0_excess": x["excess"], "fair_null_route": route,
                       "fair_null_mean": round(mean(vals), 4),
                       "fair_null_sd": round(pstdev(vals), 5),
                       "fair_null_excess": round(x["measured_rate"] - mean(vals), 4),
                       "accepted_swaps": mix})

    prim = {"pooled": ci(agg(ladder, lambda r: r["fair_null_excess"]))}
    for fam in sorted({r["family"] for r in ladder}):
        prim[fam] = ci(agg([r for r in ladder if r["family"] == fam],
                           lambda r: r["fair_null_excess"]))
    sec = {}
    for kind in REGION_KINDS:
        sub = [r for r in ladder if r["region"] == kind]
        e = agg([r for r in sub if r["decision"] == "P"], lambda r: r["fair_null_excess"])
        h = agg([r for r in sub if r["decision"] != "P"], lambda r: r["fair_null_excess"])
        sec[kind] = {"easy": ci(e), "hard": ci(h),
                     "contrast_easy_minus_hard": (round(mean(e) - mean(h), 4)
                                                  if len(e) >= 2 and len(h) >= 2 else None)}

    fam = [(k, v["p_two_sided"]) for k, v in prim.items() if v.get("p_two_sided") is not None]
    fam += [(f"contrast·{k}", None) for k in REGION_KINDS]
    ps = sorted([x for x in fam if x[1] is not None], key=lambda kv: kv[1])
    holm, M = [], 8
    for i, (k, p) in enumerate(ps):
        thr = 0.05 / (M - i)
        holm.append({"test": k, "p": p, "threshold": round(thr, 5), "reject_null": p < thr,
                     "direction": ("NEGATIVE" if prim[k]["mean"] < 0 else "POSITIVE") if p < thr else None})

    pooled = prim["pooled"]
    neg_clear = pooled["mean"] is not None and pooled["ci95"][1] < 0
    absorbed = pooled["mean"] is not None and pooled["ci95"][0] <= 0 <= pooled["ci95"][1]
    famneg = [k for k in prim if k != "pooled" and prim[k]["mean"] is not None and prim[k]["ci95"][1] < 0]
    verdict = ("PROTECTIVE-STRUCTURE-REAL" if neg_clear else
               "ABSORBED" if absorbed else
               "MIXED-BY-REGION-KIND" if famneg else "INSUFFICIENT")

    doc = {"schema": "n1-results/v1", "prereg": "prereg_v20", "sealed": "2026-07-26",
           "scored_once": True, "scored_set_n": len(ladder), "dropped": dropped,
           "losability_declared_before_scoring": {
               "primary_fails_if_absorption_reaches": 0.1604,
               "measured_absorptions": {"terrain_sparse": 0.1297, "n2_dense": 0.1586}},
           "PRIMARY": prim, "SECONDARY_easy_hard_contrast": sec,
           "holm_bonferroni_FWER_0.05_family_8": holm,
           "route_counts": {"tier1.5": sum(1 for r in ladder if r["fair_null_route"] == "tier1.5"),
                            "CP": sum(1 for r in ladder if r["fair_null_route"] == "CP")},
           "VERDICT": verdict,
           "ladder": ladder}
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    print("N1 — SCORED ONCE (prereg_v20)\n")
    print(f"  scored readings : {len(ladder)}   dropped: {len(dropped)}")
    print(f"  routes          : {doc['route_counts']}")
    print(f"\n  {'test':<22}{'mean':>9}{'ci95':>24}{'n':>5}")
    for k, v in prim.items():
        if v["mean"] is None:
            print(f"  {k:<22}{'INSUFFICIENT':>38}"); continue
        print(f"  {k:<22}{v['mean']:>+9.4f}   [{v['ci95'][0]:+.4f}, {v['ci95'][1]:+.4f}]{v['n']:>5}")
    print(f"\n  secondary — easy-hard contrast by declared region kind:")
    for k, v in sec.items():
        e, h = v["easy"], v["hard"]
        print(f"    {k:<11}easy {str(e['mean']):>8} (n={e['n']})   hard {str(h['mean']):>8} (n={h['n']})"
              f"   contrast {v['contrast_easy_minus_hard']}")
    print(f"\n  Holm (family 8):")
    for h in holm:
        print(f"    {h['test']:<22}p{'<' if prim.get(h['test'],{}).get('p_is_upper_bound') else '='}"
              f"{h['p']:<9.5f}thr={h['threshold']:.5f}  "
              f"{'REJECT (' + str(h['direction']) + ')' if h['reject_null'] else 'retain'}")
    print(f"\n  VERDICT: {verdict}")
    print(f"\nwrote {OUT.name}  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
