"""S1 (constructive saturation) yields verifier-passing refutations, plural across seeds (H1)."""
from __future__ import annotations

from desertmap import fixtures, instance
from proofcensus.sampler_s1 import sample_s1


def test_s1_planted_verifies():
    cnf, _ = instance.gen_planted(n=20, k=5, seed=0)
    r = sample_s1(cnf, seed=1)
    assert r is not None and r.verify()


def test_s1_random_unsat_verifies_and_is_plural():
    cnf = fixtures.gen_unsat_3sat(20, 4.5, fixtures._cell_seed(20, 4.5, 0))
    refs = [sample_s1(cnf, seed=s) for s in range(8)]
    assert all(r is not None and r.verify() for r in refs)      # every sample is a valid refutation
    ids = {frozenset(r.clause_ids()) for r in refs}
    assert len(ids) >= 3, "S1 should produce structurally distinct refutations across seeds (plurality)"
