"""Parallel sampling driver — process-level parallelism over independent samples (the S1 speedup).

Samples are embarrassingly parallel: each ``(instance, seed)`` runs independently. This spreads them across
CPU cores while preserving the exact three-way accounting of :mod:`proofcensus.sample`. Determinism is
per-seed (each attempt uses a fixed seed), so results are reproducible regardless of worker scheduling.
"""
from __future__ import annotations

import os
from concurrent.futures import ProcessPoolExecutor

from desertmap.instance import CNF
from proofcensus.refutation import Refutation
from proofcensus.sample import SampleResult
from proofcensus.sampler_s1 import sample_s1
from proofcensus.sampler_s2 import BUDGET_EXCEEDED, sample_s2


def _sample_one(args):
    """Worker: run one sample and return a picklable outcome ('ok'|'budget'|'discard', steps_or_None)."""
    sampler, clauses, n_vars, seed, s1_budget, node_budget = args
    cnf = CNF(n_vars, clauses)
    if sampler == "s1":
        r = sample_s1(cnf, seed=seed, budget=s1_budget)
    else:
        r = sample_s2(cnf, seed=seed, node_budget=node_budget)
    if r is BUDGET_EXCEEDED or r is None:
        return ("budget", None)
    if r.verify():                                      # gate in-worker; only verified proofs leave
        return ("ok", r.steps)
    return ("discard", None)


def sample_k_parallel(cnf: CNF, sampler: str, K: int, *, seed: int = 0, s1_budget: int = 4000,
                      node_budget: int = 200_000, n_workers: int | None = None,
                      max_attempts: int | None = None) -> SampleResult:
    """Collect ``K`` verified refutations of ``cnf`` under ``sampler`` across ``n_workers`` processes.

    Over-submits batches of seeds and drains results until ``K`` verified are gathered. Accounting matches
    :func:`proofcensus.sample.sample_k` (verified / verify-discard / budget-exceeded).
    """
    n_workers = n_workers or max(1, (os.cpu_count() or 2) - 1)
    cap = max_attempts if max_attempts is not None else (5 * K + 20)
    res = SampleResult(sampler=sampler)
    s = seed
    with ProcessPoolExecutor(max_workers=n_workers) as ex:
        while res.n_verified < K and res.n_attempts < cap:
            need = K - res.n_verified
            # Submit ~need tasks (discard/budget rates are typically ~0, so one wave usually suffices);
            # the while-loop tops up if any attempt fails to yield a verified proof.
            batch = min(cap - res.n_attempts, max(need, n_workers))
            args = [(sampler, cnf.clauses, cnf.n_vars, s + i, s1_budget, node_budget) for i in range(batch)]
            s += batch
            for tag, steps in ex.map(_sample_one, args, chunksize=1):
                res.n_attempts += 1
                if tag == "ok":
                    res.refutations.append(Refutation(cnf.n_vars, cnf.clauses, steps))
                    res.n_verified += 1
                elif tag == "budget":
                    res.n_budget_exceeded += 1
                else:
                    res.n_verify_discard += 1
                if res.n_verified >= K:
                    break
    return res
