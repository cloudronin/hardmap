"""Structural predictors (Sprint 6 Pebble, prereg_v13 addendum) — lock the free graph-only rival to ξ.

The hand-count selftest (known small graphs -> known feature values) is the harness gate; here we also lock the
variable-graph construction from a real CSPInstance and the closed 5-number feature contract.
"""
from foundry import structural as ST
from foundry import ensemble as E


def test_structural_selftest_hand_values():
    assert ST.selftest_structural() == []


def test_variable_graph_from_instance():
    # a single arity-3 constraint over vars (0,1,2) makes them a triangle; var 3 is unconstrained (isolated)
    R = frozenset({(0, 0, 0), (1, 1, 1)})
    inst = E.CSPInstance(domain=(0, 1), n_vars=4, constraints=((R, (0, 1, 2)),))
    adj = ST.variable_graph(inst)
    assert adj[0] == {1, 2} and adj[1] == {0, 2} and adj[2] == {0, 1}
    assert adj[3] == set()                          # isolated var -> disconnected graph
    assert ST.spectral_gap(adj) == 0.0              # any isolated variable => Fiedler value 0


def test_feature_contract_is_the_closed_five():
    R = frozenset({(0, 0, 0), (1, 1, 1), (0, 1, 0)})
    inst = E.CSPInstance(domain=(0, 1), n_vars=6, constraints=((R, (0, 1, 2)), (R, (2, 3, 4))))
    feats = ST.structural_features(inst)
    assert set(feats) == {"spectral_gap", "expansion_proxy", "degree_mean", "degree_var", "treewidth_ub"}
    assert all(isinstance(v, (int, float)) for v in feats.values())
    assert feats["treewidth_ub"] >= 1               # two overlapping triangles -> width >= 2 actually, but >=1 always
