#!/usr/bin/env python3
"""Adjudicate the reach census's 105 UNTYPED rows. Per-row, with the reason recorded. CENSUS MINIMALISM.

The first-pass census typed 240 of 345 by declared rules and left 105 UNTYPED rather than guessing them.
This adjudicates those 105 one at a time. It reads the atlas and the census; it reads NO outcome artifact.

TWO REFINEMENTS THE READING PRODUCED, and both move whole subclasses:

  1. A COUNTING PROBLEM'S REGION IS THE SET BEING COUNTED. `sharp-acyclic-orientations` counts acyclic
     orientations, and the SET of acyclic orientations is exactly a region this instrument can enumerate
     and blend. The `#` in front of a problem changes what the CHARGE asks, not whether the object has a
     region. Five graph rows and two others move from apparently-regionless to reachable on this.

  2. THE REGIONLESS CLASS IS NARROWER THAN THE FIRST PASS SUGGESTED, and sharper for it. It is exactly the
     rows whose answer is a single value with no set behind it — `primality` (a bit), `gcd` (one integer),
     `discrete-log` (one exponent), `matrix-multiplication` (one matrix). `factoring` sits here too: the
     factorisation is unique up to order, so its "region" has one member and uniqueness kills blending —
     the same fact Q6 recorded for well-posed Sudoku at instance scale.

THE LATTICE QUESTION, ruled binding by the owner and answered here rather than deferred: `dimension` was
declared as lattice's ramp at census, and dimension is THE SIZE AXIS. Finite-size scaling needs ramp and
size as independent knobs, so a family whose only dial is size has NO RAMP AT ALL, not a strange one.
Adjudicated below on whether a constraint dial exists at fixed dimension.
"""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "dev"))
LAT = ROOT / "foundry" / "results" / "lattice"
CENSUS = LAT / "observatory_reach_census.json"
OUT = LAT / "observatory_untyped_adjudication.json"

# ── PER-ROW ADJUDICATION. class, and the reason, which IS the artifact. ──────────────────────────────
A = {}


def put(cls, reason, *rows):
    for r in rows:
        A[r] = (cls, reason)


# ── REACH-subset: a solution is a subset of a ground set (vertices, edges, elements) ─────────────────
put("REACH-subset", "a solution is a vertex or edge SUBSET of the input graph; ambient 2^|V| or 2^|E|",
    "densest-k-subgraph", "dissociation-number", "high-degree-subgraph", "maximum-common-subgraph",
    "maximum-planar-subgraph", "min-bisection", "cluster-deletion", "cluster-editing",
    "connectivity-augmentation", "minimum-equivalent-digraph", "minimum-fill-in", "interval-completion",
    "graph-motif", "maximum-agreement-forest", "graph-spanner", "efficient-domination",
    "roman-domination", "upper-domination", "domatic-number", "firefighter", "graph-burning",
    "register-sufficiency", "maximum-feasible-linear-subsystem", "max-dispersion", "network-interdiction",
    "survivable-network-design", "minimum-sum-of-squares", "facility-location",
    "capacitated-facility-location", "k-center", "k-median", "3sum", "minimum-distance-code",
    "nearest-codeword", "graph-sandwich-pi-property", "deadlock-detection", "and-or-graph-accessibility")

# ── REACH-assignment: a solution assigns each element a value from a small domain ────────────────────
put("REACH-assignment", "a solution assigns each vertex/position a value from a small domain; ambient |D|^n",
    "achromatic-number", "b-chromatic-number", "chromatic-number", "choosability", "grundy-number",
    "thue-number", "arrowing", "generalized-ramsey-number", "closest-string", "closest-substring",
    "integer-programming", "quadratic-congruences", "integer-expression-membership",
    "sharp-acyclic-orientations", "sharp-eulerian-orientations", "sharp-contingency-tables",
    "linear-equations", "minimum-consistent-dfa")

# ── REACH-permutation: solutions are orderings; ambient n!, so enumeration is thin ───────────────────
put("REACH-permutation", "a solution is an ORDERING or tour; ambient n! rather than 2^n, so the dial "
                         "panel is thin and only very small n is enumerable",
    "bandwidth", "pagenumber", "minimum-latency", "mixed-chinese-postman", "orienteering",
    "stacker-crane", "vehicle-routing", "weighted-tardiness", "kemeny-rank-aggregation",
    "breadth-depth-search", "sharp-linear-extensions", "sharp-antichains", "sharp-eulerian-circuits",
    "string-folding", "lz78-compression", "boxicity", "thickness", "crossing-number", "graph-genus",
    "pebbling-number", "broadcast-time", "chip-firing-stabilization")

# ── REGIONLESS: a single answer with no set behind it. Uniqueness kills blending — Q6's fact, per row. ─
put("REGIONLESS-unique-answer",
    "the answer is a single value with no set behind it, so there is no region to blend. This is the "
    "scope theorem, not a gap: the observatory measures solution-set geometry and applies to "
    "search-shaped problems, not evaluation-shaped ones",
    "primality", "gcd", "discrete-log", "quadratic-residuosity", "matrix-multiplication",
    "gaussian-elimination-pivoting", "determinant", "factoring", "edit-distance")

put("REGIONLESS-language-membership",
    "the object is a LANGUAGE property (emptiness, universality, inequivalence), not a set of solutions "
    "to enumerate. A yes/no about an automaton has no region",
    "dfa-intersection-emptiness", "nfa-universality", "regex-squaring-inequivalence",
    "integer-expression-inequivalence", "planarity", "bounded-pcp")

# ── OUT-continuous ───────────────────────────────────────────────────────────────────────────────────
put("OUT-continuous", "the feasible set is continuous; no finite discrete region at fixed size",
    "linear-programming", "bilevel-integer-programming", "two-stage-adjustable-robust", "min-max-regret",
    "competitive-facility-location", "strong-nash-equilibrium")

# ── the genuinely open ones, kept open ───────────────────────────────────────────────────────────────
put("STILL-UNTYPED",
    "no confident typing. Recorded as open rather than forced into a nearby class — the same discipline "
    "that left 105 untyped in the first pass rather than guessing them",
    "network-reliability", "permanent", "tutte-polynomial")

# ── LATTICE: the binding question, answered ─────────────────────────────────────────────────────────
LATTICE_REASON = (
    "DIMENSION WAS DECLARED AS THIS FAMILY'S RAMP AT CENSUS AND DIMENSION IS THE SIZE AXIS. Finite-size "
    "scaling needs ramp and size as INDEPENDENT knobs, so a family whose only dial is size has no ramp at "
    "all rather than a strange one — a size axis must not impersonate a hardening axis. "
    "Adjudicated: at FIXED dimension these rows do have candidate constraint dials — the approximation "
    "factor gamma for SVP/CVP (the region {v : |v| <= gamma * lambda_1} widens as gamma rises), and the "
    "noise rate / modulus ratio for LWE and SIS. Those are genuine tightness knobs. BUT the ambient is "
    "unbounded integer vectors, so no finite region exists until a coefficient bound is pinned, and that "
    "is an ENCODING CHOICE this census has not made. Typed `no-natural-dial-at-fixed-encoding`: the dial "
    "candidate is named so a future build can pin it, and DIMENSION IS BARRED as the ramp regardless.")
put("no-natural-dial-at-fixed-encoding", LATTICE_REASON,
    "shortest-vector-svp", "closest-vector-cvp", "lwe", "sis")


def main() -> int:
    cen = json.loads(CENSUS.read_text())
    untyped = [r for r in cen["rows"] if r["reach_class"] == "UNTYPED"]
    ids = {r["problem_id"] for r in untyped}

    missing = sorted(ids - set(A))
    extra = sorted(set(A) - ids)
    if missing:
        print(f"FAIL — {len(missing)} untyped rows have no adjudication. Adjudicating 105 means all 105:",
              file=sys.stderr)
        for m in missing[:25]:
            print(f"    {m}", file=sys.stderr)
        return 1
    if extra:
        print(f"FAIL — {len(extra)} adjudications name rows that are not untyped: {extra[:10]}",
              file=sys.stderr)
        return 1

    out = []
    for r in untyped:
        cls, reason = A[r["problem_id"]]
        reachable = cls.startswith("REACH")
        out.append({"problem_id": r["problem_id"], "family": r["family"],
                    "was": "UNTYPED", "now": cls, "reason": reason,
                    "reachable": reachable,
                    "capture": "RAMPED" if reachable else "n.a. — not reachable",
                    "ramp_parameter": r["ramp_parameter"] if reachable else None})

    by = Counter(x["now"] for x in out)
    newly = sum(1 for x in out if x["reachable"])
    total_reach = cen["n_reachable"] + newly

    doc = {"schema": "observatory-untyped-adjudication/v1",
           "STATUS": "CENSUS ADJUDICATION — no readings, no dials, no outcome artifact read.",
           "input": f"the {len(untyped)} rows the reach census left UNTYPED rather than guessing",
           "completeness_is_asserted": ("every untyped row is adjudicated or the script halts. "
                                        "Adjudicating 105 means all 105."),
           "refinement_1_counting_problems": (
               "A COUNTING PROBLEM'S REGION IS THE SET BEING COUNTED. `sharp-acyclic-orientations` counts "
               "acyclic orientations and that SET is exactly a region this instrument enumerates and "
               "blends. The `#` changes what the CHARGE asks, not whether the object has a region."),
           "refinement_2_regionless_is_narrower": (
               "the regionless class is exactly the rows whose answer is a single value with no set "
               "behind it. `factoring` belongs there: the factorisation is unique up to order, so its "
               "region has one member and uniqueness kills blending — Q6's fact at row scale."),
           "lattice_ruling": LATTICE_REASON,
           "by_class": dict(by.most_common()),
           "newly_reachable": newly,
           "reachable_before": cen["n_reachable"],
           "reachable_after": total_reach,
           "still_untyped": by.get("STILL-UNTYPED", 0),
           "adjudications": out}
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    print("ADJUDICATING THE 105 UNTYPED\n")
    print(f"  {'class':<36}{'n':>5}")
    for k, v in by.most_common():
        print(f"  {k:<36}{v:>5}")
    print(f"\n  newly reachable   : {newly}")
    print(f"  reachable before  : {cen['n_reachable']} of 345")
    print(f"  reachable AFTER   : {total_reach} of 345")
    print(f"  still untyped     : {by.get('STILL-UNTYPED', 0)}   (kept open, not forced)")
    print(f"\n  build queue depth : {total_reach - 27} rows beyond the 27 already built")
    print(f"\nwrote {OUT.name}  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
