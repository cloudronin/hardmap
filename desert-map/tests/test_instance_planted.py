"""Planted-refutation construction (I6): roundtrip, exact controlled length, unsat, deterministic hash."""
from __future__ import annotations

import pytest

from desertmap import instance, verify


@pytest.mark.parametrize("n,k", [(20, 3), (20, 5), (20, 8), (30, 5), (40, 7)])
def test_planted_roundtrip_verifies(n, k):
    cnf, proof = instance.gen_planted(n=n, k=k, seed=0)
    assert len(proof) == k, "planted refutation length must equal the controlled chain length k"
    assert verify.verify(cnf.clause_sets(), proof, n_vars=n)


@pytest.mark.parametrize("n,k", [(20, 5), (30, 6)])
def test_planted_instance_is_unsat(n, k):
    cnf, _ = instance.gen_planted(n=n, k=k, seed=3)
    assert instance.is_sat(cnf) is False


def test_planted_hash_is_deterministic():
    a, _ = instance.gen_planted(n=20, k=5, seed=7)
    b, _ = instance.gen_planted(n=20, k=5, seed=7)
    assert a.content_hash() == b.content_hash()
    c, _ = instance.gen_planted(n=20, k=5, seed=8)
    assert a.content_hash() != c.content_hash()


def test_filler_alone_is_satisfiable():
    """C1 certifiable property: filler on its own is SAT ⇒ every refutation must engage the core.

    (We deliberately do NOT assert the planted proof is unique or shortest — that is the W[1] problem the
    experiment probes.)"""
    cnf, _ = instance.gen_planted(n=20, k=5, seed=1)
    assert instance.is_sat(instance.planted_filler(cnf)) is True


def test_every_core_clause_is_needed():
    """Construction detail (disjoint satisfiable filler): dropping any core clause makes the instance sat."""
    cnf, _ = instance.gen_planted(n=20, k=5, seed=1)
    for drop in range(6):   # core occupies indices 0..k (=5) → 6 clauses
        reduced = instance.CNF(cnf.n_vars, cnf.clauses[:drop] + cnf.clauses[drop + 1:])
        assert instance.is_sat(reduced) is True, f"dropping core clause {drop} should make it satisfiable"


# --- C2 hard negatives: "no short proof exists" control category (expected to defeat the relaxation) ---

@pytest.mark.parametrize("holes", [3, 4])
def test_php_is_unsat(holes):
    cnf = instance.gen_php(holes)
    assert cnf.n_vars == (holes + 1) * holes
    assert instance.is_sat(cnf) is False


@pytest.mark.parametrize("nv", [8, 10])
def test_tseitin_is_unsat_and_odd_charge(nv):
    cnf = instance.gen_tseitin(n_vertices=nv, seed=2, degree=3)
    assert cnf.n_vars == nv * 3 // 2
    assert instance.is_sat(cnf) is False


def test_random_3sat_shapes_and_determinism():
    cnf = instance.gen_3sat(n=20, alpha=4.5, seed=0)
    assert cnf.n_clauses == round(4.5 * 20)
    assert all(len(c) == 3 for c in cnf.clauses)
    assert all(1 <= abs(l) <= 20 for c in cnf.clauses for l in c)
    assert instance.gen_3sat(20, 4.5, 0).content_hash() == instance.gen_3sat(20, 4.5, 0).content_hash()
