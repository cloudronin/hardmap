"""Reach instrument ξ (Sprint 6 Pebble, P2) — lock the machinery. The three-pole calibration VERDICT lives in the
findings (it is an empirical run), not here; here we lock BFS distance, conditioning, the observables' behaviour on
hand-computed media, and the parity-blindness that forces the 2-affine long pole."""
from foundry import reach as X
from foundry import ensemble as E


def test_reach_selftest():
    assert X.selftest_reach() == []


def test_bfs_hand_instance():
    R = frozenset({(0, 0, 0), (1, 1, 1)})
    inst = E.CSPInstance((0, 1), 6, ((R, (0, 1, 2)), (R, (2, 3, 4))))   # var 5 isolated
    dist = X.bfs_distances(X.variable_graph(inst), 0)
    assert {u: dist.get(u) for u in range(6)} == {0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: None}


def test_condition_forces_variable():
    inst = E.CSPInstance((0, 1), 3, ((frozenset({(0, 0, 0), (1, 1, 1)}), (0, 1, 2)),))
    cond = X.condition(inst, 0, 1)
    sols = X._solutions(cond, "exact", 0, 0)
    assert sols and all(s[0] == 1 for s in sols)                        # every solution has x0 pinned to 1


def test_matching_short_pole_has_zero_far_reach():
    # the decoupled short pole (a matching) has no d>=2 pairs -> reach_score exactly 0 by construction
    inst = X._matching_instance(X.R_EQ, (0, 1), 8, seed=1)
    prof = X.aggregate([X.correlation_profile(inst, v, sampler="exact") for v in range(8)])
    assert X.reach_score(prof) == 0.0


def test_parity_blind_but_2affine_visible():
    # 3-ary XOR: both observables read ~0 (documents why the affine pole is 2-affine)
    x = E.CSPInstance((0, 1), 3, ((frozenset({(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)}), (0, 1, 2)),))
    assert max(X.aggregate([X.forcing_profile(x, 0, 1, sampler="exact")]).values(), default=0) < 1e-9
    assert max(X.aggregate([X.correlation_profile(x, 0, sampler="exact")]).values(), default=0) < 1e-9
    # 2-affine equality chain: correlation reaches far
    eqc = E.CSPInstance((0, 1), 4, tuple((X.R_EQ, (i, i + 1)) for i in range(3)))
    pc = X.aggregate([X.correlation_profile(eqc, 0, sampler="exact")])
    assert pc.get(3, 0) > 0.1
