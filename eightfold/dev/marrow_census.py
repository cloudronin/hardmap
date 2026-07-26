#!/usr/bin/env python3
"""Marrow v1 I0 — the census that sizes the project. Runs first, gates everything.

THE QUESTION, per row: does a CITABLE STANDARD RELATIONAL PRESENTATION exist?

WHAT THIS IS AND IS NOT. This is a SIZING pass, not the R20 pinning work. Its verdicts are judgments about
whether a standard presentation EXISTS and is citable; M1 re-derives them per row WITH citations under the
9-check. A row admitted here is a candidate, not a pin.

THE ADMISSION TEST, stated strictly because a loose one inflates the count and the count gates the project:
  STRATUM 1 (direct-csp)   the whole problem is CSP(Gamma) / homomorphism to a fixed finite structure --
                           a FINITE constraint language of BOUNDED ARITY. Not "has a coloring flavour".
  STRATUM 2 (vcsp-shaped)  Min-Ones / Max-Ones / Max-CSP over such a Gamma (KSTW), objective = a sum of
                           local cost functions. Again finite and bounded-arity.
  STRATUM 3 (promise)      the standard form is a PROMISE problem -- PCSP theory (BBKO), reserved for v1.2.
  STRATUM 4 (no-presentation) everything else, WITH A REASON. `n.a.` per the typing law, never blank.

WHY MEMBERSHIP IS ENUMERATED BY NAME RATHER THAN MATCHED BY PATTERN. A regex over problem names scored 82
rows; applying the strict test by hand removes a large fraction of them, because the boundary cases all
LOOK like members:
  * dominating-set is Min-Ones over (x_v OR the neighbourhood) -- UNBOUNDED arity, so not KSTW-shaped
  * equitable / acyclic / harmonious colouring carry GLOBAL side constraints (balance, no bichromatic
    cycle, global injectivity) that no finite-arity Gamma expresses
  * choosability quantifies over list assignments (Pi_2^p) -- not a plain CSP
  * betweenness / cyclic-ordering are ORDERING CSPs over an infinite domain (Bodirsky), a different theory
  * qcsp, stochastic-sat, succinct-sat are quantified/succinct -- different algebras
An estimate that counts those is not a census. The named lists below are auditable; anything unlisted falls
to stratum 4 and is printed for review rather than silently dropped.

NO CHARGE VALUE INFORMS ANY VERDICT HERE. The circularity carve-out: pinning a presentation is TYPING, a
definitional fact about the task text, citable from a textbook. The founding law applies unchanged.
"""
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "dev"))
from eightfold import atlas as A                                     # noqa: E402

AT = ROOT / "eightfold" / "results" / "atlas"
OUT = AT / "marrow-i0-census.jsonl"
SUMMARY = AT / "marrow-i0-census.json"

DIRECT, VCSP, PROMISE, NONE = "direct-csp", "vcsp-shaped", "promise", "no-presentation"
KILL1_FLOOR = 40

# ── THE FIXED-TEMPLATE TEST — surfaced BY the census, not settled by the spec ─────────────────────────
# Polymorphisms are computed OF A TEMPLATE. So the load-bearing admission question is not "is this row
# CSP-shaped?" but "is there a FIXED finite template whose Pol we can compute?" Where the template is part
# of the INPUT (H in graph-homomorphism, Gamma in maximum-csp, k in chromatic-number), there is no fixed
# Gamma and `poly_fingerprint_natural` is UNDEFINED on that row -- a computability fact, not a preference.
#
# The test cuts BOTH ways, which is why it is recorded rather than folded silently into the count.
VARYING_TEMPLATE = {
    "graph-homomorphism": "H is part of the input -> uniform CSP; no fixed Gamma to take Pol of",
    "generalized-graph-coloring": "target H general -> no fixed Gamma",
    "chromatic-number": "k is the OUTPUT, not a fixed template",
    "list-coloring": "k varies; fixed only at a pinned k",
    "precoloring-extension": "k varies; fixed only at a pinned k",
    "maximum-csp": "Gamma IS the input -- the framework, not an instance of it",
    "max-k-cut": "k varies",
}
# Rows with a genuinely fixed bounded-arity template that the first pass omitted. Recorded as a
# SELF-CAUGHT OMISSION rather than quietly folded in.
FIXED_TEMPLATE_OMITTED = {
    "d-hitting-set": (VCSP, "Min-Ones over {OR_d} at fixed d", "KSTW 2001; Karp 1972"),
    "k-set-packing": (VCSP, "packing over sets of size <= k -- bounded arity", "Garey-Johnson SP3"),
    "three-dimensional-matching": (DIRECT, "CSP({exactly-one-of-3}) -- 3DM", "Karp 1972; Garey-Johnson SP1"),
    "3-dimensional-assignment": (VCSP, "3DM with additive costs -- VCSP at bounded arity", "Karp 1972"),
}
# Considered and REJECTED under the fixed-template test, recorded so the boundary is auditable.
FIXED_TEMPLATE_REJECTED = {
    "subgraph-isomorphism": "binary CSP in form, but the host graph is INPUT -> template varies",
    "induced-subgraph-isomorphism": "as subgraph-isomorphism",
    "linear-equations": "CSP(affine) over a finite field, LP-shaped over Q -- the field is not pinned",
    "minmax-3d-matching": "3DM core, but a min-max objective is not a sum of local costs",
}

# ── STRATUM 1 — CSP(Gamma), finite language, bounded arity ────────────────────────────────────────────
# value = (standard presentation, source hint for M1's R20 pin)
DIRECT_CSP = {
    "sat":            ("CSP over all Boolean clause relations", "Schaefer 1978; Cook 1971"),
    "sat-3":          ("CSP({3-clause relations})", "Garey-Johnson LO1; Schaefer 1978"),
    "sat-2":          ("CSP({2-clause relations}) -- bijunctive", "Schaefer 1978; Krom 1967"),
    "horn-sat":       ("CSP(Horn clauses) -- closed under MIN", "Schaefer 1978"),
    "xor-sat":        ("CSP(affine relations over GF(2))", "Schaefer 1978"),
    "nae-sat":        ("CSP({NAE_3})", "Schaefer 1978; Garey-Johnson LO3"),
    "one-in-three-sat": ("CSP({1-in-3})", "Schaefer 1978; Garey-Johnson LO4"),
    "planar-3sat":    ("CSP({3-clauses}) with planar incidence", "Lichtenstein 1982"),
    "set-splitting":  ("CSP({NAE}) on a set system, arity bounded by set size", "Garey-Johnson SP4"),
    "exact-cover-x3c": ("CSP({exactly-one-of-3})", "Garey-Johnson SP2; Karp 1972"),
    "sharp-monotone-2sat": ("CSP(monotone 2-clauses); the COUNTING charge is separate from the "
                            "presentation question", "Valiant 1979; Provan-Ball 1983"),
    "graph-homomorphism": ("CSP(H) -- the definitional case", "Hell-Nesetril 1990; Feder-Vardi 1998"),
    "graph-3-coloring": ("CSP(K_3)", "Garey-Johnson GT4; Hell-Nesetril 1990"),
    "planar-3-coloring": ("CSP(K_3) restricted to planar inputs", "Garey-Johnson-Stockmeyer 1976"),
    "bipartiteness":  ("CSP(K_2)", "folklore; Hell-Nesetril 1990"),
    "chromatic-number": ("CSP(K_k) at each fixed k; the optimisation over k is the outer wrapper",
                         "Garey-Johnson GT4"),
    "list-coloring":  ("list homomorphism = CSP(K_k) with unary constraints", "Feder-Hell-Huang 1999"),
    "precoloring-extension": ("CSP(K_k) with unary constraints pinning a subset",
                              "Biró-Hujter-Tuza 1992"),
    "3-coloring-extension": ("CSP(K_3) with unary constraints", "Biró-Hujter-Tuza 1992"),
    "generalized-graph-coloring": ("CSP(H) for a general target H", "Hell-Nesetril 1990"),
    "succinct-3-coloring": ("CSP(K_3) over a succinctly-encoded input; the TEMPLATE is standard, the "
                            "input encoding is what moves the charge", "Papadimitriou-Yannakakis 1986"),
    "tseitin":        ("CSP(affine over GF(2)) on an expander -- the Tseitin formula IS an XOR system",
                       "Tseitin 1968; Urquhart 1987"),
}

# ── STRATUM 2 — Min-Ones / Max-Ones / Max-CSP over a finite bounded-arity Gamma (KSTW) ────────────────
VCSP_SHAPED = {
    "vertex-cover":   ("Min-Ones(x OR y) -- the canonical KSTW case", "KSTW 2001 Thm 2.14; Karp 1972"),
    "planar-vertex-cover": ("Min-Ones(x OR y), planar inputs", "Garey-Johnson 1977"),
    "independent-set": ("Max-Ones(NOT x OR NOT y)", "KSTW 2001 Thm 2.12; Karp 1972"),
    "planar-independent-set": ("Max-Ones(NOT x OR NOT y), planar inputs", "Garey-Johnson 1977"),
    "geometric-independent-set": ("Max-Ones(NOT x OR NOT y) on a geometric intersection graph",
                                  "Fowler-Paterson-Tanimoto 1981"),
    "clique":         ("Max-Ones on the complement -- Independent Set's dual", "Karp 1972"),
    "max-cut":        ("Max-CSP(XOR_2)", "KSTW 2001; Garey-Johnson-Stockmeyer 1976"),
    "max-directed-cut": ("Max-CSP(directed XOR_2)", "KSTW 2001"),
    "max-k-cut":      ("Max-CSP(disequality over a k-element domain)", "KSTW 2001"),
    "max-2sat":       ("Max-CSP({2-clauses})", "KSTW 2001; Garey-Johnson-Stockmeyer 1976"),
    "max-e3-sat":     ("Max-CSP({exact-3-clauses})", "Håstad 2001; KSTW 2001"),
    "max-2lin":       ("Max-CSP(linear equations mod 2, 2 vars)", "Håstad 2001"),
    "maximum-csp":    ("Max-CSP(Gamma) -- the framework itself", "Creignou 1995; KSTW 2001"),
    "min-sat":        ("Min-CSP over clause relations", "Kohli-Krishnamurti-Mirchandani 1994"),
    "minimum-sum-coloring": ("VCSP over CSP(K_k) with per-colour weights", "Kubicka-Schwenk 1989"),
}

# ── STRATUM 3 — promise problems; PCSP theory (BBKO), reserved for v1.2 ───────────────────────────────
PROMISE_ROWS = {
    "robust-csp": ("robust satisfiability of CSP(Gamma) -- a promise on near-satisfiable instances",
                   "Barto-Kozik 2016; Guruswami-Zhou 2012"),
}

# ── STRATUM 4 — reasons, grouped by WHY, so the boundary is auditable ─────────────────────────────────
# Rows whose name suggests membership but which fail the strict test. Every one of these would have been
# counted by a regex; each is excluded for a stated structural reason.
NEAR_MISS = {
    # unbounded arity -- not a finite bounded-arity Gamma
    "dominating-set": "Min-Ones over (x_v OR its neighbourhood) -- UNBOUNDED arity, outside KSTW's finite Gamma",
    "planar-dominating-set": "unbounded-arity neighbourhood constraint (see dominating-set)",
    "independent-dominating-set": "unbounded-arity neighbourhood constraint",
    "total-dominating-set": "unbounded-arity neighbourhood constraint",
    "roman-domination": "unbounded-arity neighbourhood constraint",
    "efficient-domination": "unbounded-arity neighbourhood constraint",
    "power-dominating-set": "unbounded-arity constraint with a propagation rule",
    "upper-domination": "unbounded-arity neighbourhood constraint",
    "capacitated-dominating-set": "unbounded arity plus capacities",
    "domatic-number": "partition into dominating sets -- unbounded arity",
    "hitting-set": "unbounded set arity",
    "d-hitting-set": "bounded at d, but the standard presentation is a set system, not a fixed template; "
                     "revisit at M1 -- this is the closest near-miss in the census",
    "set-cover": "unbounded set arity",
    "max-coverage": "unbounded set arity",
    # global side constraints no finite-arity Gamma expresses
    "equitable-coloring": "colouring core plus a GLOBAL balance constraint on class sizes",
    "acyclic-coloring": "colouring core plus a global no-bichromatic-cycle constraint",
    "harmonious-coloring": "colouring core plus global injectivity on adjacent pairs",
    "total-coloring": "colouring core over vertices AND edges with an incidence condition",
    "clique-coloring": "colouring core plus a constraint quantified over all maximal cliques",
    "hereditary-clique-coloring": "as clique-coloring, hereditarily",
    "group-coloring": "colouring core with an algebraic (group-labelled) side condition",
    "radio-coloring": "colouring core plus distance-dependent separation constraints",
    "thue-number": "colouring core plus a global non-repetitive-path condition",
    "b-chromatic-number": "colouring core plus a global b-vertex existence condition",
    "achromatic-number": "colouring core plus a global completeness condition",
    "grundy-number": "colouring core plus a greedy-order condition",
    "minimum-equivalent-digraph": "global reachability preservation",
    "connected-vertex-cover": "Min-Ones core plus a GLOBAL connectivity constraint",
    "capacitated-vertex-cover": "Min-Ones core plus capacities (not a fixed finite Gamma)",
    "partial-vertex-cover": "Min-Ones core plus a global coverage-count constraint",
    "maxmin-vertex-cover": "minimality is a global condition on the solution",
    "maximum-minimal-vertex-cover": "minimality is a global condition on the solution",
    "dissociation-number": "degree-bounded induced subgraph -- global degree condition",
    "feedback-vertex-set": "global acyclicity condition",
    "directed-feedback-vertex-set": "global acyclicity condition",
    "odd-cycle-transversal": "global condition over all odd cycles",
    "min-bisection": "cut core plus a GLOBAL balance constraint",
    "multiway-cut": "global separation condition between terminals",
    "multicut": "global separation condition between terminal pairs",
    "node-multiway-cut": "global separation condition",
    "sparsest-cut": "global ratio objective, not a sum of local costs",
    # quantified / succinct / different algebra
    "choosability": "quantifies over list assignments (Pi_2^p) -- not a plain CSP",
    "clique-choosability": "quantified over list assignments",
    "qcsp": "QUANTIFIED CSP -- surjective/quantified polymorphism theory, a different algebra",
    "stochastic-sat": "stochastic quantification -- PSPACE, different algebra",
    "succinct-sat": "succinct input encoding, not a finite-template CSP",
    "sigma2-sat": "quantified (Sigma_2) -- different algebra",
    "pi2-sat": "quantified (Pi_2) -- different algebra",
    "tqbf": "fully quantified -- PSPACE, different algebra",
    "sat-reconfiguration": "reconfiguration between solutions, not satisfiability of a template",
    "circuit-sat": "circuits are not CSP(Gamma) for a finite Gamma (unbounded gate arity)",
    "minmax-sat": "min-max objective, not a sum of local costs",
    # infinite-domain / ordering CSPs
    "betweenness": "ORDERING CSP over an infinite domain (Bodirsky infinite-domain theory)",
    "cyclic-ordering": "ordering CSP over an infinite domain",
    # proof-theoretic / procedural
    "unit-resolution": "a derivation procedure, not satisfiability of a template",
    "random-3sat-refutation": "proof complexity over a distribution, not a template",
    "tautology": "validity, the co-problem; not CSP(Gamma)",
    "php": "a propositional proof-complexity family, not a CSP instance class",
}


def load_rows():
    v3 = {e.problem_id: e for e in A.load_atlas(str(AT / "atlas_v3.jsonl"))}
    nat = []
    for line in (AT / "anatomy_v1.jsonl").read_text().splitlines():
        if line.strip():
            r = json.loads(line)
            if r["universe"] == "natural":
                nat.append(r["problem_id"])
    return v3, sorted(nat)


def classify(pid):
    if pid in FIXED_TEMPLATE_OMITTED:
        stratum, pres, src = FIXED_TEMPLATE_OMITTED[pid]
        return stratum, pres, src, None
    if pid in DIRECT_CSP:
        pres, src = DIRECT_CSP[pid]
        return DIRECT, pres, src, None
    if pid in VCSP_SHAPED:
        pres, src = VCSP_SHAPED[pid]
        return VCSP, pres, src, None
    if pid in PROMISE_ROWS:
        pres, src = PROMISE_ROWS[pid]
        return PROMISE, pres, src, None
    if pid in NEAR_MISS:
        return NONE, None, None, f"NEAR-MISS: {NEAR_MISS[pid]}"
    return NONE, None, None, ("no standard relational presentation over a finite bounded-arity "
                              "constraint language")


def main() -> int:
    v3, nat = load_rows()
    recs = []
    for pid in nat:
        stratum, pres, src, reason = classify(pid)
        rec = {"problem_id": pid, "problem_family": v3[pid].problem_family, "stratum": stratum,
               "sizing_verdict_only": True}
        if stratum == NONE:
            rec["presentation"] = "n.a."
            rec["reason"] = reason
        else:
            rec["presentation"] = pres
            rec["source_hint"] = src
            rec["note"] = "CANDIDATE for M1's R20 pin; not itself a pin"
        recs.append(rec)

    OUT.write_text("".join(json.dumps(r) + "\n" for r in recs))
    by = Counter(r["stratum"] for r in recs)
    presentable = by[DIRECT] + by[VCSP]
    fam = defaultdict(Counter)
    for r in recs:
        fam[r["problem_family"]][r["stratum"]] += 1

    # ── THE READINGS. Kill 1's verdict is NOT robust to the admission reading, so the band is reported
    # rather than a point estimate. The PRINCIPLED reading applies the fixed-template test in BOTH
    # directions: it removes rows whose template is input (where Pol is undefined) and adds the
    # fixed-template rows the first pass omitted.
    as_censused = presentable
    principled = presentable - len(VARYING_TEMPLATE)
    permissive = presentable + len(FIXED_TEMPLATE_REJECTED)
    readings = {
        "PRINCIPLED — fixed template required, omissions corrected": {
            "n": principled,
            "kill_1": "CLEARS" if principled >= KILL1_FLOOR else "FIRES",
            "rule": ("a row is admissible iff a FIXED finite bounded-arity template exists. Removes the "
                     f"{len(VARYING_TEMPLATE)} varying-template rows (Pol is UNDEFINED there); the "
                     f"{len(FIXED_TEMPLATE_OMITTED)} self-caught omissions are already counted in."),
            "recommended": True},
        "AS-CENSUSED — CSP-shaped, template-fixedness not applied": {
            "n": as_censused,
            "kill_1": "CLEARS" if as_censused >= KILL1_FLOOR else "FIRES",
            "rule": "admits CSP-shaped rows whether or not the template is fixed"},
        "PERMISSIVE — also admits varying-template and unpinned-field rows": {
            "n": permissive,
            "kill_1": "CLEARS" if permissive >= KILL1_FLOOR else "FIRES",
            "rule": (f"adds the {len(FIXED_TEMPLATE_REJECTED)} rows rejected by the fixed-template test "
                     "(subgraph-isomorphism kin, unpinned field, min-max objective)")},
    }

    doc = {"schema": "marrow-i0-census/v1", "prereg": "prereg_v15", "milestone": "M0a",
           "what_this_is": ("a SIZING pass. Verdicts say a standard presentation EXISTS and is citable; "
                            "M1 re-derives each per row WITH citations under the 9-check. A row admitted "
                            "here is a candidate, not a pin."),
           "admission_test": ("STRICT: a FINITE constraint language of BOUNDED ARITY. Rows with "
                              "unbounded-arity constraints, global side conditions, quantification, or "
                              "infinite domains are excluded WITH REASONS, even where the name suggests "
                              "membership."),
           "no_charge_consulted": ("no charge value informed any verdict. Pinning a presentation is "
                                   "TYPING -- a definitional fact about the task text."),
           "n_rows": len(recs), "by_stratum": dict(by),
           "presentable_strata_1_2": presentable,
           "THE_FIXED_TEMPLATE_AMBIGUITY": {
               "status": "SURFACED BY THE CENSUS — Marrow §1 does not settle it; it is an owner ruling",
               "why_it_is_load_bearing": (
                   "polymorphisms are computed OF A TEMPLATE. Where the template is part of the input "
                   "(H in graph-homomorphism, Gamma in maximum-csp, k in chromatic-number), there is no "
                   "fixed Gamma and `poly_fingerprint_natural` is UNDEFINED on that row. That is a "
                   "computability fact, not a stylistic preference — and it decides Kill 1."),
               "varying_template_rows": VARYING_TEMPLATE,
               "self_caught_omissions_added": {k: v[1] for k, v in FIXED_TEMPLATE_OMITTED.items()},
               "considered_and_rejected": FIXED_TEMPLATE_REJECTED,
               "verdict_is_not_robust": (
                   f"PRINCIPLED {principled} FIRES / AS-CENSUSED {as_censused} FIRES / "
                   f"PERMISSIVE {permissive} CLEARS — the reading decides the project")},
           "readings": readings,
           "kill_1": {"floor": KILL1_FLOOR, "observed_principled": principled,
                      "observed_as_censused": as_censused,
                      "verdict": "CLEARS" if principled >= KILL1_FLOOR else "FIRES",
                      "verdict_basis": "the PRINCIPLED reading (recommended); see `readings` for the band",
                      "consequence_if_fires": ("Marrow ships as a census note, not a build; the finding "
                                               "'the natural atlas is presentation-poor' is itself a "
                                               "statement about where closure anatomy can exist")},
           "near_misses_excluded": len([r for r in recs if r.get("reason", "").startswith("NEAR-MISS")]),
           "regex_estimate_replaced": {"planning_estimate": 82,
                                       "census": presentable,
                                       "note": ("the planning figure was a regex over problem names. The "
                                                "strict test removes rows the pattern accepted: "
                                                "unbounded-arity domination and set-cover families, "
                                                "colourings with global side constraints, quantified "
                                                "variants, and ordering CSPs.")},
           "per_family": {f: dict(c) for f, c in sorted(fam.items(), key=lambda kv: -sum(kv[1].values()))}}
    SUMMARY.write_text(json.dumps(doc, indent=1) + "\n")

    print("MARROW v1 — I0 CENSUS  (sizing pass; M1 re-derives with citations)\n")
    print(f"{'stratum':<20}{'n':>5}")
    for s in (DIRECT, VCSP, PROMISE, NONE):
        print(f"{s:<20}{by[s]:>5}")
    print(f"{'TOTAL':<20}{len(recs):>5}   (must equal 345)")
    print(f"\nTHE READINGS — Kill 1's verdict is not robust to the admission rule (floor {KILL1_FLOOR}):")
    for label, r in readings.items():
        mark = "  <== RECOMMENDED" if r.get("recommended") else ""
        print(f"  {r['n']:>4}  {r['kill_1']:<7} {label}{mark}")
    print(f"\nKILL 1 (principled reading) -> {doc['kill_1']['verdict']}")
    print(f"  planning regex estimate was 82; the census gives {principled}")
    print(f"  near-misses excluded with stated reasons: {doc['near_misses_excluded']}")
    print(f"\nper family (direct / vcsp / promise / none):")
    for f, c in doc["per_family"].items():
        print(f"  {f:<18}{c.get(DIRECT,0):>4}{c.get(VCSP,0):>6}{c.get(PROMISE,0):>8}{c.get(NONE,0):>7}")
    print(f"\nwrote {OUT.name} ({len(recs)} rows) + {SUMMARY.name}")
    print(f"  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
