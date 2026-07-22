"""GKMP connectivity relation-level predicates (prereg_v9) — the RULES, R20-verified from cs/0609072 Def 5-6.

Locks the predicate implementations against hand-checked cases; the NOT_PREDICTIVE verdict itself lives in the
findings, not here.
"""
from foundry import connectivity as C
from foundry import postlattice as PL


def test_or_free_and_nand_free_sanity():
    # OR itself is not OR-free; NAND itself is not NAND-free (the relations they are named for)
    assert C.or_free(PL.R_POS2) is False          # x∨y = {(0,1),(1,0),(1,1)}
    assert C.nand_free(PL.R_NEG2) is False         # ¬x∨¬y = {(0,0),(0,1),(1,0)}
    # and the reverse: NAND is OR-free, OR is NAND-free
    assert C.or_free(PL.R_NEG2) is True
    assert C.nand_free(PL.R_POS2) is True


def test_componentwise_bijunctive_cases():
    impl = frozenset({(0, 0), (0, 1), (1, 1)})     # implication: 1 component, majority-closed
    assert C.componentwise_bijunctive(impl) is True
    assert C.componentwise_bijunctive(PL.R_NOR3) is False   # ¬x∨¬y∨¬z: not majority-closed


def test_affine_is_isolated_singletons():
    # x⊕y⊕z=0: all 4 tuples pairwise Hamming-2 -> 4 isolated components (each trivially bijunctive)
    cls = C.classify_relation(PL.R_XOR3)
    assert cls["n_components"] == 4 and cls["componentwise_bijunctive"] is True


def test_classify_relation_shape_and_tight():
    for R in (PL.R_XOR3, PL.R_NOR3, PL.R_POS2, frozenset({(0, 0), (0, 1), (1, 1)})):
        cls = C.classify_relation(R)
        assert set(cls) >= {"or_free", "nand_free", "componentwise_bijunctive", "tight", "n_components"}
        # every Schaefer relation here is tight (Schaefer => tight)
        assert cls["tight"] == (cls["or_free"] or cls["nand_free"] or cls["componentwise_bijunctive"])
