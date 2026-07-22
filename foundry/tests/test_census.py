"""N1 Boolean census — the oracles compute correct classifications, the census validates, P1 holds.

Tests the pre-registered RULES (Schaefer/Creignou-Hermann/Barto-Kozik dichotomies + the NPI calibration), the
polymorphism verification, and the shared-kernel validation — not science verdicts (predictions 2-4 are N2+).
"""
from eightfold import atlas

from foundry import postlattice as PL
from foundry.charges import FOUNDRY_SPEC
from foundry.oracles import build_boolean_census, classify, verify_class


def _val(row, charge):
    return next(c.value for c in row.charges if c.charge == charge)


def test_census_validates_through_shared_kernel():
    for row in build_boolean_census():
        assert atlas.validate(row, FOUNDRY_SPEC) == [], (row.problem_id, atlas.validate(row, FOUNDRY_SPEC))


def test_every_coclone_declared_class_verified():
    # the polymorphism check must confirm each declared Schaefer class + faithfulness (non-0/1-valid)
    for cc in PL.BOOLEAN_COCLONES:
        assert verify_class(cc) == [], (cc.id, verify_class(cc))


def test_prediction1_npi_calibration_empty():
    # P1 (known-answer): the Schaefer dichotomy makes the NPI row empty; a non-empty NPI row = pipeline bug
    npi = [r.problem_id for r in build_boolean_census() if _val(r, "decision") == "NPI-candidate"]
    assert npi == []


def test_counting_oracle_is_creignou_hermann():
    # #CSP(Γ) ∈ FP iff Γ affine; else #P-complete
    for r in build_boolean_census():
        cc = next(c for c in PL.BOOLEAN_COCLONES if c.id == r.problem_id)
        assert _val(r, "counting") == ("FP" if cc.schaefer_class == PL.AFFINE else "#P-complete")


def test_localization_oracle_is_barto_kozik():
    # bounded-width iff Horn/dual-Horn/bijunctive; unbounded for affine (the obstruction) + NP-hard
    for r in build_boolean_census():
        cc = next(c for c in PL.BOOLEAN_COCLONES if c.id == r.problem_id)
        expect = "bounded-width" if cc.schaefer_class in (PL.HORN, PL.DUAL_HORN, PL.BIJUNCTIVE) else "unbounded-width"
        assert _val(r, "localization") == expect


def test_affine_is_the_deceptive_terrain_control():
    # xor-sat: easy decision (P) yet hard elsewhere — FP counting but inapprox + unbounded-width
    xor = next(r for r in build_boolean_census() if r.problem_id == "xor-sat")
    assert _val(xor, "decision") == "P" and _val(xor, "counting") == "FP"
    assert _val(xor, "approximation") == "inapprox" and _val(xor, "localization") == "unbounded-width"


def test_deferred_columns_are_open_not_guessed():
    # proof_size (Molloy, N4 ensemble) + the measured instruments are honestly `open`. parameterized is now
    # FILLED by the Marx dichotomy (Sprint 2.1) — see test_parameterized_oracle_is_marx.
    for r in build_boolean_census():
        for ch in ("proof_size", "average_case", "landscape"):
            assert _val(r, ch) == "open", (r.problem_id, ch)


def test_verify_class_catches_a_mislabelled_coclone():
    # a co-clone declared affine but not closed under minority must be rejected
    bad = PL.CoClone("bad", "bad", "affine", PL.AFFINE, "not affine", (PL.R_OR3,))
    assert verify_class(bad)


def test_registration_anchors_present():
    ids = {r.problem_id for r in build_boolean_census()}
    assert {"xor-sat", "horn-sat", "2-sat", "3-sat", "nae-sat", "one-in-three-sat"} <= ids


def test_parameterized_oracle_is_marx():
    # Exact-Ones CSP(Γ) parameterized by solution weight: FPT iff Γ weakly separable, else W[1] (Marx 2005 /
    # Bulatov-Marx). Among these co-clones only affine is weakly separable → FPT; every other class → W[1].
    for r in build_boolean_census():
        cc = next(c for c in PL.BOOLEAN_COCLONES if c.id == r.problem_id)
        p = next(c for c in r.charges if c.charge == "parameterized")
        assert p.value == ("FPT" if cc.schaefer_class == PL.AFFINE else "W[1]"), (cc.id, p.value)
        assert p.status == "derived" and p.provenance["condition_check"]["side"] == p.value
        assert p.perspective  # perspective-required charge (the parameter)


def test_weak_separability_criterion():
    # the verified union+difference definition (Bulatov-Marx arXiv:1206.4854) on hand-checked relations
    r_impl = frozenset({(0, 0), (0, 1), (1, 1)})               # x→y: 0-valid, fails DIFFERENCE ((1,0),(0,1))
    assert PL.is_weakly_separable([PL.R_XOR3])                 # homogeneous affine (0-valid) → WS
    assert not PL.is_weakly_separable([r_impl])                # implication → not WS
    assert not PL.is_weakly_separable([PL.R_NEG2])             # ¬x∨¬y → fails UNION ((1,0),(0,1)→(1,1)∉R)
    assert not PL.is_weakly_separable([PL.R_NOR3])             # ¬x∨¬y∨¬z → fails UNION ((1,0,0),(0,1,1)→(1,1,1))
    # weak separability implies 0-validity → a non-0-valid affine relation fails the naive check; this is WHY
    # the oracle classifies at the class level (the CKZ reps trade 0-validity away for the Max/decision charges)
    assert not PL.is_weakly_separable([PL.R_XOR2])             # x⊕y=1 is affine but NOT 0-valid → naive check fails
