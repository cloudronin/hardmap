"""S2 (DPLL → tree-resolution) verifies (R3 regression is sound), is plural, and honors the node budget (R2)."""
from __future__ import annotations

from desertmap import fixtures, instance
from proofcensus.sampler_s2 import BUDGET_EXCEEDED, sample_s2


def test_s2_planted_verifies():
    cnf, _ = instance.gen_planted(n=20, k=5, seed=0)
    r = sample_s2(cnf, seed=1)
    assert r not in (None, BUDGET_EXCEEDED) and r.verify()


def test_s2_random_unsat_verifies_and_is_plural():
    """The regression step (R3) is what makes these verify — propagated variables resolved out."""
    cnf = fixtures.gen_unsat_3sat(20, 4.5, fixtures._cell_seed(20, 4.5, 0))
    refs = [sample_s2(cnf, seed=s) for s in range(8)]
    assert all(r not in (None, BUDGET_EXCEEDED) and r.verify() for r in refs)
    ids = {frozenset(r.clause_ids()) for r in refs}
    assert len(ids) >= 3, "S2 should produce structurally distinct tree-resolution proofs across seeds"


def test_s2_node_budget_returns_sentinel():
    cnf = fixtures.gen_unsat_3sat(20, 4.5, fixtures._cell_seed(20, 4.5, 0))
    assert sample_s2(cnf, seed=1, node_budget=1) is BUDGET_EXCEEDED   # 1 node can't refute → counted, not crash


def test_s2_proofs_are_longer_than_s1_province_separation():
    """Tree proofs repeat work → systematically longer than S1 DAG proofs (R1 province separation)."""
    from proofcensus.sampler_s1 import sample_s1
    cnf = fixtures.gen_unsat_3sat(20, 4.5, fixtures._cell_seed(20, 4.5, 0))
    s1 = [sample_s1(cnf, seed=s).length for s in range(6)]
    s2 = [sample_s2(cnf, seed=s).length for s in range(6)]
    assert sorted(s2)[len(s2) // 2] > sorted(s1)[len(s1) // 2]
