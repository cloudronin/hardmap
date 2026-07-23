"""Point-to-set reach instrument (Pebble P2b, prereg_v21) — the B0 gate. Hand-computed known-answer cases lock BOTH
sensitivity (parity reads maximal where pairwise reads zero) and specificity (a disconnected far boundary reads
zero). An instrument that read everything as maximal would pass the parity case alone; the negative case is what
rules it out. The three-pole calibration VERDICT lives in the findings, not here."""
from foundry import pointset as PS
from foundry import ensemble as E
from foundry.reach import connected_corr, enumerate_solutions


def test_pointset_selftest_hand_values():
    assert PS.selftest_pointset() == []


def test_parity_sensitivity_and_pairwise_blindness():
    # 3-var parity: point-to-set target x2 vs boundary {x0,x1} = 0.5 (maximal); pairwise = 0.0.
    R3 = frozenset({(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)})
    par = E.CSPInstance((0, 1), 3, ((R3, (0, 1, 2)),))
    sols = enumerate_solutions(par)
    assert PS.pointset_signal(par, sols, 2, 1)["signal"] == 0.5
    assert max(abs(connected_corr(sols, 2, u, (0, 1))) for u in (0, 1)) < 1e-9


def test_specificity_disconnected_far_boundary_reads_zero():
    ROR = frozenset({(0, 1), (1, 0), (1, 1)})
    dec = E.CSPInstance((0, 1), 4, ((ROR, (0, 1)), (ROR, (2, 3))))
    sols = enumerate_solutions(dec)
    assert PS.pointset_signal(dec, sols, 0, 2)["signal"] == 0.0    # far boundary {x2,x3}: independent -> 0
    assert PS.pointset_signal(dec, sols, 0, 1)["signal"] > 0.0     # near boundary includes linked x1 -> > 0


def test_boundary_shell_includes_unreachable():
    ROR = frozenset({(0, 1), (1, 0), (1, 1)})
    dec = E.CSPInstance((0, 1), 4, ((ROR, (0, 1)), (ROR, (2, 3))))
    from foundry.reach import bfs_distances, variable_graph
    dist = bfs_distances(variable_graph(dec), 0)
    assert set(PS.boundary_shell(dist, 4, 0, 2)) == {2, 3}         # x1 (dist 1) out; x2,x3 (unreachable) in
    assert set(PS.boundary_shell(dist, 4, 0, 1)) == {1, 2, 3}


def test_bucket_stats_reported():
    R3 = frozenset({(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)})
    par = E.CSPInstance((0, 1), 3, ((R3, (0, 1, 2)),))
    r = PS.pointset_signal(par, enumerate_solutions(par), 2, 1)
    assert r["n_buckets"] == 4 and r["min_pop"] == 1              # parity: 4 singleton buckets (the signal lives there)
