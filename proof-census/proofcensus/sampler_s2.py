"""S2 — randomized DPLL → tree-resolution sampler (tree-like refutations).

DPLL ≡ tree resolution: the decision tree of a DPLL run on an unsat CNF unfolds into a tree-resolution
refutation. Randomized decision variable + polarity per run ⇒ different trees across seeds (H1);
structurally distinct from S1's saturation DAG (H3 — trees repeat work, no clause reuse).

**Unit-propagation regression (R3, soundness-critical).** A conflict clause is falsified by decisions AND
propagations. Before resolving on a decision variable, propagated literals must be resolved out against
their antecedent clauses. We regress at EVERY level through that node's local propagation trail (in reverse
order); nesting handles ancestor propagations at their own levels. Without this the resolvents retain
propagated variables and the verifier rejects the whole proof.

**Node budget (R2).** Plain DPLL (no clause learning) can blow up; a per-run node budget bounds it.
Budget-exceeded is a distinct outcome from a verify-discard (see :mod:`proofcensus.sample`).
"""
from __future__ import annotations

import numpy as np

from desertmap.instance import CNF
from proofcensus.refutation import Refutation

BUDGET_EXCEEDED = object()   # sentinel returned by sample_s2 when the node budget is hit


class _BudgetExceeded(Exception):
    pass


class _SatEncountered(Exception):
    pass


class _Builder:
    """Accumulates the resolution steps into an append-only bank (originals then derived resolvents)."""

    def __init__(self, cnf: CNF):
        self.orig = [frozenset(c) for c in cnf.clauses]
        self.bank = list(self.orig)
        self.oidx = {c: i for i, c in enumerate(self.orig)}   # duplicate originals collapse to one index
        self.steps: list[tuple] = []

    def resolve(self, i1: int, i2: int, pivot: int):
        r = frozenset(self.bank[i1] | self.bank[i2]) - {pivot, -pivot}
        self.bank.append(r)
        self.steps.append((i1, i2, pivot))
        return r, len(self.bank) - 1


def _propagate(clauses: list[frozenset], assign: dict):
    """Unit-propagate from ``assign`` (mutated in place). Returns (trail, conflict_clause_or_None) where
    trail = [(forced_literal, antecedent_clause), ...] in propagation order."""
    trail = []
    changed = True
    while changed:
        changed = False
        for cl in clauses:
            unassigned = []
            satisfied = False
            for lit in cl:
                v = abs(lit)
                if v in assign:
                    if assign[v] == (lit > 0):
                        satisfied = True
                        break
                else:
                    unassigned.append(lit)
            if satisfied:
                continue
            if not unassigned:
                return trail, cl                          # conflict
            if len(unassigned) == 1:
                lit = unassigned[0]
                assign[abs(lit)] = (lit > 0)
                trail.append((lit, cl))
                changed = True
    return trail, None


def _regress(builder: _Builder, c: frozenset, ci: int, trail: list):
    """Resolve out any locally-propagated literal in ``c`` against its antecedent (reverse trail order)."""
    for (f, ante) in reversed(trail):
        if -f in c:
            c, ci = builder.resolve(ci, builder.oidx[ante], abs(f))
    return c, ci


def _dll(builder: _Builder, clauses: list[frozenset], n: int, assign: dict, rng, budget: list):
    budget[0] -= 1
    if budget[0] < 0:
        raise _BudgetExceeded
    trail, conflict = _propagate(clauses, assign)
    try:
        if conflict is not None:
            return _regress(builder, conflict, builder.oidx[conflict], trail)
        unassigned = [v for v in range(1, n + 1) if v not in assign]
        if not unassigned:
            raise _SatEncountered                          # UNSAT instance ⇒ should not reach a full model
        x = int(rng.choice(unassigned))
        first = bool(rng.integers(0, 2))
        branches = []
        for val in (first, not first):
            assign[x] = val
            cb, cib = _dll(builder, clauses, n, assign, rng, budget)
            del assign[x]
            false_lit = -x if val else x
            if false_lit not in cb:                        # this branch didn't need x ⇒ prune the other
                return _regress(builder, cb, cib, trail)
            branches.append((cb, cib))
        (c0, ci0), (c1, ci1) = branches
        c, ci = builder.resolve(ci0, ci1, x)               # resolve the two branches on the decision var
        return _regress(builder, c, ci, trail)
    finally:
        for (f, _) in trail:
            assign.pop(abs(f), None)


def sample_s2(cnf: CNF, seed: int, node_budget: int = 200_000):
    """Sample one tree-resolution refutation. Returns a :class:`Refutation`, ``None`` (unexpected SAT / no
    empty), or :data:`BUDGET_EXCEEDED` if the node budget is hit."""
    rng = np.random.default_rng(seed)
    builder = _Builder(cnf)
    try:
        c, _ = _dll(builder, builder.orig, cnf.n_vars, {}, rng, [node_budget])
    except _BudgetExceeded:
        return BUDGET_EXCEEDED
    except _SatEncountered:
        return None
    if c:                                                  # root clause must be empty for a refutation
        return None
    return Refutation(cnf.n_vars, tuple(cnf.clauses), tuple(builder.steps))
