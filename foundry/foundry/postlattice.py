"""The Boolean co-clone roster — one Creignou–Kolaitis–Zanuttini plain-basis representative per co-clone.

R-B (stratify-as-generate): the roster is the **named spine of Post's lattice**, instantiated as concrete
relation sets (CKZ plain bases), NOT an enumeration of relation-sets (2^256 at arity 3 is impossible). Each
co-clone declares its Schaefer class and carries a plain basis of actual Boolean relations; the oracles
(`oracles.py`) then **verify** the declared class by testing closure under the defining polymorphism, and check
the representative is a FAITHFUL witness (non-trivially-satisfiable where the class demands it) — a real, logged
condition-check, not a hand-asserted flag.

v1 = the distinct-profile spine (affine, Horn, dual-Horn, bijunctive, the NP-hard region) via the canon∩census
registration anchors. Finer co-clones (0-/1-valid, the S0^k/S1^k threshold chains, class intersections) share a
charge profile and are a documented v1.1 extension — never silently dropped.
"""
from dataclasses import dataclass
from itertools import product

# Schaefer classes (the declared identity of a co-clone; the oracle verifies it holds)
AFFINE, HORN, DUAL_HORN, BIJUNCTIVE, NP_HARD = "affine", "horn", "dual-horn", "bijunctive", "np-hard"


# ── polymorphisms (the algebraic closure operators that define the tractable classes) ─────────────────────
def _apply(op, rows):
    return tuple(op(*[row[i] for row in rows]) for i in range(len(rows[0])))


def _closed_under(rel, op, k):
    """Is `rel` closed under the k-ary operation `op` applied coordinate-wise?"""
    return all(_apply(op, rows) in rel for rows in product(rel, repeat=k))


_MIN = lambda a, b: a & b                              # semilattice ∧      → Horn
_MAX = lambda a, b: a | b                               # semilattice ∨      → dual-Horn
_MAJ = lambda a, b, c: (a & b) | (a & c) | (b & c)      # majority           → bijunctive (2-SAT)
_MINORITY = lambda a, b, c: a ^ b ^ c                   # affine minority    → affine (linear)

_POLY = {HORN: (_MIN, 2), DUAL_HORN: (_MAX, 2), BIJUNCTIVE: (_MAJ, 3), AFFINE: (_MINORITY, 3)}


def has_polymorphism(relations, schaefer_class):
    """A LANGUAGE has a polymorphism iff EVERY relation has it (Pol is intersection-closed)."""
    op, k = _POLY[schaefer_class]
    return all(_closed_under(r, op, k) for r in relations)


def any_tractable_polymorphism(relations):
    return any(has_polymorphism(relations, c) for c in _POLY)


def is_0valid(relations):
    return all(tuple(0 for _ in next(iter(r))) in r for r in relations)


def is_1valid(relations):
    return all(tuple(1 for _ in next(iter(r))) in r for r in relations)


# ── Marx weak separability (the Exact-Ones / CSP-by-solution-size dichotomy criterion) ──────────────────────
# Bulatov & Marx, "Constraint satisfaction parameterized by solution size", SICOMP 43 (2014) 573-616
# (arXiv:1206.4854); dichotomy: Marx, Comput. Complexity 14 (2005) 153-183. A relation R (over {0,1}) is weakly
# separable iff BOTH hold on its tuples (+ = coordinatewise OR of DISJOINT tuples; disjoint = never both 1):
#   (union)      for all disjoint t1,t2 in R:                       t1+t2 in R
#   (difference) for all disjoint t1,t2 with t2 in R and t1+t2 in R: t1 in R
# A LANGUAGE is weakly separable iff every relation is. NB weak separability IMPLIES 0-validity (difference with
# t1 = all-zero forces 0 in R), so this is a faithful check only on 0-valid relations; the parameterized ORACLE
# classifies co-clones at the CLASS level (Schaefer class), because the CKZ representatives trade 0-validity away
# for the Max/decision charges (e.g. affine's x⊕y=1 is not 0-valid, yet the affine class IS weakly separable).
def _disjoint(a, b):
    return all(not (x and y) for x, y in zip(a, b))


def _union(a, b):
    return tuple(x | y for x, y in zip(a, b))


def is_weakly_separable(relations):
    """The verified Marx/Bulatov-Marx union+difference criterion (faithful on 0-valid relations)."""
    for rel in relations:
        rows = list(rel)
        arity = len(rows[0])
        universe = list(product((0, 1), repeat=arity))
        for a in rows:                                   # union closure over disjoint pairs
            for b in rows:
                if _disjoint(a, b) and _union(a, b) not in rel:
                    return False
        for t2 in rows:                                  # difference: t2, t1+t2 in R (disjoint) => t1 in R
            for t1 in universe:
                if _disjoint(t1, t2) and _union(t1, t2) in rel and t1 not in rel:
                    return False
    return True


# ── canonical relations (each a frozenset of same-arity tuples) ───────────────────────────────────────────
def _all_except(arity, excluded):
    ex = set(excluded)
    return frozenset(t for t in product((0, 1), repeat=arity) if t not in ex)


R_XOR3 = frozenset({(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)})   # x⊕y⊕z=0   (affine)
R_XOR2 = frozenset({(0, 1), (1, 0)})                              # x⊕y=1     (affine; breaks 0/1-validity)
R_OR3 = _all_except(3, [(0, 0, 0)])                               # x∨y∨z     (dual-Horn)
R_NOR3 = _all_except(3, [(1, 1, 1)])                              # ¬x∨¬y∨¬z  (Horn)
R_TRUE = frozenset({(1,)})                                       # x=1       (unit; breaks 0-validity)
R_FALSE = frozenset({(0,)})                                      # x=0       (unit; breaks 1-validity)
R_POS2 = frozenset({(0, 1), (1, 0), (1, 1)})                     # x∨y       (bijunctive; not 0-valid)
R_NEG2 = frozenset({(0, 0), (0, 1), (1, 0)})                     # ¬x∨¬y     (bijunctive; not 1-valid)
R_NAE3 = _all_except(3, [(0, 0, 0), (1, 1, 1)])                  # not-all-equal (NP-hard)
R_1IN3 = frozenset({(1, 0, 0), (0, 1, 0), (0, 0, 1)})           # exactly-one   (NP-hard)


@dataclass(frozen=True)
class CoClone:
    id: str
    name: str
    family: str          # a FOUNDRY_SPEC problem_family
    schaefer_class: str  # declared identity — VERIFIED by the oracle's polymorphism check
    encoding: str        # the CKZ plain basis, human-readable
    relations: tuple     # the plain basis as actual relations
    anchor: bool = False  # a canon∩census registration anchor


BOOLEAN_COCLONES = [
    CoClone("xor-sat", "XOR-SAT (affine / linear over GF(2))", "affine", AFFINE,
            "plain basis {x⊕y⊕z=0, x⊕y=1}", (R_XOR3, R_XOR2), anchor=True),
    CoClone("horn-sat", "Horn-SAT", "horn", HORN,
            "plain basis {¬x∨¬y∨¬z, x=1}", (R_NOR3, R_TRUE), anchor=True),
    CoClone("dual-horn", "Dual-Horn", "dual-horn", DUAL_HORN,
            "plain basis {x∨y∨z, x=0}", (R_OR3, R_FALSE)),
    CoClone("2-sat", "2-SAT (bijunctive)", "bijunctive", BIJUNCTIVE,
            "plain basis {x∨y, ¬x∨¬y}", (R_POS2, R_NEG2), anchor=True),
    CoClone("3-sat", "3-SAT (general Boolean CSP)", "np-hard-region", NP_HARD,
            "plain basis {x∨y∨z, ¬x∨¬y∨¬z} — in none of the six Schaefer classes", (R_OR3, R_NOR3), anchor=True),
    CoClone("nae-sat", "NAE-3-SAT (not-all-equal)", "np-hard-region", NP_HARD,
            "plain basis {NAE(x,y,z)}", (R_NAE3,), anchor=True),
    CoClone("one-in-three-sat", "1-in-3-SAT", "np-hard-region", NP_HARD,
            "plain basis {1-in-3(x,y,z)}", (R_1IN3,), anchor=True),
]

REGISTRATION_ANCHORS = tuple(c.id for c in BOOLEAN_COCLONES if c.anchor)
