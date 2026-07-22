"""Structural predictors (Sprint 6 "Pebble", prereg_v13 addendum) — the FREE, graph-only rival to reach ξ.

ξ costs sampling; the constraint hypergraph is free — we already generate it. Propagation range is governed by the
medium's geometry, and the medium is the constraint graph. Theory both ways: expanders are where nothing decays
(PCP/inapprox), bounded treewidth is where propagation is containable (DP). So these are a legitimate RIVAL predictor
to ξ, raced against it density-resolved (P3/P4), never a substitute.

Closed feature set, capped at FOUR (prereg_v13; same closure reasoning as Sprint 4.6). All on the variable-adjacency
graph — nodes = variables, edge iff two variables co-occur in a constraint scope, THE SAME graph ξ's BFS distance
uses — computed on instances already generated, no new sampling:
  * spectral_gap   — lambda_2(D - A), Fiedler algebraic connectivity (Cheeger: h(G) >= lambda_2/2). 0 iff disconnected.
  * expansion_proxy— sampled-min edge-expansion over K random cuts (an UPPER estimate of the true min).
  * degree_mean/var— cheapest geometry summary; also the control that makes spectral_gap's density-scaling visible.
  * treewidth_ub   — min-degree elimination UPPER BOUND (a BOUND, never 'treewidth').
"""
import numpy as np

from foundry import ensemble as E

EXPANSION_SAMPLES = 256           # K, sealed in prereg_v13


def variable_graph(inst) -> dict:
    """Undirected variable-adjacency graph as {v: set(neighbours)}. Two variables are adjacent iff they co-occur in
    some constraint scope. This is the medium's geometry ξ's BFS also walks; kept here so reach.py imports one graph."""
    adj = {v: set() for v in range(inst.n_vars)}
    for _R, scope in inst.constraints:
        s = tuple(scope)
        for i in range(len(s)):
            for j in range(i + 1, len(s)):
                a, b = s[i], s[j]
                if a != b:
                    adj[a].add(b)
                    adj[b].add(a)
    return adj


def spectral_gap(adj: dict) -> float:
    """lambda_2 of the combinatorial Laplacian L = D - A (the Fiedler algebraic connectivity). 0 iff the variable
    graph is disconnected (any isolated variable => 0). UNNORMALIZED — scales with degree (density); read
    density-resolved and alongside degree_summary (prereg_v13 declared bias)."""
    n = len(adj)
    if n < 2:
        return 0.0
    idx = {v: i for i, v in enumerate(sorted(adj))}
    L = np.zeros((n, n))
    for v, nbrs in adj.items():
        iv = idx[v]
        L[iv, iv] = len(nbrs)
        for u in nbrs:
            L[iv, idx[u]] -= 1.0
    w = np.linalg.eigvalsh((L + L.T) / 2)     # symmetric; ascending
    return round(float(w[1]), 6)               # second-smallest = Fiedler value


def expansion_proxy(adj: dict, seed="pebble-struct", n_samples=EXPANSION_SAMPLES) -> float:
    """Sampled-min edge-expansion: over K random subsets S (each vertex i.i.d. w.p. 0.5, empty/full rejected),
    h(S) = |edges crossing (S, complement)| / min(|S|, |complement|); return the MIN found. An UPPER estimate of the
    true minimum expansion (sampling can only overestimate the min). O(K*|E|), no eigendecomposition."""
    verts = sorted(adj)
    n = len(verts)
    if n < 2:
        return 0.0
    edges = [(u, v) for u in verts for v in adj[u] if u < v]
    if not edges:
        return 0.0
    rng = E.rng_for("expansion", seed, n, len(edges))
    best = None
    for _ in range(n_samples):
        inS = {v: (rng.random() < 0.5) for v in verts}
        s = sum(inS.values())
        if s == 0 or s == n:
            continue
        cut = sum(1 for u, v in edges if inS[u] != inS[v])
        h = cut / min(s, n - s)
        if best is None or h < best:
            best = h
    return round(float(best), 6) if best is not None else 0.0


def degree_summary(adj: dict) -> tuple:
    """(mean, variance) of variable degree. Two numbers; higher moments not used (closed set)."""
    degs = [len(adj[v]) for v in adj]
    if not degs:
        return (0.0, 0.0)
    m = sum(degs) / len(degs)
    var = sum((d - m) ** 2 for d in degs) / len(degs)
    return (round(m, 6), round(var, 6))


def treewidth_ub(adj: dict) -> int:
    """Upper bound on treewidth via the MIN-DEGREE elimination ordering: repeatedly eliminate the current-min-degree
    vertex, fill its neighbourhood to a clique; width = max elimination degree. A BOUND, never 'treewidth'."""
    g = {v: set(nbrs) for v, nbrs in adj.items()}
    width = 0
    while g:
        v = min(g, key=lambda x: len(g[x]))
        nbrs = g[v]
        width = max(width, len(nbrs))
        for a in nbrs:                              # make the neighbourhood a clique (fill)
            g[a] |= (nbrs - {a})
        for a in nbrs:
            g[a].discard(v)
        del g[v]
    return int(width)


def structural_features(inst, seed="pebble-struct") -> dict:
    """All four sealed features for one instance (5 numbers). The graph-only, free, instance-level tier."""
    adj = variable_graph(inst)
    dmean, dvar = degree_summary(adj)
    return {"spectral_gap": spectral_gap(adj),
            "expansion_proxy": expansion_proxy(adj, seed=seed),
            "degree_mean": dmean, "degree_var": dvar,
            "treewidth_ub": treewidth_ub(adj)}


# ── hand-count selftest (in CI): known small graphs -> known feature values ───────────────────────────────────
def _clique(n):        return {v: set(u for u in range(n) if u != v) for v in range(n)}
def _cycle(n):         return {v: {(v - 1) % n, (v + 1) % n} for v in range(n)}
def _path(n):          return {v: {u for u in (v - 1, v + 1) if 0 <= u < n} for v in range(n)}
def _two_triangles():  # two disjoint K3 on {0,1,2} and {3,4,5}
    a = {0: {1, 2}, 1: {0, 2}, 2: {0, 1}}
    b = {3: {4, 5}, 4: {3, 5}, 5: {3, 4}}
    return {**a, **b}


def selftest_structural() -> list:
    """Return [] iff every hand value matches. Spectral gaps are standard Laplacian spectra; treewidth bounds and
    degree summaries are elimination/degree hand-traces; expansion cases pick graphs with an obvious optimal cut."""
    errs = []

    def close(got, want, tag, tol=1e-6):
        if abs(got - want) > tol:
            errs.append(f"{tag}: got {got}, want {want}")

    # spectral gap = lambda_2(D-A): K3 -> 3, P3 -> 1, C4 -> 2, disconnected -> 0
    close(spectral_gap(_clique(3)), 3.0, "spectral_gap(K3)")
    close(spectral_gap(_path(3)), 1.0, "spectral_gap(P3)")
    close(spectral_gap(_cycle(4)), 2.0, "spectral_gap(C4)")
    close(spectral_gap(_two_triangles()), 0.0, "spectral_gap(2xK3 disconnected)")

    # treewidth upper bound (min-degree): tree/path -> 1, K4 -> 3, C4 -> 2, K3 -> 2
    if treewidth_ub(_path(4)) != 1: errs.append(f"treewidth_ub(P4): got {treewidth_ub(_path(4))}, want 1")
    if treewidth_ub(_clique(4)) != 3: errs.append(f"treewidth_ub(K4): got {treewidth_ub(_clique(4))}, want 3")
    if treewidth_ub(_cycle(4)) != 2: errs.append(f"treewidth_ub(C4): got {treewidth_ub(_cycle(4))}, want 2")
    if treewidth_ub(_clique(3)) != 2: errs.append(f"treewidth_ub(K3): got {treewidth_ub(_clique(3))}, want 2")

    # degree summary: K4 all degree 3 -> (3, 0); path P3 degrees [1,2,1] -> mean 4/3, var 2/9
    dm, dv = degree_summary(_clique(4))
    close(dm, 3.0, "degree_mean(K4)"); close(dv, 0.0, "degree_var(K4)")
    dm, dv = degree_summary(_path(3))
    close(dm, 4 / 3, "degree_mean(P3)"); close(dv, 2 / 9, "degree_var(P3)")

    # expansion proxy: K4 every balanced 2|2 cut = 4/2 = 2 (the min) -> 2.0; disconnected -> a 0-cut exists -> 0.0
    close(expansion_proxy(_clique(4)), 2.0, "expansion_proxy(K4)")
    close(expansion_proxy(_two_triangles()), 0.0, "expansion_proxy(2xK3)")

    return errs


if __name__ == "__main__":
    e = selftest_structural()
    print("structural selftest:", "OK" if not e else "FAIL")
    for x in e:
        print("  ", x)
