"""The reach instrument ξ (Sprint 6 "Pebble", P2). How far does information about a partial solution propagate
through a problem's constraint structure? Binned by constraint-graph distance d, fit the decay, report the reach.

TWO PRE-REGISTERED OBSERVABLES (prereg_v17; the three-pole calibration selects, against ground truth, which one
recovers the sealed ordering short<2-SAT<affine, then it is FIXED before any unknown reading):
  * "forcing" — condition one variable v=value, resample, TV-shift of each other variable's ONE-variable marginal,
    binned by d(v,u). FORCING reach: how far a pinned value FORCES others. Blind to balanced ≥3-ary parity
    (conditioning leaves marginals at 1/2), by construction.
  * "corr" — base-ensemble two-point CONNECTED correlation between a source variable and each other, binned by
    d(src,u). CORRELATION reach: the cavity-method correlation length the substrate hypothesis names. Blind to pure
    ≥3-ary parity too (3-XOR has zero pairwise correlation) — so the affine pole is 2-affine (equality/inequality),
    which carries full pairwise correlation.

Reuse: structural.variable_graph (the SAME variable-adjacency graph ξ's BFS walks), solscape samplers,
relfeatures.fit_r2. R-2 typing/bias (shared-scope adjacency compresses distances as arity grows) is P3's diagnostic.
"""
import math
from dataclasses import replace
from itertools import product

import numpy as np

from foundry import ensemble as E
from foundry import relfeatures as RF
from foundry import solscape as S
from foundry.structural import variable_graph

MIN_SOLS_SAMPLED = 8


def bfs_distances(adj: dict, src: int) -> dict:
    """Shortest-path distance from src over the variable-adjacency graph. Unreachable vars are ABSENT from the map."""
    dist = {src: 0}
    frontier, d = [src], 0
    while frontier:
        d += 1
        nxt = []
        for u in frontier:
            for w in adj[u]:
                if w not in dist:
                    dist[w] = d
                    nxt.append(w)
        frontier = nxt
    return dist


def condition(inst, v, value):
    """Pin v=value by appending a unit point-constraint (honored by every sampler; a 1-tuple relation is affine)."""
    return replace(inst, constraints=inst.constraints + ((frozenset({(value,)}), (v,)),))


def var_marginals(sols, domain, n):
    m = len(sols)
    return [{d: sum(1 for s in sols if s[v] == d) / m for d in domain} for v in range(n)]


def tv(p, q):
    return 0.5 * sum(abs(p[d] - q[d]) for d in p)


def connected_corr(sols, v, u, domain):
    """|P(x_v=x_u) − Σ_d P(x_v=d)P(x_u=d)| — the connected two-point correlation; 0 iff v,u independent."""
    m = len(sols)
    joint = sum(1 for s in sols if s[v] == s[u]) / m
    pv = {d: sum(1 for s in sols if s[v] == d) / m for d in domain}
    pu = {d: sum(1 for s in sols if s[u] == d) / m for d in domain}
    return abs(joint - sum(pv[d] * pu[d] for d in domain))


def _solutions(inst, sampler, seed, K):
    if sampler == "exact":
        return [a for a in product(inst.domain, repeat=inst.n_vars) if inst.satisfies(a)]
    return S.SAMPLERS[sampler](inst, seed, K=K)


def _enough(sols, sampler):
    return sols is not None and len(sols) >= (1 if sampler == "exact" else MIN_SOLS_SAMPLED)


def forcing_profile(inst, drop_v, value, sampler="dpll", seed=0, K=80):
    """{distance -> [marginal-TV shift]} under conditioning drop_v=value. Unreachable vars under key None."""
    base = _solutions(inst, sampler, seed, K)
    if not _enough(base, sampler):
        return None
    cond = _solutions(condition(inst, drop_v, value), sampler, seed, K)
    if not _enough(cond, sampler):
        return None
    dom, n = inst.domain, inst.n_vars
    mb, mc = var_marginals(base, dom, n), var_marginals(cond, dom, n)
    dist = bfs_distances(variable_graph(inst), drop_v)
    prof = {}
    for u in range(n):
        if u != drop_v:
            prof.setdefault(dist.get(u), []).append(tv(mb[u], mc[u]))
    return prof


def correlation_profile(inst, src_v, sampler="dpll", seed=0, K=80):
    """{distance -> [connected corr(src_v, u)]} in the BASE ensemble (no conditioning). Unreachable under key None."""
    base = _solutions(inst, sampler, seed, K)
    if not _enough(base, sampler):
        return None
    dom, n = inst.domain, inst.n_vars
    dist = bfs_distances(variable_graph(inst), src_v)
    prof = {}
    for u in range(n):
        if u != src_v:
            prof.setdefault(dist.get(u), []).append(connected_corr(base, src_v, u, dom))
    return prof


def aggregate(profiles):
    """Merge per-(instance, anchor) profiles into {distance -> mean signal} (None = cross-component / unreachable)."""
    bins = {}
    for p in profiles:
        if p:
            for d, vals in p.items():
                bins.setdefault(d, []).extend(vals)
    return {d: float(np.mean(v)) for d, v in bins.items() if v}


def fit_decay(dist_mean: dict):
    """Fit signal(d) ~ A·exp(−d/λ) on finite d>=1 (OLS of log-signal on d). Returns reach_length λ + fit r2."""
    pts = [(d, s) for d, s in dist_mean.items() if d is not None and d >= 1 and s and s > 1e-9]
    if len(pts) < 2:
        return {"reach_length": None, "r2": None, "n_points": len(pts)}
    ds = np.array([[d] for d, _ in pts], float)
    ys = np.array([math.log(s) for _, s in pts])
    r2, beta = RF.fit_r2(ds, ys)
    slope = beta[1]
    lam = (-1.0 / slope) if slope < -1e-9 else float("inf")
    return {"reach_length": ("inf" if lam == float("inf") else round(lam, 3)),
            "r2": round(float(r2), 3), "slope": round(float(slope), 4), "n_points": len(pts)}


def reach_score(dist_mean: dict):
    """Bounded, orderable reach scalar = mean signal BEYOND nearest neighbours (distances d>=2). Short pole -> ~0;
    medium -> moderate; long/non-decaying -> high. The ordering criterion (prereg_v17) uses this, not λ (which can
    be 'inf' and is not intervalable)."""
    far = [s for d, s in dist_mean.items() if d is not None and d >= 2]
    return float(np.mean(far)) if far else 0.0


def measure_reach(rels, domain, n, alpha, observable="corr", sampler="dpll", n_instances=6, base_seed=700000,
                  value=1, drops="all", K=80, instance_fn=None, max_anchors=10):
    """ξ for an ensemble: collect per-instance profiles (over drop/source variables), aggregate, fit + score.
    `instance_fn(i)->inst` overrides the default random generator (used for the decoupled short pole). `max_anchors`
    caps the drop/source variables sampled per instance (bounds cost; does not change the estimand)."""
    per_inst_scores, all_profiles = [], []
    for i in range(n_instances):
        inst = instance_fn(i) if instance_fn else E.gen_instance(rels, domain, n, alpha, base_seed + i, family_id=observable)
        adj = variable_graph(inst)
        degs = {v: len(adj[v]) for v in range(n)}
        connected = [v for v in range(n) if degs[v] > 0]
        if not connected:
            continue
        if drops == "degree_hi":
            anchors = sorted(connected, key=lambda v: -degs[v])[:max(1, len(connected) // 4)]
        elif drops == "degree_lo":
            anchors = sorted(connected, key=lambda v: degs[v])[:max(1, len(connected) // 4)]
        else:
            anchors = connected
        anchors = anchors[:max_anchors]
        inst_profs = []
        for v in anchors:
            p = (forcing_profile(inst, v, value, sampler, base_seed + 991 * i + v, K) if observable == "forcing"
                 else correlation_profile(inst, v, sampler, base_seed + 991 * i + v, K))
            if p:
                inst_profs.append(p)
                all_profiles.append(p)
        if inst_profs:
            per_inst_scores.append(reach_score(aggregate(inst_profs)))
    mean = aggregate(all_profiles)
    return {"observable": observable, "sampler": sampler, "n": n, "alpha": alpha,
            "profile": {("inf" if d is None else d): round(s, 4) for d, s in sorted(mean.items(), key=lambda kv: (kv[0] is None, kv[0]))},
            "cross_component_shift": round(mean.get(None, 0.0), 4),
            "reach_score": round(reach_score(mean), 4), "reach_fit": fit_decay(mean),
            "per_instance_scores": [round(s, 4) for s in per_inst_scores], "n_profiles": len(all_profiles)}


# ── the three sealed poles (prereg_v17) + the ordering calibration ───────────────────────────────────────────
R_EQ = frozenset({(0, 0), (1, 1)})            # 2-affine (equality): full pairwise correlation, no escape
R_IMP = frozenset({(0, 0), (0, 1), (1, 1)})   # 2-SAT (implication x->y): correlation attenuates (leaks via consequent)


def _matching_instance(rel, domain, n, seed):
    """The decoupled 'trivially-local' short pole: n//2 disjoint edges (a matching) of `rel` — cannot propagate past
    d=1 (no d>=2 finite distances exist), so reach_score is ~0 by construction. Same relation as the long pole, so
    the contrast isolates STRUCTURE (matching vs connected), not the relation."""
    rng = E.rng_for("match", seed, n)
    verts = list(range(n))
    rng.shuffle(verts)
    cons = tuple((rel, (verts[2 * i], verts[2 * i + 1])) for i in range(n // 2))
    return E.CSPInstance(domain=tuple(domain), n_vars=n, constraints=cons, meta=("matching", n, seed))


def boot_interval(scores, lo=10, hi=90, n_boot=400, seed=13):
    if scores is None or len(scores) < 2:
        return (None, None)
    rng = np.random.default_rng(seed)
    arr = np.array(scores, float)
    means = [float(np.mean(rng.choice(arr, len(arr)))) for _ in range(n_boot)]
    return (round(float(np.percentile(means, lo)), 4), round(float(np.percentile(means, hi)), 4))


def three_pole_calibration(domain=(0, 1), n=18, alpha=1.4, observable="corr", sampler="dpll",
                           n_instances=10, base_seed=808000, K=80):
    """Measure reach_score for short(decoupled matching) / medium(2-SAT) / long(2-affine) at a common density; check
    the sealed ordering short<medium<long with NON-OVERLAPPING bootstrap intervals (prereg_v17). PASS iff both."""
    long_ = measure_reach((R_EQ,), domain, n, alpha, observable, sampler, n_instances, base_seed + 1, K=K)
    med = measure_reach((R_IMP,), domain, n, alpha, observable, sampler, n_instances, base_seed + 2, K=K)
    short = measure_reach((R_EQ,), domain, n, alpha, observable, sampler, n_instances, base_seed + 3, K=K,
                          instance_fn=lambda i: _matching_instance(R_EQ, domain, n, base_seed + 3 + i))
    poles = {"short": short, "medium": med, "long": long_}
    iv = {k: boot_interval(v["per_instance_scores"]) for k, v in poles.items()}
    s, m, l = short["reach_score"], med["reach_score"], long_["reach_score"]
    ordered = s < m < l
    nonoverlap = (None not in iv["short"] + iv["medium"] + iv["long"]
                  and iv["short"][1] < iv["medium"][0] and iv["medium"][1] < iv["long"][0])
    return {"observable": observable, "sampler": sampler, "n": n, "alpha": alpha,
            "reach_scores": {"short": s, "medium": m, "long": l}, "intervals": iv,
            "ordered_short_lt_medium_lt_long": bool(ordered), "intervals_nonoverlapping": bool(nonoverlap),
            "PASS": bool(ordered and nonoverlap),
            "profiles": {k: v["profile"] for k, v in poles.items()}}


# ── hand-count selftest (CI): BFS on a hand instance; forcing/correlation on known media; parity blindness ────
def selftest_reach():
    errs = []
    # 1. BFS on a hand instance: two arity-3 constraints sharing var 2 -> known distances from var 0
    R = frozenset({(0, 0, 0), (1, 1, 1)})
    inst = E.CSPInstance((0, 1), 5, ((R, (0, 1, 2)), (R, (2, 3, 4))))
    dist = bfs_distances(variable_graph(inst), 0)
    for u, d in {0: 0, 1: 1, 2: 1, 3: 2, 4: 2}.items():
        if dist.get(u) != d:
            errs.append(f"bfs({u})={dist.get(u)} want {d}")
    # 2. forcing along an implication chain (exact): shift positive and DECREASING with distance
    chain = E.CSPInstance((0, 1), 6, tuple((R_IMP, (i, i + 1)) for i in range(5)))
    pf = aggregate([forcing_profile(chain, 0, 1, sampler="exact")])
    if not (pf.get(1, 0) > pf.get(5, -1) > 0):
        errs.append(f"forcing chain not positive+decreasing: {pf}")
    # 3. pure 3-ary parity is BLIND to BOTH observables (why the affine pole must be 2-affine)
    xor3 = frozenset({(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)})
    x = E.CSPInstance((0, 1), 3, ((xor3, (0, 1, 2)),))
    if max(aggregate([forcing_profile(x, 0, 1, sampler="exact")]).values(), default=0) > 1e-9:
        errs.append("3-XOR forcing shift should be ~0 (balanced marginals)")
    if max(aggregate([correlation_profile(x, 0, sampler="exact")]).values(), default=0) > 1e-9:
        errs.append("3-XOR pairwise correlation should be ~0 (pure 3-point)")
    # 4. 2-affine equality chain: correlation reaches FAR (non-decaying), the long-pole mechanism
    eqc = E.CSPInstance((0, 1), 5, tuple((R_EQ, (i, i + 1)) for i in range(4)))
    pc = aggregate([correlation_profile(eqc, 0, sampler="exact")])
    if not (pc.get(1, 0) > 0.1 and pc.get(4, 0) > 0.1):
        errs.append(f"eq-chain correlation should reach far: {pc}")
    return errs


if __name__ == "__main__":
    e = selftest_reach()
    print("reach selftest:", "OK" if not e else "FAIL")
    for x in e:
        print("  ", x)
