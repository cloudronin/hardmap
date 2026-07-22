"""Rigidity rank (prereg_v10) — the RULES. Rank is derived from the polymorphism flags alone (anti-circularity);
the PARTIAL verdict lives in the findings, not here."""
from foundry.rigidity import rigidity_rank


def test_rank_is_strongest_term_present():
    assert rigidity_rank(["aff"])[0] == 4                       # Maltsev
    assert rigidity_rank(["bij", "aff"])[0] == 4               # Maltsev wins over majority
    assert rigidity_rank(["0v", "horn", "bij"])[0] == 3        # majority
    assert rigidity_rank(["0v", "1v", "horn"])[0] == 2         # semilattice
    assert rigidity_rank(["0v", "1v", "dhorn"])[0] == 2


def test_zero_one_valid_only_is_edge_rank0():
    r, name, edge = rigidity_rank(["0v"])
    assert r == 0 and edge is True
    assert rigidity_rank(["0v", "1v"])[2] is True
    assert rigidity_rank(["1v"])[2] is True
