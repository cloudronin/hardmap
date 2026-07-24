"""H4 check 1 -- statistic-implementation audit.

Each helper that computes a published number is checked against an INDEPENDENT
reference (a hand-computed toy, or scipy) rather than its own output. This is the
defect-#5 audit method generalized: a construct-validity net under the numbers.
"""
import importlib.util
import math
from pathlib import Path

import pytest
from scipy.stats import spearmanr

from eightfold.structure import cramers_v


# ---- Cramér's V (bias-corrected) vs a fully hand-computed toy ---------------------------------------
def test_cramers_v_matches_hand_computed_toy():
    # 2x2 contingency [[8,2],[3,7]], n=20. By hand:
    #   chi2 (no correction) = 5.0505 -> phi2 = 0.252525
    #   phi2corr = 0.252525 - (1*1)/19 = 0.199894 ; denom = (2 - 1/19) - 1 = 0.947368
    #   V = sqrt(0.199894 / 0.947368) = 0.45934
    labels_a = ["a0"] * 10 + ["a1"] * 10
    labels_b = (["b0"] * 8 + ["b1"] * 2) + (["b0"] * 3 + ["b1"] * 7)
    v = cramers_v(labels_a, labels_b)
    assert math.isclose(v, 0.45934, abs_tol=1e-4), v


# ---- Tie-corrected Spearman vs scipy; the buggy sealed form must diverge ----------------------------
def _dev_prism_v2():
    dev = Path(__import__("foundry").__file__).resolve().parent.parent / "dev" / "prism_v2_matrix.py"
    if not dev.exists():
        pytest.skip("foundry/dev not present (non-source install)")
    spec = importlib.util.spec_from_file_location("prism_v2_matrix_audit", dev)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_corrected_spearman_matches_scipy_and_buggy_diverges():
    mod = _dev_prism_v2()
    # Heavily tied x with no monotone signal: proper tie handling gives 0; the argsort(argsort())
    # form invents order within tie-blocks and manufactures a large positive correlation.
    x = [1, 1, 1, 2, 2, 2]
    y = [1, 2, 3, 1, 2, 3]
    ref = round(float(spearmanr(x, y).correlation), 3)
    corrected = mod._spearman(x, y)
    buggy = mod._spearman_legacy(x, y)
    assert math.isclose(corrected, ref, abs_tol=1e-3), (corrected, ref)   # corrected == reference (0.0)
    assert abs(buggy - ref) > 0.1, (buggy, ref)                            # buggy fabricates ~0.71


def test_corrected_spearman_matches_scipy_on_signal_with_ties():
    mod = _dev_prism_v2()
    x = [1, 2, 3, 4, 4, 5, 6, 6]
    y = [1, 1, 2, 3, 4, 5, 5, 6]
    ref = round(float(spearmanr(x, y).correlation), 3)
    assert math.isclose(mod._spearman(x, y), ref, abs_tol=1e-3), (mod._spearman(x, y), ref)
