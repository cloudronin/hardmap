"""Lattice (G2) CI gate — the relation-level predicates, the corrected weak-separability + its GUARD
discriminator, and the witness gate (VC/IS on opposite corners of both axes)."""
from foundry import objective_oracles as OO
from foundry import postlattice as PL

OR2 = frozenset({(0, 1), (1, 0), (1, 1)})       # x∨y   vertex-cover edge relation
NAND = frozenset({(0, 0), (0, 1), (1, 0)})      # ¬x∨¬y independent-set edge relation
XNE = frozenset({(0, 1), (1, 0)})               # x≠y   width-2 affine (guard diagnostic)


def test_lattice_predicate_selftest():
    assert PL.selftest_lattice_predicates() == 0


def test_guard_is_real():
    """Def 2.1's guarded union differs from the 0-valid unconditional form exactly on x≠y — proving the
    implementation is not the old unconditional check in disguise."""
    assert PL.is_weakly_separable_general([XNE]) is True          # guarded (Def 2.1): weakly separable
    assert PL._wsep_unguarded_0valid([XNE]) is False              # unguarded (0-valid form): not
    # the census's 0-valid-normalized check agrees with the unguarded form here (both wrong for this 0-invalid rel)
    assert PL.is_weakly_separable([XNE]) is False


def test_weak_separability_ground_truth():
    """Single-relation Exact-Ones verdicts, each independently sourced (BM14 Ex 6.1 / Marx Ex 2.4 / BM14 d-HS)."""
    assert PL.is_weakly_separable_general([OR2]) is True          # VC  -> FPT
    assert PL.is_weakly_separable_general([NAND]) is False        # IS  -> W[1]
    assert PL.is_weakly_separable_general([XNE]) is True          # x≠y (width-2 affine) -> FPT
    assert PL.is_weakly_separable_general([PL.R_XOR3]) is True    # affine -> FPT
    assert PL.is_weakly_separable_general([PL.R_OR3]) is True     # pos-3-clause = 3-Hitting-Set -> FPT


def test_witness_gate():
    """VC and IS on opposite corners of BOTH axes (prereg_v29 witness-gate pass criterion)."""
    assert OO.charges([OR2], OO.MIN_ONES) == ("APX-complete", "FPT")            # Vertex Cover
    assert OO.charges([NAND], OO.MAX_ONES) == ("poly-APX-complete", "W[1]")     # Independent Set
    assert OO.selftest_objective_oracles() == 0


def test_census_oracle_untouched():
    """Lattice is additive: the census's 0-valid weak-separability check is unchanged (affine 0-valid rel FPT-side)."""
    # XOR3 is 0-valid affine: the census's is_weakly_separable is faithful here (True), matching the general form.
    assert PL.is_weakly_separable([PL.R_XOR3]) is True
