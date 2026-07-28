#!/usr/bin/env python3
"""Observatory fan-out, BATCH 10 — optimization-weighted, by ruling.

prereg_v34 was voided for clearing power against clusters its statistic could never read. Its successor
needs 10 reserved optimization clusters; the frontier holds 3. So optimization rows are ordinary build
priority until that clears, and this batch is every vetted, unbuilt, unreserved, not-capture-blocked
optimization row in the atlas — six of them.

  steiner-forest                     edge subsets connecting each terminal pair   UPWARD-closed
  survivable-network-design          edge subsets meeting connectivity demands    UPWARD-closed
  prize-collecting-steiner-tree      acyclic edge subsets, penalties on the rest  DOWNWARD-closed
  maximum-feasible-linear-subsystem  jointly-satisfiable subsets of relations     DOWNWARD-closed

The `optimization` family ramp — constraint-to-ground-set ratio — is already the Q21-corrected form for
these rows: terminals, pairs or requirements per candidate edge is a within-instance parameter at a
fixed ground set. The declaration happened to be right, so no erratum was needed here.
"""
import hashlib, json, random, sys
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "dev"))
LAT = ROOT / "foundry" / "results" / "lattice"
OUT = LAT / "observatory_batch10_panels.json"
LEDGER = LAT / "observatory_reservation.jsonl"
TRAIL = LAT / "maptrail.jsonl"
from foundry.catalog import capture as C                                        # noqa: E402
from foundry.catalog import maptrail as M                                       # noqa: E402
from foundry.catalog import reservation as RES                                  # noqa: E402
import n2_dense_control as N2                                                   # noqa: E402
from sounding_v1 import BOOL_OPS                                                # noqa: E402

SEED = 20260727
BATCH = 10
OPT = (0.5, 1.0, 1.5, 2.0, 3.0)
M_CAND = 11                # the candidate ground set — FIXED, declared, never ramped
NV = 7


def cand_edges(rng, n, m=M_CAND):
    allp = list(combinations(range(n), 2))
    rng.shuffle(allp)
    return [allp[i % len(allp)] for i in range(m)]


def _reach(n, edges, src):
    adj = {i: set() for i in range(n)}
    for u, v in edges:
        adj[u].add(v); adj[v].add(u)
    st, vis = [src], set()
    while st:
        x = st.pop()
        if x in vis:
            continue
        vis.add(x); st.extend(adj[x] - vis)
    return vis


def steiner_forest(rng, ratio, n=NV):
    """Edge subsets connecting every terminal PAIR. Upward-closed: adding edges cannot disconnect."""
    cand = cand_edges(rng, n)
    npairs = max(1, min(4, round(ratio * 2)))
    pairs = []
    for _ in range(npairs):
        a, b = rng.sample(range(n), 2)
        pairs.append((a, b))
    def ok(s):
        E = [cand[i] for i in range(M_CAND) if s[i]]
        return all(b in _reach(n, E, a) for a, b in pairs)
    f = [s for s in product((0, 1), repeat=M_CAND) if ok(s)]
    if len(f) < 2:
        return []
    b0 = min(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b0])]


def survivable_network_design(rng, ratio, n=NV):
    """Edge subsets meeting per-pair connectivity requirements (edge-disjoint path counts).
    Upward-closed. The dial is the requirement level at a fixed candidate set."""
    cand = cand_edges(rng, n)
    req = max(1, min(2, round(0.5 + ratio * 0.6)))
    a, b = rng.sample(range(n), 2)
    def edge_conn_at_least(E, s0, t0, k):
        """k edge-disjoint s-t paths exist iff every edge cut has size >= k. n is tiny; enumerate cuts."""
        for r in range(1, n):
            for side in combinations(range(n), r):
                S = set(side)
                if (s0 in S) == (t0 in S):
                    continue
                cut = sum(1 for u, v in E if (u in S) != (v in S))
                if cut < k:
                    return False
        return True
    f = [s for s in product((0, 1), repeat=M_CAND)
         if edge_conn_at_least([cand[i] for i in range(M_CAND) if s[i]], a, b, req)]
    if len(f) < 2:
        return []
    b0 = min(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b0])]


def prize_collecting_steiner_tree(rng, ratio, n=NV):
    """ACYCLIC edge subsets — forests — over a fixed candidate set. Downward-closed: a subset of a
    forest is a forest. Penalties for unreached terminals score the OPTIMAL region, not feasibility."""
    cand = cand_edges(rng, n)
    pen = max(1, round(ratio * 3))
    terms = sorted(rng.sample(range(n), max(2, min(4, round(2 + ratio)))))
    def acyclic(E):
        parent = list(range(n))
        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]; x = parent[x]
            return x
        for u, v in E:
            ru, rv = find(u), find(v)
            if ru == rv:
                return False
            parent[ru] = rv
        return True
    f = [s for s in product((0, 1), repeat=M_CAND)
         if acyclic([cand[i] for i in range(M_CAND) if s[i]])]
    if len(f) < 2:
        return []
    def cost(s):
        E = [cand[i] for i in range(M_CAND) if s[i]]
        got = _reach(n, E, terms[0]) if E else {terms[0]}
        return sum(s) + pen * sum(1 for t in terms if t not in got)
    b0 = min(cost(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if cost(s) == b0])]


def maximum_feasible_linear_subsystem(rng, ratio, nvar=None):
    """Subsets of linear relations over GF(2) that are JOINTLY SATISFIABLE. Downward-closed: a subset
    of a satisfiable system is satisfiable.

    The dial is RELATIONS PER VARIABLE, so it must move the VARIABLE COUNT — the relation count is the
    ground set and is fixed at M_CAND. A first version left nvar fixed, which made the declared dial
    reach nothing: the feasible region read 763 at every step. Fewer variables means more relations
    competing for the same solution space, hence a smaller satisfiable subfamily."""
    m = M_CAND
    nvar = max(2, min(6, round(m / (2.0 * ratio)))) if nvar is None else nvar
    rows = [[rng.randint(0, 1) for _ in range(nvar)] for _ in range(m)]
    rhs = [rng.randint(0, 1) for _ in range(m)]
    assigns = list(product((0, 1), repeat=nvar))
    def sat(idx):
        for x in assigns:
            if all(sum(rows[i][j] * x[j] for j in range(nvar)) % 2 == rhs[i] for i in idx):
                return True
        return False
    f = [s for s in product((0, 1), repeat=m)
         if sat([i for i in range(m) if s[i]])]
    if len(f) < 2:
        return []
    b0 = max(sum(s) for s in f)
    return [("feasible", f), ("optimal", [s for s in f if sum(s) == b0])]


ROWS = {
    "steiner-forest":                    (steiner_forest, "upward_closed", "optimization", OPT,
                                          "terminal pairs per candidate edge"),
    "survivable-network-design":         (survivable_network_design, "upward_closed", "optimization",
                                          OPT, "connectivity requirement per candidate edge"),
    "prize-collecting-steiner-tree":     (prize_collecting_steiner_tree, "downward_closed",
                                          "optimization", OPT, "penalty level per candidate edge"),
    "maximum-feasible-linear-subsystem": (maximum_feasible_linear_subsystem, "downward_closed",
                                          "optimization", OPT, "relations per variable"),
}


def main() -> int:
    cen = json.loads((LAT / "observatory_batch10_census.json").read_text())
    reserved = RES.reserved_rows(LEDGER)
    RES.assert_no_reserved_generators(globals(), LEDGER)
    RES.assert_no_duplicate_regions({k: v[0] for k, v in ROWS.items()}, 1.5, LEDGER,
                                    lambda: random.Random(SEED))
    leak = sorted(set(ROWS) & reserved)
    if leak:
        raise RuntimeError(f"FRONTIER LEAK — batch 10 defines generators for reserved row(s) {leak}")
    missing = sorted(set(cen["published"]) - set(ROWS))
    if missing:
        raise RuntimeError(f"census published {missing} with no generator")
    print(f"guards green: {len(reserved)} withheld, no generator for any, no duplicate regions\n")

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

    doc = {"schema": "observatory-batch10/v1",
           "STATUS": "EXPLORATORY dial panels — no verdict, no scored prediction, no seal",
           "batch": BATCH, "reach_class": "REACH-subset",
           "families": {f: cen["families"][f]["census_ramp"] for f in
                        sorted({v[2] for v in ROWS.values()})},
           "why_these_rows": cen["why_this_batch"],
           "optimization_weighted": ("by ruling — prereg_v34's successor needs 10 reserved optimization "
                                     "clusters and the frontier holds 3"),
           "frontier_reservation": {"reserved_this_batch": sorted(cen["reservation"]["reserved"]),
                                    "roster_sha256": cen["reservation"]["roster_sha256"]},
           "pipeline": "foundry.catalog.capture — one implementation for every batch",
           "excluded_at_birth": excluded, "rows": out}
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    M.emit(TRAIL, "expansion", key=f"expansion:batch{BATCH}",
           artifact=OUT.name, sha256=hashlib.sha256(OUT.read_bytes()).hexdigest(),
           rows_added=[r["row"] for r in out], n_rows=len(out),
           n_reserved=len(cen["reservation"]["reserved"]),
           admission_authority="optimization-weighted roster; vetted under the vet-before-hash amendment")
    for e in excluded:
        M.emit(TRAIL, "exclusion", key=f"exclusion:batch{BATCH}:{e['row']}",
               problem=e["row"], batch=BATCH, reasons=e["reason"], authority="conformance at birth")

    print(f"\nBATCH 10 — {len(out)} rows shipped, {len(excluded)} excluded\n")
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
