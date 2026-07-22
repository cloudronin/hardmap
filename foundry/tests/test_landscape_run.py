"""Sprint 4.2 landscape run — the SCORING RULES (not the live verdict) + the permutation hand-count selftest.

The verdicts H_I6a/H_I6b come from the live confirmation run; here we lock the harness: the permutation p on a
hand-countable 2x2 reproduces 2/20, and the score functions classify controlled synthetic inputs correctly.
"""
from foundry import landscape_run as LR


def _measured(rows):
    """rows: list of (fid, localization, poly_arm, score_0.7, score_0.9) -> a measured-dict fixture."""
    out = {}
    for fid, loc, arm, s7, s9 in rows:
        out[fid] = {"localization": loc, "poly_arm": arm, "alpha_struct": 1.0,
                    "densities": {"0.7": 0.7, "0.9": 0.9},
                    "readings": {"0.7": {"alpha": 0.7, "score": s7, "concord": 0.01, "per_sampler": {}},
                                 "0.9": {"alpha": 0.9, "score": s9, "concord": 0.01, "per_sampler": {}}}}
    return out


def test_perm_harness_reproduces_hand_count():
    assert LR.selftest_perm(n_perm=20000) == 0


def test_h_i6b_confirms_ordered_and_rejects_disordered():
    # predicted order semilattice<majority<order_median<=affine, stable at both densities -> CONFIRMED + split
    ordered = _measured([
        ("horn", "bounded", "semilattice", 0.82, 0.83), ("dhorn", "bounded", "semilattice", 0.83, 0.84),
        ("2sat", "bounded", "majority", 0.88, 0.89), ("bij", "bounded", "majority", 0.89, 0.90),
        ("order", "bounded", "order_median", 0.93, 0.93), ("median", "bounded", "order_median", 0.92, 0.93),
        ("xor", "unbounded", "affine", 0.98, 0.99), ("lineq", "unbounded", "affine", 0.99, 0.98)])
    b = LR.score_h_i6b(ordered)
    assert b["verdict"] == "CONFIRMED" and b["stable_across_densities"] and b["anomaly_bounded_width_splits"]
    # scramble the order (semilattice most rugged) -> NOT_CONFIRMED
    dis = _measured([
        ("horn", "bounded", "semilattice", 0.98, 0.99), ("2sat", "bounded", "majority", 0.88, 0.89),
        ("order", "bounded", "order_median", 0.82, 0.83), ("xor", "unbounded", "affine", 0.90, 0.90)])
    assert LR.score_h_i6b(dis)["verdict"] == "NOT_CONFIRMED"


def test_h_i6a_computes_direction_and_floor():
    # 5 affine rugged + 9 bounded mixed: direction affine-bounded > 0, n=14 (floor met), a verdict is produced
    rows = [(f"aff{i}", "unbounded", "affine", 0.97, 0.98) for i in range(5)] + \
           [(f"hb{i}", "bounded", "semilattice", 0.82, 0.83) for i in range(4)] + \
           [(f"mb{i}", "bounded", "majority", 0.89, 0.90) for i in range(3)] + \
           [(f"ob{i}", "bounded", "order_median", 0.93, 0.93) for i in range(2)]
    a = LR.score_h_i6a(_measured(rows), density="0.9")
    assert a["n_concordant"] == 14 and a["direction_affine_minus_bounded"] > 0
    assert a["verdict"] in ("SUPPORTED", "NOT_SUPPORTED")

    # too few concordant rows -> INSUFFICIENT_RESOLUTION (floor is >= 12)
    few = _measured([(f"x{i}", "unbounded", "affine", 0.9, 0.9) for i in range(4)] +
                    [(f"y{i}", "bounded", "semilattice", 0.8, 0.8) for i in range(4)])
    assert LR.score_h_i6a(few, density="0.9")["verdict"] == "INSUFFICIENT_RESOLUTION"
