#!/usr/bin/env python3
"""Observatory fan-out, BATCH 6 — the first roster drawn from a verified-clean queue.

Every row here was vetted against its own `canonical_encoding` BEFORE the roster was hashed, and every
one is a vertex- or item-subset row, so the ambient is fixed by construction. Batch 5's three mis-typings
and batch 4's two ambient-confounded exclusions are what those two checks exist for.

The planar rows take random subgraphs of a GRID, which is planar by construction — a subgraph of a planar
graph is planar, so the row's defining property holds without a planarity test that could quietly accept
a non-planar instance.
"""
import hashlib
import json
import sys
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "dev"))
LAT = ROOT / "foundry" / "results" / "lattice"
OUT = LAT / "observatory_batch6_panels.json"
LEDGER = LAT / "observatory_reservation.jsonl"
TRAIL = LAT / "maptrail.jsonl"
from foundry.catalog import capture as C                                        # noqa: E402
from foundry.catalog import maptrail as M                                       # noqa: E402
from foundry.catalog import reservation as RES                                  # noqa: E402
import n2_dense_control as N2                                                   # noqa: E402
from sounding_v1 import BOOL_OPS                                                # noqa: E402

SEED = 20260727
BATCH = 6
NG = 9
GRAPH = (0.15, 0.25, 0.35, 0.45, 0.60)
OPT = (0.5, 1.0, 1.5, 2.0, 3.0)


def G(n, p, rng):
    return [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < p]


def grid_edges(rows, cols):
    """Grid adjacency — planar by construction, and every subgraph of it is planar too."""
    E = []
    for r in range(rows):
        for c in range(cols):
            v = r * cols + c
            if c + 1 < cols:
                E.append((v, r * cols + c + 1))
            if r + 1 < rows:
                E.append((v, (r + 1) * cols + c))
    return E


def planar_graph(rng, p, rows=3, cols=3):
    return [e for e in grid_edges(rows, cols) if rng.random() < min(1.0, p * 2.2)]


def directed_feedback_vertex_set(rng, p, n=NG):
    """Vertex subsets whose removal leaves the digraph acyclic. Upward-closed; ground set is V."""
    arcs = [(i, j) for i in range(n) for j in range(n) if i != j and rng.random() < p * 0.6]
    if not arcs:
        return []

    def acyclic(removed):
        out = {i: [] for i in range(n)}
        for u, v in arcs:
            if u not in removed and v not in removed:
                out[u].append(v)
        colour = {}

        def dfs(x):
            colour[x] = 1
            for y in out[x]:
                if colour.get(y) == 1:
                    return False
                if colour.get(y) is None and not dfs(y):
                    return False
            colour[x] = 2
            return True
        return all(colour.get(x) is not None or dfs(x) for x in range(n))
    f = [s for s in product((0, 1), repeat=n)
         if acyclic({i for i in range(n) if s[i]})]
    if len(f) < 2:
        return []
    b = min(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b])]


def partial_vertex_cover(rng, p, n=NG):
    """Vertex subsets covering at least half the edges. Upward-closed."""
    E = G(n, p, rng)
    if len(E) < 2:
        return []
    t = max(1, len(E) // 2)

    def cov(s):
        return sum(1 for u, v in E if s[u] or s[v])
    f = [s for s in product((0, 1), repeat=n) if cov(s) >= t]
    if len(f) < 2:
        return []
    b = min(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b])]


def _vc(E, n, mode):
    if mode == "cover":
        f = [s for s in product((0, 1), repeat=n) if all(s[u] or s[v] for u, v in E)]
    elif mode == "independent":
        f = [s for s in product((0, 1), repeat=n) if all(not (s[u] and s[v]) for u, v in E)]
    else:                                   # dominating
        adj = {i: {i} for i in range(n)}
        for u, v in E:
            adj[u].add(v); adj[v].add(u)
        f = [s for s in product((0, 1), repeat=n) if all(any(s[u] for u in adj[v]) for v in range(n))]
    if len(f) < 2:
        return []
    b = (max if mode == "independent" else min)(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b])]


def planar_vertex_cover(rng, p, n=9):
    return _vc(planar_graph(rng, p), n, "cover")


def planar_independent_set(rng, p, n=9):
    return _vc(planar_graph(rng, p), n, "independent")


def maximum_minimal_vertex_cover(rng, p, n=NG):
    """MINIMAL vertex covers — covers with no proper sub-cover. Neither closure direction: a superset
    of a minimal cover is a cover but not minimal, a subset is not a cover."""
    E = G(n, p, rng)
    if len(E) < 2:
        return []
    covers = [s for s in product((0, 1), repeat=n) if all(s[u] or s[v] for u, v in E)]
    cs = set(covers)
    f = [s for s in covers
         if all(tuple(0 if j == i else s[j] for j in range(n)) not in cs
                for i in range(n) if s[i])]
    if len(f) < 2:
        return []
    b = max(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b])]


def multidimensional_knapsack(rng, ratio, n=11):
    """Item subsets satisfying every one of d capacity constraints. Downward-closed; ground set is the
    ITEM set, held at n, so d moves without moving the ambient."""
    d = max(1, round(ratio * 3))
    w = [[rng.randint(1, 9) for _ in range(n)] for _ in range(d)]
    cap = [sum(row) * 0.4 for row in w]
    f = [s for s in product((0, 1), repeat=n)
         if all(sum(w[k][i] for i in range(n) if s[i]) <= cap[k] for k in range(d))]
    if len(f) < 2:
        return []
    b = max(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b])]


def red_blue_set_cover(rng, ratio, m=11):
    """Subfamilies covering every BLUE element. Upward-closed; ground set is the candidate family."""
    nb = max(2, round(ratio * 4))
    sets = [frozenset(i for i in range(nb) if rng.random() < 0.45) for _ in range(m)]
    blue = set(range(nb))
    f = []
    for s in product((0, 1), repeat=m):
        cov = set()
        for i in range(m):
            if s[i]:
                cov |= sets[i]
        if cov >= blue:
            f.append(s)
    if len(f) < 2:
        return []
    b = min(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b])]


ROWS = {
    "directed-feedback-vertex-set": (directed_feedback_vertex_set, "upward_closed", "graph", GRAPH,
                                     "edge density of the ground digraph"),
    "partial-vertex-cover":         (partial_vertex_cover, "upward_closed", "graph", GRAPH,
                                     "edge density of the ground graph"),
    "planar-independent-set":       (planar_independent_set, "downward_closed", "graph", GRAPH,
                                     "edge density of the ground grid graph"),
    "planar-vertex-cover":          (planar_vertex_cover, "upward_closed", "graph", GRAPH,
                                     "edge density of the ground grid graph"),
    "multidimensional-knapsack":    (multidimensional_knapsack, "downward_closed", "optimization", OPT,
                                     "capacity constraints per item"),
    "red-blue-set-cover":           (red_blue_set_cover, "upward_closed", "optimization", OPT,
                                     "blue elements per candidate set"),
}


def main() -> int:
    cen = json.loads((LAT / "observatory_batch6_census.json").read_text())
    reserved = RES.reserved_rows(LEDGER)
    leak = sorted(set(ROWS) & reserved)
    if leak:
        raise RuntimeError(f"FRONTIER LEAK — batch 6 defines generators for reserved row(s) {leak}")
    missing = sorted(set(cen["published"]) - set(ROWS))
    if missing:
        raise RuntimeError(f"census published {missing} with no generator")
    print(f"reservation honoured: {len(reserved)} row(s) withheld across all batches\n")

    out, excluded = [], []
    ctrl = lambda region, rng: N2.cp_control(region, rng)[0]
    for row, (build, expect, fam, ramp, inst) in ROWS.items():
        print(f"  capturing {row} ...", flush=True)
        rec, ex = C.capture_row(row, build, expect, ramp, BOOL_OPS, SEED, ctrl)
        if ex:
            excluded.append(ex)
            print(f"    EXCLUDED at birth: {row} — {ex['reason'][0]}", flush=True)
        else:
            rec["family"] = fam
            rec["ramp_parameter"] = cen["families"][fam]["census_ramp"]
            rec["ramp_instantiated_as"] = inst
            out.append(rec)

    doc = {"schema": "observatory-batch6/v1",
           "STATUS": "EXPLORATORY dial panels — no verdict, no scored prediction, no seal",
           "not_citable_as": "a result. Descriptive capture only.",
           "batch": BATCH, "reach_class": "REACH-subset",
           "families": {f: cen["families"][f]["census_ramp"] for f in
                        sorted({v[2] for v in ROWS.values()})},
           "why_these_rows": cen["why_this_batch"],
           "roster_vetted_before_hashing": ("every row appears in the verified-clean queue of "
                                            "reach_subset_readjudication.json"),
           "frontier_reservation": {"reserved_this_batch": sorted(cen["reservation"]["reserved"]),
                                    "roster_sha256": cen["reservation"]["roster_sha256"]},
           "pipeline": "foundry.catalog.capture — one implementation for every batch",
           "excluded_at_birth": excluded, "rows": out}
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    M.emit(TRAIL, "expansion", key=f"expansion:batch{BATCH}",
           artifact=OUT.name, sha256=hashlib.sha256(OUT.read_bytes()).hexdigest(),
           wave=None, rows_added=[r["row"] for r in out], n_rows=len(out),
           n_reserved=len(cen["reservation"]["reserved"]), reservation_ledger=LEDGER.name,
           roster_vetted_before_hashing=True,
           admission_authority="observatory fan-out; roster drawn from the verified-clean queue")
    for e in excluded:
        M.emit(TRAIL, "exclusion", key=f"exclusion:batch{BATCH}:{e['row']}",
               problem=e["row"], batch=BATCH, reasons=e["reason"], authority="conformance at birth")

    print(f"\nBATCH 6 — {len(out)} rows shipped, {len(excluded)} excluded at birth\n")
    for r in out:
        print(f"  {r['row']}  [{r['structural_expectation'] or 'no declared structure'}]")
        for s in r["steps"]:
            if s["state"] != "usable":
                print(f"      x={s['ramp_value']:<5} {s['state']}")
                continue
            d = s["dials"]
            ex2 = {k: round(v["blend_excess"], 3) for k, v in d["flavours"].items()
                   if v["blend_excess"] is not None}
            print(f"      x={str(s['ramp_value']):<5}{s['region']:<9}r={d['r_mean']:<8}"
                  f"ov={str(d['overlap_mean']):<7}{ex2}")
        print()
    print(f"wrote {OUT.name}  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
