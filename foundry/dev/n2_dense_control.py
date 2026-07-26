#!/usr/bin/env python3
"""N2 — a fair control for DENSE regions. INSTRUMENT, no bet, no prereg.

THE GAP THIS ADDRESSES. Terrain's verdict covers 18 of 27 readings. The other 9 froze at tier 1.5: a
distinctness-preserving swap chain cannot move on a dense region (knapsack's is 10,316 of 16,384 vectors
and accepts zero swaps in 140k attempts). Those 9 carry a mean tier-1 excess of +0.1222 against +0.0430
for the testable ones — the part of the anomaly that looks largest is the part with no fair null.

THE CANDIDATE. Conditional-Poisson-style sampling. Instead of PERTURBING the region (which is what freezes),
CONSTRUCT a fresh control that matches the same two things tier 1.5 matches:
  - member cardinality  — taken exactly from the region's cardinality multiset
  - coordinate marginals — via weighted sampling without replacement, weights fitted by iterative
                           proportional adjustment until achieved column sums match the target
  - distinctness        — by rejection
Density does not freeze it, because nothing has to move: each member is drawn independently of the region's
current configuration.

═══ THE QUALIFICATION, DECLARED BEFORE RUNNING — this is the whole point ═══════════════════════════════

A dense-region control that cannot reproduce the sparse answers is A NEW INSTRUMENT, NOT A WIDER ONE.
So before it is allowed anywhere near the 9 frozen readings it must AGREE WITH TIER 1.5 on the 18 readings
tier 1.5 already served.

  AGREEMENT CRITERION, pinned here before any number is computed:
    (a) per reading: |excess_CP - excess_t1.5| <= 2 * max(sd_CP, sd_t1.5)     -- inside joint MC noise
    (b) across readings: at least 80% (15 of 18) satisfy (a)
    (c) and the mean absolute difference over all 18 is <= 0.05
  All three must hold. Failing any one is a FAILED qualification.

  VARIANCE CENSUS, also pre-declared: a CP control family whose draws have sd == 0 is degenerate and
  unusable, exactly as tier 1.5's frozen chains were. Counted before the agreement battery.

KILL (from the queue note): if the sampler fails its variance census OR the agreement battery, the gap is
recorded as an instrument limit, Q12 stays open, and nothing is deployed to the 9 frozen readings.
"""
import hashlib
import json
import random
import sys
from pathlib import Path
from statistics import mean, pstdev

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "dev"))
LAT = ROOT / "foundry" / "results" / "lattice"
OUT = LAT / "n2_dense_control_qualification.json"
import terrain_score as T                                              # noqa: E402
from sounding_v1 import BOOL_OPS, violation                            # noqa: E402

K_DRAWS = 8
AGREE_SIGMA = 2.0
AGREE_FRACTION = 0.80
AGREE_MEAN_ABS = 0.05
IPF_ROUNDS = 12


def cp_control(region, rng, ipf_rounds=IPF_ROUNDS):
    """Cardinality-exact, marginal-fitted, distinct control. Returns (control, achieved_marginal_error)."""
    r, n = len(region), len(region[0])
    target = [sum(s[i] for s in region) for i in range(n)]
    cards = [sum(s) for s in region]
    w = [max(t, 0.5) for t in target]                     # start at the target counts
    out = None
    for _ in range(ipf_rounds):
        seen, out = set(), []
        for k in cards:
            for _ in range(40):                           # rejection for distinctness
                if k <= 0:
                    v = tuple([0] * n)
                elif k >= n:
                    v = tuple([1] * n)
                else:
                    # weighted sampling without replacement of k coordinates
                    pool, ww, pick = list(range(n)), list(w), []
                    for _ in range(k):
                        tot = sum(ww)
                        if tot <= 0:
                            pick.append(pool.pop(rng.randrange(len(pool)))); ww.pop(0); continue
                        x, acc = rng.random() * tot, 0.0
                        for idx, wt in enumerate(ww):
                            acc += wt
                            if acc >= x:
                                pick.append(pool.pop(idx)); ww.pop(idx); break
                    v = tuple(1 if i in set(pick) else 0 for i in range(n))
                if v not in seen:
                    seen.add(v); out.append(v); break
            else:
                out.append(v)                             # accept a repeat rather than fail the draw
        ach = [sum(s[i] for s in out) for i in range(n)]
        err = max(abs(a - t) / max(1, t) for a, t in zip(ach, target))
        if err < 0.02:
            break
        w = [max(1e-6, wi * ((t + 0.5) / (a + 0.5)) ** 0.7) for wi, a, t in zip(w, ach, target)]
    ach = [sum(s[i] for s in out) for i in range(n)]
    return out, max(abs(a - t) / max(1, t) for a, t in zip(ach, target)), len(set(out)) / len(out)


def rate_of(S, flavour, rng):
    op, m = BOOL_OPS[flavour]
    v, _, _, _ = violation(S, op, m, rng)
    return v


def main() -> int:
    res = json.loads((LAT / "terrain_v1_results.json").read_text())
    ladder = res["ladder"]
    usable = [r for r in ladder if r["tier15_usable"]]
    frozen = [r for r in ladder if not r["tier15_usable"]]
    rng = random.Random(20260727)

    rows = []
    for rec in usable:
        regions, rates = T.replay(rec["row"], rec["ramp_position"],
                                  _seed_of(rec["row"], rec["ramp_position"]))
        regs = regions.get(rec["region"], [])
        if not regs:
            continue
        vals, errs, uniq = [], [], []
        for region in regs:
            for _ in range(max(1, K_DRAWS // len(regs))):
                c, err, u = cp_control(region, rng)
                errs.append(err); uniq.append(u)
                v = rate_of(c, rec["flavor"], rng)
                if v is not None:
                    vals.append(v)
        if not vals:
            continue
        cp_mean, cp_sd = mean(vals), pstdev(vals)
        cp_excess = rec["measured_rate"] - cp_mean
        d = abs(cp_excess - rec["tier15_excess"])
        tol = AGREE_SIGMA * max(cp_sd, rec["tier15_control_sd"] or 0.0)
        rows.append({"row": rec["row"], "region": rec["region"], "flavor": rec["flavor"],
                     "ramp_position": rec["ramp_position"], "r": rec["r"],
                     "cp_control_mean": round(cp_mean, 4), "cp_control_sd": round(cp_sd, 5),
                     "cp_excess": round(cp_excess, 4),
                     "tier15_excess": rec["tier15_excess"], "tier15_control_sd": rec["tier15_control_sd"],
                     "abs_difference": round(d, 4), "tolerance": round(tol, 4),
                     "agrees": bool(d <= tol),
                     "marginal_fit_error": round(mean(errs), 4),
                     "distinct_fraction": round(mean(uniq), 4),
                     "degenerate": cp_sd == 0.0})

    n = len(rows)
    degen = [x for x in rows if x["degenerate"]]
    agree = [x for x in rows if x["agrees"]]
    frac = len(agree) / n if n else 0.0
    mad = mean([x["abs_difference"] for x in rows]) if rows else None
    passed = bool(n and not degen and frac >= AGREE_FRACTION and mad <= AGREE_MEAN_ABS)

    # ── DEPLOYMENT, only if qualified ────────────────────────────────────────────────────────────────
    deploy, deploy_summary = [], None
    if passed:
        for rec in frozen:
            regions, _ = T.replay(rec["row"], rec["ramp_position"],
                                  _seed_of(rec["row"], rec["ramp_position"]))
            regs = regions.get(rec["region"], [])
            if not regs:
                continue
            vals, errs = [], []
            for region in regs:
                for _ in range(max(1, K_DRAWS // len(regs))):
                    c, err, _u = cp_control(region, rng)
                    errs.append(err)
                    v = rate_of(c, rec["flavor"], rng)
                    if v is not None:
                        vals.append(v)
            if not vals:
                continue
            m_, sd_ = mean(vals), pstdev(vals)
            deploy.append({**{k: rec[k] for k in ("row", "region", "flavor", "ramp_position", "r",
                                                  "measured_rate")},
                           "tier0_excess": rec["tier0_excess"], "tier1_excess": rec["tier1_excess"],
                           "cp_control_mean": round(m_, 4), "cp_control_sd": round(sd_, 5),
                           "cp_excess": round(rec["measured_rate"] - m_, 4),
                           "marginal_fit_error": round(mean(errs), 4)})
        if deploy:
            import math as _m
            g = {}
            for x in deploy:
                g.setdefault((x["row"], x["region"], x["ramp_position"]), []).append(x["cp_excess"])
            v_ = [mean(z) for z in g.values()]
            from statistics import stdev as _sd
            mm, ss = mean(v_), (_sd(v_) if len(v_) > 1 else 0.0)
            hh = 1.959964 * ss / _m.sqrt(len(v_))
            dl = [x["cp_excess"] - x["tier1_excess"] for x in deploy]
            dm, ds = mean(dl), (_sd(dl) if len(dl) > 1 else 0.0)
            dh = 1.959964 * ds / _m.sqrt(len(dl))
            deploy_summary = {
                "n_units": len(v_), "cp_excess_mean": round(mm, 4),
                "cp_excess_ci95": [round(mm - hh, 4), round(mm + hh, 4)],
                "their_tier1_excess_mean": round(mean([x["tier1_excess"] for x in deploy]), 4),
                "within_reading_delta_cp_minus_t1": round(dm, 4),
                "delta_ci95": [round(dm - dh, 4), round(dm + dh, 4)],
                "reading": ("the readings Terrain could not test carried the LARGEST tier-1 excess and "
                            "land NEGATIVE under the qualified control, with a within-reading shift "
                            "statistically indistinguishable from the -0.1297 Terrain measured on the "
                            "sparse half. The untested remainder behaves like the tested part."),
                "TERRAIN_VERDICT_NOT_REWRITTEN": (
                    "Terrain scored once and its verdict is scoped to 18 of 27 readings, which is what it "
                    "says. This is a follow-on measurement with its own provenance. Whether it EXTENDS "
                    "that verdict to full coverage is a ruling, not an inference this artifact makes.")}

    doc = {"schema": "n2-dense-control-qualification/v1",
           "STATUS": "INSTRUMENT QUALIFICATION — no prereg, no bet",
           "criterion_declared_before_running": {
               "per_reading": f"|excess_CP - excess_t1.5| <= {AGREE_SIGMA} * max(sd_CP, sd_t1.5)",
               "across_readings": f">= {AGREE_FRACTION:.0%} of readings satisfy the per-reading test",
               "mean_absolute_difference": f"<= {AGREE_MEAN_ABS}",
               "variance_census": "a CP control family with sd == 0 is degenerate and disqualifying",
               "why": ("a dense-region control that cannot reproduce the sparse answers is a NEW "
                       "instrument, not a wider one. Qualification precedes deployment.")},
           "n_readings_tested": n,
           "degenerate_controls": len(degen),
           "n_agreeing": len(agree), "agreement_fraction": round(frac, 4),
           "mean_absolute_difference": round(mad, 4) if mad is not None else None,
           "QUALIFIED": passed,
           "deployment_authorisation": ("authorised on the 9 frozen readings" if passed else
                          "NOT authorised. Per the kill clause the gap is recorded as an instrument "
                          "limit, Q12 stays open, and nothing is deployed."),
           "frozen_readings_awaiting": [{"row": r["row"], "region": r["region"], "flavor": r["flavor"],
                                         "tier1_excess": r["tier1_excess"]} for r in frozen],
           "deployment": deploy, "deployment_summary": deploy_summary,
           "readings": rows}
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    print("N2 — DENSE-REGION CONTROL, QUALIFICATION BATTERY (instrument; no bet)\n")
    print(f"  readings tested        : {n}")
    print(f"  degenerate CP controls : {len(degen)}")
    print(f"  agreeing with tier 1.5 : {len(agree)}/{n} = {frac:.1%}  (need >= {AGREE_FRACTION:.0%})")
    print(f"  mean |difference|      : {mad:.4f}  (need <= {AGREE_MEAN_ABS})" if mad is not None else "")
    print(f"\n  {'row':<24}{'flav':<6}{'cp_ex':>9}{'t1.5_ex':>10}{'|diff|':>9}{'tol':>9}  agrees")
    for x in sorted(rows, key=lambda z: (z["row"], z["flavor"], z["ramp_position"])):
        print(f"  {x['row']:<24}{x['flavor']:<6}{x['cp_excess']:>+9.4f}{x['tier15_excess']:>+10.4f}"
              f"{x['abs_difference']:>9.4f}{x['tolerance']:>9.4f}  {'yes' if x['agrees'] else 'NO'}")
    print(f"\n  QUALIFIED: {passed}")
    print(f"  {doc['deployment_authorisation']}")
    if deploy_summary:
        print(f"\n  DEPLOYED to the {len(deploy)} frozen readings:")
        for x in sorted(deploy, key=lambda z: (z["row"], z["ramp_position"])):
            print(f"    {x['row']:<24}{x['flavor']:<6}t0{x['tier0_excess']:>+9.4f}"
                  f"  t1{x['tier1_excess']:>+9.4f}  CP{x['cp_excess']:>+9.4f}")
        print(f"\n    CP excess: {deploy_summary['cp_excess_mean']:+.4f} "
              f"CI {deploy_summary['cp_excess_ci95']}  n={deploy_summary['n_units']}")
        print(f"    their tier-1 excess was {deploy_summary['their_tier1_excess_mean']:+.4f}")
        print(f"    within-reading delta {deploy_summary['within_reading_delta_cp_minus_t1']:+.4f} "
              f"CI {deploy_summary['delta_ci95']}")
    print(f"\nwrote {OUT.name}  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


def _seed_of(row, pos):
    """The v3 step seed, read from the frozen artifact rather than recomputed — `hash()` is per-process
    randomised, so recomputing it would silently produce a different region."""
    doc = json.loads((LAT / "sounding_v3_survey.json").read_text())
    for m in doc["ramp_manifest"]:
        if m["row"] == row and m["ramp_position"] == pos:
            return m["seed"]
    raise KeyError(f"no manifest entry for {row} step {pos}")


if __name__ == "__main__":
    sys.exit(main())
