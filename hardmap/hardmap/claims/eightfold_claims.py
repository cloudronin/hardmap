"""Adapters for the eightfold claims: gradient V, Crucible verdicts, Factors k*.

Fast tier recomputes from the frozen atlas via the real crucible/factors helpers
(seeded, deterministic) except Factors k*, whose held-out estimator takes ~45s, so
its fast tier reads the committed factors_v1.json and ``--full`` recomputes it.
"""
from __future__ import annotations

import functools
import json
from pathlib import Path

import eightfold
from eightfold import crucible, factors
from eightfold.atlas import load_atlas


def _results_dir() -> Path:
    return Path(eightfold.__file__).resolve().parent / "results" / "atlas"


@functools.lru_cache(maxsize=1)
def _crucible() -> dict:
    """Run the full Crucible battery once on the frozen atlas (cached per process)."""
    entries = load_atlas()
    return {
        "s1": crucible.s1_null_model(entries),
        "s2": crucible.s2_dedup(entries),
        "s3": crucible.s3_significance(entries),
        "s5": crucible.s5_adversarial_roster(entries),
    }


def gradient_v() -> dict:
    """canon.gradient.v -- recompute the hardness-gradient Cramér's V from the atlas."""
    c = _crucible()
    return {
        "full_v": c["s2"]["gradient_full_v"],
        "dedup_v": c["s2"]["gradient_dedup_v"],
        "perm_p": c["s3"]["gradient_perm_p"],
    }


def crucible_verdicts() -> dict:
    """canon.crucible.verdicts -- recompute the S1/S2/S3/S5 verdicts (S4 deferred)."""
    c = _crucible()
    return {
        "S1": c["s1"]["verdict"],
        "S2": c["s2"]["verdict"],
        "S3": c["s3"]["verdict"],
        "S5": c["s5"]["verdict"],
    }


def factors_kstar_fast() -> dict:
    """factors.kstar (fast) -- read the committed held-out-estimator result."""
    d = json.loads((_results_dir() / "factors_v1.json").read_text(encoding="utf-8"))
    return {"k_star": d["k_star"]["k_hat_1se"]}


def factors_kstar_full() -> dict:
    """factors.kstar (full) -- recompute the LCM 1-SE estimator from the atlas (~45s)."""
    fv = factors.factors_verdict(load_atlas())
    return {"k_star": fv["k_star"]["k_hat_1se"]}
