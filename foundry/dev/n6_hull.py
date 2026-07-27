#!/usr/bin/env python3
"""N6-I0 — the closure hull, its known-answer battery, and the census. NO SEAL, NO BET.

THE QUANTITY. Per (region, flavour): the CLOSURE HULL — iterate the blend operation on R to fixpoint — and
    infl  = |hull(R)| / |R|          how far the region sits from its own closure
    depth = rounds to fixpoint       whether an escape TERMINATES or cascades
A fully-closed region has infl = 1.0 and depth = 0 by theorem. The bet N6 will make is that protection is
proximity to closure; this file builds the predictor and censuses it before any text fixes.

EXACT ONLY, AND THE REASON IS NOT FASTIDIOUSNESS. A sampled hull is a LOWER BOUND, and it is biased
downward exactly where regions are large — which reintroduces the region-size confound this program has
fought since round 2, at the mechanism layer where it would be hardest to see. So a region that cannot be
closed exhaustively inside the declared budget records `UNBOUNDED-at-cap` or `TOO-LARGE` and LEAVES. That
costs about 35% of the population and is worth it.

THE INSTANCE-JOIN TRAP, closed before it opens. The survey's `measured_rate` and `r` are MEANS over a
step's instances, and instance sizes vary sharply — one `independent-set · optimal` step has instances of
sizes [4, 1, 16] against a ladder `r` of 10. A hull computed on ONE instance would pair a one-instance
predictor with a multi-instance outcome. So hulls are computed PER INSTANCE and aggregated the same way the
rate was, and the aggregation is ASSERTED against the frozen rate rather than assumed.

THE KNOWN-ANSWER BATTERY, which gates everything below. N4 verified 15 structural properties across 12
(row, region) pairs by brute force. Each implies an exact hull answer:
    upward_closed      -> infl == 1.0 under max          (closed)
    downward_closed    -> infl == 1.0 under min
    pairwise_exclusion -> infl == 1.0 under majority
    parity             -> infl == 1.0 under minority
    fixed_cardinality  -> infl  >  1.0 under min AND max  (saturated — the other direction)
    exact_equality     -> infl  >  1.0 under min AND max
**If the hull machinery cannot reproduce every one of these, it is not computing closure**, and this script
refuses to write a census. Both directions are checked, because a hull routine that returned 1.0 for
everything would pass a closed-only battery.
"""
import hashlib
import json
import random
import sys
import time
from itertools import combinations
from pathlib import Path
from statistics import mean, pstdev

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "dev"))
LAT = ROOT / "foundry" / "results" / "lattice"
OUT = LAT / "n6_hull_census.json"
import terrain_score as T                                              # noqa: E402
import sounding_v3_survey as S3                                        # noqa: E402
import sounding_v2 as S2                                               # noqa: E402
import sounding_survey as SV                                           # noqa: E402
from sounding_v1 import BOOL_OPS                                       # noqa: E402

ROUND_BUDGET = 4_000_000        # max tuples enumerated in one closure round — declared, not discovered
MEMBER_CAP = 100_000            # a hull exceeding this records UNBOUNDED-at-cap: a value class
MAX_ROUNDS = 20


def hull_profile(R, op, m):
    """EXACT closure by iteration. Returns (size, per_round_additions, status).

    status: 'exact' | 'TOO-LARGE' (a round would exceed the enumeration budget)
            | 'UNBOUNDED-at-cap' (the hull outgrew the member cap)
    No sampling path exists here on purpose — a sampled hull is a different quantity.
    """
    cur = set(R)
    rounds = []
    for _ in range(MAX_ROUNDS):
        cl = list(cur)
        n = len(cl)
        # exact enumeration cost for this round
        tot = 1
        for i in range(m):
            tot = tot * (n - i) // (i + 1)
        if tot > ROUND_BUDGET:
            return len(cur), rounds, "TOO-LARGE"
        new = set()
        for t in combinations(cl, m):
            v = op(t)
            if v not in cur:
                new.add(v)
        if not new:
            return len(cur), rounds, "exact"
        cur |= new
        rounds.append(len(new))
        if len(cur) > MEMBER_CAP:
            return len(cur), rounds, "UNBOUNDED-at-cap"
    return len(cur), rounds, "UNBOUNDED-at-cap"


# ── the known-answer battery ────────────────────────────────────────────────────────────────────────
PROPERTY_EXPECTS = {
    "upward_closed":     [("max", "closed")],
    "downward_closed":   [("min", "closed")],
    "pairwise_exclusion": [("majority", "closed")],
    "parity":            [("minority", "closed")],
    "fixed_cardinality": [("min", "saturated"), ("max", "saturated")],
    "exact_equality":    [("min", "saturated"), ("max", "saturated")],
}


def battery(rng):
    """Every N4-verified property must yield its exact hull answer. Both directions."""
    n4 = json.loads((LAT / "n4_property_forcedness.json").read_text())
    BUILD = {"set-cover": lambda: S3.set_cover(rng, 9), "hitting-set": lambda: S3.hitting_set(rng, 7),
             "feedback-vertex-set": lambda: S3.fvs(rng, 0.30),
             "odd-cycle-transversal": lambda: S3.oct_(rng, 0.30),
             "dominating-set": lambda: S3.gsub(rng, 0.25, "dom"),
             "knapsack": lambda: S3.knapsack(rng, 0.25),
             "independent-set": lambda: S2.regions_for("independent-set", rng),
             "matching": lambda: S2.regions_for("matching", rng),
             "three-dimensional-matching": lambda: SV.extra_regions("three-dimensional-matching", rng),
             "max-flow": lambda: S2.regions_for("max-flow", rng),
             "subset-sum": lambda: S3.subsum(rng, 20),
             "min-spanning-tree": lambda: S2.regions_for("min-spanning-tree", rng)}
    checks, failures = [], []
    for e in n4["entries"]:
        row, kind = e["row"], e["region"]
        for v in e["verified"]:
            prop = v["property"]
            for flavour, expect in PROPERTY_EXPECTS.get(prop, []):
                got = None
                for _ in range(4):
                    d = dict(BUILD[row]() or [])
                    reg = d.get(kind)
                    if reg and 4 <= len(reg) <= 900:
                        op, m = BOOL_OPS[flavour]
                        size, rds, st = hull_profile(reg, op, m)
                        if st != "exact":
                            continue
                        got = size / len(reg)
                        break
                if got is None:
                    checks.append({"row": row, "region": kind, "property": prop, "flavour": flavour,
                                   "expect": expect, "result": "NOT-TESTABLE (no exact region built)"})
                    continue
                ok = (abs(got - 1.0) < 1e-12) if expect == "closed" else (got > 1.0 + 1e-12)
                checks.append({"row": row, "region": kind, "property": prop, "flavour": flavour,
                               "expect": expect, "infl": round(got, 4), "pass": ok})
                if not ok:
                    failures.append(f"{row}·{kind}·{flavour}: {prop} expects {expect}, infl={got:.4f}")
    return checks, failures


def main() -> int:
    rng = random.Random(20260726)
    t0 = time.time()

    checks, failures = battery(rng)
    npass = sum(1 for c in checks if c.get("pass"))
    ntest = sum(1 for c in checks if "pass" in c)
    print("N6-I0 — KNOWN-ANSWER BATTERY (the hull must reproduce N4's verified properties)\n")
    for c in checks:
        mark = "ok " if c.get("pass") else ("--" if "pass" not in c else "FAIL")
        print(f"  {mark} {c['row']:<26}{c['region']:<10}{c['flavour']:<9}{c['property']:<19}"
              f"expect {c['expect']:<10}infl={c.get('infl', c.get('result'))}")
    print(f"\n  {npass}/{ntest} passed")
    if failures:
        print("\nFAIL — the hull machinery does not reproduce N4's verified closure. It is not computing\n"
              "closure, and no census may be written on it:", file=sys.stderr)
        for f in failures:
            print(f"    {f}", file=sys.stderr)
        return 1
    if ntest < 12:
        print(f"\nFAIL — only {ntest} battery checks were testable; a battery this thin certifies nothing.",
              file=sys.stderr)
        return 1

    # ── the census, over the N1-scored population, per instance ─────────────────────────────────────
    L = json.loads((LAT / "n1_results.json").read_text())["ladder"]
    v3 = json.loads((LAT / "sounding_v3_survey.json").read_text())
    seeds = {(m["row"], m["ramp_position"]): m["seed"] for m in v3["ramp_manifest"]}
    steps, rows, excluded, join_fail = {}, [], [], []
    for rec in L:
        key = (rec["row"], rec["ramp_position"])
        if key not in seeds:
            excluded.append({**{k: rec[k] for k in ("row", "region", "flavor")},
                             "why": "no manifest seed"}); continue
        if key not in steps:
            steps[key] = T.replay(rec["row"], rec["ramp_position"], seeds[key])
        regions, rates = steps[key]
        # THE INSTANCE-JOIN GUARD: the predictor must describe the same object as the outcome.
        got = rates.get((rec["region"], rec["flavor"]))
        if got is None or abs(got - rec["measured_rate"]) > 5e-4:
            join_fail.append({**{k: rec[k] for k in ("row", "region", "flavor")},
                              "replay_rate": got, "frozen_rate": rec["measured_rate"]})
            continue
        regs = regions.get(rec["region"], [])
        if not regs:
            excluded.append({**{k: rec[k] for k in ("row", "region", "flavor")},
                             "why": "no region on replay"}); continue
        op, m = BOOL_OPS[rec["flavor"]]
        per = []
        for reg in regs:
            size, rds, st = hull_profile(reg, op, m)
            per.append({"r": len(reg), "hull": size, "infl": size / len(reg),
                        "depth": len(rds), "rounds": rds, "status": st})
        bad = [p for p in per if p["status"] != "exact"]
        if bad:
            excluded.append({**{k: rec[k] for k in ("row", "region", "flavor")},
                             "r": rec["r"], "why": bad[0]["status"],
                             "instance_sizes": [p["r"] for p in per]})
            continue
        rows.append({"row": rec["row"], "family": rec["family"], "region": rec["region"],
                     "flavor": rec["flavor"], "ramp_position": rec["ramp_position"],
                     "r_ladder": rec["r"], "measured_rate": rec["measured_rate"],
                     "fair_null_excess": rec["fair_null_excess"],
                     "n_instances": len(per),
                     "infl": round(mean(p["infl"] for p in per), 5),
                     "depth": round(mean(p["depth"] for p in per), 4),
                     "hull_mean": round(mean(p["hull"] for p in per), 2),
                     "per_instance": per})

    if join_fail:
        print(f"\nFAIL — {len(join_fail)} readings whose replay did not reproduce the frozen rate. The "
              f"predictor would describe a different object than the outcome:", file=sys.stderr)
        for j in join_fail[:8]:
            print(f"    {j}", file=sys.stderr)
        return 1

    # ── the census kill: is the predictor degenerate? ───────────────────────────────────────────────
    by_fl = {}
    for x in rows:
        by_fl.setdefault(x["flavor"], []).append(x)
    census = {}
    for fl, xs in sorted(by_fl.items()):
        i = [x["infl"] for x in xs]
        d = [x["depth"] for x in xs]
        census[fl] = {"n": len(xs), "infl_min": round(min(i), 4), "infl_max": round(max(i), 4),
                      "infl_median": round(sorted(i)[len(i) // 2], 4), "infl_sd": round(pstdev(i), 4),
                      "n_exactly_closed": sum(1 for v in i if abs(v - 1.0) < 1e-12),
                      "depth_min": min(d), "depth_max": max(d),
                      "depth_median": round(sorted(d)[len(d) // 2], 3)}
    alli = [x["infl"] for x in rows]
    degenerate = (pstdev(alli) < 0.05) or (len({round(v, 2) for v in alli}) < 5)
    kill = ("CENSUS KILL FIRES — the predictor is degenerate on the scored population"
            if degenerate else "census passes — the predictor varies")

    doc = {"schema": "n6-hull-census/v1",
           "STATUS": "I-PHASE — no prereg, no bet, no scored prediction",
           "quantity": {"infl": "|hull(R)| / |R|", "depth": "rounds to fixpoint"},
           "exact_only": ("a sampled hull is a LOWER BOUND biased downward exactly where regions are "
                          "large, which reintroduces the region-size confound at the mechanism layer. "
                          "Regions that cannot close exhaustively inside the budget LEAVE."),
           "budget": {"round_enumeration": ROUND_BUDGET, "member_cap": MEMBER_CAP,
                      "max_rounds": MAX_ROUNDS},
           "known_answer_battery": {"tested": ntest, "passed": npass, "checks": checks,
                                    "note": ("both directions — closed properties must return infl==1.0 "
                                             "and saturating properties must return infl>1.0, so a "
                                             "routine returning 1.0 for everything cannot pass.")},
           "instance_join_guard": ("hulls computed PER INSTANCE and averaged as the survey averaged rates; "
                                   "every reading's replay asserted against its frozen measured_rate to "
                                   "5e-4 before its hull was accepted."),
           "population": {"n1_scored": len(L), "censused": len(rows), "excluded": len(excluded),
                          "coverage": round(len(rows) / len(L), 4)},
           "excluded": excluded,
           "census_by_flavour": census,
           "CENSUS_KILL": kill, "degenerate": degenerate,
           "readings": rows}
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    print(f"\nN6-I0 — THE CENSUS\n")
    print(f"  N1 scored population : {len(L)}")
    print(f"  censused (exact hull): {len(rows)}   ({len(rows)/len(L):.1%})")
    print(f"  excluded             : {len(excluded)}")
    ex = {}
    for e in excluded:
        ex[e["why"]] = ex.get(e["why"], 0) + 1
    for k, v in sorted(ex.items()):
        print(f"    {k:<22}{v}")
    print(f"\n  {'flavour':<10}{'n':>5}{'infl med':>10}{'infl max':>10}{'infl sd':>9}"
          f"{'closed':>8}{'depth med':>11}{'depth max':>10}")
    for fl, c in census.items():
        print(f"  {fl:<10}{c['n']:>5}{c['infl_median']:>10.3f}{c['infl_max']:>10.2f}"
              f"{c['infl_sd']:>9.3f}{c['n_exactly_closed']:>8}{c['depth_median']:>11.2f}"
              f"{c['depth_max']:>10}")
    print(f"\n  {kill}")
    print(f"\n  elapsed {time.time()-t0:.0f}s")
    print(f"wrote {OUT.name}  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
