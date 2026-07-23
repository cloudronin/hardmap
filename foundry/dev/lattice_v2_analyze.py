"""Lattice v2 (prereg_v30) — analysis: computes the PARAMETERIZED charge on the ALREADY-COMMITTED roster
(lattice_v2_roster.json), builds the (approx x param) joint occupancy, counts profiles vs the floor, and reports
the secondary Cramer's V WITH the sealed stratified-sampling caveat. Runs in a LATER commit than the roster.

Run: PYTHONPATH=... python foundry/dev/lattice_v2_analyze.py
"""
import json
from collections import Counter
from itertools import product

from eightfold import structure as S
from foundry import objective_oracles as OO

FLOOR_PROFILES = 6


def _rel_from_bitmask(arity, bitmask):
    """Reconstruct the relation from the AUTHORITATIVE (arity, bitmask) — robust to any readability-field issue."""
    universe = list(product((0, 1), repeat=arity))
    return frozenset(universe[i] for i in range(len(universe)) if (bitmask >> i) & 1)


def main():
    roster = json.load(open("foundry/foundry/results/lattice/lattice_v2_roster.json"))
    rows = []
    for r in roster["rows"]:
        rel = _rel_from_bitmask(r["arity"], r["bitmask"])
        apx = r["stratum"]
        par = "open" if apx == "feasibility-hard" else OO.parameterized([rel])
        rows.append({"name": r["name"], "objective": r["objective"], "approximation": apx, "parameterized": par})

    both_real = [r for r in rows if r["parameterized"] != "open"]
    profiles = sorted({(r["approximation"], r["parameterized"]) for r in both_real})
    grid = Counter((r["approximation"], r["parameterized"]) for r in both_real)
    xs = [r["approximation"] for r in both_real]
    ys = [r["parameterized"] for r in both_real]
    v = S.cramers_v(xs, ys) if len(both_real) >= 3 else None
    both_params = {r["parameterized"] for r in both_real}

    resolved = (len(profiles) >= FLOOR_PROFILES) and ({"FPT", "W[1]"} <= both_params)
    verdict = ("RESOLVED — Wall 3 breached: the generated Boolean universe CAN exhibit the gradient (association "
               "given uniform approx coverage is readable)"
               if resolved else
               "INSUFFICIENT RESOLUTION — even a stratum-spanned arity<=3 Boolean roster is too coarse (a STRONGER "
               "finding than v1: about the universe, not the representatives)")

    out = {"prereg": "v30", "roster_committed_first": "lattice_v2_roster.json (prior commit)",
           "n_rows": len(rows), "n_both_real": len(both_real), "n_distinct_profiles": len(profiles),
           "floor_profiles": FLOOR_PROFILES, "both_param_values_present": sorted(both_params),
           "empty_cells_at_arity3": roster["empty_cells_at_arity3"],
           "verdict": verdict, "resolved": resolved,
           "occupancy": {f"{a} x {p}": c for (a, p), c in sorted(grid.items())},
           "rows": rows,
           "secondary_cramers_v": v,
           "cramers_v_caveat": ("STRATIFIED SAMPLING on the approximation axis: this V measures association GIVEN "
                                "deliberately uniform approximation coverage, NOT a natural-population association. "
                                "NOT magnitude-comparable to the canon's 0.73 (curated-but-not-stratified). Both are "
                                "Cramer's V; the numbers are not comparable as magnitudes.")}

    print(f"rows={len(rows)}  both-real={len(both_real)}  profiles={len(profiles)} (floor {FLOOR_PROFILES})  "
          f"params={sorted(both_params)}")
    print(f"VERDICT: {verdict}")
    print(f"secondary Cramer's V (stratified; NOT comparable to 0.73) = {v}")
    print("occupancy (approx x param):")
    for (a, p), c in sorted(grid.items()):
        print(f"  {a:28s} x {p:5s} : {c}")
    print("\nrows:")
    for r in rows:
        print(f"  {r['objective']:9s} {r['approximation']:28s} {r['parameterized']:5s}  ({r['name']})")
    json.dump(out, open("foundry/foundry/results/lattice/lattice_v2_occupancy.json", "w"), indent=2)
    print("\nwrote lattice_v2_occupancy.json")


if __name__ == "__main__":
    main()
