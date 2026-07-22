"""Factors v1 — the estimator obeys its pre-registered RULES (prereg_v7), not a pinned k*.

These lock the harness (held-out masked-cell CV, the 1-SE parsimonious rule, the maskable-set = real-valued
invariant, the ablation plumbing, the MCA-disqualified sensitivity) and check that the selftest applies its
rule — deliberately NOT that the atlas has any particular k*. Pinning k* would manufacture the science; if the
atlas changed and the dimensionality moved, these tests must still pass.
"""
import numpy as np

from eightfold import charges as C
from eightfold import crucible as X
from eightfold import factors as F

_SMALL = dict(ks=range(1, 6), repeats=5, restarts=3, max_iters=50, loadings=False)


def test_selftest_green():
    # the F-1 gate itself: planted-k recovered AND pure-null quiet (reduced budget wiring check)
    assert F.selftest(verbose=False) == 0


def test_planted_recovered_null_quiet_rule_wellformed():
    # recompute the gate from the estimator outputs (the RULE), not a hard-coded verdict
    rp = F.estimate_rows(F._planted_factor_table(3, n_per=30, seed=F.SEED), seed=F.SEED, **_SMALL)
    rn = F.estimate_rows(F._null_factor_table(90, seed=F.SEED + 7), seed=F.SEED, **_SMALL)
    assert 3 in rp["interval"] and rp["k_hat_1se"] == 3          # recovery
    assert rn["k_hat_1se"] in (0, 1)                              # null quiet


def test_interval_is_within_1se_and_k_hat_is_parsimonious():
    r = F.estimate_rows(F._planted_factor_table(3, n_per=24, seed=F.SEED), seed=F.SEED, **_SMALL)
    best = r["curve"][r["k_argmax"]]["acc_mean"]
    se = r["curve"][r["k_argmax"]]["acc_se"]
    # every k in the interval is within 1 SE of the best; k_hat is the smallest such k (parsimonious 1-SE)
    for k in r["interval"]:
        assert r["curve"][k]["acc_mean"] >= best - se - 1e-9
    assert r["k_hat_1se"] == min(r["interval"])


def test_null_parsimony_quiet_even_when_argmax_noisy():
    # on a flat pure-null curve the argmax may be noisy, but the parsimonious 1-SE k_hat must report 1
    rn = F.estimate_rows(F._null_factor_table(90, seed=F.SEED + 7), seed=F.SEED, **_SMALL)
    assert rn["k_hat_1se"] == 1


def test_maskable_set_is_real_valued_only():
    # open/unmeasured/n.a. -> missing (-1); only real levels are encoded (and thus maskable/scorable)
    rows = [{"decision": "NPC", "counting": "open", "approximation": "n.a.", "parameterized": "FPT",
             "parallelization": "unmeasured", "proof_size": "exp", "average_case": "easy-on-average",
             "landscape": "clustering-proven"}]
    Xmat, cats = F._encode(rows, C.EIGHTFOLD_SPEC)
    charges = list(C.EIGHTFOLD_SPEC.charges)
    assert Xmat[0, charges.index("counting")] == -1      # open -> missing
    assert Xmat[0, charges.index("approximation")] == -1  # n.a. -> missing
    assert Xmat[0, charges.index("parallelization")] == -1  # unmeasured -> missing
    assert Xmat[0, charges.index("decision")] >= 0        # a real level is encoded


def test_factors_verdict_structure_ablations_and_mca_disqualified():
    # the full verdict assembly on a valid synthetic table (crucible's planted toy); tiny budget, no null
    out = F.factors_verdict(X._planted_toy(), with_null=False,
                            budget=dict(repeats=3, restarts=2, max_iters=40, ks=range(1, 4)),
                            ab_budget=dict(repeats=2, restarts=2, max_iters=30, ks=range(1, 4)))
    assert out["factors"] is True and out["prereg"] == "prereg_v7" and out["model"] == "lcm"
    # LOCO ran for every charge; the interval is a non-empty subset of the k-range
    assert set(out["ablations"]["leave_one_charge_out_k_hat"]) == set(C.EIGHTFOLD_SPEC.charges)
    assert out["k_star"]["verdict_interval"] and all(1 <= k <= 6 for k in out["k_star"]["verdict_interval"])
    # drop-measured + sensitivity-roster ablations reported
    assert isinstance(out["ablations"]["drop_measured_k_hat"], int)
    assert "k_hat_1se" in out["ablations"]["sensitivity_other_roster"]
    # MCA present but explicitly flagged S1-disqualified; it is NOT the k* claim
    assert isinstance(out["mca_sensitivity_DISQUALIFIED"]["dims_above_threshold"], int)
    assert "disqualified" in out["mca_sensitivity_DISQUALIFIED"]["note"].lower()


def test_excess_over_null_rule_wellformed():
    # the secondary reuses crucible._null_chain/_envelope on a valid table; check the reported shape/rule
    rows = X.S._grid(X._planted_toy())[2]
    e = F.excess_over_null(rows, k_hat=2, m=5, repeats=2, restarts=2, max_iters=30, burn=100, thin=20)
    for key in ("k_hat", "M", "real_gain_acc_khat_over_k1", "null_envelope", "excess_over_typing", "rule"):
        assert key in e
    assert e["excess_over_typing"] in (True, False, None)


def test_selftest_lowrank_green():
    # prereg_v8 gate: the null-corrected low-rank arm recovers a planted rank AND stays quiet on an independent null
    assert F.selftest_lowrank(verbose=False) == 0


def test_lowrank_is_null_corrected():
    # a rank is credited only if it beats the independence-null envelope (contiguous from rank 1) — so the
    # one-hot compositional artifact cannot be read as structure; an independent null must not credit rank>=2
    r = F.estimate_rows_lowrank(F._null_factor_table(80, dominant_p=0.6, seed=F.SEED + 3),
                                repeats=6, m_null=20, null_repeats=3, seed=F.SEED, loadings=False)
    assert r["k_star_excess"] <= 1
    for k, cell in r["curve"].items():
        assert "beats_null" in cell and "null_gain_p97.5" in cell


def test_sensitivity_floor_smoke():
    # R-v power calibration runs and returns the recovery curve + floor (tiny budget; miss_p given, no atlas load)
    out = F.sensitivity_floor(n=30, planted_k=2, n_seeds=2, separations=(0.9, 0.0),
                              miss_p=0.5, repeats=3, restarts=2, max_iters=30)
    assert out["sensitivity_floor"] is True
    assert set(out["recovery_frac_by_separation"]) == {0.9, 0.0}
    assert out["reliable_recovery_floor_modal_p"] in (0.9, 0.0, None)


def test_estimate_is_spec_portable():
    # the estimator reads levels through the spec (not eightfold module constants) — Foundry can reuse it
    r = F.estimate_rows(F._planted_factor_table(2, n_per=20, seed=F.SEED), spec=C.EIGHTFOLD_SPEC,
                        seed=F.SEED, **_SMALL)
    assert r["charges"] == list(C.EIGHTFOLD_SPEC.charges)
    assert r["model"] == "lcm" and 1 <= r["k_hat_1se"] <= 5
