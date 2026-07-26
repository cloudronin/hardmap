#!/usr/bin/env python3
"""Marrow v1 M1 — pin each presentable row's STANDARD RELATIONAL PRESENTATION as a COMPUTABLE template.

WHAT M1 ADDS OVER THE I0 CENSUS. The census recorded prose ("Min-Ones(x OR y)"). M2 needs a template it can
take polymorphisms OF, so every row here carries `template = {domain, relations}` with the relations written
out as explicit tuple-sets. Writing them out is what makes the admission test checkable rather than asserted
-- and it immediately caught six census over-admissions (below).

THE CIRCULARITY CARVE-OUT, unchanged: pinning a presentation is TYPING -- a definitional fact about the task
text, citable from a textbook, derived WITHOUT consulting a charge cell. No charge value informs any pin.

M1'S CLOSER LOOK CORRECTED THE CENSUS DOWNWARD, 34 -> 28. The census excluded `set-cover`, `hitting-set` and
the domination family for UNBOUNDED ARITY. Writing out the actual constraint scopes shows six ADMITTED rows
fail the same test:
  exact-cover-x3c / three-dimensional-matching / 3-dimensional-assignment
      variables are the sets/triples, and the per-ELEMENT constraint ranges over every set containing that
      element -- unbounded, exactly the shape that excluded set-cover
  k-set-packing
      sets are bounded at k, but an ELEMENT sits in unboundedly many sets and the at-most-one constraint is
      over those
  set-splitting
      one NAE constraint per SET, and sets have unbounded size (only the 3-set restriction is NAE-3SAT)
  minimum-sum-coloring
      colours come from an UNBOUNDED palette, so there is no fixed finite domain
THREE OF THE FOUR "self-caught omissions" the census ADDED are in that list. Only `d-hitting-set` was
correctly added. Recorded rather than quietly re-dropped: a sizing pass that corrects itself downward at the
next resolution is the pass working, but the direction of the correction has to be on the record.

STATUS OF THESE PINS: DRAFTED, awaiting owner sitting -- the same pattern as the Quarry v2 Channel B fills.
The citations name where the standard form is established; they have NOT been through the 9-check dual pass.
"""
import hashlib
import json
import sys
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
AT = ROOT / "eightfold" / "results" / "atlas"
OUT = AT / "marrow-presentations.jsonl"
SUMMARY = AT / "marrow-presentations.json"


# ── relation constructors, so every template below is generated rather than typed ─────────────────────
def clause(k):
    """All width-k clause relations: {0,1}^k minus its single falsifying assignment, one per sign pattern."""
    return [[list(t) for t in product((0, 1), repeat=k) if list(t) != list(a)]
            for a in product((0, 1), repeat=k)]


def horn(k):
    """Clauses with AT MOST ONE positive literal. A clause is falsified by the complement of its signs, so
    'at most one positive' means the falsifying assignment has at most one 0."""
    return [[list(t) for t in product((0, 1), repeat=k) if list(t) != list(a)]
            for a in product((0, 1), repeat=k) if sum(1 for x in a if x == 0) <= 1]


def parity(k, bit):
    return [list(t) for t in product((0, 1), repeat=k) if sum(t) % 2 == bit]


def monotone_or(k):
    """(x_1 OR ... OR x_k) -- no negations. Falsified only by all-zero."""
    return [list(t) for t in product((0, 1), repeat=k) if any(t)]


NEQ2 = [[0, 1], [1, 0]]                                   # K_2 / max-cut / x XOR y = 1
NAND2 = [[0, 0], [0, 1], [1, 0]]                          # NOT x OR NOT y -- independent set
OR2 = [[0, 1], [1, 0], [1, 1]]                            # x OR y -- vertex cover, monotone 2-clause
DICUT = [[0, 1]]                                          # NOT x AND y -- max directed cut
NAE3 = [list(t) for t in product((0, 1), repeat=3) if len(set(t)) > 1]
ONE_IN_3 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
NEQ3 = [[a, b] for a in range(3) for b in range(3) if a != b]      # K_3
UNARY3 = [[[c]] for c in range(3)]                                 # conservative: all unary relations


def T(domain, **rels):
    return {"domain": domain, "relations": rels}


# ── the pins ──────────────────────────────────────────────────────────────────────────────────────────
# (stratum, prose, template, citation, instance_restriction)
D, V = "direct-csp", "vcsp-shaped"
PINS = {
    # --- Boolean CSPs -------------------------------------------------------------------------------
    "sat": (D, "CSP over all Boolean clause relations", T(2, clauses3=clause(3), clauses2=clause(2)),
            "Cook 1971; Schaefer 1978 (the clause language is the definitional form)", None),
    "sat-3": (D, "CSP({3-clause relations})", T(2, clauses3=clause(3)),
              "Garey-Johnson LO1; Schaefer 1978", None),
    "sat-2": (D, "CSP({2-clause relations}) -- bijunctive", T(2, clauses2=clause(2)),
              "Krom 1967; Schaefer 1978", None),
    "planar-3sat": (D, "CSP({3-clause relations}); planarity restricts INSTANCES, not the template",
                    T(2, clauses3=clause(3)), "Lichtenstein 1982", "planar incidence graph"),
    "horn-sat": (D, "CSP(Horn clauses) -- closed under MIN", T(2, horn3=horn(3), horn2=horn(2)),
                 "Schaefer 1978; Dowling-Gallier 1984", None),
    "xor-sat": (D, "CSP(affine relations over GF(2))",
                T(2, xor3_even=[parity(3, 0)], xor3_odd=[parity(3, 1)],
                  xor2_even=[parity(2, 0)], xor2_odd=[parity(2, 1)]),
                "Schaefer 1978 (affine case)", None),
    "tseitin": (D, "CSP(affine over GF(2)) -- a Tseitin formula IS an XOR system on a graph",
                T(2, xor3_even=[parity(3, 0)], xor3_odd=[parity(3, 1)]),
                "Tseitin 1968; Urquhart 1987", "expander instances"),
    "nae-sat": (D, "CSP({NAE_3})", T(2, nae3=[NAE3]), "Schaefer 1978; Garey-Johnson LO3", None),
    "one-in-three-sat": (D, "CSP({1-in-3})", T(2, one_in_3=[ONE_IN_3]),
                         "Schaefer 1978; Garey-Johnson LO4", None),
    "sharp-monotone-2sat": (D, "CSP({monotone 2-clause}); the COUNTING charge is a separate question from "
                            "the presentation", T(2, mon2=[OR2]),
                            "Valiant 1979; Provan-Ball 1983", None),
    "bipartiteness": (D, "CSP(K_2) -- 2-colouring", T(2, neq=[NEQ2]),
                      "folklore; Hell-Nesetril 1990 as the H=K_2 case", None),
    # --- domain-3 CSPs ------------------------------------------------------------------------------
    "graph-3-coloring": (D, "CSP(K_3)", T(3, neq=[NEQ3]), "Garey-Johnson GT4; Hell-Nesetril 1990", None),
    "planar-3-coloring": (D, "CSP(K_3); planarity restricts INSTANCES, not the template", T(3, neq=[NEQ3]),
                          "Garey-Johnson-Stockmeyer 1976", "planar input graphs"),
    "succinct-3-coloring": (D, "CSP(K_3) over a SUCCINCTLY ENCODED input -- the template is standard; the "
                            "encoding is what moves the charge", T(3, neq=[NEQ3]),
                            "Papadimitriou-Yannakakis 1986", "succinct (circuit) input encoding"),
    "3-coloring-extension": (D, "CSP(K_3) with unary constraints -- the conservative/list form",
                             T(3, neq=[NEQ3], unaries=UNARY3),
                             "Biro-Hujter-Tuza 1992; Feder-Hell-Huang 1999", None),
    # --- VCSP-shaped (KSTW): the template is the CONSTRAINT language; the objective sits on top -------
    "vertex-cover": (V, "Min-Ones(x OR y) -- the canonical KSTW case", T(2, or2=[OR2]),
                     "KSTW 2001 Thm 2.14; Karp 1972", None),
    "planar-vertex-cover": (V, "Min-Ones(x OR y); planar instances", T(2, or2=[OR2]),
                            "Garey-Johnson 1977", "planar input graphs"),
    "independent-set": (V, "Max-Ones(NOT x OR NOT y)", T(2, nand2=[NAND2]),
                        "KSTW 2001 Thm 2.12; Karp 1972", None),
    "planar-independent-set": (V, "Max-Ones(NOT x OR NOT y); planar instances", T(2, nand2=[NAND2]),
                               "Garey-Johnson 1977", "planar input graphs"),
    "geometric-independent-set": (V, "Max-Ones(NOT x OR NOT y) on an intersection graph",
                                  T(2, nand2=[NAND2]), "Fowler-Paterson-Tanimoto 1981",
                                  "geometric intersection graphs"),
    "clique": (V, "Max-Ones(NOT x OR NOT y) on the complement -- Independent Set's dual",
               T(2, nand2=[NAND2]), "Karp 1972", "complement graph"),
    "d-hitting-set": (V, "Min-Ones over {OR_d}; pinned at d=3", T(2, or3=[monotone_or(3)]),
                      "KSTW 2001; Karp 1972 (as set cover's dual)", "sets of size <= d, pinned d=3"),
    "max-cut": (V, "Max-CSP(x XOR y = 1)", T(2, neq=[NEQ2]),
                "KSTW 2001; Garey-Johnson-Stockmeyer 1976", None),
    "max-directed-cut": (V, "Max-CSP(NOT x AND y)", T(2, dicut=[DICUT]), "KSTW 2001", None),
    "max-2sat": (V, "Max-CSP({2-clauses})", T(2, clauses2=clause(2)),
                 "KSTW 2001; Garey-Johnson-Stockmeyer 1976", None),
    "max-e3-sat": (V, "Max-CSP({exact-3-clauses})", T(2, clauses3=clause(3)),
                   "Hastad 2001; KSTW 2001", None),
    "max-2lin": (V, "Max-CSP(linear equations mod 2 in 2 variables)",
                 T(2, xor2_even=[parity(2, 0)], xor2_odd=[parity(2, 1)]), "Hastad 2001", None),
    "min-sat": (V, "Min-CSP over clause relations", T(2, clauses3=clause(3), clauses2=clause(2)),
                "Kohli-Krishnamurti-Mirchandani 1994", None),
}

# Census over-admissions caught by writing the templates out. Recorded, not silently dropped.
M1_DEMOTED = {
    "exact-cover-x3c": "variables are the sets; the per-ELEMENT constraint ranges over every set containing "
                       "that element -- UNBOUNDED arity, the same shape that excluded set-cover",
    "three-dimensional-matching": "per-element constraint over every triple containing it -- UNBOUNDED",
    "3-dimensional-assignment": "3DM with costs; inherits the unbounded per-element constraint",
    "k-set-packing": "sets are bounded at k, but an ELEMENT sits in unboundedly many sets and the "
                     "at-most-one constraint ranges over those -- UNBOUNDED",
    "set-splitting": "one NAE constraint per SET, and sets have unbounded size (only the 3-set restriction "
                     "is NAE-3SAT)",
    "minimum-sum-coloring": "colours are drawn from an UNBOUNDED palette -- no fixed finite domain",
}


def main() -> int:
    census = {r["problem_id"]: r for r in
              (json.loads(l) for l in (AT / "marrow-i0-census.jsonl").read_text().splitlines() if l.strip())}
    summ = json.loads((AT / "marrow-i0-census.json").read_text())
    varying = set(summ["THE_FIXED_TEMPLATE_AMBIGUITY"]["varying_template_rows"])
    principled = sorted(p for p, r in census.items()
                        if r["stratum"] in ("direct-csp", "vcsp-shaped") and p not in varying)

    missing = [p for p in principled if p not in PINS and p not in M1_DEMOTED]
    assert not missing, f"principled rows with no pin and no demotion reason: {missing}"

    recs = []
    for pid in sorted(PINS):
        stratum, prose, tmpl, cite, restriction = PINS[pid]
        recs.append({"problem_id": pid, "stratum": stratum, "presentation": prose,
                     "template": tmpl, "domain_size": tmpl["domain"],
                     "n_relations": sum(len(v) for v in tmpl["relations"].values()),
                     "max_arity": max(len(t) for v in tmpl["relations"].values() for r in v for t in r),
                     "instance_restriction": restriction,
                     "restriction_note": ("the template does NOT see this restriction — any closure-derived "
                                          "value is the UNRESTRICTED one" if restriction else None),
                     "citation": cite, "provenance_status": "cited",
                     "status": "DRAFTED — awaiting owner sitting; not yet 9-check dual-passed"})
    OUT.write_text("".join(json.dumps(r) + "\n" for r in recs))

    doc = {"schema": "marrow-presentations/v1", "prereg": "prereg_v15", "milestone": "M1",
           "n_pinned": len(recs),
           "census_principled_count": len(principled),
           "M1_closer_look": {
               "correction": f"{len(principled)} -> {len(recs)}",
               "why": ("writing the templates out as tuple-sets made the bounded-arity test CHECKABLE "
                       "rather than asserted, and six admitted rows failed the same test the census used "
                       "to exclude set-cover / hitting-set / the domination family"),
               "demoted": M1_DEMOTED,
               "self_correction_direction": (
                   "THREE OF THE FOUR 'self-caught omissions' the census ADDED are in the demoted list "
                   "(k-set-packing, three-dimensional-matching, 3-dimensional-assignment). Only "
                   "d-hitting-set was correctly added. The census's additions were less reliable than its "
                   "exclusions, which is worth knowing about the next sizing pass."),
               "verdict_unaffected": ("Kill 1 had already fired at 34 against a floor of 40; it fires "
                                      "harder at 28. Terroir-C was already declared INSUFFICIENT under "
                                      "every reading. No verdict moves.")},
           "by_domain": {str(d): sum(1 for r in recs if r["domain_size"] == d) for d in (2, 3)},
           "instance_restricted_rows": {r["problem_id"]: r["instance_restriction"]
                                        for r in recs if r["instance_restriction"]},
           "audit_prediction_stated_in_advance": (
               "the presentation audit (Quarry v3 §4) compares the closure-derived decision value against "
               "the cited cell. DISAGREEMENTS SHOULD CONCENTRATE ON THE INSTANCE-RESTRICTED ROWS, because "
               "the template cannot see a restriction on inputs. `succinct-3-coloring` is the sharpest "
               "case: its template is K_3 exactly as plain 3-colouring, so closure derives NPC while the "
               "cited charge is far higher — a DISAGREEMENT BY CONSTRUCTION, and a scope limit of closure "
               "anatomy rather than an errata candidate. Stated before the audit runs."),
           "status": "DRAFTED for owner sitting — the Quarry v2 Channel B pattern",
           "rows": [r["problem_id"] for r in recs]}
    SUMMARY.write_text(json.dumps(doc, indent=1) + "\n")

    print(f"MARROW M1 — presentations pinned as COMPUTABLE templates\n")
    print(f"census principled : {len(principled)}")
    print(f"M1 closer look    : {len(recs)}   ({len(M1_DEMOTED)} demoted for unbounded arity / unbounded domain)")
    print(f"  demoted: {', '.join(sorted(M1_DEMOTED))}\n")
    print(f"{'row':<28}{'dom':>4}{'rels':>6}{'arity':>7}  restriction")
    for r in recs:
        print(f"{r['problem_id']:<28}{r['domain_size']:>4}{r['n_relations']:>6}{r['max_arity']:>7}  "
              f"{r['instance_restriction'] or ''}")
    print(f"\nwrote {OUT.name} ({len(recs)} rows)  sha256 "
          f"{hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
