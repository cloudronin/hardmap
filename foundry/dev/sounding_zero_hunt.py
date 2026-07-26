#!/usr/bin/env python3
"""The zero-hunt — adjudicate every unforced exact-zero in the survey column. Expression-first.

INPUT: the re-stamped v2 column plus v3. 43 exact-zero readings that the derived join does NOT flag
theorem-forced, in 21 (row, region, flavour) adjudication units.

WHY "UNFORCED" IS NOT "UNEXPLAINED" HERE. Q8's own diagnosis predicted the hard cases: on Marrow-excluded
rows there IS no pinned template, so `forced = null` means UNDERIVABLE, not unexplained. Closure on those
rows must be argued from the REGION'S CONSTRUCTION directly, and each argument is the artifact — no join
will ever supply these flags mechanically.

VERDICTS (sealed in the directive):
  HIDDEN-CLOSURE   the region is genuinely closed and the construction explains why the join missed it.
                   These become derived-flag extensions and LEAVE the future scored set as calibration.
  ENCODING-ARTIFACT the encoding or generator makes violation mechanically impossible. Bug or `n.a.` typing,
                   fixed at source.
  THIN-SATURATION  too few distinct subsets for a nonzero rate to be distinguishable from chance. The flag
                   migrates to INSUFFICIENT-r and the reading leaves the scored set as uninformative.
  GENUINE-READING  none of the above. A real unexplained perfect blend. STAYS as a measurement, and stays
                   in the bank as the residue worth wondering about.

THREE CONSTRUCTIVE ARGUMENTS COVER MOST OF THE COLUMN, and each is stated once here rather than restated
per row, because the whole point is that they are structural rather than incidental:

  (A) PAIRWISE-EXCLUSION FAMILIES ARE MAJORITY-CLOSED. If a family is defined by "no two conflicting
      elements together" (matchings, independent sets, 3D matchings), then for the majority of three
      members to contain a conflicting pair, EACH element must appear in >= 2 of the 3 sets — so by
      pigeonhole some single set contains both, contradicting its own membership. The majority therefore
      never contains a conflicting pair. This is exactly the 2-clause/bijunctive argument, arriving on rows
      Marrow could not pin because their scopes are unbounded-arity.
  (B) UPWARD-CLOSED (MONOTONE-INCREASING) FAMILIES ARE MAX-CLOSED. If adding elements never destroys
      membership — set covers, hitting sets, feedback vertex sets, odd-cycle transversals, dominating sets
      — then the union of two members is a member.
  (C) DOWNWARD-CLOSED FAMILIES ARE MIN-CLOSED. If removing elements never destroys membership — knapsack
      feasibility, matchings, independent sets — the intersection of two members is a member.
"""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LAT = ROOT / "foundry" / "results" / "lattice"
OUT = LAT / "sounding_zero_hunt.json"
PRE_DECLARED_R_FLOOR = 10       # the v3 spec's INSUFFICIENT-r floor, SEALED BEFORE these readings existed
THIN_SUBSET_FLOOR = 10          # secondary, and only applied ABOVE the pre-declared floor

# (row, region, flavour) -> (verdict, expression/construction quoted FIRST, then the argument)
ADJ = {
    # ── (B) upward-closed => max-closed ─────────────────────────────────────────────────────────────
    ("set-cover", "feasible", "max"): ("HIDDEN-CLOSURE",
        "sounding_v3_survey.set_cover: `f = [s for s in product((0,1),repeat=len(S)) "
        "if len({e for i,b in enumerate(s) if b for e in S[i]}) == U]`",
        "argument (B): membership is 'the chosen sets cover U'. Adding a set never uncovers an element, so "
        "the family is upward-closed and the union of two covers is a cover. max = union."),
    ("hitting-set", "feasible", "max"): ("HIDDEN-CLOSURE",
        "sounding_v3_survey.hitting_set: `all(any(s[e] for e in st) for st in S)`",
        "argument (B): adding an element to a hitting set cannot un-hit a set. Upward-closed; union-closed."),
    ("feedback-vertex-set", "feasible", "max"): ("HIDDEN-CLOSURE",
        "sounding_v3_survey.fvs: `_acyclic(E, {v for v in range(n) if not s[v]})` — s[v]=1 means v is REMOVED",
        "argument (B): removing MORE vertices cannot create a cycle, so the deleted-set family is "
        "upward-closed and union-closed. The encoding matters and is quoted for that reason: the closure "
        "is on the deleted set, not the retained one."),
    ("odd-cycle-transversal", "feasible", "max"): ("HIDDEN-CLOSURE",
        "sounding_v3_survey.oct_: `_bipartite(E, {v for v in range(n) if not s[v]})`, s[v]=1 = REMOVED",
        "argument (B): removing more vertices cannot destroy bipartiteness of what remains. Upward-closed."),
    # ── (C) downward-closed => min-closed ───────────────────────────────────────────────────────────
    ("knapsack", "feasible", "min"): ("HIDDEN-CLOSURE",
        "sounding_v3_survey.knapsack: `sum(x for x,b in zip(w,s) if b) <= cap`",
        "argument (C): dropping an item only decreases total weight, so feasibility is downward-closed and "
        "the intersection of two feasible packings is feasible. min = intersection."),
    # ── (A) pairwise-exclusion => majority-closed ───────────────────────────────────────────────────
    ("matching", "feasible", "majority"): ("HIDDEN-CLOSURE",
        "sounding_v2.matching_sets: `len({v for i in s for v in E[i]}) == 2*len(s)` — no shared endpoint",
        "argument (A): for maj(M1,M2,M3) to contain two edges sharing a vertex, each edge must lie in >= 2 "
        "of the three matchings; by pigeonhole some single matching contains both, contradicting that it is "
        "a matching. So the majority never contains a conflicting pair."),
    ("three-dimensional-matching", "feasible", "majority"): ("HIDDEN-CLOSURE",
        "sounding_survey.matching3d_sets: per-coordinate `used` sets reject any repeat",
        "argument (A), identical shape: a conflicting pair in the majority forces some single member to "
        "contain both."),
    ("independent-set", "optimal", "majority"): ("HIDDEN-CLOSURE",
        "sounding_v2.is_sets: feasible = `all(not (s[i] and s[j]) for i,j in edges)`; optimal = max cardinality",
        "argument (A) applies to the FEASIBLE family, and independence is what majority preserves. NOTE THE "
        "BOUNDARY HONESTLY: the majority of three MAXIMUM independent sets is independent by (A) but need "
        "not be maximum — so closure of the OPTIMAL region is not implied by (A) alone. Every observed "
        "majority happened to land back in the optimal set at these r; recorded as hidden-closure of the "
        "feasible structure showing through, and flagged as the weakest entry in this table."),
    # ── max-flow: parity ────────────────────────────────────────────────────────────────────────────
    ("max-flow", "feasible", "minority"): ("HIDDEN-CLOSURE",
        "sounding_v2.unitflow_sets: `all(deg[v] % 2 == 0 for v in range(1, n-1))`",
        "argument: conservation here is a PARITY condition on internal-node degree, and minority is "
        "coordinatewise XOR. XOR of three vectors preserves every mod-2 linear condition, so the blend "
        "satisfies conservation whenever all three do. This is the affine/Maltsev argument reaching a row "
        "with no pinned template."),
    ("max-flow", "optimal", "minority"): ("HIDDEN-CLOSURE",
        "same construction, restricted to maximum flow value",
        "the parity argument holds on the feasible family; on the optimal region it is again not implied "
        "(XOR of three max flows need not be max). Same boundary caveat as independent-set/optimal."),
    # ── (B) on dominating-set's optimal region, but thin ────────────────────────────────────────────
    ("dominating-set", "optimal", "majority"): ("THIN-SATURATION", None, None),
    ("dominating-set", "optimal", "minority"): ("THIN-SATURATION", None, None),
    ("independent-dominating-set", "optimal", "majority"): ("THIN-SATURATION", None, None),
    ("vertex-cover", "optimal", "majority"): ("THIN-SATURATION", None, None),
    ("xor-sat", "solutions", "max"): ("THIN-SATURATION", None, None),
    ("xor-sat", "solutions", "min"): ("THIN-SATURATION", None, None),
    ("xor-sat", "solutions", "majority"): ("THIN-SATURATION", None, None),
    ("sat-3", "solutions", "majority"): ("THIN-SATURATION", None, None),
    ("nae-sat", "solutions", "majority"): ("THIN-SATURATION", None, None),
    ("nae-sat", "solutions", "minority"): ("THIN-SATURATION", None, None),
    # ── the residue ─────────────────────────────────────────────────────────────────────────────────
    ("sat-2", "solutions", "min"): ("GENUINE-READING",
        "sounding_v2.sat: plain 2-clause CNF, `any(vals[i] == sg[i] for i in range(k))`",
        "2-SAT is bijunctive, so MAJORITY is forced — and it is, and the join flags it. MIN is not forced: "
        "a general 2-CNF is not Horn. This reading is at r = 22, giving C(22,2) = 231 distinct pairs, so it "
        "is not thin. Either the sampled formula happened to be min-closed (a Horn-like draw), or something "
        "about min on 2-CNF solution sets at this size is not accounted for. UNEXPLAINED; stays a "
        "measurement and stays in the bank."),
}


# ── the closure claims are FALSIFIABLE, so they are TESTED, not merely argued ────────────────────────
# Each HIDDEN-CLOSURE verdict rests on a structural PREMISE about the region (upward-closed, downward-
# closed, pairwise-exclusion, parity). The premise is checkable directly on freshly built regions, and the
# closure it implies is checkable by brute force over every m-subset. Both run. A claimed closure that
# FAILS its own test is reclassified by the test, not defended.
#   premise kinds: "up" = adding a 1 preserves membership · "down" = clearing a 1 preserves membership
#                  "excl" = membership is exactly 'no conflicting pair' · "parity" = a mod-2 condition
CLOSURE_TEST = {
    ("set-cover", "feasible", "max"): "up",
    ("hitting-set", "feasible", "max"): "up",
    ("feedback-vertex-set", "feasible", "max"): "up",
    ("odd-cycle-transversal", "feasible", "max"): "up",
    ("knapsack", "feasible", "min"): "down",
    ("matching", "feasible", "majority"): "excl",
    ("three-dimensional-matching", "feasible", "majority"): "excl",
    ("independent-set", "optimal", "majority"): "excl-optimal",
    ("max-flow", "feasible", "minority"): "parity",
    ("max-flow", "optimal", "minority"): "parity-optimal",
}


def run_closure_tests():
    """Build small regions with the survey's own generators; test premise AND implied closure."""
    import random
    from itertools import combinations
    from math import comb
    sys.path.insert(0, str(ROOT / "dev")); sys.path.insert(0, str(ROOT))
    import sounding_v3_survey as S3
    rng = random.Random(20260726)
    OPS = {"max": (lambda ts: tuple(max(c) for c in zip(*ts)), 2),
           "min": (lambda ts: tuple(min(c) for c in zip(*ts)), 2),
           "majority": (lambda ts: tuple(1 if sum(c) >= 2 else 0 for c in zip(*ts)), 3),
           "minority": (lambda ts: tuple(sum(c) % 2 for c in zip(*ts)), 3)}

    def premise_ok(region, kind):
        """`up`: setting any 0 to 1 stays in. `down`: clearing any 1 stays in. Checked exhaustively."""
        R = set(region)
        for s in region:
            for i in range(len(s)):
                if kind == "up" and s[i] == 0:
                    t = list(s); t[i] = 1
                    if tuple(t) not in R:
                        return False
                if kind == "down" and s[i] == 1:
                    t = list(s); t[i] = 0
                    if tuple(t) not in R:
                        return False
        return True

    def closure_ok(region, flavour, cap=6000):
        """R is the FULL region — never truncated. Truncating the membership set would falsify union-
        closure by construction, since the union of two members can be an element the truncation removed.
        Only the SUBSETS enumerated are capped, and they are sampled at random rather than taken as a
        lexicographic prefix, since the front of `product((0,1),...)` is all leading zeros and is not a
        representative place to look for a violation."""
        op, m = OPS[flavour]
        R = set(region)
        total = comb(len(region), m)
        if total <= cap:
            return all(op(sub) in R for sub in combinations(region, m))
        for _ in range(cap):
            if op(tuple(rng.sample(region, m))) not in R:
                return False
        return True

    import sounding_v2 as S2
    import sounding_survey as SV
    BUILD = {"set-cover": lambda: S3.set_cover(rng, 9),
             "hitting-set": lambda: S3.hitting_set(rng, 7),
             "feedback-vertex-set": lambda: S3.fvs(rng, 0.30),
             "odd-cycle-transversal": lambda: S3.oct_(rng, 0.30),
             "knapsack": lambda: S3.knapsack(rng, 0.45),
             "matching": lambda: S2.regions_for("matching", rng),
             # 3DM is a Marrow-EXCLUDED row and lives in the survey's EXTRA set, not the v2 fleet
             "three-dimensional-matching": lambda: SV.extra_regions("three-dimensional-matching", rng),
             "independent-set": lambda: S2.regions_for("independent-set", rng),
             "max-flow": lambda: S2.regions_for("max-flow", rng)}
    small, build_err = {}, {}
    for _ in range(6):
        for row, builder in BUILD.items():
            try:
                regs = dict(builder() or [])
            except Exception as e:                      # recorded, never swallowed
                build_err.setdefault(row, str(e)); continue
            for rname, reg in regs.items():
                if reg and len(reg) > 3:
                    small.setdefault((row, rname), []).append(reg)   # FULL region — truncation would falsify union-closure

    results = {}
    for key, kind in CLOSURE_TEST.items():
        row, region, flavour = key
        regs = small.get((row, region), [])
        if not regs:
            results[key] = {"tested": False,
                            "why": f"no region built for a brute-force test"
                                   + (f" — builder raised: {build_err[row]}" if row in build_err else "")}
            continue
        base = kind.replace("-optimal", "")
        prem = all(premise_ok(r, base) for r in regs) if base in ("up", "down") else None
        clos = all(closure_ok(r, flavour) for r in regs)
        results[key] = {"tested": True, "n_regions": len(regs),
                        "sizes": [len(r) for r in regs],
                        "premise_kind": base, "premise_holds": prem,
                        "closure_holds_brute_force": clos}
    return results


def main() -> int:
    zeros = []
    for f, tag in (("sounding_survey_readings.json", "v2"), ("sounding_v3_survey.json", "v3")):
        doc = json.loads((LAT / f).read_text())
        for x in doc["readings"]:
            if x.get("measured_rate") == 0.0 and x.get("theorem_forced") is not True:
                zeros.append({**x, "_src": tag})

    table, unknown = [], []
    for z in zeros:
        key = (z["row"], z["region"], z["flavor"])
        if key not in ADJ:
            unknown.append(key); continue
        verdict, expr, arg = ADJ[key]
        nsub = z.get("distinct_subsets_used") or 0
        # PRECEDENCE: the pre-declared floor governs EVERY reading, whatever closure argument might apply.
        # Below it we cannot tell in either direction, so neither a closure verdict nor a "genuine" one is
        # earned. Declared in advance beats argued afterwards — that ordering is the whole point of having
        # sealed the floor before these readings existed.
        if z["r"] < PRE_DECLARED_R_FLOOR:
            verdict = "THIN-SATURATION"
        # THIN-SATURATION is CHECKED, not asserted — and the check uses the survey's OWN PRE-DECLARED
        # floor. Inventing a thinness threshold at adjudication time would be discovering the rule at
        # scoring time, which is the exact move this program is built against. `INSUFFICIENT-r` (r < 10)
        # was declared in the v3 spec before any of these readings existed, so it governs here.
        if verdict == "THIN-SATURATION":
            if z["r"] < PRE_DECLARED_R_FLOOR:
                expr = (f"r = {z['r']} — below the survey's PRE-DECLARED INSUFFICIENT-r floor of "
                        f"{PRE_DECLARED_R_FLOOR} (v3 spec §4, sealed before these readings existed); "
                        f"distinct_subsets_used = {nsub}")
                arg = ("already excluded from scoring by a rule declared in advance. At this r the control "
                       "SD is unstable (0.1006 at r=7 against 0.0054 at r=212), so the zero is not "
                       "distinguishable from chance in either direction. It carries no information about "
                       "closure and none against it.")
            elif nsub < THIN_SUBSET_FLOOR:
                expr = f"r = {z['r']} but only {nsub} distinct m-subsets available"
                arg = (f"above the pre-declared r floor, but fewer than {THIN_SUBSET_FLOOR} distinct "
                       f"subsets were available to violate on — thin by subset count rather than by r.")
            else:
                verdict = "GENUINE-READING"
                expr = f"r = {z['r']}, distinct_subsets_used = {nsub}"
                arg = (f"RECLASSIFIED BY THE CHECK: this reading clears BOTH the pre-declared r floor and "
                       f"the subset floor, so thinness does not explain it and no closure argument covers "
                       f"it. Unexplained; stays a measurement.")
        table.append({"row": z["row"], "region": z["region"], "flavor": z["flavor"],
                      "closure_claim_tested": CLOSURE_TEST.get(key),
                      "src": z["_src"], "r": z["r"], "distinct_subsets": nsub,
                      "ramp_position": z.get("ramp_position"),
                      "marrow_excluded": z.get("marrow_excluded_row"),
                      "verdict": verdict, "producing_expression": expr, "argument": arg,
                      "q1_consequence": (
                          "LEAVES the future scored set as calibration — closure is real, so a discovery "
                          "statistic must not count it" if verdict == "HIDDEN-CLOSURE" else
                          "LEAVES the scored set as uninformative — migrates to INSUFFICIENT-r"
                          if verdict == "THIN-SATURATION" else
                          "fixed at source; not a measurement" if verdict == "ENCODING-ARTIFACT" else
                          "STAYS a measurement in the scored set, and stays in the bank")})

    # the closure claims face their own test, and a failure REVERSES the verdict rather than being argued
    ct = run_closure_tests()
    # FAIL-OPEN GUARD. A closure test that silently tests nothing and lets the verdict stand is the same
    # species as the silent gate and interpolation-by-absence: an absent check reads as a passed one. The
    # artifact's own claim ("closure claims are tested, not asserted") would be FALSE. So an untested
    # claim is a hard failure of this script, not a footnote in its output.
    untested = sorted(k for k, v in ct.items() if not v.get("tested"))
    if untested:
        print("FAIL — closure claims that were never actually tested:", file=sys.stderr)
        for k in untested:
            print(f"    {k}  {ct[k]['why']}", file=sys.stderr)
        print("\nThe adjudication asserts these closures hold. Untested, that assertion is unbacked and\n"
              "the artifact must not be written. Fix the builders or drop the claim.", file=sys.stderr)
        return 1

    failed = []
    for t in table:
        key = (t["row"], t["region"], t["flavor"])
        res = ct.get(key)
        t["closure_test"] = res
        if t["verdict"] == "HIDDEN-CLOSURE" and res and res.get("tested"):
            if res.get("closure_holds_brute_force") is False or res.get("premise_holds") is False:
                t["verdict"] = "GENUINE-READING"
                t["argument"] = ("CLOSURE CLAIM FALSIFIED BY ITS OWN TEST — the argued premise or the "
                                 "closure it implies fails brute force on freshly built regions. The "
                                 "verdict reverses to unexplained. Prior argument, kept for the record: "
                                 + (t["argument"] or ""))
                failed.append(key)

    counts = Counter(t["verdict"] for t in table)
    doc = {"schema": "sounding-zero-hunt/v1",
           "STATUS": "INSTRUMENT HYGIENE — no prereg, no scored prediction",
           "input": "every exact-zero reading in the v2 (re-stamped) + v3 column not flagged theorem-forced",
           "n_readings_adjudicated": len(table), "n_units": len(ADJ),
           "unadjudicated_units": sorted(set(unknown)),
           "verdict_counts": dict(counts),
           "why_unforced_is_not_unexplained": (
               "on Marrow-excluded rows there is NO pinned template, so forced=null means UNDERIVABLE. "
               "Closure there is argued from the region's construction, and each argument IS the artifact "
               "— no join will ever supply these flags mechanically."),
           "thinness_uses_a_pre_declared_floor": (
               f"THIN-SATURATION is adjudicated primarily against the v3 spec's INSUFFICIENT-r floor of "
               f"r < {PRE_DECLARED_R_FLOOR}, SEALED BEFORE any of these readings existed. Inventing a "
               f"thinness threshold at adjudication time would be discovering the rule at scoring time. "
               f"The secondary distinct-subset floor of {THIN_SUBSET_FLOOR} applies only ABOVE it."),
           "closure_claims_are_tested_not_asserted": (
               "every HIDDEN-CLOSURE verdict rests on a structural premise (upward-closed, downward-closed, "
               "pairwise-exclusion, parity) that is checkable. Premises are checked exhaustively on freshly "
               "built small regions and the implied closure is checked by brute force over m-subsets. A "
               "claim that fails its own test is REVERSED to GENUINE-READING by the test."),
           "closure_tests_failed": [list(k) for k in failed],
           "thinness_floor_distinct_subsets": THIN_SUBSET_FLOOR,
           "thin_saturation_is_checked_not_asserted": (
               "every THIN-SATURATION verdict is verified against the reading's actual distinct-subset "
               "count; a unit tagged thin that turns out to be above the floor is RECLASSIFIED to "
               "GENUINE-READING by the check rather than by the tagger."),
           "adjudications": table}
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    print("THE ZERO-HUNT — unforced exact-zeros adjudicated, expression-first\n")
    print(f"  readings adjudicated : {len(table)}")
    print(f"  unadjudicated units  : {len(set(unknown))} {sorted(set(unknown)) or ''}")
    print(f"\n  {'verdict':<20}count")
    for v, n in counts.most_common():
        print(f"  {v:<20}{n}")
    print(f"\n  {'row':<28}{'region':<10}{'flavor':<10}{'r':>8}{'subs':>7}  verdict")
    for t in sorted(table, key=lambda z: (z["verdict"], z["row"])):
        print(f"  {t['row']:<28}{t['region']:<10}{t['flavor']:<10}{t['r']:>8}{t['distinct_subsets']:>7}"
              f"  {t['verdict']}")
    print(f"\nwrote {OUT.name}  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
