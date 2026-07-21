"""Population metrics on toy/real proof sets: length, backbone, overlap P(q), province separation (R1)."""
from __future__ import annotations

from desertmap import fixtures
from proofcensus import metrics
from proofcensus.sample import sample_k


def _refs(sampler, K=8):
    cnf = fixtures.gen_unsat_3sat(20, 4.5, fixtures._cell_seed(20, 4.5, 0))
    return sample_k(cnf, sampler, K, seed=0).refutations


def test_lengths_and_backbone():
    refs = _refs("s1")
    lens = metrics.lengths(refs)
    assert len(lens) == len(refs) and all(isinstance(x, int) for x in lens)
    bb = metrics.backbone(refs)
    assert all(0.0 < f <= 1.0 for f in bb.values())
    assert () in bb and bb[()] == 1.0                 # empty clause is in every proof


def test_overlap_qs_in_range():
    refs = _refs("s1")
    qs = metrics.overlap_qs(refs)
    assert len(qs) == len(refs) * (len(refs) - 1) // 2
    assert all(-1.0 <= q <= 1.0 for q in qs)


def test_province_separation_keys_and_sign():
    a, b = _refs("s1"), _refs("s2")
    ps = metrics.province_separation(a, b)
    assert set(ps) == {"intra_a", "intra_b", "inter", "separation"}
    assert -1.0 <= ps["inter"] <= 1.0


def test_trend_agreement_helper():
    alphas = [4.5, 5.0, 6.0, 8.0, 10.0]
    inc_toward_threshold = [10, 8, 6, 4, 2]           # larger at hard (low-α) end
    dec = [2, 4, 6, 8, 10]
    assert metrics.sampler_agreement_trend(alphas, inc_toward_threshold, inc_toward_threshold)["agree"]
    assert not metrics.sampler_agreement_trend(alphas, inc_toward_threshold, dec)["agree"]
