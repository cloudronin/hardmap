"""Point-to-set reach instrument (Pebble P2b, prereg_v21) — the redesign after ξ-as-built was DISQUALIFIED.

The parity diagnostic (prereg_v20) proved both of ξ's observables compute a PAIRWISE object: pure ≥3-ary parity
reads ~0 despite maximal propagation. Per Montanari-Semerjian, "reach" is the POINT-TO-SET length — how far a
*partial solution* (a boundary SET, not a single variable) biases a distant target. This instrument measures that.

Operation (harvest once, group many). For a target variable i and radius r:
  * boundary shell B_r = variables at constraint-graph distance >= r from i (unreachable = infinity, included);
  * group the harvested solutions into BUCKETS keyed by their restriction to B_r (each bucket = one boundary
    realization; its population = the surviving solutions);
  * point-to-set signal(r) = bucket-weighted mean TV(conditional dist of x_i, baseline dist of x_i).
One solution harvest per instance serves every radius and every target; bucketing is a dict pass.

reach_score (PINNED, prereg_v21 R-3): the signal at the LARGEST valid radius (far-boundary persistence). Others
(area-under-curve, fitted decay length) are reported as SENSITIVITY ONLY, never substituted after seeing results.

Reuse: bfs_distances, variable_graph, enumerate_solutions, connected_corr (all from reach.py); the samplers;
the exact/sampled provenance + manifest discipline. Net-new is only the boundary-shell bucketing.
"""
import statistics as st

from foundry.reach import bfs_distances, variable_graph, enumerate_solutions, connected_corr, aggregate  # noqa: F401

TARGET_CAP = 8        # R-2: max target variables sampled per instance (cost bound; policy sealed in v21)
POP_CAP = 1000        # R-2: max solutions used for the estimate (subsample if larger); exact iff |sols| <= POP_CAP
MIN_SOLUTIONS = 16    # resolution floor: total solutions per cell (NOT per-bucket — parity's singletons ARE signal)
MIN_BUCKETS = 4       # resolution floor: distinct boundary realizations (the boundary must actually vary)


def boundary_shell(dist: dict, n: int, i: int, r: int):
    """Variables at distance >= r from i (unreachable => infinity, INCLUDED), excluding i. `dist` = bfs from i."""
    return [v for v in range(n) if v != i and (dist.get(v) is None or dist[v] >= r)]


def _dist_of(sols, v, domain):
    m = len(sols)
    return {d: sum(1 for s in sols if s[v] == d) / m for d in domain}


def _tv(p, q):
    return 0.5 * sum(abs(p[d] - q[d]) for d in p)


def pointset_signal(inst, sols, i, r, dist=None):
    """Point-to-set signal at radius r for target i, + bucket-population stats (the pre-fit resolution report)."""
    dom, n = inst.domain, inst.n_vars
    if dist is None:
        dist = bfs_distances(variable_graph(inst), i)
    B = boundary_shell(dist, n, i, r)
    baseline = _dist_of(sols, i, dom)
    buckets = {}
    for s in sols:
        buckets.setdefault(tuple(s[v] for v in B), []).append(s)
    m = len(sols)
    signal = sum((len(b) / m) * _tv(_dist_of(b, i, dom), baseline) for b in buckets.values())
    pops = sorted(len(b) for b in buckets.values())
    return {"signal": round(signal, 4), "n_buckets": len(buckets),
            "min_pop": pops[0], "median_pop": pops[len(pops) // 2]}


def pointset_profile(inst, sols, i):
    """{radius r -> signal(r) + bucket stats} for target i, r = 1 .. (max finite distance + 1). One BFS, reused."""
    dist = bfs_distances(variable_graph(inst), i)
    finite = [d for d in dist.values() if d > 0]
    rmax = (max(finite) if finite else 1) + 1     # +1 so the far/unreachable shell is probed
    return {r: pointset_signal(inst, sols, i, r, dist=dist) for r in range(1, rmax + 1)}


# ── hand-count selftest (B0 gate): sensitivity AND specificity, both hand-computed ───────────────────────────
def selftest_pointset():
    from foundry import ensemble as E
    errs = []

    # (1) SENSITIVITY — 3-var parity x0⊕x1⊕x2=0. Target x2, boundary {x0,x1} (r=1): every realization PINS x2 ->
    #     signal 0.5 (maximal). The identical system reads 0.0 pairwise. This is the instrument's reason to exist.
    R3 = frozenset({(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)})
    par = E.CSPInstance((0, 1), 3, ((R3, (0, 1, 2)),))
    psols = enumerate_solutions(par)
    sig = pointset_signal(par, psols, 2, 1)["signal"]
    if abs(sig - 0.5) > 1e-9:
        errs.append(f"parity point-to-set signal should be 0.5, got {sig}")
    pairwise = max(abs(connected_corr(psols, 2, u, (0, 1))) for u in (0, 1))
    if pairwise > 1e-9:
        errs.append(f"parity PAIRWISE correlation should be ~0, got {pairwise}")

    # (2) SPECIFICITY (R-1) — two DISJOINT 2-SAT constraints on {x0,x1} and {x2,x3}. Target x0; far boundary
    #     {x2,x3} at r=2 is a DIFFERENT component -> conditioning on it cannot move x0 -> signal EXACTLY 0.
    #     (At r=1 the boundary includes x1, which IS linked, so that signal is >0 — checked, to prove r matters.)
    ROR = frozenset({(0, 1), (1, 0), (1, 1)})
    dec = E.CSPInstance((0, 1), 4, ((ROR, (0, 1)), (ROR, (2, 3))))
    dsols = enumerate_solutions(dec)                       # 3 x 3 = 9 solutions
    far = pointset_signal(dec, dsols, 0, 2)["signal"]      # boundary {x2,x3}, disconnected
    if abs(far - 0.0) > 1e-9:
        errs.append(f"disconnected far-boundary signal should be 0.0, got {far}")
    near = pointset_signal(dec, dsols, 0, 1)["signal"]     # boundary includes x1 (linked) -> must be > 0
    if not near > 0.0:
        errs.append(f"near boundary (linked x1) signal should be > 0, got {near}")

    return errs


if __name__ == "__main__":
    e = selftest_pointset()
    print("pointset selftest:", "OK" if not e else "FAIL")
    for x in e:
        print("  ", x)
