"""N1 v1.1 — finer Boolean tier (Sprint 3.5 Session 1).

Extends the Post's-lattice spine to co-clones deferred at N1: the 0-valid / 1-valid classes and their
intersections with the Schaefer classes. Each representative is a CONCRETE Boolean language whose charges are
COMPUTED from its polymorphisms + the verified dichotomy theorems (no declared class, no hand-assignment) — the
same verify-by-polymorphism discipline N1 uses, extended.

Why this is the enrichment path (Sprint 3.5 memo): the general-domain counting/approximation/parameterized
dichotomies are DEFER (UGC-conditional or not implementable in budget), so the census cannot grow richer via
domain-3. Boolean co-clones, by contrast, get ALL of decision/counting/approximation/parameterized/localization
filled — so every distinct-profile Boolean co-clone is a both-real (approx,param) row.

Charge rules (each a verified theorem; matches the N1 oracle, extended to 0-/1-valid):
  decision       Schaefer 1978        — P iff 0-valid, 1-valid, Horn, dual-Horn, bijunctive, or affine; else NPC.
  approximation  KSTW 2001 + Håstad   — PO iff 0-valid or 1-valid (all-0/all-1 maximises Max); inapprox iff affine
                                        and NOT 0/1-valid (Max-kLIN, Håstad); else APX-complete. (2-monotone PO
                                        cases are conservatively NOT claimed — only the certain 0/1-valid PO.)
  counting       Creignou-Hermann 96  — FP iff affine; else #P-complete.
  parameterized  Marx 2005            — FPT iff affine OR (0-valid AND weakly separable, computed faithfully on
                                        0-valid relations); else W[1] (weak separability ⟹ 0-valid).
  localization   Barto-Kozik 2014     — bounded-width iff a semilattice (min/max) or majority polymorphism (WNU
                                        of all arities); affine (minority-only) and NP-hard → unbounded.
  parallelization ABISV 2009          — verified per-class only for the pure Schaefer classes; for the finer /
                                        mixed / 0-1-valid co-clones the within-P NC/P-complete refinement is not
                                        cleanly verified here → `open` (honest), n.a. when decision is NPC (E2).
"""
from foundry import postlattice as PL
from foundry.census import derived, language, na, op


def classify_boolean(rels):
    """Compute every charge for a Boolean constraint language from its relations + the verified theorems."""
    zv, ov = PL.is_0valid(rels), PL.is_1valid(rels)
    horn = PL.has_polymorphism(rels, PL.HORN)
    dhorn = PL.has_polymorphism(rels, PL.DUAL_HORN)
    bij = PL.has_polymorphism(rels, PL.BIJUNCTIVE)
    aff = PL.has_polymorphism(rels, PL.AFFINE)
    tractable = zv or ov or horn or dhorn or bij or aff

    decision = "P" if tractable else "NPC"
    if zv or ov:
        approx = "PO"
    elif aff:
        approx = "inapprox"
    else:
        approx = "APX-complete"
    counting = "FP" if aff else "#P-complete"
    if aff or (zv and PL.is_weakly_separable(rels)):
        param = "FPT"
    else:
        param = "W[1]"
    localization = "bounded-width" if (horn or dhorn or bij) else "unbounded-width"
    parallelization = None if tractable else "n.a."   # None -> `open` cell; n.a. for NPC (E2)
    polys = [n for n, ok in (("0-valid", zv), ("1-valid", ov), ("min/Horn", horn), ("max/dualHorn", dhorn),
                             ("majority/bijunctive", bij), ("minority/affine", aff)) if ok]
    return {"decision": decision, "approximation": approx, "counting": counting, "parameterized": param,
            "localization": localization, "parallelization": parallelization, "polymorphisms": polys,
            "0valid": zv, "1valid": ov, "affine": aff, "weakly_separable": PL.is_weakly_separable(rels)}


# ── candidate finer languages (relations from postlattice; charges COMPUTED, then deduped by profile) ───────
_R = PL  # R_XOR3, R_XOR2, R_OR3, R_NOR3, R_TRUE, R_FALSE, R_POS2, R_NEG2 live in postlattice
R_XOR3_1 = frozenset({(0, 0, 1), (0, 1, 0), (1, 0, 0), (1, 1, 1)})   # x⊕y⊕z = 1 (affine, 1-valid, not 0-valid)

_CANDIDATES = [
    # id, name, encoding, relations
    ("zerovalid-affine", "0-valid affine (homogeneous XOR)", "Γ = {x⊕y⊕z=0} (0-valid, minority)", (_R.R_XOR3,)),
    ("zerovalid-horn", "0-valid Horn", "Γ = {¬x∨¬y∨¬z, x=0} (0-valid, min)", (_R.R_NOR3, _R.R_FALSE)),
    ("zerovalid-bijunctive", "0-valid bijunctive", "Γ = {¬x∨¬y} (0-valid, majority)", (_R.R_NEG2,)),
    ("onevalid-affine", "1-valid affine", "Γ = {x⊕y⊕z=1} (1-valid, minority)", (R_XOR3_1,)),
    ("onevalid-dualhorn", "1-valid dual-Horn", "Γ = {x∨y∨z, x=1} (1-valid, max)", (_R.R_OR3, _R.R_TRUE)),
    ("onevalid-bijunctive", "1-valid bijunctive", "Γ = {x∨y} (1-valid, majority)", (_R.R_POS2,)),
    ("zerovalid-dualhorn", "0-valid dual-Horn", "Γ = {x=0} (0-valid, max)", (_R.R_FALSE,)),
    ("onevalid-horn", "1-valid Horn", "Γ = {x=1} (1-valid, min)", (_R.R_TRUE,)),
]


def _row(cid, name, enc, rels):
    c = classify_boolean(rels)
    cells = [
        derived("decision", c["decision"], "CSP(Γ) satisfiability",
                theorem="Schaefer 1978", condition=f"Γ has polymorphisms {c['polymorphisms']}", cite="Schaefer, STOC 1978"),
        derived("counting", c["counting"], "#CSP(Γ): count satisfying assignments", theorem="Creignou-Hermann 1996",
                condition=("Γ is affine → Gaussian elimination" if c["affine"] else "Γ is not affine"),
                cite="Creignou & Hermann, Inf. Comput. 125 (1996)"),
        derived("approximation", c["approximation"], "Max-CSP(Γ): maximise satisfied constraints",
                theorem="KSTW 2001 / Håstad 2001",
                condition=("0-/1-valid → all-0/all-1 maximises Max → PO" if c["approximation"] == "PO"
                           else ("Max over affine (Max-kLIN) inapprox unless P=NP" if c["approximation"] == "inapprox"
                                 else "not 0-/1-valid/affine → Max-CSP APX-complete")),
                cite="Khanna-Sudan-Trevisan-Williamson, SICOMP 30 (2001); Håstad, JACM 48 (2001)"),
        derived("parameterized", c["parameterized"], "Exact-Ones CSP(Γ): satisfying assignment of weight exactly k",
                theorem="Marx 2005",
                condition=("affine is weakly separable → FPT" if c["affine"]
                           else ("0-valid and weakly separable (union+difference closure) → FPT" if c["parameterized"] == "FPT"
                                 else "not weakly separable (weak separability ⟹ 0-valid) → W[1]-complete")),
                cite="Marx, Comput. Complexity 14 (2005); Bulatov & Marx, SICOMP 43 (2014)",
                perspective="solution weight k (number of variables set to 1)"),
    ]
    if c["parallelization"] == "n.a.":
        cells.append(na("parallelization", "decision is NPC — parallelization is a within-P classification (E2)"))
    else:
        cells.append(op("parallelization", "within-P NC/P-complete — ABISV refinement not verified for this finer/mixed co-clone"))
    cells += [
        op("proof_size", "instrument column (N4)"),
        derived("localization", c["localization"], "solvable by local consistency (bounded relational width)?",
                theorem="Barto-Kozik 2014",
                condition=("has a semilattice/majority polymorphism → WNU of all arities → bounded width"
                           if c["localization"] == "bounded-width"
                           else "affine (minority-only) or NP-hard → not bounded width"),
                cite="Barto & Kozik, JACM 61 (2014)"),
        op("average_case", "instrument column (N4)"),
        op("landscape", "instrument column (N4)"),
    ]
    return language(cid, name, "constructed", enc, cells,
                    notes=f"N1 v1.1 finer Boolean co-clone (Sprint 3.5). Polymorphisms: {c['polymorphisms']}.")


def build_finer_census():
    """Build the finer-tier rows — one per DISTINCT CO-CLONE (distinct polymorphism set), matching N1's
    convention (N1 kept 7 co-clones over 4 profiles). The eight candidates are eight distinct co-clones: the
    0-valid/1-valid intersections with each Schaefer class, plus the two constant co-clones {x=0},{x=1}. Some
    share a full charge PROFILE (reported separately as the effective-n); none share a co-clone."""
    return [_row(cid, name, enc, rels) for cid, name, enc, rels in _CANDIDATES]
