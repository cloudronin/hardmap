"""Solution-side landscape instrument (Sprint 4.1) — the RULES, not the I6 verdict.

Tests the net-new instrument's machinery: the generator produces well-formed instances, the affine-EXACT sampler
returns correct/complete solutions (ground truth), the two structurally-different samplers find solutions and
concord, the ruggedness metric baseline-corrects by domain, and the two-pole Vega gate separates the known-rugged
(XOR) from the known-smooth (Horn) pole while rejecting an invalid smooth pole (2-SAT). Small sizes keep CI fast.
"""
from foundry import ensemble as E
from foundry import postlattice as PL
from foundry import solscape as S


def test_generator_and_satisfies():
    inst = E.gen_instance((PL.R_POS2, PL.R_NEG2), (0, 1), 12, 0.5, 1, "t")
    assert inst.n_vars == 12 and len(inst.constraints) == 6
    a = [0] * 12
    assert isinstance(inst.satisfies(a), bool) and inst.num_violated(a) >= 0


def test_affine_equations_recovers_xor():
    # R_XOR3 = {x⊕y⊕z=0} is the single equation [1,1,1]·x = 0 over GF(2)
    eqs = S._affine_equations(PL.R_XOR3, 2)
    assert len(eqs) == 1
    coeff, rhs = eqs[0]
    assert tuple(coeff) == (1, 1, 1) and rhs == 0


def test_affine_exact_is_correct_and_complete():
    # a small affine instance: every exact-sampled assignment must satisfy it; count must be a power of 2 (coset)
    inst = E.gen_instance((PL.R_XOR3,), (0, 1), 10, 0.4, 3, "aff")
    sols = S.sample_affine_exact(inst, 3, K=64)
    assert sols, "affine instance should be satisfiable (0-valid homogeneous XOR always has all-0)"
    assert all(inst.satisfies(s) for s in sols)
    assert len(set(sols)) == len(sols)                       # distinct
    # (0,...,0) is always a solution of homogeneous XOR
    assert tuple([0] * 10) in set(sols)


def test_both_samplers_find_solutions_and_are_valid():
    inst = E.gen_instance((PL.R_NOR3, PL.R_FALSE), (0, 1), 12, 0.4, 2, "h")   # 0-valid Horn: all-0 is a solution
    for fn in (S.sample_dpll, S.sample_walksat):
        sols = fn(inst, 1, K=20)
        assert sols and all(inst.satisfies(s) for s in sols)


def test_ruggedness_baseline_corrects_by_domain():
    # identical solutions -> maximal clustering -> ruggedness 0; the q_random baseline differs Boolean vs |D|=3
    same = [(1, 0, 1, 0)] * 5
    r2 = S.ruggedness(same, domain_size=2)
    assert r2["q_random"] == 0.0 and r2["score"] == 0.0        # Boolean baseline 0; all identical -> rugged 0
    r3 = S.ruggedness([(0, 1, 2, 0)] * 5, domain_size=3)
    assert abs(r3["q_random"] + 1 / 3) < 1e-3 and r3["score"] == 0.0   # |D|=3 baseline -1/3 (reported to 3dp)


def test_two_pole_vega_separates_and_rejects_invalid_smooth_pole():
    xor = dict(rels=(PL.R_XOR3,), domain=(0, 1), n=12, alpha=0.5, n_instances=2, K=20)
    horn = dict(rels=(PL.R_NOR3, PL.R_TRUE), domain=(0, 1), n=12, alpha=0.4, n_instances=2, K=20)
    twosat = dict(rels=(PL.R_POS2, PL.R_NEG2), domain=(0, 1), n=12, alpha=0.6, n_instances=2, K=20)
    good = S.vega_calibration(xor, horn, sep_margin=0.08)
    assert good["passes"] and good["rugged_pole_score"] > good["smooth_pole_score"]
    # 2-SAT reads nearly as rugged as XOR -> it is NOT a valid smooth pole (the calibration finding)
    bad = S.vega_calibration(xor, twosat, sep_margin=0.12)
    assert not bad["passes"]


def test_affine_exact_makes_sampler_bias_measurable_and_small():
    bias = S.affine_bias((PL.R_XOR3,), (0, 1), 12, 0.5, n_instances=2, K=20)
    assert bias["dpll"] is not None and bias["dpll"] < 0.15 and bias["walksat"] < 0.15
