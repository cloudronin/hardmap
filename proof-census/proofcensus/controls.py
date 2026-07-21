"""Controls (spec §3.4): planted-core backbone calibration + the S1-vs-S1 glitch noise bound.

- **Planted-core calibration:** on a planted instance the filler is satisfiable on its own, so every
  refutation must engage the core clauses — the backbone metric must therefore identify the planted core at
  ~100% frequency. This is the calibration standard for the backbone metric.
- **Glitch bound:** run the same sampler with two independent seed banks and measure the metric
  disagreement; that bounds sampler noise, the floor an S1-vs-S2 *trend* difference must clear to count as
  terrain (R1).
"""
from __future__ import annotations

from desertmap import instance
from proofcensus import metrics
from proofcensus.refutation import clause_id
from proofcensus.sample import sample_k


def planted_backbone_calibration(n: int = 20, k: int = 5, K: int = 50, sampler: str = "s1",
                                 seed: int = 0, thresh: float = 0.99) -> dict:
    """Sample K refutations of a planted instance and check the planted CORE clauses are backbone (~100%)."""
    cnf, _ = instance.gen_planted(n=n, k=k, seed=seed)
    core_ids = [clause_id(cnf.clauses[i]) for i in range(k + 1)]     # core occupies indices 0..k
    res = sample_k(cnf, sampler, K, seed=seed)
    bb = metrics.backbone(res.refutations)
    core_freqs = {cid: bb.get(cid, 0.0) for cid in core_ids}
    min_core = min(core_freqs.values()) if core_freqs else 0.0
    return {
        "sampler": sampler, "n": n, "k": k, "K_verified": res.n_verified,
        "core_freqs": core_freqs, "min_core_freq": min_core,
        "passes": min_core >= thresh,
    }


def glitch_bound(cnf, sampler: str, K: int, metric_fn, seed_a: int = 1000, seed_b: int = 9000) -> dict:
    """Run ``sampler`` twice with disjoint seed banks; return each metric value and their absolute gap.

    ``metric_fn`` maps a list of refutations → a scalar (e.g. ``lambda r: metrics.median(metrics.lengths(r))``).
    The gap is the S1-vs-S1 noise floor for that metric on this cell.
    """
    a = sample_k(cnf, sampler, K, seed=seed_a)
    b = sample_k(cnf, sampler, K, seed=seed_b)
    va, vb = metric_fn(a.refutations), metric_fn(b.refutations)
    return {"value_a": va, "value_b": vb, "gap": abs(va - vb),
            "n_a": a.n_verified, "n_b": b.n_verified}
