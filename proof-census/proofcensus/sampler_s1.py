"""S1 — randomized constructive-saturation sampler (DAG-like refutations).

Grows a clause bank by resolving compatible pairs, greedily preferring the smallest *new* resolvent (the
directedness that closes in few steps) with randomized pair order, random tie-breaking, and ``noise`` random
picks — so independent seeds reach different refutations (H1). Records provenance for every derived row, then
back-traces the empty clause to extract the used sub-DAG as a :class:`~proofcensus.refutation.Refutation`.
This is the constructive prover that scored 100% in Desert Map's calibration, instrumented to emit the proof.

Per-call cost is dominated by the number of resolutions to close (kept small by the smallest-resolvent
preference). Sweep-scale throughput comes from process parallelism over independent samples
(:mod:`proofcensus.sweep`) — NOT from de-directing this loop (sampled/undirected variants explore far more
before closing and are slower).
"""
from __future__ import annotations

import numpy as np

from desertmap.instance import CNF
from proofcensus.refutation import Refutation


def sample_s1(cnf: CNF, seed: int, budget: int = 4000, noise: float = 0.3,
              cand_cap: int = 400) -> Refutation | None:
    """Sample one refutation of ``cnf`` (or ``None`` if the empty clause isn't derived within ``budget``).

    ``noise`` controls diversity: with probability ``noise`` a random valid resolvent is taken instead of a
    smallest one (ties broken at random regardless). ``cand_cap`` bounds candidate gathering per step.
    """
    rng = np.random.default_rng(seed)
    bank: list[frozenset] = [frozenset(c) for c in cnf.clauses]
    m = len(bank)
    seen = set(bank)
    prov: dict[int, tuple] = {}
    empty_idx: int | None = None

    for _ in range(budget):
        n = len(bank)
        cands: list[tuple] = []                       # (size, i, j, pivot, resolvent)
        found_empty = False
        for ai in rng.permutation(n):
            i = int(ai)
            A = bank[i]
            for j in range(n):
                if i == j:
                    continue
                B = bank[j]
                for pv in (abs(l) for l in A if -l in B):
                    r = frozenset(A | B) - {pv, -pv}
                    if r in seen:
                        continue
                    cands.append((len(r), i, j, pv, r))
                    if not r:
                        found_empty = True
                        break
                if found_empty:
                    break
            if found_empty or len(cands) >= cand_cap:
                break
        if not cands:
            break                                     # saturated without empty (guard; unexpected for unsat)

        empties = [c for c in cands if c[0] == 0]
        if empties:
            choice = empties[0]
        elif rng.random() < noise:
            choice = cands[int(rng.integers(0, len(cands)))]
        else:
            msz = min(c[0] for c in cands)
            smalls = [c for c in cands if c[0] == msz]
            choice = smalls[int(rng.integers(0, len(smalls)))]

        _, i, j, pv, r = choice
        bank.append(r)
        seen.add(r)
        prov[len(bank) - 1] = (i, j, pv)
        if not r:
            empty_idx = len(bank) - 1
            break

    if empty_idx is None:
        return None

    # Back-trace the used sub-DAG from the empty clause; derived indices are causal (parents < child).
    used: set[int] = set()
    stack = [empty_idx]
    while stack:
        idx = stack.pop()
        if idx < m or idx in used:
            continue
        used.add(idx)
        pi, pj, _ = prov[idx]
        stack.extend((pi, pj))

    order = sorted(used)                              # ascending == topological order
    newidx = {o: o for o in range(m)}
    for pos, d in enumerate(order):
        newidx[d] = m + pos
    steps = tuple((newidx[prov[d][0]], newidx[prov[d][1]], prov[d][2]) for d in order)
    return Refutation(cnf.n_vars, tuple(cnf.clauses), steps)
