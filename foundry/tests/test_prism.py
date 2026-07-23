"""Prism (prereg_v32) CI gate — the corrected charge oracles, NPI calibration, the v3-reproduction sanity gate,
and the netting selftest (a classical identity nets to 0; the affine=>weakly-separable bridge nets the
counting<->param theorem-identity to 0 while a real Lattice-charge pair survives)."""
from itertools import product

from eightfold import structure as S
from foundry import prism


def _roster():
    return prism.build_roster(3)


def test_prism_charge_selftest():
    assert prism.selftest_prism() == 0


def test_i3_bounded_width_correction():
    """The 0/1-valid trivial-satisfiability guard fires (finer's naive horn|dh|bij would miss it)."""
    R = frozenset({(0, 0, 0), (0, 1, 1), (1, 1, 0)})   # 0-valid, not horn/dual-horn/bijunctive/affine
    f = prism._flags([R])
    assert not (f["horn"] or f["dualhorn"] or f["bijunctive"] or f["affine"])   # naive predicate would say unbounded
    assert prism.bounded_width(f) == "bounded-width"                            # corrected: trivial-sat first


def test_npi_calibration():
    """Prediction 1: decision has no intermediate value (Schaefer dichotomy)."""
    assert {c["decision"] for _, _, _, c in _roster()} <= {"P", "NPC"}


def test_v3_reproduction():
    """The approx<->param headline on the 166 both-real rows reproduces v3's V=0.256 (same roster)."""
    rows = []
    for _, _, _, c in _roster():
        if c["parameterized"] != "open":
            rows.append((c["approx_maxones"], c["parameterized"]))
            rows.append((c["approx_minones"], c["parameterized"]))
    v = S.cramers_v([a for a, _ in rows], [p for _, p in rows])
    assert abs(v - 0.256) < 0.01


def _pooled_v(rows, a_col, b_col, inputs):
    """within-shared-stratum pooled Cramer's V (the netting)."""
    both = [r for r in rows if r[a_col] not in {"open", "n.a."} and r[b_col] not in {"open", "n.a."}]
    shared = sorted(inputs[a_col] & inputs[b_col])
    strata = {}
    for r in both:
        strata.setdefault(tuple(r["flags"][f] for f in shared), []).append(r)
    pooled = 0.0
    for mem in strata.values():
        xs = [m[a_col] for m in mem]; ys = [m[b_col] for m in mem]
        if len(set(xs)) > 1 and len(set(ys)) > 1:
            v = S.cramers_v(xs, ys)
            pooled += (v if v == v else 0.0) * len(mem) / max(1, len(both))
    return pooled


def test_netting_identity_and_bridge():
    rows = [{**c} for _, _, _, c in _roster()]
    net_inputs = {**prism.CHARGE_INPUTS, "parameterized": prism.CHARGE_INPUTS["parameterized"] | {"affine"}}
    # classical identity: decision<->counting nets to 0
    assert _pooled_v(rows, "decision", "counting", prism.CHARGE_INPUTS) < 0.02
    # affine=>WS bridge: counting<->param is a spurious LITERAL survivor that the bridge nets to 0
    lit = _pooled_v(rows, "counting", "parameterized", prism.CHARGE_INPUTS)
    bridge = _pooled_v(rows, "counting", "parameterized", net_inputs)
    assert lit > 0.5 and bridge < 0.02          # 0.736 -> 0.0
    # a real Lattice-charge pair still carries a residual after the bridge (approx_minones<->param)
    assert _pooled_v(rows, "approx_minones", "parameterized", net_inputs) > 0.1
