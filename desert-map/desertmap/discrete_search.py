"""Discrete proof-search baseline (spec §3.5): WalkSAT-style stochastic local search over the SAME proof
object the relaxation optimizes (torch-free).

Purpose (calibration): run a matched-compute discrete search on the planted instances. If discrete search
finds a verifying refutation where gradient descent from random init does not, the E0 barrier is
GD-specific (the shattering signal — keep going). If discrete search ALSO fails, the instances/proof-space
are simply hard at this budget (supports kill 6.1). This does not touch the relaxation and does not consume
operator-redesign budget.

A candidate proof is arrays ``i1[L], i2[L], pivot[L]`` with the causal constraint ``i1[t], i2[t] < m+t``.
Energy rewards reaching a small derived clause via an all-valid prefix; energy 0 ⇔ the proof verifies.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from desertmap import verify
from desertmap.instance import CNF

_W = 10.0  # penalty weight per invalid step in the prefix (an invalid step voids the refutation)


def energy(cnf: CNF, i1, i2, pivot) -> tuple[float, bool]:
    """Return (energy, verifies). Energy = min over steps of ``W·invalid_prefix + derived_clause_size``;
    a fully-valid prefix reaching the empty clause gives energy 0 and verifies=True.
    """
    bank = [frozenset(c) for c in cnf.clauses]
    invalid_prefix = 0
    best = float("inf")
    L = len(i1)
    for t in range(L):
        a, b = bank[i1[t]], bank[i2[t]]
        pv = int(pivot[t])
        valid = verify.step_valid(a, b, pv)
        r = frozenset(a | b) - {pv, -pv}
        bank.append(r)
        if not valid:
            invalid_prefix += 1
        cost = _W * invalid_prefix + len(r)
        if cost < best:
            best = cost
        if valid and invalid_prefix == 0 and len(r) == 0:
            return 0.0, True
    return best, False


@dataclass
class SearchResult:
    success: list      # per-restart bool
    success_rate: float
    iters_to_solve: list   # per successful restart
    total_moves: int


def _rand_proof(cnf: CNF, L: int, rng) -> tuple:
    m = cnf.n_clauses
    i1 = np.array([rng.integers(0, m + t) for t in range(L)])
    i2 = np.array([rng.integers(0, m + t) for t in range(L)])
    pivot = rng.integers(1, cnf.n_vars + 1, size=L)
    return i1, i2, pivot


def walksat_proof_search(cnf: CNF, L: int, restarts: int, iters: int, *,
                         noise: float = 0.3, n_candidates: int = 8, seed: int = 0) -> SearchResult:
    """WalkSAT-style search: each iteration reassigns one component of one step — with prob ``noise`` a
    random move, else the best of ``n_candidates`` random reassignments (greedy). ``restarts`` independent
    runs of ``iters`` moves each (matched compute ≈ restarts×iters objective evals)."""
    rng = np.random.default_rng(seed)
    m = cnf.n_clauses
    success, iters_to_solve, total_moves = [], [], 0

    for _ in range(restarts):
        i1, i2, pivot = _rand_proof(cnf, L, rng)
        e, ok = energy(cnf, i1, i2, pivot)
        solved_at = None
        for it in range(iters):
            total_moves += 1
            if ok:
                solved_at = it
                break
            t = int(rng.integers(0, L))
            comp = int(rng.integers(0, 3))   # 0=i1, 1=i2, 2=pivot

            def apply(val):
                a1, a2, ap = i1.copy(), i2.copy(), pivot.copy()
                if comp == 0:
                    a1[t] = val
                elif comp == 1:
                    a2[t] = val
                else:
                    ap[t] = val
                return a1, a2, ap

            hi = (m + t) if comp < 2 else cnf.n_vars
            lo = 0 if comp < 2 else 1
            if rng.random() < noise:
                cand = [int(rng.integers(lo, hi + (0 if comp < 2 else 1)))]
            else:
                cand = [int(rng.integers(lo, hi + (0 if comp < 2 else 1))) for _ in range(n_candidates)]
            best_val, best_e, best_state, best_ok = None, float("inf"), None, False
            for v in cand:
                a1, a2, ap = apply(v)
                ee, o = energy(cnf, a1, a2, ap)
                if ee < best_e:
                    best_val, best_e, best_state, best_ok = v, ee, (a1, a2, ap), o
            # accept if it improves or ties (WalkSAT accepts sideways/noise moves)
            if best_e <= e or rng.random() < noise:
                i1, i2, pivot = best_state
                e, ok = best_e, best_ok
        success.append(bool(ok or solved_at is not None))
        if success[-1]:
            iters_to_solve.append(solved_at if solved_at is not None else iters)

    return SearchResult(success=success, success_rate=sum(success) / len(success),
                        iters_to_solve=iters_to_solve, total_moves=total_moves)


def constructive_search(cnf: CNF, restarts: int, budget: int, *,
                        noise: float = 0.2, seed: int = 0) -> SearchResult:
    """Constructive greedy resolution search (instance-hardness probe — does NOT use the fixed-per-step
    selection parameterization that the relaxation and walksat_proof_search share).

    Grow a clause bank by repeatedly resolving a compatible pair, greedily preferring the smallest *new*
    resolvent (with ``noise`` random picks), up to ``budget`` resolutions. Success = the empty clause is
    derived. If this finds refutations easily where GD / array-WalkSAT do not, the barrier is specific to
    the fixed-selection *parameterization*, not the instance.
    """
    rng = np.random.default_rng(seed)
    success, iters_to_solve, total = [], [], 0

    for _ in range(restarts):
        bank = [frozenset(c) for c in cnf.clauses]
        seen = set(bank)
        solved_at = None
        for step in range(budget):
            total += 1
            # collect candidate resolvent moves (sample pairs to bound cost)
            n = len(bank)
            idx = rng.permutation(n)
            best = None  # (size, i, j, pivot, resolvent)
            tried = 0
            for a in range(n):
                i = int(idx[a])
                for j in range(n):
                    if i == j:
                        continue
                    A, B = bank[i], bank[j]
                    shared = [abs(l) for l in A if -l in B]
                    for pv in shared:
                        r = frozenset(A | B) - {pv, -pv}
                        if r in seen:
                            continue
                        tried += 1
                        cand = (len(r), i, j, pv, r)
                        if best is None or cand[0] < best[0]:
                            best = cand
                        if len(r) == 0:
                            best = cand
                            break
                    if best is not None and best[0] == 0:
                        break
                    if tried >= 200:
                        break
                if best is not None and best[0] == 0:
                    break
            if best is None:
                break
            # noise: sometimes take a random valid resolvent instead of the greedy-smallest
            if rng.random() < noise and tried > 0:
                i = int(rng.integers(0, n)); j = int(rng.integers(0, n))
                if i != j:
                    shared = [abs(l) for l in bank[i] if -l in bank[j]]
                    if shared:
                        pv = int(rng.choice(shared))
                        r = frozenset(bank[i] | bank[j]) - {pv, -pv}
                        if r not in seen:
                            best = (len(r), i, j, pv, r)
            _, i, j, pv, r = best
            bank.append(r); seen.add(r)
            if len(r) == 0:
                solved_at = step
                break
        success.append(solved_at is not None)
        if solved_at is not None:
            iters_to_solve.append(solved_at)

    return SearchResult(success=success, success_rate=sum(success) / len(success),
                        iters_to_solve=iters_to_solve, total_moves=total)
