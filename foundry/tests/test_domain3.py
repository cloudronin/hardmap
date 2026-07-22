"""N3 general-domain tier + Sprint 3 analysis — the RULES (verified dichotomies), not the science verdicts.

Tests that the polymorphism test agrees with the textbook complexity of the curated domain-3 languages
(Bulatov/Zhuk decision, Barto-Kozik localization), that the domain-3 rows fill only the verified general-domain
charges, that the full census still passes P1, and that the P2/P3 harness returns well-formed structure.
"""
from eightfold import atlas

from foundry import analysis as A
from foundry import domain3 as D
from foundry.charges import FOUNDRY_SPEC


def test_curated_d3_classifications_verified():
    # the polymorphism test must agree with each language's textbook-certain complexity (R20 cross-check)
    for lang in D.CURATED_D3:
        assert D.verify(lang) == [], (lang.id, D.verify(lang))


def test_bulatov_zhuk_decision_and_barto_kozik_width():
    C = {l.id: D.classify(l) for l in D.CURATED_D3}
    # decision (Bulatov/Zhuk): WNU polymorphism → P; ≠_3 / NAE-3 have none → NPC
    assert C["3-coloring"]["decision"] == "NPC" and C["nae-3dom"]["decision"] == "NPC"
    assert C["lin-eq-z3"]["decision"] == "P" and C["order-3"]["decision"] == "P"
    # localization (Barto-Kozik): affine is tractable but UNBOUNDED width (the |D|=3 XOR analogue); order is bounded
    assert C["lin-eq-z3"]["localization"] == "unbounded-width"
    assert C["order-3"]["localization"] == "bounded-width"


def test_d3_census_rows_validate_and_scope():
    for r in D.build_d3_census():
        assert atlas.validate(r, FOUNDRY_SPEC) == [], (r.problem_id, atlas.validate(r, FOUNDRY_SPEC))
        vals = {c.charge: c.value for c in r.charges}
        assert vals["decision"] in ("P", "NPC")
        assert vals["localization"] in ("bounded-width", "unbounded-width")
        # parameterized stays open (Bulatov-Marx Thm 4.1 IMPLEMENTABLE-heavy, not yet built)
        assert vals["parameterized"] == "open"
        # counting: #P-complete iff NP-hard decision (counting >= decision); open for tractable-decision
        assert vals["counting"] == ("#P-complete" if vals["decision"] == "NPC" else "open")
        # approximation: PO where const-valid/semilattice (Thapper-Zivny verified sufficient); else open (UGC-conditional)
        assert vals["approximation"] in ("PO", "open")


def test_domain3_approximation_counting_oracles():
    cl = {l.id: D.classify(l) for l in D.CURATED_D3}
    for l in D.CURATED_D3:
        ap = D.approximation_d3(l.relations)
        cn = D.counting_d3(l.relations, cl[l.id]["decision"])
        if l.id in ("lin-eq-z3", "order-3", "median-3", "lin-eq-z3-b"):
            assert ap == "PO", (l.id, ap)                 # const-valid / semilattice → PO (Thapper-Zivny)
        if l.id in ("3-coloring", "nae-3dom"):
            assert cn == "#P-complete" and ap is None      # NP-hard → #P-complete counting; Max not-PO → open


def test_full_census_p1_calibration_holds():
    # P1: no NPI-candidate row (Schaefer/Bulatov-Zhuk: CSP decision is P or NPC, never NP-intermediate)
    npi = [r.problem_id for r in A.full_census()
           if next(c.value for c in r.charges if c.charge == "decision") == "NPI-candidate"]
    assert npi == []


def test_p2_permutation_selftest_reproduces_hand_count():
    # the fix for the impossible p=0.0002: the permutation must run on the both-real rows only, so a table with
    # 6 identical + 1 distinct row gives the hand-countable p = 1/7 (and a 3-row analogue gives 1/3)
    assert A.selftest_p2_perm(n_perm=4000) == 0


def test_p2_corrected_harness_and_sociology_struck():
    # locks the Sprint-3 correction, independent of census size: the affine/XOR decoupling is a DESCRIPTIVE
    # observation (not a ruling), and the roster-sociology reading is struck (it contradicted Crucible S5)
    p2 = A.p2_gradient(n_perm=4000)
    assert p2["descriptive_observation"]["decoupling_witness_xor_sat"] == {"approximation": "inapprox", "parameterized": "FPT"}
    assert "STRUCK" in p2["roster_sociology"]
    # the corrected permutation harness reproduces the hand-countable p (the fix for the impossible 0.0002)
    assert A.selftest_p2_perm(n_perm=4000) == 0


def test_p3_factors_harness_runs():
    p3 = A.p3_factors(budget=dict(repeats=4, restarts=3, max_iters=40, ks=range(1, 4)))
    assert isinstance(p3["census_k_hat_1se"], int) and isinstance(p3["same_world"], bool)
