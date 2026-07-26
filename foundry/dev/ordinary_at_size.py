#!/usr/bin/env python3
"""ORDINARY-AT-SIZE — the base-rate lens, and the fourth explanation class the zero-hunt could not name.

THE GAP N3 EXPOSED. The zero-hunt's vocabulary had three ways a zero could be explained — HIDDEN-CLOSURE
(a theorem), ENCODING-ARTIFACT (the instrument), THIN-SATURATION (too few subsets for a nonzero rate to be
OBSERVABLE) — and GENUINE-READING for "none of the above".

N3 demonstrated a fourth. At r = 22, 231 distinct pairs were available and a nonzero rate was perfectly
observable. It simply did not occur, because **64.5 % of random 2-CNF solution sets with r < 25 are
min-closed**. The reading was admissible by every floor, unexplained by theorem or artifact, and entirely
unremarkable against the size-conditioned base rate of the phenomenon.

    ORDINARY-AT-SIZE — admissible by every floor, unexplained by theorem or artifact, and unremarkable
    against the size-conditioned base rate.

"Notable" requires a base rate the same way an excess requires a control. THIN-SATURATION asks whether the
instrument COULD have spoken; this asks whether what it said was unusual.

THE LENS, applied to any (row, region, flavour) zero:
  1. rebuild many fresh instances from the row's own generator
  2. keep those whose region size lands near the reading's r
  3. measure how often the flavour's violation rate is exactly 0 in that size band
  4. compare the reading to that base rate

DECISION, declared here before running:
  base rate >= 0.20 in the reading's size band  -> ORDINARY-AT-SIZE
  base rate <= 0.05                             -> stays GENUINE-READING; the reading is unusual
  in between                                    -> INSUFFICIENT-baserate, reported and not forced
"""
import hashlib
import json
import random
import sys
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "dev"))
LAT = ROOT / "foundry" / "results" / "lattice"
OUT = LAT / "ordinary_at_size.json"
import sounding_v3_survey as S3                                        # noqa: E402

N_DRAWS = 400
ORDINARY_FLOOR, GENUINE_CEILING = 0.20, 0.05
OPS = {"majority": (lambda ts: tuple(1 if sum(c) >= 2 else 0 for c in zip(*ts)), 3),
       "minority": (lambda ts: tuple(c[0] ^ c[1] ^ c[2] for c in zip(*ts)), 3),
       "min": (lambda ts: tuple(min(c) for c in zip(*ts)), 2),
       "max": (lambda ts: tuple(max(c) for c in zip(*ts)), 2)}


def violation_exact(region, flavour):
    """Exhaustive over distinct m-subsets — these regions are small, so no cap and no doubt."""
    op, m = OPS[flavour]
    R = set(region)
    subs = list(combinations(region, m))
    if not subs:
        return None
    return sum(1 for s in subs if op(s) not in R) / len(subs)


def band(r, target, width=0.5):
    return target * (1 - width) <= r <= target * (1 + width)


def lens(name, builder, region_kind, flavour, target_r, rng):
    rows = []
    for t in range(N_DRAWS):
        try:
            d = dict(builder(random.Random(20260726 + t)) or [])
        except Exception:
            continue
        reg = d.get(region_kind)
        if not reg or len(reg) < 2:
            continue
        v = violation_exact(reg, flavour)
        if v is None:
            continue
        rows.append({"r": len(reg), "rate": round(v, 6), "zero": v == 0.0})
    inband = [x for x in rows if band(x["r"], target_r)]
    base = (sum(x["zero"] for x in inband) / len(inband)) if inband else None
    overall = (sum(x["zero"] for x in rows) / len(rows)) if rows else None
    if base is None or len(inband) < 20:
        verdict, why = "INSUFFICIENT-baserate", (
            f"only {len(inband)} of {len(rows)} draws landed in the size band around r={target_r}; "
            f"the base rate is not estimable at usable precision.")
    elif base >= ORDINARY_FLOOR:
        verdict, why = "ORDINARY-AT-SIZE", (
            f"{base:.1%} of freshly drawn regions in this size band read exactly 0. The reading is what "
            f"typically happens at its size.")
    elif base <= GENUINE_CEILING:
        verdict, why = "GENUINE-READING", (
            f"only {base:.1%} of freshly drawn regions in this size band read exactly 0. The reading is "
            f"unusual and stays unexplained.")
    else:
        verdict, why = "INSUFFICIENT-baserate", (
            f"base rate {base:.1%} falls between the declared floor ({ORDINARY_FLOOR:.0%}) and ceiling "
            f"({GENUINE_CEILING:.0%}); neither call is earned and neither is forced.")
    bands = {}
    for x in rows:
        k = "r<25" if x["r"] < 25 else ("25<=r<100" if x["r"] < 100 else "r>=100")
        b = bands.setdefault(k, {"n": 0, "zeros": 0})
        b["n"] += 1; b["zeros"] += x["zero"]
    return {"reading": name, "region_kind": region_kind, "flavor": flavour, "target_r": target_r,
            "n_draws": len(rows), "n_in_band": len(inband),
            "base_rate_in_band": round(base, 4) if base is not None else None,
            "base_rate_overall": round(overall, 4) if overall is not None else None,
            "by_size_band": {k: {**v, "rate": round(v["zeros"] / v["n"], 4)} for k, v in bands.items()},
            "VERDICT": verdict, "why": why}


def main() -> int:
    rng = random.Random(20260730)
    results = [
        lens("independent-set·optimal·majority",
             lambda r: S3.gsub(r, 0.35, "is"), "optimal", "majority", 10, rng),
    ]
    doc = {"schema": "ordinary-at-size/v1",
           "STATUS": "verdict-term application — the base-rate lens",
           "the_term": ("ORDINARY-AT-SIZE: admissible by every floor, unexplained by theorem or artifact, "
                        "and unremarkable against the size-conditioned base rate of the phenomenon."),
           "why_it_is_needed": ("THIN-SATURATION asks whether the instrument COULD have spoken. This asks "
                                "whether what it said was unusual. 'Notable' requires a base rate the "
                                "same way an excess requires a control."),
           "decision_declared_before_running": {
               "ordinary_at_size_if_base_rate_at_or_above": ORDINARY_FLOOR,
               "stays_genuine_if_base_rate_at_or_below": GENUINE_CEILING,
               "otherwise": "INSUFFICIENT-baserate, reported and not forced"},
           "results": results}
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    print("ORDINARY-AT-SIZE — the base-rate lens\n")
    for r in results:
        print(f"  {r['reading']}")
        print(f"    draws {r['n_draws']}, in size band around r={r['target_r']}: {r['n_in_band']}")
        print(f"    base rate in band : {r['base_rate_in_band']}")
        print(f"    base rate overall : {r['base_rate_overall']}")
        print(f"    by size band      : {r['by_size_band']}")
        print(f"    VERDICT: {r['VERDICT']}")
        print(f"    {r['why']}")
    print(f"\nwrote {OUT.name}  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
