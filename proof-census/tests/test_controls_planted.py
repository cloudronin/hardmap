"""Planted-core backbone calibration (spec §3.4): the backbone metric must identify the planted core ~100%."""
from __future__ import annotations

import pytest

from proofcensus.controls import planted_backbone_calibration


@pytest.mark.parametrize("sampler", ["s1", "s2"])
def test_planted_core_is_backbone(sampler):
    cal = planted_backbone_calibration(n=20, k=5, K=20, sampler=sampler)
    assert cal["K_verified"] == 20
    # Filler is satisfiable on its own ⇒ every refutation engages the core ⇒ core clauses at frequency 1.0.
    assert cal["passes"], f"planted core not backbone: min_core_freq={cal['min_core_freq']}"
    assert cal["min_core_freq"] == 1.0
