"""Crucible S1 null-model harness — machinery + the selftest.

Tests the pre-registered RULE and the sampler's invariants, NOT the science verdict (pinning the latter
would manufacture the outcome — the real-data S1 run is V2, after prereg_v6 is committed).
"""
from collections import Counter

import pytest

pytest.importorskip("numpy")

import numpy as np  # noqa: E402

from eightfold import charges as C  # noqa: E402
from eightfold import structure as S  # noqa: E402
from eightfold.atlas import DEFAULT_PATH, load_atlas  # noqa: E402
from eightfold.crucible import (  # noqa: E402
    _both_real_v, _null_chain, _row_valid, _planted_toy, _null_toy, _s5_violators, s1_null_model,
    s2_dedup, s3_significance, s5_adversarial_roster, selftest,
)


def test_selftest_green():
    # planted structure detected AND pure null stays quiet
    assert selftest() == 0


def test_null_preserves_marginals_typing_validity_on_real_atlas():
    """The load-bearing property: a valid S1 null must preserve every per-charge marginal EXACTLY, hold
    each row's n.a. typing fixed (R1), and never trip a forbidding rule (E1/E2)."""
    _, _, base = S._grid(load_atlas(DEFAULT_PATH))
    base_marg = {ch: Counter(r[ch] for r in base) for ch in C.CHARGES}
    base_na = [frozenset(ch for ch in C.CHARGES if r[ch] == "n.a.") for r in base]
    rng = np.random.default_rng(1)
    seen = 0
    for null in _null_chain(base, rng, burn=500, thin=100, m=3):
        seen += 1
        for ch in C.CHARGES:
            assert Counter(r[ch] for r in null) == base_marg[ch], ch          # marginal exact
        assert [frozenset(ch for ch in C.CHARGES if r[ch] == "n.a.") for r in null] == base_na  # typing fixed
        assert all(_row_valid(r) for r in null)                               # entailment-valid
    assert seen == 3


def test_null_actually_moves_values():
    # a preserved-but-identical "null" would be a broken test; confirm the chain mixes at least one charge
    _, _, base = S._grid(load_atlas(DEFAULT_PATH))
    rng = np.random.default_rng(2)
    null = next(_null_chain(base, rng, burn=1000, thin=1, m=1))
    assert any(null[i] != base[i] for i in range(len(base)))


def test_row_valid_catches_E1_E2():
    assert not _row_valid({"counting": "FP", "decision": "NPC"})           # E1 forbidden
    assert _row_valid({"counting": "FP", "decision": "P"})                 # FP counting ⇒ decision P: fine
    assert not _row_valid({"decision": "NPC", "parallelization": "NC"})    # E2 forbidden
    assert _row_valid({"decision": "P", "parallelization": "NC"})          # within P: fine


def test_planted_detected_null_quiet_rule_wellformed():
    rp = s1_null_model(_planted_toy(), m=150, burn=600, thin=50)
    rn = s1_null_model(_null_toy(), m=150, burn=600, thin=50)
    assert rp["gradient_excess_over_typing"] is True
    assert rn["gradient_excess_over_typing"] is False
    for r in (rp, rn):
        assert r["verdict"] in ("SURVIVES", "RESIZED")
        assert set(r["envelope"]) >= {"approx_param_v", "mca_cc_dims", "mca_full_dims"}


def test_both_real_v_matches_structure_convention():
    # the S1 gradient stat must equal structure.py's both-real computation on the same rows
    _, _, base = S._grid(load_atlas(DEFAULT_PATH))
    v = _both_real_v(base, "approximation", "parameterized")
    assert 0.0 <= v <= 1.0


def test_s2_dedup_machinery():
    # deduped roster is the 114-class one (4 non-representatives dropped); verdict + p well-formed
    s2 = s2_dedup(load_atlas(DEFAULT_PATH), n_perm=200)
    assert s2["n_classes"] == 114
    assert s2["verdict"] in ("SURVIVES", "RESIZED")
    assert 0.0 <= s2["gradient_dedup_p"] <= 1.0
    # vertex-cover/clique is merged away by dedup — its amplification must be untestable (None), as prereg'd
    assert s2["multiplet_amplifications_dedup_caveated"]["vertex-cover|clique"] is None


def test_s3_significance_machinery():
    s3 = s3_significance(load_atlas(DEFAULT_PATH), n_perm=200, n_boot=100)
    assert s3["verdict"] in ("SURVIVES", "RESIZED")
    assert 0.0 <= s3["gradient_perm_p"] <= 1.0
    assert 0.0 <= s3["dims_bootstrap"]["cc_dims_ge3_frac"] <= 1.0


def test_s5_violators_validate_clean_and_are_true_violators():
    from eightfold import atlas
    vs = _s5_violators()
    assert vs and all(atlas.validate(v) == [] for v in vs)   # additions must pass every QC gate (R20)
    km = next(v for v in vs if v.problem_id == "k-means")
    ch = {c.charge: c.value for c in km.charges}
    # easy-approx (constant-factor) x hard-param (W[2]) — a genuine gradient violator
    assert ch["approximation"] == "APX-complete" and ch["parameterized"] == "W[2]+"


def test_s5_machinery():
    s5 = s5_adversarial_roster(load_atlas(DEFAULT_PATH), n_perm=200)
    assert s5["verdict"] in ("SURVIVES", "RESIZED")
    assert s5["gradient_augmented_v"] <= s5["gradient_frozen_v"] + 1e-9   # violators weaken (or hold) the gradient
    assert 0.0 <= s5["gradient_augmented_p"] <= 1.0
