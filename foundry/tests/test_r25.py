"""R25 census residual audit (Sprint 4, Task 0) — the RULES, not a pinned verdict.

Tests that the netting machinery correctly identifies the census oracle columns as fully theorem-forced, so the
residual is exactly zero three independent ways, and that the anchor cross-validation against the real canon is
perspective-aware. A non-zero residual is a STOP-the-line bug — this test is the CI guard for it (the byte-
identical ethic applied to the R25 statistics), the analogue of the P2 permutation hand-count selftest.
"""
from foundry import r25


def test_census_r25_residual_is_zero():
    # the top-level selftest: predicted residual is zero, confirmed
    assert r25.census_r25_selftest(verbose=False) == 0


def test_provenance_netting_removes_all_both_real_rows():
    a = r25.census_residual_audit()
    pv = a["P2_provenance_netting"]
    # every both-real (approx, param) row is theorem-`derived`, so netting empties the table
    assert pv["all_both_real_rows_are_derived"]
    assert pv["level_net_theorem_forced"]["n"] == 0
    assert pv["level_net_theorem_forced"]["v"] is None      # V undefined on the empty residual
    assert pv["survives"] is False                          # the OPPOSITE of the canon (which survives)
    # raw V is the live H_P2_scaled association (a real, non-trivial number that nets to zero)
    assert pv["level_raw"]["v"] is not None and pv["level_raw"]["v"] > 0.0


def test_within_stratum_association_is_zero():
    a = r25.census_residual_audit()
    assert a["P2_within_stratum"]["pooled_within_stratum_v"] == 0.0


def test_functional_determination_is_falsifiable_and_holds():
    # same polymorphism profile ⟹ same oracle charges — and the check is NON-vacuous (real multi-row strata,
    # spanning the N1 and finer oracle code paths), so it could actually fail if the two paths disagreed.
    a = r25.census_residual_audit()["functional_determination"]
    assert a["all_strata_charge_constant"]
    assert a["n_multi_row_groups"] >= 1 and a["max_group_size"] >= 2


def test_p3_residual_dimensionality_is_zero():
    p3 = r25.census_residual_audit()["P3_dimensionality"]
    assert p3["n_nonderived_oracle_cells"] == 0
    assert p3["residual_dimensionality"] == 0


def test_anchor_crossvalidation_is_perspective_aware():
    ax = r25.census_residual_audit()["anchor_crossvalidation"]
    # decision/counting/approximation cross-validate census↔canon at every anchor
    assert ax["all_perspective_free_cells_agree"] and ax["n_disagree"] == 0 and ax["n_agree"] > 0
    # parameterized is logged as perspective-divergent (canon treewidth vs census Exact-Ones), NOT compared
    for aid, row in ax["per_anchor"].items():
        assert row["parameterized_perspective_divergent"]["comparable"] is False
