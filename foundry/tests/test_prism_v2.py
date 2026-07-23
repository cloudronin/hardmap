"""Prism v2 (prereg_v33) CI gate — the arity-4 roster: reproduction gate + NPI (pred 1), the parity
known-answer rows (odd-parity-4 purely-affine => unbounded-width/FPT; even-parity-4 affine-but-0/1-valid =>
bounded-width), the affine confound (every unbounded-width param-real class is affine — why the localization
arm was dropped), the tie-corrected Spearman (construct-validity error #2 fix), and the pred-5 anti-canon
sign (Min-Ones non-affine residual Spearman < 0, replicated at arity 4)."""
from itertools import product

import numpy as np
import pytest

from eightfold import structure as S
from foundry import prism


# --- the corrected (tie-averaged) Spearman vs the buggy argsort form (construct-validity error #2) ---
def _avg_rank(a):
    order = sorted(range(len(a)), key=lambda i: a[i])
    r = [0.0] * len(a)
    i = 0
    while i < len(a):
        j = i
        while j + 1 < len(a) and a[order[j + 1]] == a[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2.0
        i = j + 1
    return r


def _spearman_tc(x, y):
    return round(float(np.corrcoef(_avg_rank(list(x)), _avg_rank(list(y)))[0, 1]), 3)


def _spearman_buggy(x, y):
    return round(float(np.corrcoef(np.argsort(np.argsort(x)), np.argsort(np.argsort(y)))[0, 1]), 3)


def _rel(pred, n=4):
    return frozenset(t for t in product((0, 1), repeat=n) if pred(t))


@pytest.fixture(scope="module")
def roster4():
    return prism.build_roster(4)


def test_reproduction_gate_and_npi():
    """Pred 1: the arity-<=3 subset reproduces v1's approx<->param V=0.256; decision has no intermediate value."""
    r3 = prism.build_roster(3)
    rows = []
    for _, _, _, c in r3:
        if c["parameterized"] != "open":
            rows.append((c["approx_maxones"], c["parameterized"]))
            rows.append((c["approx_minones"], c["parameterized"]))
    v = S.cramers_v([a for a, _ in rows], [p for _, p in rows])
    assert abs(v - 0.256) < 0.01
    assert {c["decision"] for _, _, _, c in r3} <= {"P", "NPC"}


def test_parity_known_answers():
    """odd-parity-4 = purely affine => unbounded-width, decision P, param FPT; even-parity-4 = affine but
    0/1-valid => bounded-width (the constant-polymorphism guard — the retraction that kept the predicate)."""
    odd = prism.charges(_rel(lambda t: sum(t) % 2 == 1))
    even = prism.charges(_rel(lambda t: sum(t) % 2 == 0))
    assert odd["flags"]["affine"] and even["flags"]["affine"]
    assert odd["localization"] == "unbounded-width"
    assert odd["decision"] == "P" and odd["parameterized"] == "FPT"
    assert even["localization"] == "bounded-width"          # 0/1-valid constant polymorphism => bounded


def test_spearman_tie_correction():
    """The corrected metric tie-averages ranks (matches scipy); the buggy argsort form does not — and the two
    disagree on tied data, which is why construct-validity error #2 flipped verdicts."""
    x, y = [5, 5, 5, 1], [1, 2, 3, 4]
    assert _spearman_tc(x, y) == -0.775
    assert _spearman_buggy(x, y) != _spearman_tc(x, y)


def test_affine_confound_localization_arm_dropped(roster4):
    """Pred 2: every unbounded-width param-real class is affine — so the bridge nets them all out and the
    localization-absorption arm (dropped from the seal) is untestable on the bridge-completed residual."""
    unb_pr = [c for _, _, _, c in roster4
              if c["localization"] == "unbounded-width" and c["parameterized"] != "open"]
    assert unb_pr, "expected some unbounded-width param-real classes at arity 4"
    assert all(c["flags"]["affine"] for c in unb_pr)


def test_pred5_anti_canon_sign(roster4):
    """Pred 5: the Min-Ones non-affine residual runs anti-canon (tie-corrected Spearman < 0) at arity 4 —
    the replication (attenuated) of v1's -0.564."""
    rank = {v: i for i, v in enumerate(prism.OO.APPROX_ORDER)}
    d = [(rank[c["approx_minones"]], 0 if c["parameterized"] == "FPT" else 1)
         for _, _, _, c in roster4
         if not c["flags"]["affine"] and c["parameterized"] != "open" and c["approx_minones"] not in {"open", "n.a."}]
    assert _spearman_tc([a for a, _ in d], [p for _, p in d]) < 0
