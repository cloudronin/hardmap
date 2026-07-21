"""Calibration harness (spec §3.5 discrete baselines) — the tool that produced the refined kill verdict.

Locks: (1) the energy oracle agrees with the verifier; (2) constructive (order-free) search recovers a
planted refutation; (3) array-WalkSAT on the fixed-selection parameterization does NOT easily recover it
(the parameterization pathology — see docs/findings/NEGATIVE-RESULT.md). Torch-free."""
from __future__ import annotations

import numpy as np

from desertmap import instance
from desertmap.discrete_search import constructive_search, energy, walksat_proof_search


def test_energy_agrees_with_verifier_on_planted():
    cnf, proof = instance.gen_planted(n=20, k=5, seed=0)
    L = 12
    i1 = [s[0] for s in proof] + [0] * (L - len(proof))
    i2 = [s[1] for s in proof] + [1] * (L - len(proof))
    pv = [s[2] for s in proof] + [1] * (L - len(proof))
    e, ok = energy(cnf, np.array(i1), np.array(i2), np.array(pv))
    assert ok is True and e == 0.0


def test_constructive_search_recovers_planted():
    for n in (20, 40):
        cnf, _ = instance.gen_planted(n=n, k=5, seed=0)
        r = constructive_search(cnf, restarts=8, budget=60, seed=1)
        assert r.success_rate == 1.0, f"constructive search should refute the planted n={n} instance"


def test_walksat_fixed_selection_does_not_recover_at_modest_budget():
    """The fixed-selection parameterization is search-hostile (the negative result). A modest-budget
    array-WalkSAT run does not recover the planted proof — documenting, not gating."""
    cnf, _ = instance.gen_planted(n=20, k=5, seed=0)
    r = walksat_proof_search(cnf, L=12, restarts=8, iters=400, seed=1)
    assert r.success_rate == 0.0
