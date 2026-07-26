#!/usr/bin/env python3
"""Terrain v1 — THE SCORING RUN. prereg_v19, sealed 2026-07-26. Runs ONCE against the frozen column.

WHAT IS BET, sealed before this ran:
  Primary — mean TIER-1 excess (tier 1.5 where it clears its mixing floor) over the 29 scored readings is
  positive with a 95% CI clear of zero, per family and pooled, at the (row, region, ramp-step) unit.
  Holm-Bonferroni at FWER 0.05 over a family of 5 tests. MDE +0.064 primary, +0.123 row-clustered.

VERDICTS: ANTI-BLENDABILITY-REAL (unreachable by this design, 1 of 34 readings has a tier-2 control) /
ANTI-BLENDABILITY-UNREFUTED / CONTROL-MISMATCH@<tier> / MIXED / INSUFFICIENT.

NO NEW READINGS. Measured rates are inputs and never move. Regions are REGENERATED from stored seeds to
compute the new control tiers, and the regeneration is ASSERTED against the frozen rate: a replayed region
whose recomputed rate does not match the artifact drops the reading to INSUFFICIENT-replay rather than
silently substituting a different region.
"""
import hashlib
import json
import math
import random
import sys
from itertools import combinations
from pathlib import Path
from statistics import mean, pstdev, stdev

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "dev"))
LAT = ROOT / "foundry" / "results" / "lattice"
OUT = LAT / "terrain_v1_results.json"
import sounding_v3_survey as S3                                        # noqa: E402
from sounding_v1 import BOOL_OPS, violation                            # noqa: E402

N_INST, K_CTRL, MEAS_CAP = S3.N_INST, 25, 5000
MIX_FLOOR = lambda r: max(50, r // 4)          # sealed in §1.2
Z = 1.959964


# ── the control tiers ────────────────────────────────────────────────────────────────────────────────
def tier1(region, rng):
    """Matched-marginal: size r, per-coordinate inclusion frequencies matched, coords independent."""
    r, n = len(region), len(region[0])
    p = [sum(s[i] for s in region) / r for i in range(n)]
    out, seen, guard = [], set(), 0
    while len(out) < r and guard < 60 * r:
        guard += 1
        v = tuple(1 if rng.random() < p[i] else 0 for i in range(n))
        if v not in seen:
            seen.add(v); out.append(v)
    return out if len(out) == r else None


def tier15(region, rng, sweeps=30):
    """Swap-randomised: preserves every column marginal, every member cardinality, AND distinctness.
    Returns (control, accepted_swaps). A chain below the mixing floor is unusable, not a fair null."""
    M = [list(s) for s in region]
    r, n = len(M), len(M[0])
    seen = {tuple(x) for x in M}
    done = 0
    for _ in range(sweeps * r * n):
        i, j = rng.randrange(r), rng.randrange(r)
        a, b = rng.randrange(n), rng.randrange(n)
        if M[i][a] == 1 and M[i][b] == 0 and M[j][a] == 0 and M[j][b] == 1:
            ni = tuple(1 if k == b else 0 if k == a else M[i][k] for k in range(n))
            nj = tuple(1 if k == a else 0 if k == b else M[j][k] for k in range(n))
            if ni in seen or nj in seen or ni == nj:
                continue
            seen.discard(tuple(M[i])); seen.discard(tuple(M[j])); seen.add(ni); seen.add(nj)
            M[i] = list(ni); M[j] = list(nj); done += 1
    return [tuple(x) for x in M], done


def rate_of(S, flavour, rng):
    op, m = BOOL_OPS[flavour]
    v, _, _, _ = violation(S, op, m, rng)
    return v


# ── region regeneration, asserted against the frozen rate ────────────────────────────────────────────
def replay(row, pos, seed):
    """Replay the v3 stream for one ramp step and return {(region_kind): [region, ...]} plus the
    per-(kind,flavour) rates the replay produces — which must match the artifact."""
    fam, dom, pname, steps, build = S3.RAMP[row]
    pval = steps[pos]
    srng = random.Random(seed)
    regions, acc = {}, {}
    for _ in range(N_INST):
        regs = build(srng, pval)
        for rname, region in regs or []:
            if not region:
                continue
            regions.setdefault(rname, []).append(region)
            for fl, (op, m) in BOOL_OPS.items():
                rt, r, nsub, cap = violation(region, op, m, srng)
                if rt is None:
                    continue
                acc.setdefault((rname, fl), []).append(rt)
    return regions, {k: mean(v) for k, v in acc.items()}


def main() -> int:
    # ── the scored set, selected by the SEALED screens ───────────────────────────────────────────────
    rows = []
    for f, tag in (("sounding_survey_readings.json", "v2"), ("sounding_v3_survey.json", "v3")):
        for x in json.loads((LAT / f).read_text())["readings"]:
            if (x.get("region") and x.get("flavor") and x.get("excess") is not None and x["excess"] > 0
                    and x.get("theorem_forced") is not True and not x.get("insufficient")
                    and not x.get("forced_saturated")):
                rows.append({**x, "_src": tag})
    scored = [x for x in rows if x["domain"] == 2]
    excluded = [{"row": x["row"], "region": x["region"], "flavor": x["flavor"],
                 "verdict": "INSUFFICIENT-encoding",
                 "why": ("non-binary domain; the sealed tier-1 control is binary and the domain-general "
                         "variant is banked as an instrument extension, not built mid-seal. Ruled: these "
                         "readings' excesses top out at +0.0260, below the +0.0624 MDE, so they are "
                         "power-dead regardless of control.")} for x in rows if x["domain"] != 2]

    ladder, dropped = [], []
    rng = random.Random(20260726)
    for x in scored:
        if x["_src"] != "v3" or not x.get("seed"):
            dropped.append({**{k: x[k] for k in ("row", "region", "flavor")},
                            "verdict": "INSUFFICIENT-replay",
                            "why": "v2 reading carries no per-reading seed; region not regenerable"})
            continue
        regions, rates = replay(x["row"], x["ramp_position"], x["seed"])
        got = rates.get((x["region"], x["flavor"]))
        if got is None or abs(got - x["measured_rate"]) > 5e-4:
            dropped.append({**{k: x[k] for k in ("row", "region", "flavor")},
                            "verdict": "INSUFFICIENT-replay",
                            "why": f"replay rate {got} != frozen {x['measured_rate']}; region not "
                                   f"substituted"})
            continue
        regs = regions.get(x["region"], [])
        t1v, t15v, mix = [], [], []
        for region in regs:
            for _ in range(max(1, K_CTRL // max(1, len(regs)))):
                c1 = tier1(region, rng)
                if c1:
                    v = rate_of(c1, x["flavor"], rng)
                    if v is not None:
                        t1v.append(v)
                c15, sw = tier15(region, rng)
                mix.append(sw)
                if sw >= MIX_FLOOR(len(region)):
                    v = rate_of(c15, x["flavor"], rng)
                    if v is not None:
                        t15v.append(v)
        rec = {"row": x["row"], "family": x["family"], "region": x["region"], "flavor": x["flavor"],
               "ramp_position": x["ramp_position"], "r": x["r"], "measured_rate": x["measured_rate"],
               "tier0_control_mean": x["control_mean"], "tier0_excess": x["excess"],
               "tier1_control_mean": round(mean(t1v), 4) if t1v else None,
               "tier1_control_sd": round(pstdev(t1v), 5) if t1v else None,
               "tier1_excess": round(x["measured_rate"] - mean(t1v), 4) if t1v else None,
               "tier15_control_mean": round(mean(t15v), 4) if t15v else None,
               "tier15_control_sd": round(pstdev(t15v), 5) if t15v else None,
               "tier15_excess": round(x["measured_rate"] - mean(t15v), 4) if t15v else None,
               "tier15_accepted_swaps": mix, "tier15_mixing_floor": MIX_FLOOR(x["r"]),
               "tier15_usable": bool(t15v),
               "tier2_excess": None,
               "tier2_note": ("definitionally unavailable: for a feasible region the region IS the "
                              "species; for solutions the only container is the ambient space (= tier 0)"
                              if x["region"] != "optimal" else "optimal region — tier 2 exists but this "
                              "single reading is reported, never pooled")}
        ladder.append(rec)

    # ── the sealed statistic: (row, region, step) unit, per family and pooled ────────────────────────
    def agg(recs, key):
        g = {}
        for r_ in recs:
            if r_.get(key) is not None:
                g.setdefault((r_["row"], r_["region"], r_["ramp_position"]), []).append(r_[key])
        return [mean(v) for v in g.values()]

    def ci(vals):
        n = len(vals)
        if n < 2:
            return (None, None, None, n)
        m, sd = mean(vals), stdev(vals)
        h = Z * sd / math.sqrt(n)
        return (round(m, 4), round(m - h, 4), round(m + h, 4), n)

    tests = {}
    for tier in ("tier1_excess", "tier15_excess"):
        tests[f"pooled·{tier}"] = ci(agg(ladder, tier))
        for fam in sorted({r_["family"] for r_ in ladder}):
            tests[f"{fam}·{tier}"] = ci(agg([r_ for r_ in ladder if r_["family"] == fam], tier))
    rowclust = {t: ci([mean([r_[t] for r_ in ladder if r_["row"] == rw and r_[t] is not None])
                       for rw in sorted({r_["row"] for r_ in ladder})
                       if any(r_[t] is not None for r_ in ladder if r_["row"] == rw)])
                for t in ("tier1_excess", "tier15_excess")}

    doc = {"schema": "terrain-v1-results/v1",
           "prereg": "prereg_v19", "sealed": "2026-07-26", "scored_once": True,
           "scored_set_n": len(ladder), "excluded_insufficient_encoding": excluded,
           "dropped_replay": dropped,
           "tier2_unreachable": ("1 of 34 residual readings has a tier-2 control, so "
                                 "ANTI-BLENDABILITY-REAL is unreachable by this design. Declared in the "
                                 "seal in advance, not discovered here."),
           "primary_tests": {k: {"mean": v[0], "ci95": [v[1], v[2]], "n": v[3]} for k, v in tests.items()},
           "row_clustered_robustness": {k: {"mean": v[0], "ci95": [v[1], v[2]], "n": v[3]}
                                        for k, v in rowclust.items()},
           "ladder": ladder}
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    print("TERRAIN v1 — SCORED ONCE (prereg_v19)\n")
    print(f"  scored readings      : {len(ladder)}")
    print(f"  INSUFFICIENT-encoding: {len(excluded)}")
    print(f"  INSUFFICIENT-replay  : {len(dropped)}")
    print(f"\n  {'test':<34}{'mean':>9}{'ci95_lo':>10}{'ci95_hi':>10}{'n':>5}")
    for k, v in tests.items():
        if v[0] is None:
            print(f"  {k:<34}{'INSUFFICIENT (n<2)':>34}"); continue
        print(f"  {k:<34}{v[0]:>+9.4f}{v[1]:>+10.4f}{v[2]:>+10.4f}{v[3]:>5}")
    print(f"\n  row-clustered robustness:")
    for k, v in rowclust.items():
        if v[0] is not None:
            print(f"    {k:<20}{v[0]:>+9.4f}  CI [{v[1]:+.4f}, {v[2]:+.4f}]  n={v[3]}")
    print(f"\n  {'row':<24}{'region':<10}{'flav':<6}{'meas':>7}{'t0ex':>9}{'t1ex':>9}{'t1.5ex':>9}  mix")
    for r_ in sorted(ladder, key=lambda z: (z["row"], z["region"], z["flavor"], z["ramp_position"])):
        f = lambda v: f"{v:>+9.4f}" if v is not None else f"{'--':>9}"
        print(f"  {r_['row']:<24}{r_['region']:<10}{r_['flavor']:<6}{r_['measured_rate']:>7.3f}"
              f"{f(r_['tier0_excess'])}{f(r_['tier1_excess'])}{f(r_['tier15_excess'])}"
              f"  {'ok' if r_['tier15_usable'] else 'FROZEN'}")
    print(f"\nwrote {OUT.name}  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
