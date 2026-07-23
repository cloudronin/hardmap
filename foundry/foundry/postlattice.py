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
from itertools import combinations, product

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


# ── Lattice (G2): relation-level predicates for the KSTW Max-Ones / Min-Ones oracle (L1 §3-6) ──────────────
# Lattice rows are SINGLE-relation languages, so these classify a single relation (a language = every relation
# has the property). is_width2affine / is_IHSB are CUT-OUT tests: R has property P iff the conjunction of the
# P-clauses satisfied by every tuple of R cuts out exactly R. NB `is_2monotone` is deliberately NOT here — it
# is the Max-CSP/Min-CSP PO condition, not a Max-Ones/Min-Ones one (owner spec-defect #3, Pebble methods thread).
def _inter(a, b):
    return tuple(x & y for x, y in zip(a, b))


def _cutout(rel, clause_gens):
    rows = list(rel)
    n = len(rows[0])
    held = [fn for _, fn in clause_gens(n) if all(fn(t) for t in rows)]
    return frozenset(t for t in product((0, 1), repeat=n) if all(fn(t) for fn in held)) == rel


def _w2affine_clauses(n):
    for i in range(n):
        for c in (0, 1):
            yield (("u", i, c), (lambda t, i=i, c=c: t[i] == c))
    for i in range(n):
        for j in range(i + 1, n):
            for c in (0, 1):
                yield (("b", i, j, c), (lambda t, i=i, j=j, c=c: (t[i] ^ t[j]) == c))


def is_width2affine(relations):
    """KSTW PO condition (both axes): every relation cut out by <=2-variable GF(2) equations (x_i=c, x_i^x_j=c)."""
    return all(_cutout(r, _w2affine_clauses) for r in relations)


def is_strongly_0valid(relations):
    """KSTW Max-Ones poly-APX condition: every relation satisfied by ALL weight-<=1 assignments (0 + every e_i)."""
    for rel in relations:
        n = len(next(iter(rel)))
        if tuple(0 for _ in range(n)) not in rel:
            return False
        if any(tuple(1 if j == i else 0 for j in range(n)) not in rel for i in range(n)):
            return False
    return True


def _ihsb_plus_clauses(n):
    for r in range(1, n + 1):                                   # positive clauses OR(S), width <= n (= B, finite)
        for S in combinations(range(n), r):
            yield (("pos", S), (lambda t, S=S: any(t[i] == 1 for i in S)))
    for i in range(n):                                          # implications ¬x_i ∨ x_j
        for j in range(n):
            if i != j:
                yield (("imp", i, j), (lambda t, i=i, j=j: t[i] == 0 or t[j] == 1))
    for i in range(n):                                          # negative units ¬x_i
        yield (("neg", i), (lambda t, i=i: t[i] == 0))


def _is_ihsb_plus(rel):
    return _cutout(rel, _ihsb_plus_clauses)


def _is_ihsb_minus(rel):
    return _is_ihsb_plus(frozenset(tuple(1 - x for x in t) for t in rel))   # IHS-B- iff complement is IHS-B+


def is_IHSB(relations):
    """KSTW Min-Ones APX condition: the language is uniformly IHS-B+ (all rels) or uniformly IHS-B- (all rels)."""
    return all(_is_ihsb_plus(r) for r in relations) or all(_is_ihsb_minus(r) for r in relations)


# ── Marx Def 2.1 general weak separability (relation-level; faithful on 0-INVALID relations) ────────────────
# Marx, Comput. Complexity 14 (2005), Definition 2.1 — the GENERAL form. Distinct from is_weakly_separable
# above, which is the 0-VALID simplified form (Marx Lemma 2.2 / Bulatov-Marx Def 3.2). The census uses the
# 0-valid form at the CLASS level (correct there); Lattice's SINGLE relations are 0-invalid, so it needs the
# general Def 2.1. The UNION condition is GUARDED (fires only when the intersection is satisfying) -> does not
# require or imply 0-validity. Exact-Ones({R}) is FPT iff R is weakly separable (Marx Thm 3.2), else W[1].
def _xor3(a, b, c):
    return tuple(x ^ y ^ z for x, y, z in zip(a, b, c))


def _proper_subset(a, b):
    return a != b and all(x <= y for x, y in zip(a, b))


def is_weakly_separable_general(relations):
    """Marx 2005 Def 2.1 (general): (1) guarded union — (x1&x2)∈R ⇒ (x1|x2)∈R; (2) difference — x1⊊x2⊊x3 ⇒
    (x1^x2^x3)∈R. Language weakly separable iff every relation is. Faithful on 0-invalid relations."""
    for rel in relations:
        rows = list(rel)
        for a in rows:                                          # (1) GUARDED union
            for b in rows:
                if _inter(a, b) in rel and _union(a, b) not in rel:
                    return False
        for x1 in rows:                                         # (2) difference over proper 3-chains
            for x2 in rows:
                if not _proper_subset(x1, x2):
                    continue
                for x3 in rows:
                    if _proper_subset(x2, x3) and _xor3(x1, x2, x3) not in rel:
                        return False
    return True


def _wsep_unguarded_0valid(relations):
    """The 0-valid form's UNCONDITIONAL disjoint-union — used ONLY by the guard-discriminator selftest, to prove
    is_weakly_separable_general is not the unconditional check in disguise."""
    for rel in relations:
        rows = list(rel)
        for a in rows:
            for b in rows:
                if _disjoint(a, b) and _union(a, b) not in rel:
                    return False
    return True


def selftest_lattice_predicates(verbose=False):
    """Hand-value CI gate for the Lattice relation-level predicates + the guard discriminator. 0 = pass."""
    OR2 = frozenset({(0, 1), (1, 0), (1, 1)}); NAND = frozenset({(0, 0), (0, 1), (1, 0)})
    XNE = frozenset({(0, 1), (1, 0)})                            # x≠y, width-2 affine (the diagnostic)
    XOR3 = frozenset({(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)})
    OR3 = frozenset(t for t in product((0, 1), repeat=3) if t != (0, 0, 0))
    UNIT0 = frozenset({(0,)})
    checks = [
        ("width2affine XNE", is_width2affine([XNE]), True),
        ("width2affine XOR3", is_width2affine([XOR3]), False),
        ("width2affine UNIT0", is_width2affine([UNIT0]), True),
        ("strongly0valid NAND", is_strongly_0valid([NAND]), True),
        ("strongly0valid OR2", is_strongly_0valid([OR2]), False),
        ("IHSB OR2 (+)", is_IHSB([OR2]), True),
        ("IHSB NAND (-)", is_IHSB([NAND]), True),
        ("IHSB XOR3", is_IHSB([XOR3]), False),
        # weak separability (Marx Def 2.1) — ground-truth-checked (BM14 Ex 6.1 / Marx Ex 2.4 / BM14 d-Hitting-Set)
        ("wsep OR2->FPT", is_weakly_separable_general([OR2]), True),
        ("wsep NAND->W[1]", is_weakly_separable_general([NAND]), False),
        ("wsep XNE->FPT", is_weakly_separable_general([XNE]), True),
        ("wsep XOR3->FPT", is_weakly_separable_general([XOR3]), True),
        ("wsep OR3->FPT", is_weakly_separable_general([OR3]), True),
        # GUARD DISCRIMINATOR: on x≠y guarded and unguarded MUST disagree; impl returns the guarded value
        ("guard XNE guarded=True", is_weakly_separable_general([XNE]), True),
        ("guard XNE unguarded=False", _wsep_unguarded_0valid([XNE]), False),
    ]
    bad = [(n, g, e) for n, g, e in checks if g != e]
    if verbose or bad:
        for n, g, e in checks:
            print(f"  {'ok ' if g == e else 'BAD'} {n}: got={g} exp={e}")
    return 1 if bad else 0


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
