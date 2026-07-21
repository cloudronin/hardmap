"""Population statistics on verifier-passing refutations (spec §3.3).

Every function takes a list of :class:`~proofcensus.refutation.Refutation` (assumed already verifier-gated,
AGENTS.md invariant 1). Overlap uses canonical clause-id sets (I3). All per-sampler; cross-sampler
comparison is judged on TRENDS across the α sweep, never levels (R1) — see `sampler_agreement_trend`.
"""
from __future__ import annotations

import itertools
from collections import Counter

from proofcensus.refutation import Refutation, jaccard


def lengths(refs: list[Refutation]) -> list[int]:
    """Proof lengths (number of resolution steps) — the length distribution for a cell."""
    return [r.length for r in refs]


def backbone(refs: list[Refutation]) -> dict[tuple, float]:
    """Per clause-id, the fraction of the ``refs`` whose proof contains it (∈ (0,1]). The 'backbone' is the
    set of clause-ids near frequency 1 (mandatory proof content)."""
    if not refs:
        return {}
    k = len(refs)
    cnt: Counter = Counter()
    for r in refs:
        for cid in r.clause_ids():
            cnt[cid] += 1
    return {cid: c / k for cid, c in cnt.items()}


def backbone_size(refs: list[Refutation], thresh: float = 0.95) -> int:
    """Number of clause-ids appearing in ≥ ``thresh`` fraction of proofs (backbone strength proxy)."""
    return sum(1 for f in backbone(refs).values() if f >= thresh)


def overlap_qs(refs: list[Refutation]) -> list[float]:
    """All pairwise spin-overlaps q = 2·Jaccard(clause_ids) − 1 over the K(K−1)/2 proof pairs (P(q) sample)."""
    ids = [r.clause_ids() for r in refs]
    return [2.0 * jaccard(a, b) - 1.0 for a, b in itertools.combinations(ids, 2)]


def pairwise_jaccards(refs: list[Refutation]) -> list[float]:
    ids = [r.clause_ids() for r in refs]
    return [jaccard(a, b) for a, b in itertools.combinations(ids, 2)]


def median(xs: list[float]) -> float | None:
    return sorted(xs)[len(xs) // 2] if xs else None


def province_separation(refs_a: list[Refutation], refs_b: list[Refutation]) -> dict:
    """Exploratory (R1): how far apart two samplers' provinces sit — mean INTER-sampler overlap vs the mean
    INTRA-sampler overlaps. A large intra-vs-inter gap is a *finding* (the samplers occupy different regions
    of one refutation set), never an artifact.
    """
    ids_a = [r.clause_ids() for r in refs_a]
    ids_b = [r.clause_ids() for r in refs_b]

    def mean(xs):
        return sum(xs) / len(xs) if xs else float("nan")

    intra_a = mean([jaccard(x, y) for x, y in itertools.combinations(ids_a, 2)])
    intra_b = mean([jaccard(x, y) for x, y in itertools.combinations(ids_b, 2)])
    inter = mean([jaccard(x, y) for x in ids_a for y in ids_b])
    return {"intra_a": intra_a, "intra_b": intra_b, "inter": inter,
            "separation": (intra_a + intra_b) / 2 - inter}


def _trend_sign(alphas: list[float], values: list[float]) -> int:
    """Sign of the trend toward threshold: +1 = metric LARGER at the hard (low-α) end, −1 = smaller, 0 flat.
    Orders α ascending (hard/threshold end first) and takes hard-end minus easy-end (robust for a 5-point
    sweep)."""
    order = sorted(range(len(alphas)), key=lambda i: alphas[i])   # α ascending = hardest (toward threshold) first
    v = [values[i] for i in order]
    d = v[0] - v[-1]                                               # hard-end (toward threshold) minus easy-end
    eps = 1e-9
    return 1 if d > eps else (-1 if d < -eps else 0)


def sampler_agreement_trend(alphas: list[float], series_a: list[float], series_b: list[float]) -> dict:
    """H3 replication is on TRENDS, not levels (R1): do both samplers' α-series move the same direction
    toward threshold? Returns each trend sign and whether they agree."""
    sa, sb = _trend_sign(alphas, series_a), _trend_sign(alphas, series_b)
    return {"trend_a": sa, "trend_b": sb, "agree": sa == sb and sa != 0}
