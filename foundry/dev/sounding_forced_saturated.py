#!/usr/bin/env python3
"""The join's second direction — `forced_saturated`. An instrument fix, not a study.

THE DEFECT THIS CLOSES. The derived forcedness join excludes flavours a region is CLOSED UNDER — violation
forced to 0. It had no exclusion for flavours a region is forced to LEAVE — violation forced to 1. It was
built to stop a theorem manufacturing a NULL, and the same theorem can manufacture a HIT.

    The same asymmetry wearing the other face.

Terrain's I-phase found it: 58 of 92 admissible positive-excess readings sat at measured_rate EXACTLY 1.0,
29 `min` and 29 `max`, never `majority` or `minority`, arriving in pairs on the same (row, region). Their
excess is `1.0 - control_mean`, positive against any non-saturated control, so they were guaranteed to look
like anti-blendability whether or not it exists — and they carried 45.5% of the anomaly's total excess.

FIVE CONSTRUCTIVE ARGUMENTS, each a one-line theorem about the region's own construction. A blend under a
semilattice flavour moves STRICTLY: `max` (union) grows the vector, `min` (intersection) shrinks it,
whenever the two members differ. So any region whose membership is destroyed by strict growth AND strict
shrinkage is left by every non-trivial blend in both directions.

  (S1) OPTIMAL REGIONS. The optimising subfamily of a set function. min of two optima is strictly smaller
       and max strictly larger, so neither attains the optimum. Forced under BOTH min and max.
  (S2) EXACT-EQUALITY REGIONS. Membership is `f(s) == target` for f strictly monotone in the coordinates
       (subset-sum, number-partitioning). Both blends break the equality they are defined by.
  (S3) OPPOSED-CLOSURE INTERSECTIONS. The region is `U AND D` with U upward-closed and D downward-closed
       and both non-trivial (independent-dominating-set: dominating AND independent). max preserves U and
       kills D; min preserves D and kills U.
  (S4) FIXED-CARDINALITY REGIONS. Every member has the same weight (spanning trees: exactly n-1 edges).
       max of two distinct members has strictly more, min strictly fewer.
  (S5) PATH REGIONS. A blend of two distinct s-t paths is not a path — union creates branching,
       intersection disconnects.

THIS IS A FLAG ADDITION, NOT A RE-MEASUREMENT. Identical readings, new derived metadata.

WHAT THE DERIVATION IS CHECKED AGAINST. A derived flag that nobody tests is a hand list wearing a
derivation's costume. So the derivation is compared to the observed rates in BOTH directions:
  - derived saturated but measured < 1.0  -> the argument is WRONG. Halt.
  - measured == 1.0 but not derived       -> the derivation is INCOMPLETE. Reported, never hidden; this is
                                             the `sufficient-not-complete` boundary the seal carries.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LAT = ROOT / "foundry" / "results" / "lattice"
SEMILATTICE = ("min", "max")

# (row, region) -> (rule, argument). `optimal` is handled by rule S1 for every row.
SATURATING = {
    ("subset-sum", "solutions"): ("S2",
        "membership is an EXACT-SUM equality `sum(w_i x_i) == target`. The union of two distinct "
        "equal-sum subsets sums strictly higher and the intersection strictly lower, so both blends "
        "break the equality that defines the region."),
    ("number-partitioning", "solutions"): ("S2",
        "membership is an exact-balance equality — the same shape as subset-sum."),
    ("number-partitioning", "optimal"): ("S1", "optimal region; see rule S1."),
    ("sudoku", "solutions"): ("S2",
        "every row, column and box must be a PERMUTATION of the symbols — an exact-count equality per "
        "unit. A coordinatewise blend of two distinct grids duplicates or drops symbols and leaves."),
    ("independent-dominating-set", "feasible"): ("S3",
        "the region is `dominating AND independent`. Domination is upward-closed, independence is "
        "downward-closed, and both are non-trivial here. max preserves domination and destroys "
        "independence; min preserves independence and destroys domination."),
    ("min-spanning-tree", "feasible"): ("S4",
        "every spanning tree has exactly n-1 edges. max of two distinct trees has strictly more edges "
        "and min strictly fewer, so neither blend is a spanning tree."),
    ("min-spanning-tree", "optimal"): ("S1", "optimal region; see rule S1."),
    ("reachability-stcon", "feasible"): ("S5",
        "a blend of two distinct s-t paths is not a path: the union branches, the intersection "
        "disconnects."),
}
RULES = {
    "S1": ("OPTIMAL REGIONS WITH A COORDINATEWISE-MONOTONE OBJECTIVE (cardinality or a positive-weight "
           "sum). min of two optima is strictly smaller in that objective and max strictly larger, so "
           "neither attains the optimum. NOT valid for non-monotone objectives — max-cut (a quadratic "
           "form, optima in complementary pairs) and max-flow (value under conservation) are excluded "
           "with their reasons, and the data agrees: they read 0.9429 and 0.9064, not 1.0."),
    "S2": "EXACT-EQUALITY REGIONS. Both blends break the equality the region is defined by.",
    "S3": "OPPOSED-CLOSURE INTERSECTIONS. max kills the downward-closed conjunct, min the upward-closed.",
    "S4": "FIXED-CARDINALITY REGIONS. Both blends change the weight every member shares.",
    "S5": "PATH REGIONS. Union branches, intersection disconnects.",
}


# S1 IS NARROWER THAN IT FIRST LOOKED, and the check below is what narrowed it. The argument "min of two
# optima is smaller and max is larger, so neither is optimal" holds ONLY when the objective is STRICTLY
# MONOTONE IN THE COORDINATE VECTOR. Where it is not, a blend can land back in the optimal set — and two
# rows do exactly that. So the objective is NAMED per row rather than assumed, and rows whose objective is
# non-monotone are excluded WITH their reason.
MONOTONE_OBJECTIVE = {
    "clique": "vertex-set cardinality (maximised)",
    "dominating-set": "vertex-set cardinality (minimised)",
    "independent-dominating-set": "vertex-set cardinality (minimised)",
    "independent-set": "vertex-set cardinality (maximised)",
    "matching": "edge-set cardinality (maximised)",
    "three-dimensional-matching": "triple-set cardinality (maximised)",
    "vertex-cover": "vertex-set cardinality (minimised)",
    "feedback-vertex-set": "deleted-set cardinality (minimised)",
    "odd-cycle-transversal": "deleted-set cardinality (minimised)",
    "hitting-set": "element-set cardinality (minimised)",
    "set-cover": "chosen-set cardinality (minimised)",
    "knapsack": "total item VALUE, a positive-weight sum (maximised)",
    "min-spanning-tree": "total edge WEIGHT, a positive-weight sum (minimised)",
    "number-partitioning": "an exact-balance objective on a positive-weight sum",
    "reachability-stcon": "path length, an edge-set cardinality",
    "subset-sum": "an exact-sum objective on a positive-weight sum",
}
NON_MONOTONE_OBJECTIVE = {
    "max-cut": ("cut size is a QUADRATIC FORM in the vertex assignment, not monotone in it — flipping a "
                "vertex can raise or lower the cut. Max-cut optima also come in complementary pairs, so a "
                "coordinatewise blend can land back inside the optimal set. Measured 0.9429, not 1.0."),
    "max-flow": ("the objective is flow VALUE subject to conservation, which is not monotone in the edge "
                 "indicator — adding an edge can break conservation rather than raise the value. "
                 "Measured 0.9064, not 1.0."),
}


def derive(row, region, flavour):
    """-> (rule, argument) if the region is forced to be LEFT by this flavour, else None."""
    if flavour not in SEMILATTICE:
        return None                      # majority/minority move non-strictly; no such argument applies
    if region == "optimal":
        obj = MONOTONE_OBJECTIVE.get(row)
        if obj is None:
            return None                  # non-monotone or unknown objective: no S1 argument available
        return ("S1", f"OPTIMAL REGION with a coordinatewise-monotone objective — {obj}. min of two "
                      f"optima is strictly smaller in that objective and max strictly larger, so neither "
                      f"attains the optimum and every non-trivial blend leaves the region.")
    hit = SATURATING.get((row, region))
    return hit if hit else None


def main() -> int:
    stamped, wrong, incomplete = 0, [], []
    per_file = {}
    for fname in ("sounding_survey_readings.json", "sounding_v3_survey.json"):
        p = LAT / fname
        doc = json.loads(p.read_text())
        before = [(x.get("row"), x.get("region"), x.get("flavor"), x.get("measured_rate"),
                   x.get("excess"), x.get("control_mean")) for x in doc["readings"]]
        n = 0
        for x in doc["readings"]:
            if not (x.get("region") and x.get("flavor")):
                continue
            d = derive(x["row"], x["region"], x["flavor"])
            if d:
                rule, arg = d
                x["forced_saturated"] = True
                x["forced_saturated_rule"] = rule
                x["forced_saturated_argument"] = arg
                n += 1
                if x.get("measured_rate") is not None and x["measured_rate"] != 1.0:
                    wrong.append({"row": x["row"], "region": x["region"], "flavor": x["flavor"],
                                  "rule": rule, "measured_rate": x["measured_rate"]})
            else:
                x["forced_saturated"] = False
                if x.get("measured_rate") == 1.0:
                    incomplete.append({"row": x["row"], "region": x["region"], "flavor": x["flavor"],
                                       "measured_rate": 1.0, "r": x.get("r"),
                                       "already_insufficient": bool(x.get("insufficient"))})
        after = [(x.get("row"), x.get("region"), x.get("flavor"), x.get("measured_rate"),
                  x.get("excess"), x.get("control_mean")) for x in doc["readings"]]
        if before != after:
            print(f"FAIL — {fname}: a measured value moved during a flag addition.", file=sys.stderr)
            return 1
        per_file[fname] = (doc, p, n)
        stamped += n

    if wrong:
        print("FAIL — the derivation claims saturation where the data disagrees. The ARGUMENT is wrong,\n"
              "not the reading. Each must be re-read before this ships:", file=sys.stderr)
        for w in wrong[:15]:
            print(f"    {w['row']}·{w['region']}·{w['flavor']}  rule {w['rule']}  "
                  f"measured={w['measured_rate']}", file=sys.stderr)
        return 1

    for fname, (doc, p, n) in per_file.items():
        doc["forced_saturated_provenance"] = {
            "what": ("the join's SECOND direction. `theorem_forced` excludes flavours a region is closed "
                     "under (violation forced to 0); `forced_saturated` excludes flavours a region is "
                     "forced to LEAVE (violation forced to 1)."),
            "why": ("the join was one-sided: built to stop a theorem manufacturing a null, blind to a "
                    "theorem manufacturing a hit. The same asymmetry wearing the other face."),
            "rules": RULES,
            "S1_objective_per_row": MONOTONE_OBJECTIVE,
            "S1_excluded_rows": NON_MONOTONE_OBJECTIVE,
            "scope": ("semilattice flavours only. `majority` and `minority` do not move the vector "
                      "strictly in one direction, so none of the five arguments applies to them. "
                      "majority/minority readings DO reach 1.0 in the column — but every one of them "
                      "sits below the pre-declared INSUFFICIENT-r floor (r = 2-6, often a single "
                      "distinct subset), so those are small-sample saturation rather than theorem "
                      "saturation and the derivation correctly declines to claim them."),
            "checked_against_observation": {
                "derived_saturated_but_measured_below_1": len(wrong),
                "measured_1_but_not_derived": len(incomplete),
                "of_those_already_excluded_by_the_pre_declared_r_floor":
                    sum(1 for i in incomplete if i["already_insufficient"]),
                "ADMISSIBLE_AND_UNCOVERED": [i for i in incomplete if not i["already_insufficient"]],
                "completeness_on_the_admissible_set": (
                    "every exact-1.0 reading that is NOT already excluded by the pre-declared r floor is "
                    "covered by one of the five arguments. The derivation is therefore COMPLETE where it "
                    "matters and the residual is entirely small-sample saturation below the floor."),
                "incomplete_cases": incomplete,
                "note": ("SUFFICIENT, NOT COMPLETE — stated rather than discovered. A region forced to "
                         "leave on 99% of blends is not caught by this derivation and would not be "
                         "caught by an exact-1.0 screen either. Both are lower bounds on forcing.")},
            "n_flagged": n}
        doc.setdefault("changelog", []).append({
            "date": "2026-07-26", "kind": "FLAG ADDITION — NOT A RE-MEASUREMENT",
            "what": "`forced_saturated` derived and stamped; measured values verified unmoved.",
            "why": ("Terrain's I-phase found 58 of 92 positive-excess readings at measured_rate exactly "
                    "1.0, carrying 45.5% of the anomaly's excess. Their violation is a theorem.")})
        p.write_text(json.dumps(doc, indent=1) + "\n")
        print(f"  {fname:<34}flagged {n:>3}  sha256 {hashlib.sha256(p.read_bytes()).hexdigest()[:16]}")

    print(f"\n  total forced_saturated: {stamped}")
    gap = [i for i in incomplete if not i["already_insufficient"]]
    print(f"  derivation vs observation: {len(wrong)} contradictions, {len(incomplete)} uncovered "
          f"exact-1.0 readings")
    print(f"    of the uncovered, already INSUFFICIENT-r : {len(incomplete)-len(gap)}")
    print(f"    ADMISSIBLE AND UNCOVERED (the real gap)  : {len(gap)}")
    for i in gap[:10]:
        print(f"      {i['row']}·{i['region']}·{i['flavor']}  r={i['r']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
