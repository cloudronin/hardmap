"""Lattice (G2) objective oracles — the approximation + parameterized charges for a single-relation
(Boolean relation, objective) pair. R20-pinned to docs/findings/Lattice-I-phase.md:

- approximation: KSTW Thm 2.12 (Max-Ones) / Thm 2.14 (Min-Ones), strict priority lists (§1-2). Objective-DEPENDENT.
- parameterized: Marx Exact-Ones / Bulatov-Marx OCSP solution-size (exactly-k), FPT iff weakly separable
  (Marx 2005 Def 2.1 general form; §9). Objective-INDEPENDENT — a property of the relation (OCSP({R})). This
  supersedes the L1 §6 direction speculation: §9 pinned the charge as exact-k OCSP (BM14), which is one problem
  per relation, not a per-objective ≤k/≥k value. The witness confirms exact-k = natural for VC/IS.

feasibility-hard rows (SAT(Γ) NP-hard) carry parameterized = `open` (cannot parameterize an infeasible search;
prereg_v29 decision 4).
"""
from foundry import postlattice as PL

MAX_ONES, MIN_ONES = "max-ones", "min-ones"

# KSTW-native approximation vocab, easy->hard (prereg_v29 decisions 1-2; ordinal caveat travels with any rank stat)
APPROX_ORDER = ("PO", "APX-complete", "Min-Horn-Deletion-complete", "Nearest-Codeword-complete",
                "poly-APX-complete", "decidable-not-approximable", "feasibility-hard")
PARAM_ORDER = ("FPT", "W[1]")


def _affine(rels): return PL.has_polymorphism(rels, PL.AFFINE)
def _horn(rels): return PL.has_polymorphism(rels, PL.HORN)             # weakly negative
def _dualhorn(rels): return PL.has_polymorphism(rels, PL.DUAL_HORN)    # weakly positive
def _bijunctive(rels): return PL.has_polymorphism(rels, PL.BIJUNCTIVE)  # 2CNF


def approximation_maxones(rels):
    """KSTW Thm 2.12 (Max-Ones) — strict priority list. `rels` = the language (a single relation for Lattice)."""
    if PL.is_1valid(rels) or _dualhorn(rels) or PL.is_width2affine(rels):
        return "PO"
    if _affine(rels):
        return "APX-complete"
    if PL.is_strongly_0valid(rels) or _horn(rels) or _bijunctive(rels):
        return "poly-APX-complete"
    if PL.is_0valid(rels):
        return "decidable-not-approximable"
    return "feasibility-hard"


def approximation_minones(rels):
    """KSTW Thm 2.14 (Min-Ones) — strict priority list."""
    if PL.is_0valid(rels) or _horn(rels) or PL.is_width2affine(rels):
        return "PO"
    if _bijunctive(rels) or PL.is_IHSB(rels):
        return "APX-complete"
    if _affine(rels):
        return "Nearest-Codeword-complete"
    if _dualhorn(rels):
        return "Min-Horn-Deletion-complete"
    if PL.is_1valid(rels):
        return "poly-APX-complete"
    return "feasibility-hard"


def approximation(rels, objective):
    return approximation_maxones(rels) if objective == MAX_ONES else approximation_minones(rels)


def parameterized(rels):
    """OCSP / Exact-Ones solution-size charge (BM14 exact-k), objective-independent. FPT iff weakly separable
    (Marx Def 2.1 general form, faithful on 0-invalid single relations)."""
    return "FPT" if PL.is_weakly_separable_general(rels) else "W[1]"


def charges(rels, objective):
    """(approximation, parameterized) for a (relation-language, objective) row. Parameterized is `open` when the
    approximation is feasibility-hard (prereg_v29 decision 4)."""
    apx = approximation(rels, objective)
    par = "open" if apx == "feasibility-hard" else parameterized(rels)
    return apx, par


def selftest_objective_oracles(verbose=False):
    """Witness gate + occupancy print over the Boolean co-clone relations. Returns 0 iff the witness passes."""
    OR2 = frozenset({(0, 1), (1, 0), (1, 1)}); NAND = frozenset({(0, 0), (0, 1), (1, 0)})
    # WITNESS: VC = Min-Ones(OR2) = (APX-complete, FPT); IS = Max-Ones(NAND) = (poly-APX-complete, W[1])
    vc = charges([OR2], MIN_ONES)
    is_ = charges([NAND], MAX_ONES)
    witness_ok = (vc == ("APX-complete", "FPT")) and (is_ == ("poly-APX-complete", "W[1]"))
    print(f"  WITNESS  VC=Min-Ones(OR2)={vc}  IS=Max-Ones(NAND)={is_}  -> {'PASS' if witness_ok else 'FAIL'}")
    if verbose:
        rels = {"XOR3": PL.R_XOR3, "XOR2(x!=y)": PL.R_XOR2, "NOR3(Horn)": PL.R_NOR3, "TRUE(x=1)": PL.R_TRUE,
                "OR3(dualHorn)": PL.R_OR3, "FALSE(x=0)": PL.R_FALSE, "OR2(VC)": PL.R_POS2, "NAND(IS)": PL.R_NEG2,
                "NAE3": PL.R_NAE3, "1IN3": PL.R_1IN3}
        print(f"\n  {'relation':14s} {'Max-Ones (approx,param)':30s} {'Min-Ones (approx,param)':30s}")
        profiles = set(); nrows = 0
        for name, R in rels.items():
            cmax = charges([R], MAX_ONES); cmin = charges([R], MIN_ONES)
            print(f"  {name:14s} {str(cmax):30s} {str(cmin):30s}")
            for c in (cmax, cmin):
                if c[1] != "open":
                    profiles.add(c); nrows += 1
        print(f"\n  both-real rows={nrows}  distinct profiles={len(profiles)}  (prereg floor: rows>=15 AND profiles>=6)")
        print(f"  profiles: {sorted(profiles)}")
    return 0 if witness_ok else 1


if __name__ == "__main__":
    selftest_objective_oracles(verbose=True)
