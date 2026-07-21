"""Refutation object + canonical clause identity (I3) — the single source of clause equality.

A refutation is an ordered list of resolution steps ``(i1, i2, pivot)`` over a bank whose rows are the
original CNF clauses (indices ``0..m-1``) followed by each derived resolvent in derivation order (signed-int
literal convention of :mod:`desertmap.verify`). A derived resolvent's IDENTITY is its canonical sorted-literal
tuple, so identical resolvents produced by different proofs compare equal. A proof's ``clause_ids`` is the set
of canonical ids of every clause appearing as a node in its DAG (originals used as parents + all resolvents);
population overlap is Jaccard on these sets.
"""
from __future__ import annotations

from dataclasses import dataclass

from desertmap import verify


def clause_id(literals) -> tuple:
    """Canonical identity of a clause: literals sorted by (|var|, sign). Empty clause → ``()``."""
    return tuple(sorted(literals, key=lambda x: (abs(x), x < 0)))


@dataclass(frozen=True)
class Refutation:
    """A verifiable Resolution refutation, sampler-agnostic. ``origin_clauses`` is the full CNF (shared
    across samples of one instance); ``steps`` index the bank (originals then derived resolvents)."""

    n_vars: int
    origin_clauses: tuple            # ((lit,...), ...) — the original formula, canonical per clause
    steps: tuple                     # ((i1, i2, pivot), ...)

    @property
    def length(self) -> int:
        """Number of resolution steps (proof length)."""
        return len(self.steps)

    def bank(self) -> list[frozenset]:
        """Rebuild the full clause bank by executing the steps (originals + derived resolvents)."""
        bank = [frozenset(c) for c in self.origin_clauses]
        for (i1, i2, pv) in self.steps:
            bank.append(frozenset(bank[i1] | bank[i2]) - {pv, -pv})
        return bank

    def clause_ids(self) -> frozenset:
        """Canonical ids of every clause that is a node in the proof DAG (parents used + resolvents)."""
        bank = [frozenset(c) for c in self.origin_clauses]
        ids: set[tuple] = set()
        for (i1, i2, pv) in self.steps:
            a, b = bank[i1], bank[i2]
            r = frozenset(a | b) - {pv, -pv}
            bank.append(r)
            ids.add(clause_id(a)); ids.add(clause_id(b)); ids.add(clause_id(r))
        return frozenset(ids)

    def verify(self) -> bool:
        """True iff this is a valid Resolution refutation of ``origin_clauses`` (the frozen M1 oracle)."""
        return verify.verify([frozenset(c) for c in self.origin_clauses], self.steps, n_vars=self.n_vars)


def jaccard(a: frozenset, b: frozenset) -> float:
    """|a∩b| / |a∪b| ∈ [0,1]; 1.0 for two empty sets (degenerate but well-defined)."""
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


def overlap_q(a: "Refutation", b: "Refutation") -> float:
    """Spin-overlap of two proofs: q = 2·Jaccard(clause_ids) − 1 ∈ [−1, 1] (Desert Map I2 convention)."""
    return 2.0 * jaccard(a.clause_ids(), b.clause_ids()) - 1.0
