#!/usr/bin/env python3
"""Observatory fan-out, BATCH 4 — the queue's bulk, plus the row that narrowed a rule.

  edge-dominating-set        edge subsets dominating every edge        UPWARD-closed
  cluster-vertex-deletion    vertex subsets leaving disjoint cliques   UPWARD-closed
  feedback-arc-set           arc subsets whose removal breaks cycles   UPWARD-closed
  connected-vertex-cover     covers that also induce a connected graph neither
  3sum                       size-3 subsets summing to zero            FIXED CARDINALITY
  3-partition                size-3 subsets hitting the triple target  FIXED CARDINALITY

3SUM IS HERE ON PURPOSE. Its members all have weight 3, so it declares `fixed_cardinality` honestly and
passes conformance — but its region is the size-3 subsets SUMMING TO ZERO, which depends entirely on the
instance. The descriptor@v2 rule would have called that structurally flat and dropped the row from Helm's
swept population. v3 narrows the rule to require the frames to show the region standing still, and this
row is the case that forced it.

The reserved rows have no generator here, as always: a batch that never learned how to build a row cannot
burn the ground it sits on.
"""
import hashlib
import json
import sys
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "dev"))
LAT = ROOT / "foundry" / "results" / "lattice"
OUT = LAT / "observatory_batch4_panels.json"
LEDGER = LAT / "observatory_reservation.jsonl"
TRAIL = LAT / "maptrail.jsonl"
from foundry.catalog import capture as C                                        # noqa: E402
from foundry.catalog import maptrail as M                                       # noqa: E402
from foundry.catalog import reservation as RES                                  # noqa: E402
import n2_dense_control as N2                                                   # noqa: E402
from sounding_v1 import BOOL_OPS                                                # noqa: E402

SEED = 20260727
BATCH = 4
NG = 9                       # graph order
GRAPH = (0.15, 0.25, 0.35, 0.45, 0.60)
NUM = (0.2, 0.35, 0.5, 0.65, 0.8)


def G(n, p, rng):
    return [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < p]


# ── graph rows ──────────────────────────────────────────────────────────────────────────────────────
def edge_dominating_set(rng, p, n=NG):
    """Edge subsets D such that every edge shares an endpoint with some edge of D. Upward-closed."""
    E = G(n, p, rng)
    if not (2 <= len(E) <= 12):
        return []
    m = len(E)
    def dominates(idx):
        chosen = [E[i] for i in idx]
        return all(any(set(e) & set(c) for c in chosen) for e in E)
    f = [s for s in product((0, 1), repeat=m)
         if dominates([i for i in range(m) if s[i]])]
    if len(f) < 2:
        return []
    b = min(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b])]


def cluster_vertex_deletion(rng, p, n=NG):
    """Vertex subsets whose removal leaves every component a clique. Upward-closed: deleting more
    vertices from a disjoint union of cliques leaves a disjoint union of cliques."""
    E = G(n, p, rng)
    adj = {i: set() for i in range(n)}
    for u, v in E:
        adj[u].add(v); adj[v].add(u)

    def cluster_after(removed):
        keep = [x for x in range(n) if x not in removed]
        ks = set(keep)
        seen, comps = set(), []
        for s0 in keep:
            if s0 in seen:
                continue
            cur, st = set(), [s0]
            while st:
                x = st.pop()
                if x in cur:
                    continue
                cur.add(x); seen.add(x)
                st.extend((adj[x] & ks) - cur)
            comps.append(cur)
        return all(v in adj[u] for c in comps for u in c for v in c if u != v)
    f = [s for s in product((0, 1), repeat=n)
         if cluster_after({i for i in range(n) if s[i]})]
    if len(f) < 2:
        return []
    b = min(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b])]


def feedback_arc_set(rng, p, n=NG):
    """Arc subsets whose removal makes the digraph acyclic. Upward-closed."""
    arcs = [(i, j) for i in range(n) for j in range(n)
            if i != j and rng.random() < p * 0.7]
    if not (2 <= len(arcs) <= 12):
        return []
    m = len(arcs)

    def acyclic(idx):
        keep = [arcs[i] for i in range(m) if i not in idx]
        out = {i: [] for i in range(n)}
        for u, v in keep:
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
    f = [s for s in product((0, 1), repeat=m)
         if acyclic({i for i in range(m) if s[i]})]
    if len(f) < 2:
        return []
    b = min(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b])]


def connected_vertex_cover(rng, p, n=NG):
    """Vertex covers that ALSO induce a connected subgraph. Neither direction: adding a vertex keeps
    the cover but can leave the induced subgraph disconnected."""
    E = G(n, p, rng)
    if not E:
        return []
    adj = {i: set() for i in range(n)}
    for u, v in E:
        adj[u].add(v); adj[v].add(u)

    def ok(s):
        S = {i for i in range(n) if s[i]}
        if not S or any(u not in S and v not in S for u, v in E):
            return False
        st, seen = [next(iter(S))], set()
        while st:
            x = st.pop()
            if x in seen:
                continue
            seen.add(x)
            st.extend((adj[x] & S) - seen)
        return seen == S
    f = [s for s in product((0, 1), repeat=n) if ok(s)]
    if len(f) < 2:
        return []
    b = min(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b])]


# ── number-theoretic rows ───────────────────────────────────────────────────────────────────────────
def three_sum(rng, frac, n=14):
    """Size-3 subsets summing to zero. Fixed cardinality — and NOT structurally flat, because which
    triples qualify is entirely instance-dependent. This is the row that narrowed the v2 rule."""
    V = max(2, round(frac * 20))
    vals = [rng.randint(-V, V) for _ in range(n)]
    f = [tuple(1 if i in c else 0 for i in range(n))
         for c in combinations(range(n), 3) if sum(vals[i] for i in c) == 0]
    if len(f) < 2:
        return []
    return [("feasible", f)]


def three_partition(rng, frac, n=12):
    """Size-3 subsets hitting the per-triple target of a planted 4-triple partition."""
    V = max(3, round(frac * 20))
    base = [rng.randint(1, V) for _ in range(n)]
    target = sum(base) // (n // 3)
    f = [tuple(1 if i in c else 0 for i in range(n))
         for c in combinations(range(n), 3) if sum(base[i] for i in c) == target]
    if len(f) < 2:
        return []
    return [("feasible", f)]


ROWS = {
    "edge-dominating-set":     (edge_dominating_set, "upward_closed", "graph", GRAPH,
                                "edge density of the ground graph"),
    "cluster-vertex-deletion": (cluster_vertex_deletion, "upward_closed", "graph", GRAPH,
                                "edge density of the ground graph"),
    "feedback-arc-set":        (feedback_arc_set, "upward_closed", "graph", GRAPH,
                                "arc density of the ground digraph"),
    "connected-vertex-cover":  (connected_vertex_cover, None, "graph", GRAPH,
                                "edge density of the ground graph"),
    "3sum":                    (three_sum, "fixed_cardinality", "number-theoretic", NUM,
                                "value range"),
    "3-partition":             (three_partition, "fixed_cardinality", "number-theoretic", NUM,
                                "value range"),
}


def main() -> int:
    cen = json.loads((LAT / "observatory_batch4_census.json").read_text())
    reserved = RES.reserved_rows(LEDGER)
    leak = sorted(set(ROWS) & reserved)
    if leak:
        raise RuntimeError(f"FRONTIER LEAK — batch 4 defines generators for reserved row(s) {leak}")
    missing = sorted(set(cen["published"]) - set(ROWS))
    if missing:
        raise RuntimeError(f"census published {missing} but this batch has no generator for them")
    extra = sorted(set(ROWS) - set(cen["published"]))
    if extra:
        raise RuntimeError(f"batch defines {extra}, which the census did not publish")
    print(f"reservation honoured: {len(reserved)} row(s) withheld across all batches, no generator "
          f"defined for any of them\n")

    out, excluded = [], []
    ctrl = lambda region, rng: N2.cp_control(region, rng)[0]
    for row, (build, expect, fam, ramp, instantiates) in ROWS.items():
        print(f"  capturing {row} ...", flush=True)
        rec, ex = C.capture_row(row, build, expect, ramp, BOOL_OPS, SEED, ctrl)
        if ex:
            excluded.append(ex)
            print(f"    EXCLUDED at birth: {row} — {ex['reason'][0]}", flush=True)
        else:
            rec["family"] = fam
            rec["ramp_parameter"] = cen["families"][fam]["census_ramp"]
            rec["ramp_instantiated_as"] = instantiates
            out.append(rec)

    doc = {"schema": "observatory-batch4/v1",
           "STATUS": "EXPLORATORY dial panels — no verdict, no scored prediction, no seal",
           "not_citable_as": "a result. Descriptive capture only.",
           "batch": BATCH, "reach_class": "REACH-subset",
           "families": {f: cen["families"][f]["census_ramp"] for f in
                        sorted({v[2] for v in ROWS.values()})},
           "why_these_rows": cen["why_this_batch"],
           "frontier_reservation": {
               "reserved_this_batch": sorted(set(cen["reservation"]["reserved"])),
               "roster_sha256": cen["reservation"]["roster_sha256"],
               "note": "reserved rows are not captured and have no generator in this file"},
           "pipeline": "foundry.catalog.capture — one implementation for every batch",
           "excluded_at_birth": excluded, "rows": out}
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    M.emit(TRAIL, "expansion", key=f"expansion:batch{BATCH}",
           artifact=OUT.name, sha256=hashlib.sha256(OUT.read_bytes()).hexdigest(),
           wave=None, rows_added=[r["row"] for r in out], n_rows=len(out),
           n_reserved=len(cen["reservation"]["reserved"]), reservation_ledger=LEDGER.name,
           admission_authority="observatory fan-out, conformance-tested at birth; frontier reserved "
                               "per Helm §5 before capture")
    for e in excluded:
        M.emit(TRAIL, "exclusion", key=f"exclusion:batch{BATCH}:{e['row']}",
               problem=e["row"], batch=BATCH, reasons=e["reason"],
               authority="conformance at birth")

    print(f"\nBATCH 4 — {len(out)} rows shipped, {len(excluded)} excluded at birth\n")
    for r in out:
        print(f"  {r['row']}  [{r['structural_expectation'] or 'no declared structure'}]  "
              f"{r['family']} / {r['ramp_instantiated_as']}")
        for s in r["steps"]:
            if s["state"] != "usable":
                print(f"      x={s['ramp_value']:<5} {s['state']}")
                continue
            d = s["dials"]
            ex2 = {k: round(v["blend_excess"], 3) for k, v in d["flavours"].items()
                   if v["blend_excess"] is not None}
            print(f"      x={s['ramp_value']:<5}{s['region']:<9}r={d['r_mean']:<8}"
                  f"ov={str(d['overlap_mean']):<7}BC={str(d['bimodality_coefficient']):<7}{ex2}")
        print()
    print(f"wrote {OUT.name}  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
