"""K-sampling driver: reaches K verified refutations with disjoint three-way accounting (R2)."""
from __future__ import annotations

import pytest

from desertmap import fixtures
from proofcensus.sample import sample_k


@pytest.mark.parametrize("sampler", ["s1", "s2"])
def test_sample_k_reaches_K_verified(sampler):
    cnf = fixtures.gen_unsat_3sat(20, 4.5, fixtures._cell_seed(20, 4.5, 0))
    res = sample_k(cnf, sampler, K=5, seed=0)
    assert res.n_verified == 5
    assert len(res.refutations) == 5
    assert all(r.verify() for r in res.refutations)               # only verifier-passing proofs kept
    # accounting is disjoint and covers every attempt
    assert res.n_attempts == res.n_verified + res.n_verify_discard + res.n_budget_exceeded


def test_budget_exceeded_counted_separately():
    """A tiny S2 node budget forces budget-exceeded attempts, counted apart from verify-discards (R2)."""
    cnf = fixtures.gen_unsat_3sat(20, 4.5, fixtures._cell_seed(20, 4.5, 0))
    res = sample_k(cnf, "s2", K=1, seed=0, node_budget=1, max_attempts=5)
    assert res.n_verified == 0
    assert res.n_budget_exceeded == res.n_attempts               # every attempt hit the budget
    assert res.n_verify_discard == 0


def test_parallel_driver_matches_gating():
    """The parallel sweep driver yields K verified proofs with the same three-way accounting."""
    from proofcensus.sweep import sample_k_parallel
    cnf = fixtures.gen_unsat_3sat(20, 4.5, fixtures._cell_seed(20, 4.5, 0))
    res = sample_k_parallel(cnf, "s1", K=6, seed=0, n_workers=2)
    assert res.n_verified == 6
    assert all(r.verify() for r in res.refutations)
    assert res.n_attempts == res.n_verified + res.n_verify_discard + res.n_budget_exceeded
