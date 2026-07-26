#!/usr/bin/env python3
"""N4 — property-derived forcedness, with verify-on-declare. INSTRUMENT HYGIENE, not a bet.

WHAT THIS CONVERTS. The zero-hunt adjudicated 29 readings as HIDDEN-CLOSURE using three structural
arguments plus parity. Those verdicts live in prose. This turns them into a STANDING SCHEMA: a region
declares a structural PROPERTY, and its forced flavours derive from the property mechanically.

THE DISEASE-GUARD, which is the whole reason this can ship. A declared property is a hand-written entry
wearing derivation's clothes UNLESS IT IS MECHANICALLY VERIFIED. The template route earned its authority by
being checkable; a property route that merely asserts "this region is upward-closed" reintroduces exactly
the rules-that-live-in-recall problem the derivation was built to end.

So: EVERY declared property ships with a per-region brute-force check, and AN UNVERIFIED PROPERTY IS NO
PROPERTY. A declaration whose check fails does not downgrade to a warning — it is dropped, loudly.

    derive  UNION  assert-with-argument  UNION  verify-on-declare

THE PROPERTY VOCABULARY, and the flavours each one forces. Both directions are derived, because the join
now has two (see sounding_forced_saturated.py):

  upward_closed     membership survives setting a 0 to 1     -> max-CLOSED   (violation forced to 0)
  downward_closed   membership survives clearing a 1 to 0    -> min-CLOSED   (violation forced to 0)
  pairwise_exclusion  membership is 'no conflicting pair'    -> majority-CLOSED (forced to 0)
  parity            membership is a mod-2 linear condition   -> minority-CLOSED (forced to 0)
  fixed_cardinality every member has the same weight         -> min and max SATURATED (forced to 1)
  exact_equality    membership is f(s) == target, f monotone -> min and max SATURATED (forced to 1)

A region may declare several. Contradictory implications on one flavour are a HARD ERROR, not a
precedence rule — if a region is declared both upward-closed and fixed-cardinality, one declaration is
wrong and quietly preferring one would hide it.
"""
import hashlib
import json
import random
import sys
from itertools import combinations
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "dev"))
LAT = ROOT / "foundry" / "results" / "lattice"
OUT = LAT / "n4_property_forcedness.json"
import sounding_v3_survey as S3                                        # noqa: E402
import sounding_v2 as S2                                               # noqa: E402
import sounding_survey as SV                                           # noqa: E402

CHECK_CAP = 4000

PROPERTY_IMPLIES = {
    "upward_closed":     {"max": ("closed", "union of two members is a member")},
    "downward_closed":   {"min": ("closed", "intersection of two members is a member")},
    "pairwise_exclusion": {"majority": ("closed",
                          "a conflicting pair in the majority forces some single member to contain both")},
    "parity":            {"minority": ("closed", "XOR preserves every mod-2 linear condition")},
    "fixed_cardinality": {"min": ("saturated", "intersection has strictly fewer elements"),
                          "max": ("saturated", "union has strictly more elements")},
    "exact_equality":    {"min": ("saturated", "intersection breaks the equality"),
                          "max": ("saturated", "union breaks the equality")},
}

# (row, region) -> declared properties. Each is CHECKED below; an unverified declaration is dropped.
DECLARED = {
    ("set-cover", "feasible"): ["upward_closed"],
    ("hitting-set", "feasible"): ["upward_closed"],
    ("feedback-vertex-set", "feasible"): ["upward_closed"],
    ("odd-cycle-transversal", "feasible"): ["upward_closed"],
    ("dominating-set", "feasible"): ["upward_closed"],
    ("knapsack", "feasible"): ["downward_closed"],
    ("independent-set", "feasible"): ["downward_closed", "pairwise_exclusion"],
    ("matching", "feasible"): ["downward_closed", "pairwise_exclusion"],
    ("three-dimensional-matching", "feasible"): ["downward_closed", "pairwise_exclusion"],
    ("max-flow", "feasible"): ["parity"],
    ("subset-sum", "solutions"): ["exact_equality"],
    ("min-spanning-tree", "feasible"): ["fixed_cardinality"],
}

OPS = {"max": (lambda ts: tuple(max(c) for c in zip(*ts)), 2),
       "min": (lambda ts: tuple(min(c) for c in zip(*ts)), 2),
       "majority": (lambda ts: tuple(1 if sum(c) >= 2 else 0 for c in zip(*ts)), 3),
       "minority": (lambda ts: tuple(c[0] ^ c[1] ^ c[2] for c in zip(*ts)), 3)}


def check_property(region, prop, rng):
    """Brute-force verification of a DECLARED property on one region. Returns (ok, detail)."""
    R = set(region)
    n = len(region[0])
    if prop == "upward_closed":
        for s in region:
            for i in range(n):
                if s[i] == 0:
                    t = list(s); t[i] = 1
                    if tuple(t) not in R:
                        return False, f"setting coord {i} of {s} to 1 leaves the region"
        return True, "exhaustive: every single-bit raise stays inside"
    if prop == "downward_closed":
        for s in region:
            for i in range(n):
                if s[i] == 1:
                    t = list(s); t[i] = 0
                    if tuple(t) not in R:
                        return False, f"clearing coord {i} of {s} leaves the region"
        return True, "exhaustive: every single-bit clear stays inside"
    if prop == "fixed_cardinality":
        c = {sum(s) for s in region}
        return (len(c) == 1), (f"all members have weight {c.pop()}" if len(c) == 1
                               else f"weights vary: {sorted(c)[:6]}")
    if prop == "parity":
        # every member satisfies the same set of mod-2 linear constraints: check closure under XOR of 3
        for _ in range(min(CHECK_CAP, 800)):
            a, b, c = (rng.choice(region) for _ in range(3))
            if tuple(x ^ y ^ z for x, y, z in zip(a, b, c)) not in R:
                return False, "XOR of three members left the region"
        return True, "sampled: XOR of three members stayed inside"
    if prop == "pairwise_exclusion":
        # membership must be exactly 'no conflicting pair': derive the conflict set, then confirm it
        # characterises the region. A region with a non-pairwise constraint fails here.
        conflicts = [(i, j) for i in range(n) for j in range(i + 1, n)
                     if not any(s[i] and s[j] for s in region)]
        for s in region:
            if any(s[i] and s[j] for i, j in conflicts):
                return False, "a member violates the derived conflict set"
        # and every non-member must violate one — checked on the region's own closure
        for _ in range(min(CHECK_CAP, 600)):
            t = tuple(rng.randint(0, 1) for _ in range(n))
            ok = not any(t[i] and t[j] for i, j in conflicts)
            if ok and t not in R:
                return False, "a conflict-free vector is NOT in the region — membership is not pairwise"
        return True, f"derived {len(conflicts)} conflicting pairs and they characterise membership"
    if prop == "exact_equality":
        # both blends must leave, and the region must not be closed under either
        for _ in range(min(CHECK_CAP, 600)):
            a, b = rng.choice(region), rng.choice(region)
            if a == b:
                continue
            if OPS["min"][0]((a, b)) in R or OPS["max"][0]((a, b)) in R:
                return False, "a blend of two distinct members stayed inside"
        return True, "sampled: no blend of two distinct members stayed inside"
    return False, "unknown property"


def observed(region, flavour, rng, cap=CHECK_CAP):
    op, m = OPS[flavour]
    R = set(region)
    tot = comb(len(region), m)
    if tot <= cap:
        bad = sum(1 for sub in combinations(region, m) if op(sub) not in R)
        return bad / tot
    bad = sum(1 for _ in range(cap) if op(tuple(rng.sample(region, m))) not in R)
    return bad / cap


def main() -> int:
    rng = random.Random(20260726)
    BUILD = {"set-cover": lambda: S3.set_cover(rng, 9), "hitting-set": lambda: S3.hitting_set(rng, 7),
             "feedback-vertex-set": lambda: S3.fvs(rng, 0.30), "odd-cycle-transversal": lambda: S3.oct_(rng, 0.30),
             # dominating-set is not in the v2 fleet — it lives in v3's ramp via gsub(..., "dom")
             "dominating-set": lambda: S3.gsub(rng, 0.25, "dom"),
             # 0.45 yields ~5959 members, above the verification window; 0.25 gives ~931 with the
             # same structure — the property is scale-free, the check is not
             "knapsack": lambda: S3.knapsack(rng, 0.25),
             "independent-set": lambda: S2.regions_for("independent-set", rng),
             "matching": lambda: S2.regions_for("matching", rng),
             "three-dimensional-matching": lambda: SV.extra_regions("three-dimensional-matching", rng),
             "max-flow": lambda: S2.regions_for("max-flow", rng),
             "subset-sum": lambda: S3.subsum(rng, 20),
             "min-spanning-tree": lambda: S2.regions_for("min-spanning-tree", rng)}

    entries, dropped, contradictions = [], [], []
    for (row, region_kind), props in sorted(DECLARED.items()):
        regs = []
        for _ in range(3):
            try:
                d = dict(BUILD[row]() or [])
            except Exception as e:
                dropped.append({"row": row, "region": region_kind, "property": props,
                                "why": f"builder raised: {e}"}); regs = []; break
            r = d.get(region_kind)
            if r and 4 <= len(r) <= 8000:
                regs.append(r)
        if not regs:
            if not any(x["row"] == row for x in dropped):
                dropped.append({"row": row, "region": region_kind, "property": props,
                                "why": "no region of usable size built for verification"})
            continue
        verified, failed = [], []
        for prop in props:
            res = [check_property(r, prop, rng) for r in regs]
            if all(ok for ok, _ in res):
                verified.append({"property": prop, "checked_on_regions": len(regs),
                                 "detail": res[0][1]})
            else:
                failed.append({"property": prop, "detail": next(d for ok, d in res if not ok)})
        for f in failed:
            dropped.append({"row": row, "region": region_kind, "property": f["property"],
                            "why": "VERIFICATION FAILED — declaration dropped, not downgraded: "
                                   + f["detail"]})
        # derive the forced flavours from the VERIFIED properties only
        forced = {}
        for v in verified:
            for fl, (kind, why) in PROPERTY_IMPLIES[v["property"]].items():
                if fl in forced and forced[fl]["kind"] != kind:
                    contradictions.append({"row": row, "region": region_kind, "flavour": fl,
                                           "from": [forced[fl]["property"], v["property"]],
                                           "why": "one declaration implies closed and the other saturated"})
                forced[fl] = {"kind": kind, "property": v["property"], "argument": why}
        # and CHECK the derived flags against the observed rate on the same regions
        agree, disagree = [], []
        for fl, f in forced.items():
            rates = [observed(r, fl, rng) for r in regs]
            want0 = f["kind"] == "closed"
            ok = all(x == 0.0 for x in rates) if want0 else all(x == 1.0 for x in rates)
            (agree if ok else disagree).append({"flavour": fl, "expected": f["kind"],
                                                "observed_rates": [round(x, 4) for x in rates]})
        entries.append({"row": row, "region": region_kind,
                        "declared": props, "verified": verified,
                        "dropped_declarations": failed,
                        "derived_forced": forced,
                        "flags_agree_with_observation": agree,
                        "flags_DISAGREE_with_observation": disagree})

    hard = [e for e in entries if e["flags_DISAGREE_with_observation"]]
    doc = {"schema": "n4-property-forcedness/v1",
           "STATUS": "INSTRUMENT HYGIENE — no prereg, no bet, no scored prediction",
           "what": ("structural properties declared per (row, region), MECHANICALLY VERIFIED, and forced "
                    "flavours derived from the verified properties in both directions (closed / saturated)"),
           "the_disease_guard": ("a declared property is a hand-written entry wearing derivation's clothes "
                                 "unless it is verified. Every declaration is brute-force checked and an "
                                 "unverified declaration is DROPPED, not downgraded."),
           "property_vocabulary": {k: {f: v[0] for f, v in imp.items()}
                                   for k, imp in PROPERTY_IMPLIES.items()},
           "n_declarations": sum(len(v) for v in DECLARED.values()),
           "n_verified": sum(len(e["verified"]) for e in entries),
           "n_dropped": len(dropped),
           "contradictions": contradictions,
           "entries_whose_derived_flags_disagree_with_observation": hard,
           "entries": entries, "dropped": dropped}
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    print("N4 — PROPERTY-DERIVED FORCEDNESS, VERIFY-ON-DECLARE (hygiene; no bet)\n")
    print(f"  declarations : {doc['n_declarations']}")
    print(f"  verified     : {doc['n_verified']}")
    print(f"  dropped      : {doc['n_dropped']}")
    print(f"  contradictions: {len(contradictions)}")
    print(f"\n  {'row':<28}{'region':<10}{'declared':<38}verified")
    for e in entries:
        print(f"  {e['row']:<28}{e['region']:<10}{','.join(e['declared']):<38}"
              f"{','.join(v['property'] for v in e['verified']) or '(none)'}")
    if dropped:
        print(f"\n  DROPPED DECLARATIONS:")
        for d in dropped:
            print(f"    {d['row']}·{d['region']}·{d['property']}: {d['why'][:100]}")
    if hard:
        print(f"\n  FLAGS DISAGREEING WITH OBSERVATION (these would be wrong flags):")
        for e in hard:
            for d in e["flags_DISAGREE_with_observation"]:
                print(f"    {e['row']}·{e['region']}·{d['flavour']} expected {d['expected']}, "
                      f"observed {d['observed_rates']}")
    print(f"\nwrote {OUT.name}  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 1 if contradictions else 0


if __name__ == "__main__":
    sys.exit(main())
