"""Exact Resolution verifier — the trusted, dependency-free oracle (M1, AGENTS.md invariant 1).

A run "succeeds" iff its *decoded discrete* proof verifies HERE — never because a soft loss is low. This
module must import and run with NO ML stack (no torch/numpy); it is the backstop the whole experiment
trusts. Keep it pure-stdlib.

Conventions
-----------
Literals are signed nonzero ints (DIMACS style): variable v ∈ {1..n}, positive literal ``+v``, negative
literal ``-v``. A clause is a ``frozenset[int]`` of literals; the empty clause is ``frozenset()``. A CNF is a
list/sequence of clauses (the original formula). A discrete proof is a sequence of resolution steps
``(i1, i2, pivot)`` where ``i1, i2`` index the *bank* (0..m-1 = original clauses in order, then each derived
resolvent appended in derivation order) and ``pivot`` is an unsigned variable in {1..n}.

A step ``(i1, i2, v)`` is valid iff one parent contains ``+v`` and the other contains ``-v`` (either
orientation). Its resolvent is ``(A | B) \\ {+v, -v}``. The refutation succeeds iff some derived resolvent is
the empty clause.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

Literal = int
Clause = frozenset  # frozenset[int]
Step = tuple  # (i1: int, i2: int, pivot: int)


def resolvent(a: Clause, b: Clause, pivot: int) -> Clause:
    """Return the resolvent of clauses ``a`` and ``b`` on unsigned variable ``pivot``.

    Requires ``pivot > 0``. Does NOT check orientation validity — use :func:`step_valid` for that. The
    resolvent is ``(a ∪ b)`` with both polarities of the pivot removed.
    """
    if pivot <= 0:
        raise ValueError(f"pivot must be a positive variable index, got {pivot}")
    return frozenset(a | b) - {pivot, -pivot}


def step_valid(a: Clause, b: Clause, pivot: int) -> bool:
    """True iff resolving ``a`` and ``b`` on ``pivot`` is a legal resolution step.

    Legal iff exactly-opposite polarities of ``pivot`` appear across the two parents: (``+v`` in a and
    ``-v`` in b) or (``-v`` in a and ``+v`` in b).
    """
    if pivot <= 0:
        return False
    return (pivot in a and -pivot in b) or (-pivot in a and pivot in b)


@dataclass(frozen=True)
class VerifyResult:
    """Detailed verification outcome (the boolean :func:`verify` wraps this)."""

    ok: bool                       # did the proof derive the empty clause via all-valid steps?
    empty_at: int | None           # bank index of the first empty clause derived (None if never)
    first_bad_step: int | None     # index into proof of the first invalid step (None if all valid)
    reason: str                    # human-readable explanation


def check(cnf: Sequence[Iterable[int]], proof: Sequence[Step], n_vars: int | None = None) -> VerifyResult:
    """Verify a discrete resolution proof against ``cnf``; return a detailed :class:`VerifyResult`.

    Every step is checked for (a) in-range, causal bank references and (b) legal pivot orientation. The
    proof succeeds the moment an empty resolvent is produced; trailing unused steps are still processed but
    do not affect success (an earlier empty clause already refutes). An out-of-range or forward reference,
    or an illegal pivot, makes the whole proof invalid.
    """
    bank: list[Clause] = [frozenset(c) for c in cnf]
    m = len(bank)

    # Validate variable ranges in the original CNF if n_vars is given (cheap corruption catch).
    if n_vars is not None:
        for ci, c in enumerate(bank):
            for lit in c:
                if lit == 0 or abs(lit) > n_vars:
                    return VerifyResult(False, None, None,
                                        f"cnf clause {ci} has out-of-range literal {lit} (n_vars={n_vars})")

    empty_at: int | None = None
    for si, step in enumerate(proof):
        if len(step) != 3:
            return VerifyResult(False, None, si, f"step {si} is not a 3-tuple (i1,i2,pivot): {step!r}")
        i1, i2, pivot = step
        cur = len(bank)  # index the resolvent will occupy; parents must be strictly earlier (causal)
        if not (0 <= i1 < cur and 0 <= i2 < cur):
            return VerifyResult(False, empty_at, si,
                                f"step {si} references bank rows ({i1},{i2}) not in [0,{cur}) (forward/oob)")
        a, b = bank[i1], bank[i2]
        if not step_valid(a, b, pivot):
            return VerifyResult(False, empty_at, si,
                                f"step {si} invalid: pivot {pivot} not resolvable across parents {i1},{i2}")
        r = resolvent(a, b, pivot)
        bank.append(r)
        if not r:
            # The empty clause is derived: the refutation is complete. Stop here — trailing steps (e.g. the
            # decoder always emits the full budget L of steps) are irrelevant and must not invalidate a
            # valid refutation. Every step processed so far was checked valid.
            empty_at = len(bank) - 1
            return VerifyResult(True, empty_at, None, f"empty clause derived at bank row {empty_at}")

    return VerifyResult(False, None, None, "no empty clause derived (proof does not refute)")


def verify(cnf: Sequence[Iterable[int]], proof: Sequence[Step], n_vars: int | None = None) -> bool:
    """Boolean gate: True iff ``proof`` is a valid Resolution refutation of ``cnf``. Wraps :func:`check`."""
    return check(cnf, proof, n_vars).ok
