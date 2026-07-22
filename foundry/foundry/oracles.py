"""Dichotomy oracles — assign each co-clone's charges by the verified classification theorems.

Each oracle VERIFIES the co-clone's declared Schaefer class (polymorphism closure + faithfulness: a non-trivial
tractable witness must not be 0-/1-valid, else its Max is trivially PO), then emits a `derived` cell whose
logged `condition_check` records the computed check and whose `side` equals the value (FOUNDRY_SPEC gate 6b).
The parameterized column is filled by the Marx dichotomy (Sprint 2.1, class-level: FPT iff weakly separable).
proof_size/Molloy and the measured instrument columns (average_case, landscape) remain `open` — honest, not
guessed (I-phase discipline).
"""
from foundry import postlattice as PL
from foundry.census import derived, language, na, op


def verify_class(cc):
    """Verify the co-clone's declared class + faithfulness. Returns [] if OK, else error strings."""
    errs, rels = [], cc.relations
    if cc.schaefer_class == PL.NP_HARD:
        if PL.any_tractable_polymorphism(rels):
            errs.append(f"{cc.id}: declared NP-hard but HAS a tractable polymorphism")
    else:
        if not PL.has_polymorphism(rels, cc.schaefer_class):
            errs.append(f"{cc.id}: declared {cc.schaefer_class} but not closed under its polymorphism")
        if PL.is_0valid(rels) or PL.is_1valid(rels):
            errs.append(f"{cc.id}: representative is 0-/1-valid — Max trivially PO, not a faithful "
                        f"{cc.schaefer_class} witness")
    return errs


def classify(cc):
    """Return the ChargeCells for co-clone `cc`, charged by the verified dichotomies."""
    k = cc.schaefer_class
    tractable = k != PL.NP_HARD
    cells = []

    # decision — Schaefer 1978
    cells.append(derived("decision", "P" if tractable else "NPC", "CSP(Γ) satisfiability",
                         theorem="Schaefer 1978",
                         condition=(f"Γ is in the tractable class '{k}'" if tractable
                                    else "Γ is in none of the six Schaefer classes"),
                         cite="Schaefer, STOC 1978"))
    # counting — Creignou-Hermann 1996: FP iff affine
    cells.append(derived("counting", "FP" if k == PL.AFFINE else "#P-complete",
                         "#CSP(Γ): count satisfying assignments", theorem="Creignou-Hermann 1996",
                         condition=("Γ is affine → Gaussian elimination" if k == PL.AFFINE else "Γ is not affine"),
                         cite="Creignou & Hermann, Inf. Comput. 125 (1996)"))
    # approximation — KSTW 2001 (+ Håstad 2001 for affine)
    if k == PL.AFFINE:
        aval, acond, acite = ("inapprox", "Max over affine (Max-3LIN) has no constant-factor approx unless P=NP",
                              "Håstad, JACM 48 (2001)")
    else:
        aval, acond, acite = ("APX-complete", "Γ is not 0-/1-valid nor 2-monotone → Max-CSP APX-complete",
                              "Khanna-Sudan-Trevisan-Williamson, SICOMP 30 (2001)")
    cells.append(derived("approximation", aval, "Max-CSP(Γ): maximise satisfied constraints",
                         theorem="KSTW 2001 / Håstad 2001", condition=acond, cite=acite))
    # parallelization — ABISV 2009 (within-P); n.a. for NPC (E2)
    if not tractable:
        cells.append(na("parallelization", "decision is NPC — parallelization is a within-P classification (E2)"))
    elif k in (PL.HORN, PL.DUAL_HORN):
        cells.append(derived("parallelization", "P-complete", "within-P: is CSP(Γ) in NC?",
                             theorem="ABISV 2009", condition=f"{k}-SAT (unit propagation) is P-complete",
                             cite="Allender-Bauland-Immerman-Schnoor-Vollmer, JCSS 75 (2009)"))
    else:  # affine ∈ ⊕L, bijunctive ∈ NL — both ⊆ NC
        cells.append(derived("parallelization", "NC", "within-P: is CSP(Γ) in NC?",
                             theorem="ABISV 2009",
                             condition=f"{k} is in {'⊕L' if k == PL.AFFINE else 'NL'} ⊆ NC",
                             cite="Allender-Bauland-Immerman-Schnoor-Vollmer, JCSS 75 (2009)"))
    # localization — Barto-Kozik 2014: bounded width iff a weak-NU polymorphism exists (obstruction = affine)
    if k in (PL.HORN, PL.DUAL_HORN, PL.BIJUNCTIVE):
        lval, lcond = "bounded-width", f"{k} has a weak-NU polymorphism (min/max/majority)"
    else:
        lval, lcond = "unbounded-width", ("affine expresses linear equations (the sole bounded-width obstruction)"
                                          if k == PL.AFFINE else "NP-hard → not bounded width")
    cells.append(derived("localization", lval, "solvable by local consistency (bounded relational width)?",
                         theorem="Barto-Kozik 2014", condition=lcond, cite="Barto & Kozik, JACM 61 (2014)"))
    # parameterized — Marx 2005 (parameterized Schaefer dichotomy): Exact-Ones CSP(Γ) (a satisfying assignment
    # of weight exactly k, parameterized by k) is FPT iff Γ is weakly separable, else W[1]-complete. The verdict
    # is CLASS-level (like counting): weak separability implies 0-validity, and the CKZ representatives trade
    # 0-validity away for the Max/decision charges, so a naive per-relation check would misfire (affine's x⊕y=1
    # is not 0-valid, yet affine IS weakly separable). Only affine is weakly separable among these co-clones.
    if k == PL.AFFINE:
        pval, pcond = "FPT", "affine is weakly separable (Bulatov-Marx) → Exact-Ones CSP(Γ) is FPT"
    elif k in (PL.HORN, PL.DUAL_HORN, PL.BIJUNCTIVE):
        pval, pcond = "W[1]", (f"{k} contains implication x→y, which fails the difference condition of weak "
                               f"separability → Exact-Ones W[1]-complete (decision is P, but the weight-k "
                               f"restriction is W[1]-hard)")
    else:  # np-hard-region
        pval, pcond = "W[1]", ("Γ is in none of the tractable Schaefer classes, a fortiori not weakly separable "
                               "→ Exact-Ones W[1]-complete (W[1]-membership holds even though decision is NP-complete)")
    cells.append(derived("parameterized", pval,
                         "Exact-Ones CSP(Γ): a satisfying assignment of weight exactly k, parameterized by k",
                         theorem="Marx 2005 (parameterized Schaefer dichotomy)", condition=pcond,
                         cite="Marx, Comput. Complexity 14 (2005) 153-183; Bulatov & Marx, SICOMP 43 (2014) 573-616 (arXiv:1206.4854)",
                         perspective="solution weight k (number of variables set to 1)"))
    # deferred (verified dichotomy exists, per-co-clone check not computed) + measured → open (honest)
    cells.append(op("proof_size", "random Γ-instance refutation size — Molloy (needs the N4 ensemble design, I5)"))
    cells.append(op("average_case", "random Γ-ensemble difficulty — measured instrument column (N4)"))
    cells.append(op("landscape", "random Γ-ensemble solution geometry — measured instrument column (N4)"))
    return cells


def census_row(cc):
    """Build a ProblemEntry (census row) for co-clone `cc` (verify its class first)."""
    errs = verify_class(cc)
    if errs:
        raise ValueError("; ".join(errs))
    notes = "Registration anchor (canon∩census overlap)." if cc.anchor else None
    return language(cc.id, cc.name, cc.family, cc.encoding, classify(cc), notes=notes)


def build_boolean_census():
    """The N1 Boolean census: one verified, charged row per co-clone in the roster."""
    return [census_row(cc) for cc in PL.BOOLEAN_COCLONES]
