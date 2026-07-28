#!/usr/bin/env python3
"""Observatory fan-out, BATCH 9 — the Q21-corrected dial, applied across a whole batch.

Every edge-subset row here runs on a WITHIN-INSTANCE parameter at a fixed ground set. Edge density
cannot be the dial when the ground set IS the edge set — that was the confound the ambient census
found, and the census erratum prescribed exactly this form. So the candidate-edge list is held at a
declared size and the dial moves something inside the instance: terminal count, component target, or
the vertex count the candidate edges are drawn over.

  steiner-tree              edge subsets connecting all terminals      UPWARD-closed
  node-multiway-cut         VERTEX subsets separating the terminals    UPWARD-closed
  target-set-selection      seed sets that activate the whole graph    UPWARD-closed
  graph-motif               vertex subsets realising a colour multiset neither
  maximum-induced-matching  edge subsets inducing no further edges     DOWNWARD-closed
  planar-matching-count     matchings over a planar candidate set      DOWNWARD-closed

The last two are the first rows the program has ever built where a COUNTING charge meets a measured
region — the decide-versus-count comparison the census banked becomes physically possible here.
"""
import hashlib, json, random, sys
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "dev"))
LAT = ROOT / "foundry" / "results" / "lattice"
OUT = LAT / "observatory_batch9_panels.json"
LEDGER = LAT / "observatory_reservation.jsonl"
TRAIL = LAT / "maptrail.jsonl"
from foundry.catalog import capture as C                                        # noqa: E402
from foundry.catalog import maptrail as M                                       # noqa: E402
from foundry.catalog import reservation as RES                                  # noqa: E402
import n2_dense_control as N2                                                   # noqa: E402
from sounding_v1 import BOOL_OPS                                                # noqa: E402

SEED = 20260727
BATCH = 9
GRAPH = (0.2, 0.35, 0.5, 0.65, 0.8)
M_CAND = 11                # the candidate-edge ground set — FIXED, declared, never ramped
NV = 7                     # vertex ground set for the vertex-subset rows — likewise fixed


def cand_edges(rng, n, m=M_CAND):
    """A fixed-size candidate edge list. Same width at every ramp value, by construction."""
    allp = list(combinations(range(n), 2))
    rng.shuffle(allp)
    return [allp[i % len(allp)] for i in range(m)]


def _components(n, edges, removed=frozenset()):
    adj = {i: set() for i in range(n)}
    for k, (u, v) in enumerate(edges):
        if k not in removed:
            adj[u].add(v); adj[v].add(u)
    seen, comps = set(), []
    for s0 in range(n):
        if s0 in seen:
            continue
        cur, st = set(), [s0]
        while st:
            x = st.pop()
            if x in cur:
                continue
            cur.add(x); seen.add(x); st.extend(adj[x] - cur)
        comps.append(cur)
    return comps


def steiner_tree(rng, frac, n=NV):
    """Edge subsets connecting every terminal. Upward-closed: adding edges cannot disconnect."""
    cand = cand_edges(rng, n)
    t = max(2, min(n, round(2 + frac * (n - 2))))
    terms = sorted(rng.sample(range(n), t))
    def ok(s):
        comps = _components(n, [cand[i] for i in range(M_CAND) if s[i]])
        return any(set(terms) <= c for c in comps)
    f = [s for s in product((0, 1), repeat=M_CAND) if ok(s)]
    if len(f) < 2:
        return []
    b = min(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b])]


def node_multiway_cut(rng, frac, n=9):
    """VERTEX subsets whose removal pairwise separates the terminals. Ground set is V, fixed at n."""
    cand = cand_edges(rng, n)
    # TERMINALS MUST BE PAIRWISE NON-ADJACENT. Two terminals joined by an edge cannot be separated by
    # removing NON-terminal vertices at all, so a random draw makes the region empty by definition
    # rather than by the dial — a generator bug, not a hard instance.
    t = max(2, min(4, round(2 + frac * 2)))
    adj0 = {i: set() for i in range(n)}
    for u, v in cand:
        adj0[u].add(v); adj0[v].add(u)
    terms = []
    for v in rng.sample(range(n), n):
        if len(terms) >= t:
            break
        if all(v not in adj0[w] for w in terms):
            terms.append(v)
    if len(terms) < 2:
        return []
    terms = sorted(terms)
    def ok(s):
        S = {i for i in range(n) if s[i]}
        if S & set(terms):
            return False
        adj = {i: set() for i in range(n)}
        for u, v in cand:
            if u not in S and v not in S:
                adj[u].add(v); adj[v].add(u)
        for a, b2 in combinations(terms, 2):
            st, vis = [a], set()
            while st:
                x = st.pop()
                if x in vis:
                    continue
                vis.add(x); st.extend(adj[x] - vis)
            if b2 in vis:
                return False
        return True
    f = [s for s in product((0, 1), repeat=n) if ok(s)]
    if len(f) < 2:
        return []
    b = min(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b])]


def target_set_selection(rng, frac, n=NV):
    """Seed sets that activate every vertex under per-vertex thresholds. Upward-closed."""
    cand = cand_edges(rng, n)
    adj = {i: set() for i in range(n)}
    for u, v in cand:
        adj[u].add(v); adj[v].add(u)
    thr = {v: max(1, round(frac * max(1, len(adj[v])))) for v in range(n)}
    def activates(s):
        act = {i for i in range(n) if s[i]}
        changed = True
        while changed:
            changed = False
            for v in range(n):
                if v not in act and len(adj[v] & act) >= thr[v]:
                    act.add(v); changed = True
        return len(act) == n
    f = [s for s in product((0, 1), repeat=n) if activates(s)]
    if len(f) < 2:
        return []
    b = min(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b])]


def graph_motif(rng, frac, n=10):
    """Vertex subsets that are CONNECTED and realise a colour multiset. Neither closure direction."""
    cand = cand_edges(rng, n)
    adj = {i: set() for i in range(n)}
    for u, v in cand:
        adj[u].add(v); adj[v].add(u)
    ncol = 2                                    # few colours -> many subsets share a multiset
    col = [rng.randrange(ncol) for _ in range(n)]
    k = max(2, min(n - 2, round(2 + frac * 4)))
    motif = sorted(col[i] for i in rng.sample(range(n), k))
    def ok(s):
        S = [i for i in range(n) if s[i]]
        if sorted(col[i] for i in S) != motif:
            return False
        st, vis = [S[0]], set()
        while st:
            x = st.pop()
            if x in vis:
                continue
            vis.add(x); st.extend((adj[x] & set(S)) - vis)
        return vis == set(S)
    f = [s for s in product((0, 1), repeat=n) if any(s) and ok(s)]
    if len(f) < 2:
        return []
    return [("feasible", f)]


def maximum_induced_matching(rng, frac, n=NV):
    """Edge subsets that are a matching AND induce no further candidate edge. Downward-closed.
    The dial is VERTICES PER CANDIDATE EDGE: more vertices spread the incidences and loosen the
    induced constraint, with the ground set held at M_CAND throughout."""
    nv = max(4, round(4 + frac * 8))
    cand = cand_edges(rng, nv)
    def ok(s):
        idx = [i for i in range(M_CAND) if s[i]]
        vs = [set(cand[i]) for i in idx]
        if any(a & b for a, b in combinations(vs, 2)):
            return False
        chosen = set().union(*vs) if vs else set()
        for j in range(M_CAND):
            if j in idx:
                continue
            u, v = cand[j]
            if u in chosen and v in chosen:
                return False
        return True
    f = [s for s in product((0, 1), repeat=M_CAND) if ok(s)]
    if len(f) < 2:
        return []
    b = max(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b])]


def planar_matching_count(rng, frac, n=NV):
    """Matchings over a PLANAR candidate set (a grid subgraph — planar by construction, since every
    subgraph of a planar graph is planar). Downward-closed. Dial: vertices per candidate edge."""
    rows, cols = 3, max(2, round(2 + frac * 3))
    grid = []
    for r in range(rows):
        for c in range(cols):
            v = r * cols + c
            if c + 1 < cols:
                grid.append((v, r * cols + c + 1))
            if r + 1 < rows:
                grid.append((v, (r + 1) * cols + c))
    if len(grid) < 2:
        return []
    cand = [grid[i % len(grid)] for i in range(M_CAND)]
    def ok(s):
        vs = [set(cand[i]) for i in range(M_CAND) if s[i]]
        return not any(a & b for a, b in combinations(vs, 2))
    f = [s for s in product((0, 1), repeat=M_CAND) if ok(s)]
    if len(f) < 2:
        return []
    b = max(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b])]


ROWS = {
    "steiner-tree":             (steiner_tree, "upward_closed", "graph", GRAPH,
                                 "terminal count at fixed candidate-edge set"),
    "node-multiway-cut":        (node_multiway_cut, "upward_closed", "graph", GRAPH,
                                 "terminal count at fixed vertex set"),
    "target-set-selection":     (target_set_selection, "upward_closed", "graph", GRAPH,
                                 "activation threshold at fixed vertex set"),
    "graph-motif":              (graph_motif, None, "graph", GRAPH,
                                 "motif size at fixed vertex set"),
    "maximum-induced-matching": (maximum_induced_matching, "downward_closed", "graph", GRAPH,
                                 "vertices per candidate edge"),
    "planar-matching-count":    (planar_matching_count, "downward_closed", "graph", GRAPH,
                                 "vertices per candidate edge"),
}


def main() -> int:
    cen = json.loads((LAT / "observatory_batch9_census.json").read_text())
    reserved = RES.reserved_rows(LEDGER)
    RES.assert_no_reserved_generators(globals(), LEDGER)
    RES.assert_no_duplicate_regions({k: v[0] for k, v in ROWS.items()}, 0.5, LEDGER,
                                    lambda: random.Random(SEED))
    leak = sorted(set(ROWS) & reserved)
    if leak:
        raise RuntimeError(f"FRONTIER LEAK — batch 9 defines generators for reserved row(s) {leak}")
    missing = sorted(set(cen["published"]) - set(ROWS))
    if missing:
        raise RuntimeError(f"census published {missing} with no generator")
    print(f"guards green: {len(reserved)} row(s) withheld, no generator for any of them, "
          f"no two generators computing the same region\n")

    out, excluded = [], []
    ctrl = lambda region, rng: N2.cp_control(region, rng)[0]
    for row, (build, expect, fam, ramp, inst) in ROWS.items():
        print(f"  capturing {row} ...", flush=True)
        rec, ex = C.capture_row(row, build, expect, ramp, BOOL_OPS, SEED, ctrl)
        if ex:
            excluded.append(ex)
            print(f"    EXCLUDED at birth: {row} — {ex['reason'][0][:88]}", flush=True)
        else:
            rec["family"] = fam
            rec["ramp_parameter"] = cen["families"][fam]["census_ramp"]
            rec["ramp_instantiated_as"] = inst
            out.append(rec)

    doc = {"schema": "observatory-batch9/v1",
           "STATUS": "EXPLORATORY dial panels — no verdict, no scored prediction, no seal",
           "batch": BATCH, "reach_class": "REACH-subset",
           "families": {f: cen["families"][f]["census_ramp"] for f in
                        sorted({v[2] for v in ROWS.values()})},
           "why_these_rows": cen["why_this_batch"],
           "q21_corrected_dial": ("every edge-subset row runs on a WITHIN-INSTANCE parameter at a fixed "
                                  f"ground set of {M_CAND} candidate edges. Edge density cannot be the "
                                  "dial when the ground set IS the edge set."),
           "counting_rows_first_build": ("planar-matching-count is the first row the program has built "
                                         "where a COUNTING charge meets a measured region — the "
                                         "decide-versus-count comparison becomes physically possible"),
           "frontier_reservation": {"reserved_this_batch": sorted(cen["reservation"]["reserved"]),
                                    "roster_sha256": cen["reservation"]["roster_sha256"]},
           "pipeline": "foundry.catalog.capture — one implementation for every batch",
           "excluded_at_birth": excluded, "rows": out}
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    M.emit(TRAIL, "expansion", key=f"expansion:batch{BATCH}",
           artifact=OUT.name, sha256=hashlib.sha256(OUT.read_bytes()).hexdigest(),
           rows_added=[r["row"] for r in out], n_rows=len(out),
           n_reserved=len(cen["reservation"]["reserved"]),
           admission_authority="roster from the 59-row adjudication, qualified under the "
                               "vet-before-hash amendment")
    for e in excluded:
        M.emit(TRAIL, "exclusion", key=f"exclusion:batch{BATCH}:{e['row']}",
               problem=e["row"], batch=BATCH, reasons=e["reason"], authority="conformance at birth")

    print(f"\nBATCH 9 — {len(out)} rows shipped, {len(excluded)} excluded\n")
    for r in out:
        print(f"  {r['row']}  [{r['structural_expectation'] or '—'}]  {r['ramp_instantiated_as']}")
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
