#!/usr/bin/env python3
"""N3 — the sat-2 zero. prereg_v21, sealed 2026-07-26. Scores once.

THE READING. `sat-2 · solutions · min` at ramp ratio 1.6, seed 20265280: measured violation rate EXACTLY
0.0 over 354 distinct pairs at r = 22. 2-SAT is bijunctive so `majority` is forced and the join flags it;
`min` is NOT forced, because a general 2-CNF is not Horn. The zero-hunt left it standing as one of two
GENUINE-READINGs.

THE SEALED SPLIT, declared before running:
  CHANCE-COMPOSITION  the sampled formulas drew Horn-like, and Horn => min-closed
  PREVALENCE          general 2-CNF solution sets at this size are min-closed far more often than the
                      Horn route alone predicts

DECISION RULE (sealed):
  min-closed rate ~ Horn rate, min-closed formulas predominantly Horn   -> CHANCE-COMPOSITION
  min-closed rate >> Horn rate, min-closed NON-Horn formulas common     -> PREVALENCE
  min-closed rate ~ 0 across re-draws                                   -> CHANCE-COMPOSITION (rare draw)
  neither pattern separates                                             -> INSUFFICIENT

THE PRIOR, COMPUTED BEFORE ANY DATA. At ratio 1.6 with n = 12 the generator emits m = 19 clauses. A
2-clause is Horn iff at most one of its two literals is positive -- 3 of 4 sign patterns -- so
P(whole formula Horn) = 0.75^19 = 0.00423, i.e. 0.42%. A chance-Horn draw is a priori RARE, which means
PREVALENCE is the branch the arithmetic favours before the study runs. Stated now so it cannot be
presented as a surprise afterwards.

Horn => min-closed, but min-closed does NOT => Horn: a small solution set can be closed by accident. That
is why min-closure is measured DIRECTLY rather than inferred from the Horn indicator, and why the rate is
reported conditioned on r.
"""
import hashlib
import json
import random
import sys
from itertools import combinations, product
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "dev"))
OUT = ROOT / "foundry" / "results" / "lattice" / "n3_sat2_zero.json"

N_DRAWS, N_VARS, RATIO, K = 300, 12, 1.6, 2
BASE_SEED = 20260726


def draw(rng, n=N_VARS, ratio=RATIO, k=K):
    """The survey's own sat() emission rule for mode='plain', re-emitted with its clauses exposed."""
    m = max(1, int(ratio * n))
    cls = [(tuple(rng.sample(range(n), k)), tuple(rng.randint(0, 1) for _ in range(k)))
           for _ in range(m)]
    sols = [a for a in product((0, 1), repeat=n)
            if all(any(a[vs[i]] == sg[i] for i in range(k)) for vs, sg in cls)]
    return cls, sols


def is_horn(cls):
    """At most one POSITIVE literal per clause. sg[i]=1 means the literal is positive."""
    return all(sum(sg) <= 1 for _vs, sg in cls)


def min_closed(sols):
    """Exhaustive over all distinct pairs -- r is small enough that no cap is needed."""
    S = set(sols)
    return all(tuple(min(a[i], b[i]) for i in range(len(a))) in S for a, b in combinations(sols, 2))


def main() -> int:
    rows = []
    for t in range(N_DRAWS):
        rng = random.Random(BASE_SEED + t)
        cls, sols = draw(rng)
        if len(sols) < 2:
            rows.append({"trial": t, "r": len(sols), "horn": is_horn(cls), "min_closed": None,
                         "skipped": "fewer than 2 solutions"})
            continue
        rows.append({"trial": t, "r": len(sols), "horn": is_horn(cls), "min_closed": min_closed(sols)})

    use = [x for x in rows if x["min_closed"] is not None]
    horn = [x for x in use if x["horn"]]
    mc = [x for x in use if x["min_closed"]]
    mc_nonhorn = [x for x in mc if not x["horn"]]
    horn_rate = len(horn) / len(use)
    mc_rate = len(mc) / len(use)

    # the sealed decision rule, applied mechanically
    if mc_rate == 0:
        verdict = "CHANCE-COMPOSITION"
        why = ("no re-draw at this ratio produced a min-closed solution set, so the original reading is a "
               "rare draw rather than evidence of prevalence.")
    elif mc_rate > 3 * max(horn_rate, 1e-9) and len(mc_nonhorn) >= max(3, 0.5 * len(mc)):
        verdict = "PREVALENCE"
        why = (f"min-closure appears at {mc_rate:.1%} against a Horn rate of {horn_rate:.1%}, and "
               f"{len(mc_nonhorn)} of {len(mc)} min-closed formulas are NOT Horn. The Horn route cannot "
               f"carry the explanation.")
    elif abs(mc_rate - horn_rate) <= 0.02 and len(mc_nonhorn) <= 0.2 * max(1, len(mc)):
        verdict = "CHANCE-COMPOSITION"
        why = ("min-closure tracks the Horn rate and min-closed formulas are predominantly Horn.")
    else:
        verdict = "INSUFFICIENT"
        why = ("neither pattern separates at this N: the rates differ but the non-Horn share does not "
               "meet the declared threshold in either direction.")

    by_r = {}
    for x in use:
        b = "r<25" if x["r"] < 25 else ("25<=r<100" if x["r"] < 100 else "r>=100")
        d = by_r.setdefault(b, {"n": 0, "min_closed": 0})
        d["n"] += 1; d["min_closed"] += bool(x["min_closed"])

    doc = {"schema": "n3-sat2-zero/v1", "prereg": "prereg_v21", "sealed": "2026-07-26",
           "scored_once": True,
           "prior_computed_before_data": {"clauses": int(RATIO * N_VARS), "p_clause_horn": 0.75,
                                          "p_formula_horn": round(0.75 ** int(RATIO * N_VARS), 5)},
           "n_draws": N_DRAWS, "n_usable": len(use),
           "horn_rate": round(horn_rate, 4), "min_closed_rate": round(mc_rate, 4),
           "n_min_closed": len(mc), "n_min_closed_and_NOT_horn": len(mc_nonhorn),
           "joint_table": {"horn & min-closed": sum(1 for x in use if x["horn"] and x["min_closed"]),
                           "horn & not-min-closed": sum(1 for x in use if x["horn"] and not x["min_closed"]),
                           "not-horn & min-closed": len(mc_nonhorn),
                           "not-horn & not-min-closed": sum(1 for x in use
                                                            if not x["horn"] and not x["min_closed"])},
           "min_closed_rate_by_region_size": by_r,
           "original_reading": {"row": "sat-2", "region": "solutions", "flavor": "min", "r": 22,
                                "measured_rate": 0.0, "ramp_value": 1.6, "seed": 20265280},
           "VERDICT": verdict, "why": why, "trials": rows}
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    print("N3 — THE SAT-2 ZERO, SCORED ONCE (prereg_v21)\n")
    print(f"  prior, computed before data: P(formula Horn) = 0.75^{int(RATIO*N_VARS)} = "
          f"{0.75**int(RATIO*N_VARS):.5f}")
    print(f"  draws {N_DRAWS}, usable {len(use)}\n")
    print(f"  Horn rate       : {horn_rate:.4f}  ({len(horn)}/{len(use)})")
    print(f"  min-closed rate : {mc_rate:.4f}  ({len(mc)}/{len(use)})")
    print(f"  min-closed AND NOT Horn : {len(mc_nonhorn)}")
    print(f"\n  joint table: {doc['joint_table']}")
    print(f"  min-closed by region size: {by_r}")
    print(f"\n  VERDICT: {verdict}")
    print(f"  {why}")
    print(f"\nwrote {OUT.name}  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
