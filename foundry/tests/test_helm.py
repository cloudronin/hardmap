"""Known-answer battery for Helm's statistics and screens (Helm §8, guard rails).

HAND-COMPUTED, NOT SNAPSHOTTED. A snapshot proves the sweep still does what it did; a hand-computed
fixture proves it does what it should. Helm's numbers set the forking-paths denominator and the family
correction for every seal downstream, so a silent drift in `spearman` or `holm` would corrupt the
correction on every wave at once and leave no diff to point at.

THE SCREENS ARE TESTED BY MAKING THEM FIRE. A screen that has never rejected anything is a screen nobody
has tested — so there are fixtures here that are supposed to be thrown out, and the test is that they are.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from foundry.helm import screens as S      # noqa: E402
from foundry.helm import slate as SL       # noqa: E402
from foundry.helm import sweep as SW       # noqa: E402


# ── rank correlation ────────────────────────────────────────────────────────────────────────────────
def test_spearman_perfect_monotone():
    assert abs(SW.spearman([1, 2, 3, 4], [10, 20, 30, 40]) - 1.0) < 1e-12


def test_spearman_perfect_inverse():
    assert abs(SW.spearman([1, 2, 3, 4], [40, 30, 20, 10]) + 1.0) < 1e-12


def test_spearman_is_rank_based_not_value_based():
    """A monotone but wildly non-linear map must not move rho at all."""
    assert abs(SW.spearman([1, 2, 3, 4], [1, 4, 9, 1000]) - 1.0) < 1e-12


def test_spearman_with_ties_uses_average_ranks():
    """x ranks (1.5,1.5,3.5,3.5), y ranks (1,2,3,4) -> num 4.0, da 2, db sqrt(5) -> 0.894427.
    Hand-computed."""
    r = SW.spearman([1, 1, 2, 2], [1, 2, 3, 4])
    assert abs(r - 4.0 / (2 * 5 ** 0.5)) < 1e-12


def test_spearman_undefined_on_a_constant_column():
    assert SW.spearman([1, 1, 1, 1], [1, 2, 3, 4]) is None


def test_spearman_none_below_three_points():
    assert SW.spearman([1, 2], [1, 2]) is None


# ── association ─────────────────────────────────────────────────────────────────────────────────────
def test_cramers_v_perfect_association_is_one():
    assert abs(SW.cramers_v([("a", "x"), ("a", "x"), ("b", "y"), ("b", "y")]) - 1.0) < 1e-12


def test_cramers_v_no_association_is_zero():
    assert abs(SW.cramers_v([("a", "x"), ("a", "y"), ("b", "x"), ("b", "y")])) < 1e-12


def test_cramers_v_needs_two_levels_on_both_axes():
    assert SW.cramers_v([("a", "x"), ("a", "y")]) is None


# ── the family correction ───────────────────────────────────────────────────────────────────────────
def test_holm_thresholds_are_the_step_down_ladder():
    """Three hypotheses -> 0.05/3, 0.05/2, 0.05/1 assigned by ascending p. Hand-computed."""
    t = S.holm([0.01, 0.02, 0.03])
    assert abs(t[0] - 0.05 / 3) < 1e-12
    assert abs(t[1] - 0.05 / 2) < 1e-12
    assert abs(t[2] - 0.05 / 1) < 1e-12


def test_holm_orders_by_p_not_by_position():
    t = S.holm([0.03, 0.01])
    assert abs(t[1] - 0.05 / 2) < 1e-12 and abs(t[0] - 0.05) < 1e-12


# ── power ───────────────────────────────────────────────────────────────────────────────────────────
def test_mde_is_undefined_below_four_clusters():
    """Fisher's z needs n - 3 > 0. Four is a mathematical minimum, not a chosen floor."""
    assert S.mde_correlation(3) is None
    assert S.mde_correlation(2) is None
    assert S.mde_correlation(4) is not None


def test_mde_shrinks_as_the_frontier_grows():
    assert S.mde_correlation(10) > S.mde_correlation(30) > S.mde_correlation(100)


def test_mde_at_four_clusters_is_nearly_one():
    """tanh(2.801585 / sqrt(1)) = 0.99266 — a four-row frontier can only adjudicate an almost perfect
    correlation, which is the honest reading of a four-row frontier."""
    assert abs(S.mde_correlation(4) - 0.992664) < 1e-5


# ── the screens fire ────────────────────────────────────────────────────────────────────────────────
def _cand(**kw):
    base = {"kind": "co-movement", "descriptors": ["excess_ref", "overlap_ref"],
            "null": "cluster permutation", "frontier_null": "the same, on the reserved rows",
            "disclosed": 0.99, "n": 100, "n_clusters": 20, "candidate_id": "c1",
            "statistic": "s", "generating_query": "SELECT 1", "stamp": "disclosed-prior"}
    base.update(kw)
    return base


FRONTIER_BIG = {"n_clusters": 40, "n_cells": 260}
FRONTIER_TINY = {"n_clusters": 2, "n_cells": 13}


def test_a_null_for_the_disclosed_statistic_does_not_pass_screen_one():
    """THE DISTINCTION THAT MAKES SCREEN 1 REAL. An in-sample null always exists — the in-sample number
    was computed with it. What a seal needs is a null for the BET, and a candidate carrying only the
    former is held, not slated."""
    d, rule, _ = S.screen(_cand(frontier_null=None), None, FRONTIER_BIG, set())
    assert d == "HELD" and rule == "null-missing"


def test_screen_reports_the_candidates_own_reason_for_the_missing_null():
    d, rule, detail = S.screen(_cand(frontier_null=None, why_no_frontier_null="v1 has not pinned it"),
                               None, FRONTIER_BIG, set())
    assert detail == "v1 has not pinned it"


def test_netting_rejects_a_definitionally_coupled_pair():
    """excess_ref is a MEMBER of the set excess_max maximises, so rho is partly forced by arithmetic."""
    d, rule, detail = S.screen(_cand(descriptors=["excess_ref", "excess_max"]), None,
                               FRONTIER_BIG, set())
    assert d == "REJECTED" and rule == "netting"
    assert "by construction" in detail


def test_netting_does_not_reject_an_uncoupled_pair():
    d, rule, _ = S.screen(_cand(descriptors=["overlap_ref", "r_ref"]), None, FRONTIER_BIG, set())
    assert d == "SLATED", (d, rule)


def test_coupled_pairs_are_still_enumerated_so_the_denominator_stays_honest():
    """A denominator that omits the questions we knew were bad is a denominator we chose. The coupled
    pairs must appear in the sweep and be REJECTED, not be quietly absent from it."""
    coupled = {frozenset(p) for p in S.DEFINITIONAL_COUPLING}
    from itertools import combinations
    enumerated = {frozenset(p) for p in combinations(SW.NUMERIC, 2)}
    assert coupled <= enumerated, "a coupled pair was removed from enumeration instead of screened"


def test_screen_rejects_a_seal_prohibited_descriptor():
    """The catalog's own flag governs — a transition descriptor has no typed null at v1."""
    d, rule, detail = S.screen(_cand(descriptors=["kink_sharpness"]), None, FRONTIER_BIG,
                               {"kink_step", "kink_sharpness"})
    assert d == "REJECTED" and rule == "null-missing"
    assert "SEAL_PROHIBITED_AT_V1" in detail


def test_screen_rejects_an_f2_violating_charge_candidate():
    d, rule, _ = S.screen(_cand(kind="association", charge="approx-ratio",
                                charge_is_a_fixed_row_label=False), None, FRONTIER_BIG, set())
    assert d == "REJECTED" and rule == "F2-foreclosed"


def test_screen_holds_rather_than_kills_on_power():
    """A candidate the frontier cannot adjudicate is HELD with its gap named — never killed."""
    d, rule, detail = S.screen(_cand(), None, FRONTIER_TINY, set())
    assert d == "HELD" and rule == "power-fail"
    assert "more reserved rows" in detail


def test_screen_slates_a_powered_candidate():
    d, rule, _ = S.screen(_cand(disclosed=0.95), None, FRONTIER_BIG, set())
    assert d == "SLATED" and rule is None


def test_a_closed_bank_question_is_rejected_not_slated():
    d, rule, _ = S.screen(_cand(kind="bank-import", bank_status="CLOSED", null=None),
                          None, FRONTIER_BIG, set())
    assert d == "REJECTED"


def test_an_open_bank_question_is_held_for_want_of_a_statistic():
    d, rule, detail = S.screen(_cand(kind="bank-import", bank_status="OPEN", null=None),
                               None, FRONTIER_BIG, set())
    assert d == "HELD" and "eyeball ban" in detail


# ── the slate ───────────────────────────────────────────────────────────────────────────────────────
def test_sealed_bet_fixes_direction_from_the_disclosed_prior():
    assert "negative" in SL.sealed_bet(_cand(disclosed=-0.4))
    assert "positive" in SL.sealed_bet(_cand(disclosed=+0.4))


def test_required_clusters_inverts_the_mde():
    """The HOLD queue's promise: the number recorded is the frontier size that actually clears the gap."""
    for rho in (0.5, 0.7, 0.9):
        n = S.required_clusters(rho)
        assert S.mde_correlation(n) <= rho, (rho, n, S.mde_correlation(n))
        assert S.mde_correlation(n - 1) > rho, "recorded gap is larger than it needs to be"


def test_required_clusters_undefined_at_the_boundaries():
    assert S.required_clusters(0.0) is None and S.required_clusters(1.0) is None


def test_ranking_refuses_to_score_a_candidate_with_no_mde():
    """A slated candidate has cleared the power screen, so its MDE is defined. Scoring 0.0 for a
    missing MDE would flatten a whole slate to one tied value — a ranking that has stopped ranking."""
    import pytest
    with pytest.raises(ValueError, match="screen/rank disagreement"):
        SL.power_proxy(_cand(), FRONTIER_BIG, None)


def test_novelty_penalises_a_descriptor_the_bank_already_asks_about():
    bank = [{"statistic": "Q16: the coherence dial and the blend-excess trajectory move together"}]
    fresh = SL.novelty(_cand(descriptors=["r_ref"]), bank)
    stale = SL.novelty(_cand(descriptors=["coherence"]), bank)
    assert fresh == 1.0 and stale < 1.0


def test_every_swept_candidate_carries_a_reproducible_query():
    """The eyeball ban, mechanised: a candidate with no generating query entered by looking."""
    from foundry.helm.sweep import bank_imports
    bank = ROOT / "docs" / "findings" / "sounding-survey-banked-questions.md"
    for c in bank_imports(bank):
        assert c["generating_query"], c
        assert c["stamp"] == "disclosed-prior"


# ── the structurally-flat backstop (ruling, 2026-07-27) ─────────────────────────────────────────────
def test_structurally_flat_candidate_is_rejected():
    """The sweep queries `sweepable_catalog`, so a flat cell should never reach candidacy. This is the
    backstop for any path that bypasses the view — and it is tested because an untested backstop is
    indistinguishable from an absent one."""
    d, rule, detail = S.screen(_cand(structurally_flat=True), None, FRONTIER_BIG, set())
    assert d == "REJECTED" and rule == "structurally-flat"
    assert "BY CONSTRUCTION" in detail


# ── the stratified extremal null (ruling, 2026-07-27) ───────────────────────────────────────────────
def _anom(**kw):
    base = {"kind": "anomaly", "descriptors": ["overlap_ref"], "candidate_id": "a1",
            "null": "pooled", "frontier_null": SW.EXTREMAL_NULL, "disclosed": 3.0,
            "stratum": {"family": "algebraic", "region": "feasible", "flavour": "majority"},
            "statistic": "s", "generating_query": "SELECT 1", "stamp": "disclosed-prior"}
    base.update(kw)
    return base


def test_the_pinned_null_unblocks_screen_one_for_anomalies():
    """Wave 1 held all 22 extremals for want of a frontier null. The ruling pinned one; they must now
    fail (if at all) on SUPPLY, not on the null's absence."""
    d, rule, _ = S.screen(_anom(), None, {**FRONTIER_BIG, "strata": {"algebraic": 40}}, set())
    assert d == "SLATED", (d, rule)


def test_anomaly_is_held_when_its_own_stratum_is_thin():
    """Supply is judged WITHIN the stratum, not on the frontier's total — a large frontier concentrated
    in other families adjudicates nothing here."""
    f = {**FRONTIER_BIG, "strata": {"graph": 500, "algebraic": 1}}
    d, rule, detail = S.screen(_anom(), None, f, set())
    assert d == "HELD" and rule == "power-fail"
    assert "algebraic" in detail and str(S.MIN_STRATUM_CELLS) in detail


def test_a_cross_stratum_candidate_is_judged_on_its_thinnest_stratum():
    """A count spanning every stratum is adjudicable only when the weakest one clears the floor."""
    f = {**FRONTIER_BIG, "strata": {"graph": 500, "algebraic": 1}}
    d, rule, _ = S.screen(_anom(stratum={"family": None}), None, f, set())
    assert d == "HELD" and rule == "power-fail"


def test_the_stratum_floor_is_where_significance_becomes_attainable():
    """A one-sided permutation over m cells attains no p below 1/(m+1). The floor must be the first
    size at which alpha is reachable — derived, not chosen."""
    assert 1 / (S.MIN_STRATUM_CELLS - 1 + 1) <= S.ALPHA
    assert 1 / (S.MIN_STRATUM_CELLS - 2 + 1) > S.ALPHA


def test_frontier_strata_counts_reserved_rows_by_family():
    import sqlite3
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE problems (problem_id TEXT PRIMARY KEY, family TEXT)")
    con.executemany("INSERT INTO problems VALUES (?,?)",
                    [("a", "algebraic"), ("b", "optimization"), ("c", "algebraic")])
    assert S.frontier_strata(con, {"a", "c"}) == {"algebraic": 2}
    assert S.frontier_strata(con, set()) == {}


# ── ambient stability (minted 2026-07-27) ───────────────────────────────────────────────────────────
def test_ambient_stability_accepts_a_fixed_ground_set():
    """A vertex-subset row has width n at every step, whatever the dial does."""
    from foundry.catalog import capture as CAP
    import random
    build = lambda rng, v: [("feasible", [(0,) * 9, (1,) * 9])]
    stable, widths = CAP.ambient_stability(build, (0.1, 0.5, 0.9), random.Random(0))
    assert stable is True and set(widths) == {9}


def test_ambient_stability_rejects_a_ground_set_that_grows_with_the_dial():
    """An EDGE-subset row's width is |E|, which edge density ramps — so the ambient moves with the
    dial and a trajectory over it confounds tightening with a growing space."""
    from foundry.catalog import capture as CAP
    import random
    build = lambda rng, v: [("feasible", [(0,) * int(v * 20), (1,) * int(v * 20)])]
    stable, widths = CAP.ambient_stability(build, (0.3, 0.5, 0.9), random.Random(0))
    assert stable is False and len(set(widths)) > 1


def test_ambient_stability_is_undecided_when_nothing_builds():
    from foundry.catalog import capture as CAP
    import random
    stable, widths = CAP.ambient_stability(lambda rng, v: [], (0.1, 0.5), random.Random(0))
    assert stable is None and widths == []


# ── Ruling 2: population match and HELD-path-gated ──────────────────────────────────────────────────
def test_family_candidate_with_no_frontier_rows_is_held_not_slated():
    """A family-specific prior scored on a family-absent frontier tests a broader cousin with the
    prior as decoration — the lesson Terroir's strata and N6-R's tiers each paid for once."""
    f = {**FRONTIER_BIG, "strata": {"graph": 10}, "family_supply": {"number-theoretic": 3}}
    d, rule, detail = S.screen(_cand(group="number-theoretic", disclosed=0.99), None, f, set())
    assert d == "HELD" and rule == "population-mismatch"
    assert "ZERO number-theoretic" in detail


def test_an_exhausted_family_is_path_gated_not_power_gated():
    """The distinction that matters: no reservation can ever revive this, so the hold must say so."""
    f = {**FRONTIER_BIG, "strata": {"graph": 10}, "family_supply": {"graph": 5}}
    d, rule, detail = S.screen(_cand(group="number-theoretic", disclosed=0.99), None, f, set())
    assert d == "HELD" and rule == "path-gated"
    assert "cannot close through scheduled building" in detail


def test_path_gated_holds_carry_a_revival_mechanism_and_an_expiry():
    """A hold that cannot name its revival mechanism is a zombie."""
    f = {**FRONTIER_BIG, "strata": {"graph": 10}, "family_supply": {}}
    out = S.run([_cand(group="number-theoretic", disclosed=0.99)], None, f, set())
    r = out[0]
    assert r["hold_kind"] == "HELD-path-gated"
    assert "capture-path build decision" in r["revives_on"]
    assert "INSUFFICIENT-by-population" in r["closes_as"]


def test_a_pooled_candidate_is_never_population_mismatched():
    f = {**FRONTIER_BIG, "strata": {"graph": 10}, "family_supply": {}}
    d, rule, _ = S.screen(_cand(group="pooled", disclosed=0.99), None, f, set())
    assert d == "SLATED", (d, rule)


# ── the wave-4 sitting, compiled into screens (ruled 2026-07-27) ────────────────────────────────────
FRONTIER_SIZED = {**FRONTIER_BIG, "strata": {"optimization": 4}, "family_supply": {"optimization": 9}}


def test_definitional_consumption_kills_r_against_its_own_flag():
    """INSUFFICIENT-r's trigger IS r below the floor. Correlating r with the share of flags derived
    from r is a vacuous comparison in descriptor clothing."""
    d, rule, detail = S.screen(_cand(descriptors=["r_ref", "insufficient_share"],
                                     group="optimization"), None, FRONTIER_SIZED, set())
    assert d == "REJECTED" and rule == "definitional-consumption"
    assert "vacuous" in detail


def test_a_size_marginal_containing_r_ref_is_barred_not_held():
    """There is no version of this question with size held out — conditioning r_ref on itself is not
    a weaker question, it is not the question."""
    d, rule, detail = S.screen(_cand(descriptors=["bimodality_max", "r_ref"], group="graph"),
                               None, {**FRONTIER_SIZED, "strata": {"graph": 4},
                                      "family_supply": {"graph": 9}}, set())
    assert d == "REJECTED" and rule == "size-marginal"
    assert "cannot be conditioned on r" in detail


def test_two_size_coupled_descriptors_need_the_conditioned_prior_to_reach_a_slate():
    """Marginals with size in both hands don't get a sitting."""
    d, rule, _ = S.screen(_cand(descriptors=["bimodality_max", "insufficient_share"],
                                group="optimization"), None, FRONTIER_SIZED, set())
    assert d == "HELD" and rule == "needs-r-conditioning"


def test_the_conditioned_prior_is_what_gets_screened():
    """Once conditioned, the PARTIAL is the effect the power screen sees — not the marginal."""
    c = _cand(descriptors=["bimodality_max", "insufficient_share"], group="optimization",
              disclosed=0.99, disclosed_partial_r=0.10)
    d, rule, _ = S.screen(c, None, FRONTIER_SIZED, set())
    assert d == "HELD" and rule == "power-fail", "the marginal 0.99 must not carry a weak partial"


def test_an_unconfounded_pair_is_untouched_by_the_size_rules():
    d, rule, _ = S.screen(_cand(descriptors=["overlap_ref", "excess_ref"], group="optimization",
                                disclosed=0.95), None, FRONTIER_SIZED, set())
    assert d == "SLATED", (d, rule)


def test_partial_spearman_removes_a_pure_common_cause():
    """x and y both driven by z and nothing else -> the partial collapses toward zero."""
    z = list(range(20))
    x = [v * 2 for v in z]
    y = [v * 3 for v in z]
    assert abs(SW.spearman(x, y) - 1.0) < 1e-12
    assert abs(SW.partial_spearman(x, y, z) or 0.0) < 1e-9


def test_partial_spearman_is_none_when_undefined():
    assert SW.partial_spearman([1, 1, 1], [1, 2, 3], [1, 2, 3]) is None


# ── coupling travels the derivation graph (ruled 2026-07-27, wave-5 sitting) ────────────────────────
def test_a_flag_inherits_its_size_coupling_from_what_it_derives_from():
    """bimodal_flag is a threshold ON size-inflated raw BC. The screens carried coupling as metadata on
    DESCRIPTORS, so a flag inheriting it through derivation was invisible — and reached a slate."""
    assert S._size_coupled("bimodal_flag")
    assert "bimodal_flag" in S.SIZE_COUPLED


def test_an_association_on_a_size_coupled_descriptor_needs_stratification():
    """One size-coupled side is enough: the charge may track r independently, so the association could
    be entirely r-mediated."""
    f = {**FRONTIER_BIG, "strata": {"pooled": 10}, "family_supply": {}}
    c = _cand(kind="association", descriptors=["bimodal_flag"], group="pooled",
              charge="landscape", charge_is_a_fixed_row_label=True, disclosed=0.407)
    d, rule, detail = S.screen(c, None, f, set())
    assert d == "HELD" and rule == "needs-r-stratification"
    assert "r-mediated" in detail


def test_an_uncoupled_association_still_slates():
    f = {**FRONTIER_BIG, "strata": {"pooled": 10}, "family_supply": {}}
    c = _cand(kind="association", descriptors=["traj_class"], group="pooled",
              charge="landscape", charge_is_a_fixed_row_label=True, disclosed=0.9)
    assert S.screen(c, None, f, set())[0] == "SLATED"


def test_overlap_ref_is_not_size_coupled():
    """THE DISTINCTION THE SITTING TURNED ON. Mean pairwise agreement is unbiased at any r >= 2 — two
    solutions can disagree everywhere, so nothing forces coherence at small r. Pairing it with size is
    an empirical question, not arithmetic correlating with its own shadow."""
    assert not S._size_coupled("overlap_ref")
