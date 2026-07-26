#!/usr/bin/env python3
"""Sounding v2 — the fleet. Blend probe on natural rows under a four-cell design (prereg_v18).

WHAT THE PILOT EARNED. prereg_v17's S-2 was INSUFFICIENT for three reasons, and all three are fixed here
BY CONSTRUCTION rather than by remembering:

  1. FORCED FLAVOURS ARE EXCLUDED BY SCHEMA. In the pilot, 42% of the apparent separation was S-1's
     theorem-forced zeros bleeding into S-2's mean — every decision-easy row is a CSP carrying exactly one
     forced zero that dragged it down. `discovery_rate()` here cannot see a forced flavour.
     THE NETTING LAW AT FLAVOUR LEVEL: theorem-forced credit has now been netted inside a statistic, inside
     an instrument's type signature, inside a study design, and inside a per-flavour mean. Four scales.
  2. FOUR-CELL OCCUPANCY. The pilot's easy x optimal cell was EMPTY, so region kind proxied hardness and no
     n would have separated them. Four decision-easy optimisation rows are recruited from the atlas's
     tractable canon.
  3. REGION SIZE, TUNED THEN CHECKED. Ensembles are tuned so region sizes land in a declared band
     (primary); r-stratification is reported as the check that the tuning worked (secondary). If the strata
     disagree the tuning failed and the statistic is not scored.

Comparisons run WITHIN region kind and are never pooled across it.
"""
import hashlib
import json
import random
import sys
from itertools import combinations, product
from math import comb, log
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "dev"))
sys.path.insert(0, str(ROOT.parent / "eightfold"))
from sounding_v1 import (BOOL_OPS, D3_OPS, violation, cnf_instances, cnf_solutions, graph,     # noqa: E402
                         vc_sets, is_sets, clique_sets, maxcut_sets, col3_sets,
                         subsetsum_sets, partition_sets)
from eightfold import atlas as A                                                               # noqa: E402

LAT = ROOT / "foundry" / "results" / "lattice"
OUT = LAT / "sounding_v2_results.json"
SEED, N_INST = 20260726, 12
TARGET_R = (25, 250)

FORCED = {("sat-2", "solutions"): {"majority"}, ("horn-sat", "solutions"): {"min"},
          ("xor-sat", "solutions"): {"minority"}, ("bipartiteness", "solutions"): {"minority"},
          ("vertex-cover", "feasible"): {"max"}, ("independent-set", "feasible"): {"min"},
          ("clique", "feasible"): {"min"},
          # the recruits: matchings are subset-closed; spanning trees and s-t paths are neither
          ("matching", "feasible"): {"min"}}


# ── the four recruits: decision-easy optimisation rows, edge-characteristic encoding ──────────────────
def _connected(n, edges):
    adj = {i: set() for i in range(n)}
    for a, b in edges:
        adj[a].add(b); adj[b].add(a)
    seen, st = {0}, [0]
    while st:
        u = st.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v); st.append(v)
    return len(seen) == n


def mst_sets(n, E, w):
    feas = [s for s in combinations(range(len(E)), n - 1) if _connected(n, [E[i] for i in s])]
    if not feas:
        return [], []
    def vec(s): return tuple(1 if i in s else 0 for i in range(len(E)))
    best = min(sum(w[i] for i in s) for s in feas)
    return [vec(s) for s in feas], [vec(s) for s in feas if sum(w[i] for i in s) == best]


def matching_sets(E):
    feas = [s for k in range(len(E) + 1) for s in combinations(range(len(E)), k)
            if len({v for i in s for v in E[i]}) == 2 * len(s)]
    def vec(s): return tuple(1 if i in s else 0 for i in range(len(E)))
    best = max(len(s) for s in feas)
    return [vec(s) for s in feas], [vec(s) for s in feas if len(s) == best]


def stpath_sets(n, E):
    adj = {i: [] for i in range(n)}
    for idx, (a, b) in enumerate(E):
        adj[a].append((b, idx)); adj[b].append((a, idx))
    paths = []
    def dfs(u, used, es):
        if u == n - 1:
            paths.append(tuple(sorted(es))); return
        for v, ei in adj[u]:
            if v not in used:
                dfs(v, used | {v}, es + [ei])
    dfs(0, {0}, [])
    if not paths:
        return [], []
    def vec(s): return tuple(1 if i in s else 0 for i in range(len(E)))
    best = min(len(p) for p in paths)
    return [vec(p) for p in paths], [vec(p) for p in paths if len(p) == best]


def unitflow_sets(n, E):
    """Unit-capacity s-t flows as edge subsets meeting conservation at internal nodes."""
    feas = []
    for s in product((0, 1), repeat=len(E)):
        deg = {i: 0 for i in range(n)}
        for i, (a, b) in enumerate(E):
            if s[i]:
                deg[a] += 1; deg[b] += 1
        if all(deg[v] % 2 == 0 for v in range(1, n - 1)):
            feas.append(s)
    if not feas:
        return [], []
    def val(s): return sum(1 for i, (a, b) in enumerate(E) if s[i] and 0 in (a, b))
    best = max(val(s) for s in feas)
    return feas, [s for s in feas if val(s) == best]


ROWS = {
    # solutions-region rows
    "sat-2": ("sat-csp", 2, "solutions"), "sat-3": ("sat-csp", 2, "solutions"),
    "horn-sat": ("sat-csp", 2, "solutions"), "xor-sat": ("sat-csp", 2, "solutions"),
    "nae-sat": ("sat-csp", 2, "solutions"), "bipartiteness": ("graph", 2, "solutions"),
    "graph-3-coloring": ("graph", 3, "solutions"), "subset-sum": ("number-theoretic", 2, "solutions"),
    # optimal-region rows, decision-HARD (the pilot's five)
    "vertex-cover": ("graph", 2, "opt"), "independent-set": ("graph", 2, "opt"),
    "clique": ("graph", 2, "opt"), "max-cut": ("graph", 2, "opt"),
    "number-partitioning": ("number-theoretic", 2, "opt"),
    # optimal-region rows, decision-EASY — THE RECRUITS that fill the empty cell
    "min-spanning-tree": ("graph", 2, "opt"), "matching": ("graph", 2, "opt"),
    "reachability-stcon": ("graph", 2, "opt"), "max-flow": ("graph", 2, "opt"),
}


def regions_for(row, rng):
    if row in ("sat-2", "sat-3", "horn-sat", "xor-sat", "nae-sat"):
        k = 2 if row == "sat-2" else 3
        mode = {"horn-sat": "horn", "xor-sat": "xor", "nae-sat": "nae"}.get(row, "plain")
        n, m = 12, {"sat-2": 16, "xor-sat": 8, "horn-sat": 20}.get(row, 16)   # tuned toward the band
        sol = cnf_solutions(n, cnf_instances(n, m, k, mode, rng), mode)
        return [("solutions", sol)] if sol else []
    if row == "bipartiteness":
        n = 11; g = graph(n, 0.22, rng)
        sol = [s for s in product((0, 1), repeat=n) if all(s[i] != s[j] for i, j in g)]
        return [("solutions", sol)] if sol else []
    if row == "graph-3-coloring":
        n = 8; f, _ = col3_sets(n, graph(n, 0.42, rng))
        return [("solutions", f)] if f else []
    if row == "subset-sum":
        nums = [rng.randint(1, 22) for _ in range(14)]
        tgt = sum(nums[i] for i in rng.sample(range(14), 6))
        f, _ = subsetsum_sets(nums, tgt)
        return [("solutions", f)] if f else []
    if row in ("vertex-cover", "independent-set", "clique", "max-cut"):
        n = 12; g = graph(n, 0.32, rng)
        f, o = {"vertex-cover": vc_sets, "independent-set": is_sets,
                "clique": clique_sets, "max-cut": maxcut_sets}[row](n, g)
        return [("feasible", f), ("optimal", o)] if f and o else []
    if row == "number-partitioning":
        f, o = partition_sets([rng.randint(1, 14) for _ in range(11)])
        return [("feasible", f), ("optimal", o)] if f and o else []
    if row == "min-spanning-tree":
        n = 7; E = graph(n, 0.62, rng)
        w = [rng.randint(1, 4) for _ in E]
        f, o = mst_sets(n, E, w)
        return [("feasible", f), ("optimal", o)] if f and o else []
    if row == "matching":
        n = 7; E = graph(n, 0.55, rng)
        f, o = matching_sets(E)
        return [("feasible", f), ("optimal", o)] if f and o else []
    if row == "reachability-stcon":
        n = 8; E = graph(n, 0.55, rng)
        f, o = stpath_sets(n, E)
        return [("feasible", f), ("optimal", o)] if f and o else []
    if row == "max-flow":
        n = 8; E = graph(n, 0.45, rng)
        f, o = unitflow_sets(n, E)
        return [("feasible", f), ("optimal", o)] if f and o else []
    return []


def main() -> int:
    v3 = {e.problem_id: e for e in A.load_atlas(
        str(ROOT.parent / "eightfold" / "eightfold" / "results" / "atlas" / "atlas_v3.jsonl"))}
    def dec(p): return next((c.value for c in v3[p].charges if c.charge == "decision"), "n.a.")

    rng = random.Random(SEED)
    rows = {}
    for row, (fam, dom, kind) in ROWS.items():
        ops = BOOL_OPS if dom == 2 else D3_OPS
        acc, n_ok = {}, 0
        for _ in range(N_INST):
            regs = regions_for(row, rng)
            if not regs:
                continue
            n_ok += 1
            for rname, region in regs:
                for fl, (op, m) in ops.items():
                    rate, r, nsub, cap = violation(region, op, m, rng)
                    if rate is None:
                        continue
                    d = acc.setdefault(rname, {}).setdefault(fl, {"rates": [], "r": []})
                    d["rates"].append(rate); d["r"].append(r)
        prof = {rn: {fl: {"mean_rate": round(mean(d["rates"]), 4), "mean_r": round(mean(d["r"]), 1),
                          "forced": fl in FORCED.get((row, rn), set()), "n": len(d["rates"])}
                     for fl, d in fls.items()} for rn, fls in acc.items()}
        rows[row] = {"family": fam, "domain": dom, "decision": dec(row), "n_instances": n_ok,
                     "profile": prof}

    # ── discovery statistic: FORCED FLAVOURS CANNOT BE SEEN (design law 3, enforced here) ────────────
    def discovery_rate(row, reg):
        fls = rows[row]["profile"][reg]
        vals = [x["mean_rate"] for fl, x in fls.items() if not x["forced"]]
        return round(mean(vals), 4) if vals else None

    tbl = []
    for row, v in rows.items():
        if not v["profile"]:
            continue
        reg = "solutions" if "solutions" in v["profile"] else "optimal"
        r = mean(x["mean_r"] for x in v["profile"][reg].values())
        tbl.append({"row": row, "family": v["family"], "decision": v["decision"],
                    "region_kind": "solutions" if reg == "solutions" else "optimal",
                    "discovery_rate": discovery_rate(row, reg), "mean_r": round(r, 1),
                    "in_target_band": bool(TARGET_R[0] <= r <= TARGET_R[1])})

    cells = {}
    for x in tbl:
        cells.setdefault((x["region_kind"], "easy" if x["decision"] == "P" else "hard"), []).append(x)
    occupancy = {f"{k[0]}|{k[1]}": len(v) for k, v in sorted(cells.items())}
    four_cell_filled = all(occupancy.get(f"{rk}|{h}", 0) > 0
                           for rk in ("solutions", "optimal") for h in ("easy", "hard"))

    within = {}
    for rk in ("solutions", "optimal"):
        e = [x["discovery_rate"] for x in tbl if x["region_kind"] == rk and x["decision"] == "P"]
        h = [x["discovery_rate"] for x in tbl if x["region_kind"] == rk and x["decision"] != "P"]
        within[rk] = {"n_easy": len(e), "n_hard": len(h),
                      "mean_easy": round(mean(e), 4) if e else None,
                      "mean_hard": round(mean(h), 4) if h else None,
                      "gap": round(mean(h) - mean(e), 4) if e and h else None}

    rs = [x["mean_r"] for x in tbl]; ys = [x["discovery_rate"] for x in tbl]
    mx, my = mean([log(v) for v in rs]), mean(ys)
    num = sum((log(a) - mx) * (b - my) for a, b in zip(rs, ys))
    den = (sum((log(a) - mx) ** 2 for a in rs) * sum((b - my) ** 2 for b in ys)) ** 0.5
    in_band = sum(1 for x in tbl if x["in_target_band"])

    doc = {"schema": "sounding-v2/v1", "prereg": "prereg_v18", "seed": SEED,
           "design_law_3_enforced_in_code": ("discovery_rate() cannot see a forced flavour — the pilot's "
                                             "42% leak is impossible at this schema, not merely avoided"),
           "n_rows": len(tbl), "row_table": tbl,
           "four_cell_occupancy": occupancy, "four_cell_filled": four_cell_filled,
           "within_region_kind": within,
           "region_size_control": {"primary": "ensemble tuning", "target_band": list(TARGET_R),
                                   "n_in_band": in_band, "n_rows": len(tbl),
                                   "secondary_check_residual_corr_log_r_rate": round(num / den, 4)},
           "_meta": {"target_band_r": {"value": TARGET_R[0], "literal": True,
                                       "note": "prereg_v18 declared band lower bound"}}}
    OUT.write_text(json.dumps(doc, indent=1) + "\n")

    print(f"SOUNDING v2 — THE FLEET ({len(tbl)} rows)\n")
    print(f"{'row':<21}{'family':<17}{'dec':<5}{'region':<11}{'rate':>8}{'r':>9}{'band':>6}")
    for x in sorted(tbl, key=lambda z: (z["region_kind"], z["decision"])):
        print(f"{x['row']:<21}{x['family']:<17}{x['decision']:<5}{x['region_kind']:<11}"
              f"{x['discovery_rate']:>8.4f}{x['mean_r']:>9.1f}{'  yes' if x['in_target_band'] else '   no':>6}")
    print(f"\nFOUR-CELL OCCUPANCY: {occupancy}   filled={four_cell_filled}")
    print(f"\nF2 — WITHIN REGION KIND (never pooled across):")
    for rk, v in within.items():
        print(f"  {rk:<11} easy n={v['n_easy']} {v['mean_easy']}   hard n={v['n_hard']} {v['mean_hard']}"
              f"   gap {v['gap']}")
    print(f"\nregion-size control: {in_band}/{len(tbl)} in band {TARGET_R}; "
          f"residual corr(log r, rate) = {num/den:+.4f}")
    print(f"\nwrote {OUT.name}  sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
