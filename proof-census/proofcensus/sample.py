"""K-sampling driver with verifier gating + three-way accounting (spec §3.1, R2).

Runs a sampler with varying seeds until ``K`` verifier-passing refutations are collected, tracking three
disjoint outcomes per attempt: **verified**, **verify-discard** (a proof was built but failed the M1
verifier), and **budget-exceeded** (S1 resolution budget or S2 node budget hit — no proof this attempt).
"""
from __future__ import annotations

from dataclasses import dataclass, field

from desertmap.instance import CNF
from proofcensus.refutation import Refutation
from proofcensus.sampler_s1 import sample_s1
from proofcensus.sampler_s2 import BUDGET_EXCEEDED, sample_s2


@dataclass
class SampleResult:
    sampler: str
    refutations: list = field(default_factory=list)
    n_verified: int = 0
    n_verify_discard: int = 0
    n_budget_exceeded: int = 0
    n_attempts: int = 0

    @property
    def verify_discard_rate(self) -> float:
        return self.n_verify_discard / self.n_attempts if self.n_attempts else 0.0

    @property
    def budget_rate(self) -> float:
        return self.n_budget_exceeded / self.n_attempts if self.n_attempts else 0.0


def _run(sampler: str, cnf: CNF, seed: int, s1_budget: int, node_budget: int):
    if sampler == "s1":
        return sample_s1(cnf, seed=seed, budget=s1_budget)
    if sampler == "s2":
        return sample_s2(cnf, seed=seed, node_budget=node_budget)
    raise ValueError(f"unknown sampler {sampler!r} (expected 's1' or 's2')")


def sample_k(cnf: CNF, sampler: str, K: int, *, seed: int = 0, s1_budget: int = 4000,
             node_budget: int = 200_000, max_attempts: int | None = None) -> SampleResult:
    """Collect ``K`` verified refutations of ``cnf`` under ``sampler`` ('s1'|'s2'). Seeds advance per
    attempt for diversity. ``max_attempts`` caps the loop (default ``5K+20``)."""
    res = SampleResult(sampler=sampler)
    cap = max_attempts if max_attempts is not None else (5 * K + 20)
    s = seed
    while res.n_verified < K and res.n_attempts < cap:
        res.n_attempts += 1
        r = _run(sampler, cnf, s, s1_budget, node_budget)
        s += 1
        if r is BUDGET_EXCEEDED or r is None:      # no proof this attempt (compute limit / saturation miss)
            res.n_budget_exceeded += 1
            continue
        if isinstance(r, Refutation) and r.verify():
            res.refutations.append(r)
            res.n_verified += 1
        else:                                       # built something that failed the verifier — must not enter stats
            res.n_verify_discard += 1
    return res
