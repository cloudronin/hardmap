"""Relation-level features (prereg_v11) + the B permutation harness hand-count selftest — the RULES."""
from foundry import postlattice as PL
from foundry import relfeatures as RF


def test_tuple_dispersion_known_cases():
    # XOR3: all 4 tuples pairwise Hamming-2 over arity 3 -> normalized dispersion 2/3
    assert abs(RF.tuple_dispersion(PL.R_XOR3) - 2 / 3) < 1e-3
    # a single-tuple / identical set has zero dispersion
    assert RF.tuple_dispersion(frozenset({(0, 0, 0)})) == 0.0


def test_density():
    assert RF.density(PL.R_XOR3) == 0.5                    # 4 of 8
    assert RF.density(PL.R_NOR3) == round(7 / 8, 3)        # all except (1,1,1)


def test_B_permutation_harness_hand_count():
    assert RF.selftest_perm() == 0
