#!/usr/bin/env python3
"""Observatory fan-out, BATCH 8 — the first roster from a queue whose regions were all read.

Every row here is SUBSET-VERIFIED by the region-formulation audit, not merely lexicon-matched. Most are
edge- or arc-subset rows, which is the Q21 shape — the ground set is what edge density ramps. So each
generator draws a FIXED CANDIDATE LIST of declared size and ramps the density of the base graph within
it. The ambient is then constant across the ramp by construction, and the scoping is stated per row.
"""
import hashlib, json, sys
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "dev"))
LAT = ROOT / "foundry" / "results" / "lattice"
OUT = LAT / "observatory_batch8_panels.json"
LEDGER = LAT / "observatory_reservation.jsonl"
TRAIL = LAT / "maptrail.jsonl"
from foundry.catalog import capture as C                                        # noqa: E402
from foundry.catalog import maptrail as M                                       # noqa: E402
from foundry.catalog import reservation as RES                                  # noqa: E402
import n2_dense_control as N2                                                   # noqa: E402
from sounding_v1 import BOOL_OPS                                                # noqa: E402

SEED = 20260727
BATCH = 8
GRAPH = (0.15, 0.25, 0.35, 0.45, 0.60)
OPT = (0.5, 1.0, 1.5, 2.0, 3.0)
NV = 6
M_CAND = 11                       # the FIXED candidate-list size — the ground set, declared


def _cands(n, rng):
    """A fixed-size candidate list of vertex pairs. Same width at every ramp value, by construction."""
    allp = list(combinations(range(n), 2))
    return [allp[i % len(allp)] for i in range(M_CAND)]


def _chordal(n, edges):
    adj = {i: set() for i in range(n)}
    for u, v in edges:
        adj[u].add(v); adj[v].add(u)
    rem, order = set(range(n)), []
    while rem:                                     # perfect elimination ordering, greedy
        pick = None
        for v in sorted(rem):
            nb = adj[v] & rem
            if all(b in adj[a] for a, b in combinations(sorted(nb), 2)):
                pick = v; break
        if pick is None:
            return False
        order.append(pick); rem.discard(pick)
    return True


def _interval(n, edges):
    """Interval graphs are chordal and AT-free; chordality alone is a necessary condition and is used
    here as the declared surrogate — stated, not hidden, because it makes the row a SUPERSET test."""
    return _chordal(n, edges)


def _base(rng, p, n=NV):
    return {e for e in combinations(range(n), 2) if rng.random() < p}


def minimum_fill_in(rng, p, n=NV):
    """Candidate pairs ADDED to make the base chordal. Upward-closed: adding more edges to a chordal
    completion keeps it chordal only if... it does not in general — so the declared expectation is
    checked at birth rather than assumed."""
    base, cand = _base(rng, p, n), _cands(n, rng)
    f = [s for s in product((0, 1), repeat=M_CAND)
         if _chordal(n, base | {cand[i] for i in range(M_CAND) if s[i]})]
    if len(f) < 2:
        return []
    b = min(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b])]


def interval_completion(rng, p, n=NV):
    base, cand = _base(rng, p, n), _cands(n, rng)
    f = [s for s in product((0, 1), repeat=M_CAND)
         if _interval(n, base | {cand[i] for i in range(M_CAND) if s[i]})]
    if len(f) < 2:
        return []
    b = min(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b])]


def graph_sandwich_pi_property(rng, p, n=NV):
    """Subsets of a fixed candidate list, added to F, such that the result is P4-free (cograph)."""
    base, cand = _base(rng, p * 0.6, n), _cands(n, rng)

    def p4_free(edges):
        adj = {i: set() for i in range(n)}
        for u, v in edges:
            adj[u].add(v); adj[v].add(u)
        for q in combinations(range(n), 4):
            for perm in ((0, 1, 2, 3), (0, 2, 1, 3), (0, 1, 3, 2), (1, 0, 2, 3),
                         (1, 0, 3, 2), (2, 0, 1, 3)):
                a, b, c, d = (q[i] for i in perm)
                if (b in adj[a] and c in adj[b] and d in adj[c]
                        and c not in adj[a] and d not in adj[a] and d not in adj[b]):
                    return False
        return True
    f = [s for s in product((0, 1), repeat=M_CAND)
         if p4_free(base | {cand[i] for i in range(M_CAND) if s[i]})]
    if len(f) < 2:
        return []
    b = max(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b])]


def minimum_equivalent_digraph(rng, p, n=NV):
    """Arc subsets of a FIXED candidate list preserving the base's reachability. Ground set fixed."""
    allarcs = [(i, j) for i in range(n) for j in range(n) if i != j]
    cand = [allarcs[i % len(allarcs)] for i in range(M_CAND)]
    base = [a for a in cand if rng.random() < max(p, 0.3)]
    if len(base) < 2:
        return []

    def reach(arcs):
        out = {i: [] for i in range(n)}
        for u, v in arcs:
            out[u].append(v)
        seen = set()
        for s0 in range(n):
            st, vis = [s0], set()
            while st:
                x = st.pop()
                if x in vis:
                    continue
                vis.add(x); st.extend(out[x])
            seen |= {(s0, t) for t in vis}
        return seen
    target = reach(base)
    f = [s for s in product((0, 1), repeat=M_CAND)
         if reach([cand[i] for i in range(M_CAND) if s[i]]) >= target]
    if len(f) < 2:
        return []
    b = min(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b])]


def bilevel_knapsack(rng, ratio, n=11):
    """The LEADER's item subset. Expensive, not mis-typed: the predicate solves the follower's optimum
    inside — which the audit recorded as an affordability note rather than a typing verdict."""
    w = [rng.randint(1, 9) for _ in range(n)]
    lead_cap = sum(w) / (1.0 + ratio)
    f = [s for s in product((0, 1), repeat=n)
         if sum(w[i] for i in range(n) if s[i]) <= lead_cap]
    if len(f) < 2:
        return []
    prof = [rng.randint(1, 9) for _ in range(n)]
    def follower(s):                       # the inner optimum, solved per candidate
        rem = [i for i in range(n) if not s[i]]
        cap = lead_cap * 0.5
        best, tot = 0, 0
        for i in sorted(rem, key=lambda j: -prof[j] / w[j]):
            if tot + w[i] <= cap:
                tot += w[i]; best += prof[i]
        return best
    b = min(follower(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if follower(s) == b])]


def network_interdiction(rng, ratio, n=NV):
    """Interdiction sets over a FIXED candidate-edge list that cut the source from the sink."""
    allp = list(combinations(range(n), 2))
    cand = [allp[i % len(allp)] for i in range(M_CAND)]
    def connected(removed):
        adj = {i: set() for i in range(n)}
        for k, (u, v) in enumerate(cand):
            if k not in removed:
                adj[u].add(v); adj[v].add(u)
        st, vis = [0], set()
        while st:
            x = st.pop()
            if x in vis:
                continue
            vis.add(x); st.extend(adj[x] - vis)
        return (n - 1) in vis
    f = [s for s in product((0, 1), repeat=M_CAND)
         if not connected({i for i in range(M_CAND) if s[i]})]
    if len(f) < 2:
        return []
    b = min(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b])]


ROWS = {
    "interval-completion":        (interval_completion, "upward_closed", "graph", GRAPH,
                                   "edge density over a fixed candidate-pair list"),
    "minimum-equivalent-digraph": (minimum_equivalent_digraph, None, "graph", GRAPH,
                                   "arc density over a fixed candidate-arc list"),
    "graph-sandwich-pi-property": (graph_sandwich_pi_property, None, "graph", GRAPH,
                                   "edge density over a fixed candidate-pair list"),
    "bilevel-knapsack":           (bilevel_knapsack, "downward_closed", "optimization", OPT,
                                   "capacity tightness per item"),
    "network-interdiction":       (network_interdiction, "upward_closed", "optimization", OPT,
                                   "interdiction budget per candidate"),
}


def main() -> int:
    cen = json.loads((LAT / "observatory_batch8_census.json").read_text())
    reserved = RES.reserved_rows(LEDGER)
    leak = sorted(set(ROWS) & reserved)
    if leak:
        raise RuntimeError(f"FRONTIER LEAK — batch 8 defines generators for reserved row(s) {leak}")
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
            print(f"    EXCLUDED at birth: {row} — {ex['reason'][0][:90]}", flush=True)
        else:
            rec["family"] = fam
            rec["ramp_parameter"] = cen["families"][fam]["census_ramp"]
            rec["ramp_instantiated_as"] = inst
            out.append(rec)

    doc = {"schema": "observatory-batch8/v1",
           "STATUS": "EXPLORATORY dial panels — no verdict, no scored prediction, no seal",
           "batch": BATCH, "reach_class": "REACH-subset",
           "families": {f: cen["families"][f]["census_ramp"] for f in
                        sorted({v[2] for v in ROWS.values()})},
           "why_these_rows": cen["why_this_batch"],
           "region_formulation_read": ("every row SUBSET-VERIFIED by the region-formulation audit, not "
                                       "merely lexicon-matched"),
           "fixed_candidate_lists": ("edge- and arc-subset rows draw a candidate list of declared size "
                                     f"({M_CAND}) so the ambient is constant across the ramp by "
                                     "construction. This SCOPES the instance family, stated here."),
           "declared_surrogate": ("interval-completion tests CHORDALITY, a necessary condition for "
                                  "interval graphs rather than a sufficient one — so the row is a "
                                  "superset test. Stated, not hidden."),
           "frontier_reservation": {"reserved_this_batch": sorted(cen["reservation"]["reserved"]),
                                    "roster_sha256": cen["reservation"]["roster_sha256"]},
           "pipeline": "foundry.catalog.capture — one implementation for every batch",
           "excluded_at_birth": excluded, "rows": out}
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    M.emit(TRAIL, "expansion", key=f"expansion:batch{BATCH}",
           artifact=OUT.name, sha256=hashlib.sha256(OUT.read_bytes()).hexdigest(),
           rows_added=[r["row"] for r in out], n_rows=len(out),
           n_reserved=len(cen["reservation"]["reserved"]),
           admission_authority="roster drawn from region-formulation-audited rows")
    for e in excluded:
        M.emit(TRAIL, "exclusion", key=f"exclusion:batch{BATCH}:{e['row']}",
               problem=e["row"], batch=BATCH, reasons=e["reason"], authority="conformance at birth")

    print(f"\nBATCH 8 — {len(out)} rows shipped, {len(excluded)} excluded\n")
    for r in out:
        print(f"  {r['row']}  [{r['structural_expectation'] or '—'}]")
        for s in r["steps"]:
            if s["state"] != "usable":
                print(f"      x={s['ramp_value']:<5} {s['state']}"); continue
            d = s["dials"]
            ex2 = {k: round(v["blend_excess"], 3) for k, v in d["flavours"].items()
                   if v["blend_excess"] is not None}
            print(f"      x={str(s['ramp_value']):<5}{s['region']:<9}r={d['r_mean']:<8}{ex2}")
        print()
    print(f"wrote {OUT.name}  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
