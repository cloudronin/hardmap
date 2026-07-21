"""A1 — satisfiable-instance negative control (spec §3.5): the verifier backstop is actually wired.

Resolution is sound: a satisfiable CNF has NO refutation, so no decoded proof may ever verify on a SAT
instance. Here we prove the backstop at the verifier level — SAT control instances are confirmed sat, and a
large battery of arbitrary discrete proofs never verifies against them. (Phase 2 extends this to run the
real relaxation + decode end-to-end via run.py; the assertion is the same: zero decodes verify.)"""
from __future__ import annotations

import numpy as np
import pytest

from desertmap import fixtures, instance, verify


def _random_proof(n_clauses: int, n_vars: int, length: int, rng) -> list[tuple]:
    """Arbitrary (causally valid-indexed) discrete proof; pivots random — most steps will be illegal."""
    proof = []
    for t in range(length):
        cur = n_clauses + t
        i1 = int(rng.integers(0, cur))
        i2 = int(rng.integers(0, cur))
        pivot = int(rng.integers(1, n_vars + 1))
        proof.append((i1, i2, pivot))
    return proof


@pytest.mark.parametrize("idx", range(5))
def test_sat_control_instances_are_satisfiable(idx):
    cnf = fixtures.gen_sat_3sat(fixtures.SAT_CTRL_N, fixtures.SAT_CTRL_ALPHA,
                                fixtures._cell_seed(fixtures.SAT_CTRL_N, fixtures.SAT_CTRL_ALPHA, idx))
    assert instance.is_sat(cnf) is True


def test_no_random_proof_verifies_on_sat_instances():
    """Backstop: across many SAT instances × many random proofs, the verifier never reports success."""
    rng = np.random.default_rng(0)
    verified = 0
    for cnf in fixtures.iter_sat_control(count=5):
        for _ in range(200):
            proof = _random_proof(cnf.n_clauses, cnf.n_vars, length=4 * cnf.n_vars, rng=rng)
            if verify.verify(cnf.clause_sets(), proof, n_vars=cnf.n_vars):
                verified += 1
    assert verified == 0, "verifier accepted a 'refutation' of a satisfiable instance — backstop is broken"


def test_soundness_even_a_wellformed_chain_cannot_refute_sat():
    """A structurally valid resolution chain still cannot derive the empty clause from a sat instance."""
    cnf = next(iter(fixtures.iter_sat_control(count=1)))
    # Attempt: resolve consecutive clauses on shared variables where possible; never reaches empty.
    proof, bank = [], cnf.clause_sets()
    for i in range(len(bank) - 1):
        a, b = bank[i], bank[i + 1]
        shared = [abs(l) for l in a if -l in b]
        if shared:
            proof.append((i, i + 1, shared[0]))
    assert not verify.verify(cnf.clause_sets(), proof, n_vars=cnf.n_vars)
