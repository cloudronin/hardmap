"""N1 v1.1 finer Boolean tier + H_P2_scaled — the computed classifier obeys the verified theorems (the RULES).

classify_boolean computes every charge from a language's polymorphisms + the dichotomy theorems; these tests
check the rules on hand-verifiable languages (0-valid → PO Max; affine → FP counting + FPT param; NP-hard →
APX-complete + W[1]), that the finer rows validate through the shared kernel, and that H_P2_scaled runs only when
the pre-registered floor is met and returns a well-formed verdict.
"""
from eightfold import atlas

from foundry import analysis as A
from foundry import finer as FN
from foundry import postlattice as PL
from foundry.charges import FOUNDRY_SPEC


def test_classify_boolean_rules_on_hand_cases():
    # 0-valid affine (homogeneous XOR): PO Max (0-valid), FP counting (affine), FPT param (0-valid & WS), unbounded
    c = FN.classify_boolean((PL.R_XOR3,))
    assert (c["decision"], c["counting"], c["approximation"], c["parameterized"], c["localization"]) == \
           ("P", "FP", "PO", "FPT", "unbounded-width")
    # 0-valid Horn: PO (0-valid), #P-complete (not affine), W[1] (R_NOR3 fails weak-separability union), bounded
    c = FN.classify_boolean((PL.R_NOR3, PL.R_FALSE))
    assert (c["decision"], c["approximation"], c["parameterized"], c["localization"]) == \
           ("P", "PO", "W[1]", "bounded-width")
    # NP-hard region (NAE-3): NPC, APX-complete Max (not 0/1-valid/affine), W[1], unbounded
    c = FN.classify_boolean((PL.R_NAE3,))
    assert (c["decision"], c["approximation"], c["parameterized"], c["localization"]) == \
           ("NPC", "APX-complete", "W[1]", "unbounded-width")


def test_finer_rows_validate_through_kernel():
    for r in FN.build_finer_census():
        assert atlas.validate(r, FOUNDRY_SPEC) == [], (r.problem_id, atlas.validate(r, FOUNDRY_SPEC))


def test_enriched_census_p1_holds_and_floor_met():
    rows = A.full_census()
    npi = [r.problem_id for r in rows if next(c.value for c in r.charges if c.charge == "decision") == "NPI-candidate"]
    assert npi == []                                          # P1 still holds on the enriched census
    both = A._contingency(A.S._grid(rows)[2])
    assert len(both) >= 15 and len(set(both)) >= 4            # the pre-registered H_P2_scaled floor


def test_h_p2_scaled_runs_and_verdict_wellformed():
    h = A.h_p2_scaled(n_perm=3000)
    assert h["floor_met"] is True
    assert h["verdict"] in ("POSITIVE", "REVERSED", "STRATIFIED")
    # the association is theorem-forced (both charges are polymorphism functions) — the note records it
    assert "theorem-forced" in h["theorem_forced_note"]
