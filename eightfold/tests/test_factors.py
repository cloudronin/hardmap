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


def test_degenerate_secondary_zero_is_kept_and_acknowledged():
    # instance 26's rule, applied to the k*=1 secondary: the zero STAYS (it is what the expression
    # evaluates to) and the artifact says why, rather than being encoded as `null` — which would assert
    # NOT COMPUTED about a value that was. The acknowledgement is derived from the run, so it exists
    # exactly when the block is degenerate.
    out = F.factors_verdict(X._planted_toy(), with_null=True,
                            budget=dict(repeats=3, restarts=2, max_iters=40, ks=range(1, 4)),
                            ab_budget=dict(repeats=2, restarts=2, max_iters=30, ks=range(1, 4)))
    e = out["excess_over_null"]
    acked = {a["stat"]: a for a in out["extremal_acknowledged"]}
    if e.get("applicable") is False:
        assert e["real_gain_acc_khat_over_k1"] == 0.0
        a = acked["excess_over_null.real_gain_acc_khat_over_k1"]
        assert a["value"] == 0.0 and a["identity_arithmetic"]["nulls_drawn"] == 0
        assert "INVARIANT UNDER THE INPUT" in a["why_the_exactness_is_expected"]
    else:                                              # non-degenerate run: no acknowledgement is owed
        assert "excess_over_null.real_gain_acc_khat_over_k1" not in acked


def test_excess_over_null_rule_wellformed():
    # the secondary reuses crucible._null_chain/_envelope on a valid table; check the reported shape/rule
    rows = X.S._grid(X._planted_toy())[2]
    e = F.excess_over_null(rows, k_hat=2, m=5, repeats=2, restarts=2, max_iters=30, burn=100, thin=20)
    for key in ("k_hat", "M", "real_gain_acc_khat_over_k1", "null_envelope", "excess_over_typing", "rule"):
        assert key in e
    assert e["excess_over_typing"] in (True, False, None)
    assert e["applicable"] is True


def test_excess_over_null_is_inapplicable_not_false_at_k_hat_1():
    # THE DEGENERACY (found by the tidy-number gate, 2026-07-25). At k_hat == 1 the statistic is
    # acc[1] - acc[1] = 0 on every table, real and null alike, so the old block reported an all-zero envelope
    # with one_sided_p_ge = 1.0 and declared `excess_over_typing: false` — a verdict no input could have
    # changed. The estimator must now say it has nothing to say, and must not burn M nulls proving 0 == 0.
    rows = X.S._grid(X._planted_toy())[2]
    e = F.excess_over_null(rows, k_hat=1, m=5, repeats=2, restarts=2, max_iters=30, burn=100, thin=20)
    assert e["applicable"] is False
    assert e["excess_over_typing"] is None            # NOT False — false is a test outcome, and none was had
    assert e["null_envelope"] is None                 # a constant has no distribution: UNDEFINED, not unmeasured
    assert e["M"] == 0                                # the null loop is skipped, not run and discarded
    assert "identically" in e["not_applicable_reason"]
    # the GAIN is kept, not nulled (instance 26: encoding a computed value as `null` asserts NOT COMPUTED
    # about something that was). It is 0.0, and it owes the tidy-number gate an acknowledgement — which
    # factors_verdict derives from this block rather than hardcoding.
    assert e["real_gain_acc_khat_over_k1"] == 0.0


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
    # the acknowledgements are DERIVED from this run's numbers, not a fixed list that outlives its data.
    # The acknowledger's contract is exactly two adjudicated causes — the k=0 self-identity, and a
    # null_gain_p97.5 that lands inside the discretised null's zero atom — and it must cover those and
    # nothing else. An extremal at a cause nobody has read must stay UNacknowledged so the tidy-number gate
    # is the thing that fails on it; an acknowledgement for a value that is not extremal is a stale waiver.
    acked = {a["stat"] for a in r["extremal_acknowledged"]}
    contract = {f"curve.{k}.{f}" for k, cell in r["curve"].items()
                for f in ("gain_over_k0", "null_gain_p97.5")
                if cell[f] == 0.0 and (k == 0 or f == "null_gain_p97.5")}
    assert acked == contract
    assert {"curve.0.gain_over_k0", "curve.0.null_gain_p97.5"} <= acked   # the k=0 identities, always
    # every acknowledgement points at a value that really is extremal, and carries a reason
    for a in r["extremal_acknowledged"]:
        k, field = a["stat"].split(".")[1], a["stat"].split(".", 2)[2]
        assert r["curve"][int(k)][field] == a["value"] == 0.0
        assert len(a["why_the_exactness_is_expected"]) > 80


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
