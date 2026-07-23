"""Prism v1 (prereg_v32) — multi-charge table on the natural arity-<=3 Boolean roster (Lattice v3's 90 symmetry
classes). Every charge is a `derived` oracle value; ONLY netted residuals are findings (r25 / prism_matrix).

R20-pinned (prereg_v32 I_phase_verdicts):
  decision        Schaefer 1978        P iff any tractable polymorphism, else NPC.
  counting        Creignou-Hermann 96  FP iff affine, else #P-complete.
  localization    Barto-Kozik 2014     CORRECTED: bounded-width iff (0-valid OR 1-valid) OR Horn OR dual-Horn OR
                                       bijunctive — trivial-satisfiability FIRST (finer's naive horn|dh|bij misses
                                       39 arity-3 0/1-valid rels). Affine obstruction vacuous at arity<=3 single-rel.
  parallelization ABISV 2009           co-clone-level: NP-hard->n.a.; (Horn|dual-Horn) & !(bij|affine)->P-complete;
                                       else NC. CAVEAT: not a pure invariant at the ABISV R2 boundary (documented).
  approx_counting Dyer-Goldberg-Jerrum affine->FP; else IM2 (=Horn AND dual-Horn = min&max-closed)->#BIS-equivalent;
                                       else->#SAT-equivalent.
  approximation   KSTW (objective_oracles)   Max-Ones / Min-Ones, objective-dependent (two columns).
  parameterized   Marx general (objective_oracles)  FPT iff weakly separable (Def 2.1), else W[1].
"""
from itertools import permutations, product

from foundry import objective_oracles as OO
from foundry import postlattice as PL


# ── roster: all non-trivial arity-<=3 Boolean relations, symmetry-deduped (coordinate permutation) ──────────
def all_relations(max_arity=3):
    for a in range(1, max_arity + 1):
        universe = list(product((0, 1), repeat=a))
        m = 2 ** a
        for mask in range(1, 2 ** m - 1):                       # non-empty, non-full
            yield a, frozenset(universe[i] for i in range(m) if (mask >> i) & 1)


def canonical(a, rel):
    best = None
    for sigma in permutations(range(a)):
        permuted = tuple(sorted(tuple(t[sigma[i]] for i in range(a)) for t in rel))
        if best is None or permuted < best:
            best = permuted
    return (a, best)


def symmetry_classes(max_arity=3):
    """One representative relation per coordinate-permutation orbit + the orbit (class) size."""
    orbit = {}
    for a, rel in all_relations(max_arity):
        orbit.setdefault(canonical(a, rel), []).append((a, rel))
    return [(members[0][0], members[0][1], len(members)) for members in orbit.values()]


# ── the per-relation charges (all objective-independent except approximation) ───────────────────────────────
def _flags(rels):
    return {"0valid": PL.is_0valid(rels), "1valid": PL.is_1valid(rels),
            "horn": PL.has_polymorphism(rels, PL.HORN), "dualhorn": PL.has_polymorphism(rels, PL.DUAL_HORN),
            "bijunctive": PL.has_polymorphism(rels, PL.BIJUNCTIVE), "affine": PL.has_polymorphism(rels, PL.AFFINE),
            "width2affine": PL.is_width2affine(rels), "strongly0valid": PL.is_strongly_0valid(rels),
            "IHSB": PL.is_IHSB(rels), "general_wsep": PL.is_weakly_separable_general(rels)}


def decision(f):
    return "P" if (f["0valid"] or f["1valid"] or f["horn"] or f["dualhorn"] or f["bijunctive"] or f["affine"]) else "NPC"


def counting(f):
    return "FP" if f["affine"] else "#P-complete"


def bounded_width(f):
    """CORRECTED (I3): trivial-satisfiability first, THEN the semilattice/majority polymorphisms."""
    return "bounded-width" if (f["0valid"] or f["1valid"] or f["horn"] or f["dualhorn"] or f["bijunctive"]) \
        else "unbounded-width"


def parallelization(f):
    """co-clone-level ABISV (I1 caveat: not a pure invariant at the R2 boundary)."""
    if decision(f) == "NPC":
        return "n.a."
    if (f["horn"] or f["dualhorn"]) and not (f["bijunctive"] or f["affine"]):
        return "P-complete"
    return "NC"


def approx_counting(f):
    """DGJ trichotomy (I2): affine->FP; else IM2 (Horn AND dual-Horn)->#BIS-equivalent; else->#SAT-equivalent."""
    if f["affine"]:
        return "FP"
    if f["horn"] and f["dualhorn"]:
        return "#BIS-equivalent"
    return "#SAT-equivalent"


def charges(rel):
    """The full per-relation charge dict for a single Boolean relation `rel` (frozenset of tuples). Approximation
    is objective-dependent (two keys); everything else is objective-independent."""
    rels = [rel]
    f = _flags(rels)
    apx_max, par_max = OO.charges(rels, OO.MAX_ONES)   # (approx, param) — param is objective-independent
    apx_min, _ = OO.charges(rels, OO.MIN_ONES)
    par = par_max if par_max != "open" else ("open" if apx_min == "feasibility-hard" else OO.parameterized(rels))
    return {"decision": decision(f), "counting": counting(f), "localization": bounded_width(f),
            "parallelization": parallelization(f), "approx_counting": approx_counting(f),
            "approx_maxones": apx_max, "approx_minones": apx_min, "parameterized": par, "flags": f}


# the predicate set each charge reads (for the PER-PAIR shared-input netting; prereg_v32 netting design)
CHARGE_INPUTS = {
    "decision": {"0valid", "1valid", "horn", "dualhorn", "bijunctive", "affine"},
    "counting": {"affine"},
    "localization": {"0valid", "1valid", "horn", "dualhorn", "bijunctive"},
    "parallelization": {"0valid", "1valid", "horn", "dualhorn", "bijunctive", "affine"},
    "approx_counting": {"affine", "horn", "dualhorn"},
    "approx_maxones": {"0valid", "1valid", "horn", "dualhorn", "bijunctive", "affine", "width2affine", "strongly0valid", "IHSB"},
    "approx_minones": {"0valid", "1valid", "horn", "dualhorn", "bijunctive", "affine", "width2affine", "strongly0valid", "IHSB"},
    "parameterized": {"general_wsep"},
}


def build_roster(max_arity=3):
    """Return [(arity, rel, class_size, charges_dict)] over the symmetry classes."""
    out = []
    for a, rel, size in symmetry_classes(max_arity):
        out.append((a, rel, size, charges(rel)))
    return out


def selftest_prism(verbose=False):
    """Hand-value CI gate: the I3 correction fires; the witness charges hold; NPI holds. 0 = pass."""
    R_0val = frozenset({(0, 0, 0), (0, 1, 1), (1, 1, 0)})   # {000,011,110}: 0-valid, not horn/dh/bij/affine (I3 witness)
    OR2 = frozenset({(0, 1), (1, 0), (1, 1)}); NAND = frozenset({(0, 0), (0, 1), (1, 0)})
    checks = [
        ("I3 witness {000,011,110} bounded-width", bounded_width(_flags([R_0val])), "bounded-width"),
        ("  naive (horn|dh|bij) would say", "unbounded-width" if not (_flags([R_0val])["horn"] or _flags([R_0val])["dualhorn"] or _flags([R_0val])["bijunctive"]) else "?", "unbounded-width"),
        ("approx_counting XOR3 (affine)->FP", approx_counting(_flags([PL.R_XOR3])), "FP"),
        ("approx_counting OR2 (not affine, not IM2)", approx_counting(_flags([OR2])), "#SAT-equivalent"),
        ("approx_counting NAND", approx_counting(_flags([NAND])), "#SAT-equivalent"),
        ("witness VC=Min-Ones(OR2) approx", charges(OR2)["approx_minones"], "APX-complete"),
        ("witness IS=Max-Ones(NAND) approx", charges(NAND)["approx_maxones"], "poly-APX-complete"),
        ("witness VC param", charges(OR2)["parameterized"], "FPT"),
        ("witness IS param", charges(NAND)["parameterized"], "W[1]"),
    ]
    bad = [(n, g, e) for n, g, e in checks if g != e]
    if verbose or bad:
        for n, g, e in checks:
            print(f"  {'ok ' if g == e else 'BAD'} {n}: got={g} exp={e}")
    return 1 if bad else 0


if __name__ == "__main__":
    import sys
    sys.exit(selftest_prism(verbose=True))
