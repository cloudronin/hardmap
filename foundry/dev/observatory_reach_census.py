#!/usr/bin/env python3
"""The observatory reach census — all 345 natural rows. THE STANDING BUILD'S FIRST MOTION.

WHAT THIS ASKS, and it is NOT what Marrow's I0 asked. Marrow asked *can a relational template be pinned?*
and found 34 presentable rows. This asks *can the observatory generate instances and compute dials?* —
a strictly different question, and the survey already proved they diverge: `set-cover`, `knapsack`,
`dominating-set` are all Marrow-excluded and were fully surveyed anyway, because the probe enumerates
solutions directly and does not care whether a finite template exists.

CENSUS MINIMALISM GOVERNS. This computes reach classification and ramp declarations. It reads the atlas
and the fleet. It reads NO outcome artifact — no excess, no overlap, no hull, no violation rate.

═══ WHAT IS A TYPING AND WHAT IS A MEASUREMENT — the distinction this census must not blur ═══════════

  BUILT is a MEASUREMENT: the generator exists in the fleet or it does not, and the census imports it.
  Every other class is a TYPING: a declared rule over the row's family and identity, recording which
  rule fired. A typing is a claim about THE OBSERVATORY'S REACH, not about the problem, and it is
  falsified the moment someone builds a generator for a row typed unreachable.

Rows no rule types are `UNTYPED` and are COUNTED, never guessed. Marrow's spec warned that a regex over
problem names is not a census; the same warning applies here, so the rule that fired is recorded per row
and the untyped count is reported as a first-class number rather than absorbed.

═══ RAMPED BY DEFAULT ═══════════════════════════════════════════════════════════════════════════════

Every reachable row is captured along a RAMP, not at a point. The ramp parameter is declared PER FAMILY
here, at census, so no row's dial is chosen after seeing its readings. Point-capture is the exception and
requires the census to find no natural dial — recorded with its reason.
"""
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "dev"))
LAT = ROOT / "foundry" / "results" / "lattice"
AT = ROOT.parent / "eightfold" / "eightfold" / "results" / "atlas"
OUT = LAT / "observatory_reach_census.json"

# ── FAMILY RAMP PARAMETERS, DECLARED AT CENSUS ───────────────────────────────────────────────────────
# The knob that tightens constraints. Chosen per family before any row is captured, so no dial is
# selected after seeing readings. Where a family's rows need per-row knobs, the family names the KIND
# and the row's builder declares the values at birth.
FAMILY_RAMP = {
    "sat-csp":          {"param": "clause/variable ratio", "kind": "constraint density",
                         "precedent": "sat-2, sat-3, horn-sat, xor-sat, nae-sat in v3"},
    "graph":            {"param": "edge density", "kind": "constraint density",
                         "precedent": "vertex-cover, independent-set, dominating-set, fvs, oct in v3"},
    "optimization":     {"param": "constraint-to-ground-set ratio", "kind": "constraint density",
                         "precedent": "set-cover (n sets), hitting-set (n sets) in v3"},
    "number-theoretic": {"param": "capacity fraction or value range", "kind": "feasibility tightness",
                         "precedent": "knapsack (capacity fraction), subset-sum (value range) in v3"},
    "string":           {"param": "pattern/text length ratio", "kind": "constraint density",
                         "precedent": "none yet — declared here, first use at build"},
    "algebraic":        {"param": "system density (equations per unknown)", "kind": "constraint density",
                         "precedent": "xor-sat's ratio ramp is the nearest analogue"},
    "matrix":           {"param": "fill density", "kind": "constraint density", "precedent": "none yet"},
    "lattice":          {"param": "dimension", "kind": "size", "precedent": "none yet",
                         "caution": "a size knob is NOT a constraint-tightness knob; flagged"},
    "geometric":        {"param": "point density", "kind": "constraint density", "precedent": "none yet",
                         "caution": "most geometric rows are continuous and unreachable regardless"},
    "logic-proof":      {"param": None, "kind": None,
                         "why": "the object is a derivation, not a solution set — outside this "
                                "instrument. The proof census reads these rows."},
}

# ── THE TYPING RULES, declared. Each row records which fired. ────────────────────────────────────────
SUBSET_PAT = re.compile(
    r"cover|set|matching|independent|clique|packing|cut|subset|partition|selection|dominating|"
    r"vertex|edge|hitting|knapsack|scheduling|transversal|feedback|clustering|colou?ring-number|"
    r"spanning|flow|path|cycle|tree|arborescence|steiner|bin|bipartite", re.I)
ASSIGN_PAT = re.compile(r"sat\b|sat-|csp|colou?ring|assignment|labell?ing|homomorphism|constraint", re.I)
PERM_PAT = re.compile(
    r"tsp|travel|tour|hamilton|sequenc|ordering|arrangement|isomorph|permutation|alignment|"
    r"superstring|sorting|schedul.*order", re.I)
CONT_PAT = re.compile(r"euclid|geometr|planar-embed|convex|polygon|nearest-neighbou?r|metric", re.I)


def type_row(pid, family):
    """Return (reach_class, rule, note). A TYPING, never a measurement."""
    if family == "logic-proof":
        return ("OUT-proof-object", "R5-family-logic-proof",
                "the object is a derivation, not a solution set; the proof census reads these")
    if family == "geometric" or CONT_PAT.search(pid):
        return ("OUT-continuous", "R6-continuous-or-geometric",
                "no finite discrete solution region at fixed size")
    if PERM_PAT.search(pid):
        return ("REACH-permutation", "R4-permutation-or-ordering",
                "solutions are orderings; ambient is n! rather than 2^n, so enumeration is limited to "
                "very small n and the dial panel is thin")
    if family == "sat-csp" or ASSIGN_PAT.search(pid):
        return ("REACH-assignment", "R2-assignment",
                "solutions are variable assignments over a small domain; ambient |D|^n")
    if SUBSET_PAT.search(pid):
        return ("REACH-subset", "R3-subset-selection",
                "solutions are subsets of a ground set; ambient 2^n, enumerable at n <= ~20")
    if family in ("number-theoretic", "optimization", "graph", "algebraic", "matrix", "lattice"):
        return ("UNTYPED", "no-rule-fired",
                f"family `{family}` is plausibly reachable but the row's identity matched no declared "
                f"pattern — needs adjudication, not a guess")
    return ("UNTYPED", "no-rule-fired", "no declared rule matched")


def main() -> int:
    marrow = {}
    for line in (AT / "marrow-i0-census.jsonl").read_text().splitlines():
        if line.strip():
            r = json.loads(line)
            marrow[r["problem_id"]] = r
    nat = [json.loads(l) for l in (AT / "anatomy_v1.jsonl").read_text().splitlines() if l.strip()]
    nat = [r for r in nat if r["universe"] == "natural"]

    # BUILT is a MEASUREMENT — imported from the fleet, not asserted
    import sounding_v2 as S2, sounding_v3_survey as S3, sounding_survey as SV
    built = set(S2.ROWS) | set(S3.RAMP) | set(SV.EXTRA)

    rows, unresolved = [], []
    for r in nat:
        pid = r["problem_id"]
        fam = marrow.get(pid, {}).get("problem_family")
        if pid in built:
            cls, rule, note = ("BUILT", "R1-generator-exists-in-fleet",
                               "generator imported from the fleet; reach is measured, not typed")
        else:
            cls, rule, note = type_row(pid, fam)
        ramp = FAMILY_RAMP.get(fam, {"param": None, "kind": None,
                                     "why": f"no ramp declared for family `{fam}`"})
        reachable = cls.startswith("BUILT") or cls.startswith("REACH")
        point_only = bool(reachable and ramp.get("param") is None)
        rec = {"problem_id": pid, "family": fam,
               "marrow_stratum": marrow.get(pid, {}).get("stratum"),
               "reach_class": cls, "rule_fired": rule, "note": note,
               "reachable": reachable,
               "capture": ("RAMPED" if (reachable and not point_only) else
                           ("POINT" if point_only else "n.a. — not reachable")),
               "ramp_parameter": ramp.get("param") if reachable else None,
               "ramp_kind": ramp.get("kind") if reachable else None,
               "point_capture_reason": ("the census found no natural dial for family "
                                        f"`{fam}`" if point_only else None)}
        rows.append(rec)
        if cls == "UNTYPED":
            unresolved.append(rec)

    by_class = Counter(r["reach_class"] for r in rows)
    by_cap = Counter(r["capture"] for r in rows)
    fam_class = {}
    for r in rows:
        fam_class.setdefault(r["family"], Counter())[r["reach_class"]] += 1

    doc = {"schema": "observatory-reach-census/v1",
           "STATUS": "CENSUS — classification and ramp declaration. No readings, no dials, no outcome read.",
           "what_this_asks": ("can the observatory generate instances and compute dials on this row — "
                              "NOT whether a relational template can be pinned. Marrow asked the second "
                              "question and found 34 presentable rows; the survey then measured "
                              "set-cover, knapsack and dominating-set, all Marrow-excluded, because the "
                              "probe enumerates solutions directly."),
           "typing_vs_measurement": ("BUILT is a MEASUREMENT — the generator exists in the fleet and is "
                                     "imported. Every other class is a TYPING: a declared rule over "
                                     "family and identity, recording which rule fired. A typing is a "
                                     "claim about the OBSERVATORY'S REACH, not about the problem, and it "
                                     "is falsified the moment someone builds a generator for a row typed "
                                     "unreachable."),
           "untyped_are_counted_not_guessed": ("Marrow's spec warned that a regex over problem names is "
                                               "not a census. Rows no rule types are UNTYPED and "
                                               "reported as a first-class number."),
           "ramped_by_default": ("every reachable row is captured along a ramp. The ramp parameter is "
                                 "declared PER FAMILY here, at census, so no row's dial is chosen after "
                                 "seeing its readings. Point-capture is the exception and requires the "
                                 "census to find no natural dial."),
           "family_ramp_parameters": FAMILY_RAMP,
           "n_rows": len(rows),
           "by_reach_class": dict(by_class.most_common()),
           "by_capture_mode": dict(by_cap.most_common()),
           "n_reachable": sum(1 for r in rows if r["reachable"]),
           "n_untyped": len(unresolved),
           "by_family": {k: dict(v.most_common()) for k, v in sorted(fam_class.items(), key=lambda z: str(z[0]))},
           "rows": rows}
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    print("THE OBSERVATORY REACH CENSUS — 345 natural rows\n")
    print(f"  {'reach class':<22}{'n':>5}")
    for k, v in by_class.most_common():
        print(f"  {k:<22}{v:>5}")
    print(f"\n  reachable : {doc['n_reachable']} of {len(rows)}")
    print(f"  UNTYPED   : {len(unresolved)}   (counted, not guessed)")
    print(f"\n  capture mode: {dict(by_cap.most_common())}")
    print(f"\n  {'family':<18}{'BUILT':>7}{'subset':>8}{'assign':>8}{'perm':>6}{'proof':>7}"
          f"{'cont':>6}{'untyped':>9}")
    for fam, c in sorted(fam_class.items(), key=lambda z: -sum(z[1].values())):
        print(f"  {str(fam):<18}{c['BUILT']:>7}{c['REACH-subset']:>8}{c['REACH-assignment']:>8}"
              f"{c['REACH-permutation']:>6}{c['OUT-proof-object']:>7}{c['OUT-continuous']:>6}"
              f"{c['UNTYPED']:>9}")
    print(f"\n  family ramp parameters declared at census:")
    for fam, spec in FAMILY_RAMP.items():
        p = spec.get("param") or "— (not reachable)"
        print(f"    {fam:<18}{p}")
    print(f"\nwrote {OUT.name}  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
