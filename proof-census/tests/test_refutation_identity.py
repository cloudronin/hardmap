"""Canonical clause identity (I3), proof identity sets, and Jaccard/overlap correctness."""
from __future__ import annotations

from desertmap import instance
from proofcensus.refutation import Refutation, clause_id, jaccard, overlap_q


def test_clause_id_is_canonical():
    assert clause_id([2, -1, 3]) == clause_id([-1, 3, 2]) == (-1, 2, 3)
    assert clause_id([]) == ()                      # empty clause id


def test_refutation_verifies_and_reports_identity():
    cnf, proof = instance.gen_planted(n=20, k=5, seed=0)
    ref = Refutation(cnf.n_vars, tuple(cnf.clauses), tuple(proof))
    assert ref.verify()
    assert ref.length == 5
    ids = ref.clause_ids()
    assert () in ids                                # the empty clause is a node
    assert clause_id(cnf.clauses[0]) in ids         # (x1) core clause appears


def test_jaccard_and_overlap_q():
    assert jaccard(frozenset({1, 2}), frozenset({1, 2})) == 1.0
    assert jaccard(frozenset({1}), frozenset({2})) == 0.0
    assert jaccard(frozenset({1, 2, 3}), frozenset({2, 3, 4})) == 0.5


def test_overlap_q_maps_jaccard_to_pm1():
    cnf, proof = instance.gen_planted(n=20, k=5, seed=0)
    ref = Refutation(cnf.n_vars, tuple(cnf.clauses), tuple(proof))
    assert overlap_q(ref, ref) == 1.0               # identical proofs → q=1
