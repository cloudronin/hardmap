#!/usr/bin/env python3
"""Observatory fan-out, BATCH 2 — six graph rows, adding the direction batch 1 never covered.

BATCH 1 HAD NO UPWARD-CLOSED ROW. Two downward-closed, two fixed-cardinality, two neither — which left
the screen stack's max-closed direction unexercised on new generators. Batch 2 opens with two
upward-closed rows for exactly that reason.

  graph-spanner              edge subsets meeting a distance guarantee     UPWARD-closed
  connectivity-augmentation  edge subsets restoring connectivity           UPWARD-closed
  cluster-deletion           edge subsets whose removal leaves cliques     DOWNWARD-closed
  upper-domination           independent dominating sets                   neither
  k-center                   size-k centre sets                            FIXED CARDINALITY
  max-dispersion             size-k spread sets                            FIXED CARDINALITY

The capture pipeline is `foundry.catalog.capture` — one implementation for every batch. A batch is a
table of generators and nothing else.
"""
import hashlib, json, random, sys
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "dev"))
LAT = ROOT / "foundry" / "results" / "lattice"
OUT = LAT / "observatory_batch2_panels.json"
from foundry.catalog import capture as C
import n2_dense_control as N2
from sounding_v1 import BOOL_OPS

SEED = 20260726
RAMP = (0.15, 0.25, 0.35, 0.45, 0.60)      # edge density — the family dial declared at census
N = 9


def G(n, p, rng):
    return [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < p]


def _reach(n, edges):
    a = {i: set() for i in range(n)}
    for u, v in edges:
        a[u].add(v); a[v].add(u)
    seen, st = {0}, [0]
    while st:
        x = st.pop()
        for y in a[x]:
            if y not in seen:
                seen.add(y); st.append(y)
    return seen


def _dist_ok(n, E, sub, stretch=3):
    """Every edge of E must be spanned within `stretch` hops in the subgraph — the spanner condition."""
    a = {i: set() for i in range(n)}
    for u, v in sub:
        a[u].add(v); a[v].add(u)
    for u, v in E:
        seen, frontier, d = {u}, [u], 0
        ok = False
        while frontier and d < stretch:
            nxt = []
            for x in frontier:
                for y in a[x]:
                    if y == v:
                        ok = True; break
                    if y not in seen:
                        seen.add(y); nxt.append(y)
                if ok: break
            if ok: break
            frontier = nxt; d += 1
        if not ok:
            return False
    return True


def graph_spanner(rng, p, n=N):
    E = G(n, p, rng)
    if not E or len(E) > 14: return []
    m = len(E)
    f = [s for s in product((0, 1), repeat=m)
         if _dist_ok(n, E, [E[i] for i in range(m) if s[i]])]
    if not f: return []
    b = min(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b])]


def connectivity_augmentation(rng, p, n=N):
    """Edge subsets whose ADDITION connects the graph. Upward-closed: adding more can only help."""
    base = G(n, p * 0.5, rng)
    cand = [e for e in G(n, 0.55, rng) if e not in base][:13]
    if not cand: return []
    m = len(cand)
    f = [s for s in product((0, 1), repeat=m)
         if len(_reach(n, base + [cand[i] for i in range(m) if s[i]])) == n]
    if not f: return []
    b = min(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b])]


def cluster_deletion(rng, p, n=N):
    """Edge subsets to DELETE so every component is a clique. Downward-closed in the kept set."""
    E = G(n, p, rng)
    if not E or len(E) > 14: return []
    m = len(E)
    def cliquey(keep):
        a = {i: set() for i in range(n)}
        for u, v in keep:
            a[u].add(v); a[v].add(u)
        comp, seen = [], set()
        for s0 in range(n):
            if s0 in seen: continue
            cur, st = set(), [s0]
            while st:
                x = st.pop()
                if x in cur: continue
                cur.add(x); seen.add(x)
                st.extend(a[x] - cur)
            comp.append(cur)
        return all(all(v in a[u] for u in c for v in c if u != v) for c in comp)
    f = [s for s in product((0, 1), repeat=m) if cliquey([E[i] for i in range(m) if s[i]])]
    if not f: return []
    b = max(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b])]


def upper_domination(rng, p, n=N):
    E = G(n, p, rng)
    a = {i: {i} for i in range(n)}
    for u, v in E:
        a[u].add(v); a[v].add(u)
    f = [s for s in product((0, 1), repeat=n)
         if all(any(s[u] for u in a[v]) for v in range(n))
         and all(not (s[u] and s[v]) for u, v in E)]
    if not f: return []
    b = max(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b])]


def _apsp(n, E):
    INF = 99
    d = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    for u, v in E:
        d[u][v] = d[v][u] = 1
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return d


def k_center(rng, p, n=N, k=3):
    E = G(n, p, rng); d = _apsp(n, E)
    f = [s for s in product((0, 1), repeat=n) if sum(s) == k]
    cost = lambda s: max(min(d[v][u] for u in range(n) if s[u]) for v in range(n))
    b = min(cost(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if cost(s) == b])]


def max_dispersion(rng, p, n=N, k=3):
    E = G(n, p, rng); d = _apsp(n, E)
    f = [s for s in product((0, 1), repeat=n) if sum(s) == k]
    spread = lambda s: min(d[u][v] for u in range(n) for v in range(n) if u < v and s[u] and s[v])
    b = max(spread(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if spread(s) == b])]


ROWS = {
    "graph-spanner":             (graph_spanner,             "upward_closed"),
    "connectivity-augmentation": (connectivity_augmentation, "upward_closed"),
    "cluster-deletion":          (cluster_deletion,          None),
    "upper-domination":          (upper_domination,          None),
    "k-center":                  (k_center,                  "fixed_cardinality"),
    "max-dispersion":            (max_dispersion,            "fixed_cardinality"),
}


def main():
    out, excluded = [], []
    ctrl = lambda region, rng: N2.cp_control(region, rng)[0]
    for row, (build, expect) in ROWS.items():
        print(f"  capturing {row} ...", flush=True)
        rec, ex = C.capture_row(row, build, expect, RAMP, BOOL_OPS, SEED, ctrl)
        if ex:
            excluded.append(ex); print(f"    EXCLUDED at birth: {row} — {ex['reason'][0]}", flush=True)
        else:
            rec["family"] = "graph"; rec["ramp_parameter"] = "edge density"
            out.append(rec)
    doc = {"schema": "observatory-batch2/v1",
           "STATUS": "EXPLORATORY dial panels — no verdict, no scored prediction, no seal",
           "not_citable_as": "a result. Descriptive capture only.",
           "batch": 2, "family": "graph", "reach_class": "REACH-subset",
           "ramp_parameter_declared_at_census": "edge density",
           "why_these_six": ("batch 1 had NO upward-closed row, leaving the screen stack's max-closed "
                             "direction unexercised on new generators. Two upward-closed rows open this "
                             "batch for exactly that reason."),
           "pipeline": "foundry.catalog.capture — one implementation for every batch",
           "excluded_at_birth": excluded, "rows": out}
    OUT.write_text(json.dumps(doc, indent=1) + "\n")
    print(f"\nBATCH 2 — {len(out)} rows shipped, {len(excluded)} excluded at birth\n")
    for r in out:
        print(f"  {r['row']}  [{r['structural_expectation'] or 'no declared structure'}]")
        for s in r["steps"]:
            if s["state"] != "usable":
                print(f"      p={s['ramp_value']:<5} {s['state']}"); continue
            d = s["dials"]
            ex2 = {k: round(v["blend_excess"], 3) for k, v in d["flavours"].items()
                   if v["blend_excess"] is not None}
            print(f"      p={s['ramp_value']:<5}{s['region']:<9}r={d['r_mean']:<8}"
                  f"ov={str(d['overlap_mean']):<7}BC={str(d['bimodality_coefficient']):<7}{ex2}")
        print()
    print(f"wrote {OUT.name}  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
