"""M1 done-gate: the exact Resolution verifier accepts 100 known-valid proofs and rejects 100 corrupted
proofs — plus unit checks on the soft-free resolvent/step primitives. verify.py is the trusted oracle."""
from __future__ import annotations

import pytest

from desertmap import instance, verify


# --- operator units ------------------------------------------------------------------------------

def test_resolvent_cancels_pivot_and_unions():
    a = frozenset({1, 2})       # (x1 ∨ x2)
    b = frozenset({-1, 3})      # (¬x1 ∨ x3)
    assert verify.resolvent(a, b, 1) == frozenset({2, 3})


def test_resolvent_to_empty():
    assert verify.resolvent(frozenset({5}), frozenset({-5}), 5) == frozenset()


def test_step_valid_orientation():
    a, b = frozenset({1, 2}), frozenset({-1, 3})
    assert verify.step_valid(a, b, 1)          # +1 in a, -1 in b
    assert verify.step_valid(b, a, 1)          # symmetric
    assert not verify.step_valid(a, b, 2)      # 2 only positive in a — not resolvable
    assert not verify.step_valid(a, b, 0)      # non-positive pivot
    assert not verify.step_valid(frozenset({1}), frozenset({1}), 1)  # same polarity


def test_resolvent_rejects_nonpositive_pivot():
    with pytest.raises(ValueError):
        verify.resolvent(frozenset({1}), frozenset({-1}), -1)


# --- the 100/100 gate ----------------------------------------------------------------------------

def _valid_corpus(target: int = 100):
    """Deterministically build `target` distinct (cnf, valid-proof) pairs from planted instances."""
    corpus = []
    sizes = (20, 30, 40)
    ks = (3, 4, 5, 6, 7, 8)
    seed = 0
    while len(corpus) < target:
        n = sizes[seed % len(sizes)]
        k = ks[seed % len(ks)]
        cnf, proof = instance.gen_planted(n=n, k=k, seed=seed)
        corpus.append((cnf, proof, n))
        seed += 1
    return corpus


def test_accepts_100_known_valid():
    corpus = _valid_corpus(100)
    assert len(corpus) == 100
    for cnf, proof, n in corpus:
        assert verify.verify(cnf.clause_sets(), proof, n_vars=n), "a known-valid planted proof was rejected"


def _corrupt(proof, kind, n):
    """Return a proof guaranteed INVALID under `kind` (each breaks refutation for sure)."""
    p = list(proof)
    if kind == 0:                       # truncate: drop the final step → empty clause never derived
        return p[:-1]
    if kind == 1:                       # out-of-range parent
        i1, i2, v = p[-1]
        return p[:-1] + [(10_000_000, i2, v)]
    if kind == 2:                       # forward reference: parent index >= current bank size
        i1, i2, v = p[-1]
        return p[:-1] + [(i1, len(proof) + 10_000, v)]
    if kind == 3:                       # illegal pivot (non-positive)
        i1, i2, v = p[-1]
        return p[:-1] + [(i1, i2, 0)]
    if kind == 4:                       # pivot = a variable not resolvable across the final parents
        i1, i2, _ = p[-1]
        return p[:-1] + [(i1, i2, n)]   # var n is a filler var, absent from the chain's unit parents
    raise AssertionError(kind)


def test_rejects_100_corrupted():
    corpus = _valid_corpus(100)
    rejected = 0
    for i, (cnf, proof, n) in enumerate(corpus):
        bad = _corrupt(proof, i % 5, n)
        assert not verify.verify(cnf.clause_sets(), bad, n_vars=n), (
            f"corruption kind {i % 5} on instance {i} still verified"
        )
        rejected += 1
    assert rejected == 100


def test_cnf_range_corruption_caught():
    cnf, proof = instance.gen_planted(n=20, k=5, seed=1)
    bad_cnf = [frozenset({999})] + cnf.clause_sets()[1:]   # literal out of range for n_vars=20
    r = verify.check(bad_cnf, proof, n_vars=20)
    assert not r.ok and "out-of-range" in r.reason
